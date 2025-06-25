"""
Assign handles to digital resources.

   Flow:

- Creates a list of digital resource records without AgID using the Alma SRU API, in MARC21XML format.
- Mints new AgID and Handle identifier/URL for each record.
- Creates a merged collection of MARC records from the list, including fields containing the newly minted AgID
identifier and Handle identifier/URL.
- Uploads the merged collection of MARC records in Information Interchange Format (ANSI Z39.2), which commonly uses
the .mrc suffix. MARC transport format to Alma's Amazon S3 bucket.
- Emails library staff a status report, listing the records updated.

    Notes:
        GitHub Issue: https://github.com/USDA-REE-ARS/nal-library-systems-support/issues/2209

"""
import datetime
import os.path
from argparse import ArgumentParser

import pymarc
from pymarc import Record, Field, Subfield, Indicators, XMLWriter
import srupymarc  # local SRU client designed for MARC using PyMARC package
import tomli
import boto3
from botocore.exceptions import ClientError
import logging
import os
from openpyxl import Workbook
from email.message import EmailMessage
import smtplib

import handle_client  # local Handle client for minting Handles



def get_command_line_parameters():
    """
    Reads the configuration file from command line and return SRU endpoint, location for MARC output file
       and initiates the Handle minting object

    Returns:
        configuration_file: Full path to TOML configuration file
        debug_flag bool: Debug flag - prevents minting handles
    """
    arg_parser = ArgumentParser()
    arg_parser.add_argument('-cf', '--config', type=str,
                            help='Location of configuration file',
                            default="/app/configurations/handle/assign_handles.toml")
    arg_parser.add_argument("--debug", action="store_true", help="Debug flag - prevents minting handles")
    args = arg_parser.parse_args()

    config_file = args.config
    debug_flag = args.debug
    return config_file, debug_flag


def get_configuration(config_file):
    if os.path.isfile(config_file):
        with open(config_file, "rb") as f:
            configuration_dict = tomli.load(f)
    else:
        print('Configuration file not found at ' + config_file)
        exit()

    if "sru_endpoint" not in configuration_dict:
        print("Configuration file does not contain 'SRU endpoint' parameter key")
        exit()

    if "sru_query" not in configuration_dict:
        print("Configuration file does not contain 'SRU query' parameter key")
        exit()

    if "marc_output_directory" not in configuration_dict:
        print("Configuration file is missing output directory, 'marc_out_directory' parameter key")
        exit()

    marc_output_directory = configuration_dict["marc_output_directory"]
    if not os.path.isdir(marc_output_directory):
        print(f"Output directory, {marc_output_directory} does not exists")
        exit()

    return configuration_dict


def get_digital_resources_wo_handles(sru_endpoint, sru_query, maximum_records=20):
    """
    Get list of Digital resource records in MARC21 that do not have Handles assigned.

    Args:
        sru_endpoint str: Endpoint URL for Alma SRU interface.
        sru_query str: used to find records requiring handles
        maximum_records int: maximum number of records to return

    Returns:
        dr_record_wo_handles_list: list of PyMARC records objects
    """

    # SRU query for records created using the information center form without AgID identifiers:
    # sru_query = 'alma.local_notes=information_center_form and local_field_974=""'

    try:
        client = srupymarc.Client(sru_endpoint, maximum_records=maximum_records)
        srupymarc_response = client.searchretrieve(sru_query)
        dr_record_wo_handles_list = srupymarc_response.records
        return dr_record_wo_handles_list
    except Exception as e:
        print(f"Error occurred: {e}")
    return []


def create_merge_record_with_handle(marc_record, minted_handle):
    """
    Creates a merge minimum MARC pymarc Record from SRU adding handle and other fields.

    Args:
        marc_record: A PyMARC Record object
        minted_handle: A newly minted PID for this digital item metadata record

    Returns:
        MARC record: A pymarc record object for adding Handle and PID with this merge record.
        field_list: List of fields to be added to reporting spreadsheet.

    Notes: We are building a minimum MARC record to add the PID and Handle identifier.
    """
    field_list = []
    # Handle derivatives
    #    Sample Handle: '10113/345566'
    handle_url = 'https://handle.nal.usda.gov/' + minted_handle
    pid = minted_handle.split('/', 1)[1]  # Get pid which is after slash
    agid_value = 'agid:' + pid
    agid_control_number = agid_value + '-01nal_inst'

    merge_record: Record = Record()

    # MARC Control number tag 001
    field_001 = marc_record.get_fields('001')
    if field_001:
        merge_record.add_field(field_001[0])
        field_list.append(field_001[0].data)
    else:
        field_list.append('NA')

    # MARC Fixed Fields tag 008
    field_008: list = marc_record.get_fields('008')
    if field_008:
        merge_record.add_field(field_008[0])

    # MARC Other Standard Identifier tag 024
    merge_record.add_field(
        Field(
            tag='024',
            indicators=Indicators('7', ' '),
            subfields=[
                Subfield(code='a', value=minted_handle),
                Subfield(code='2', value='hdl')
            ]
        )
    )
    field_list.append(minted_handle)

    # MARC System Control Number tag 035
    merge_record.add_field(
        Field(
            tag='035',
            indicators=Indicators(' ', ' '),
            subfields=[
                Subfield(code='a', value=agid_control_number)
            ]
        )
    )

    # MARC Main Title tag 593
    value_593g = 'NA'
    field_593_list = marc_record.get_fields('593')
    if field_593_list:
        for field_593 in field_593_list:
            subfield_g = field_593.get_subfields('g')
            if subfield_g:
                value_593g = subfield_g[0]
    field_list.append(value_593g)

    # MARC Main Title tag 245
    field_245 = marc_record.get_fields('245')
    if field_245:
        merge_record.add_field(field_245[0])
        field_list.append(marc_record.title)
    else:
        field_list.append('NA')

    # MARC Electronic Location tag 856
    merge_record.add_field(
        Field(
            tag='856',
            indicators=Indicators(' ', '0'),
            subfields=[
                Subfield(code='u', value=handle_url),
                Subfield(code='3', value='Available in National Agricultural Library Digital Collections')
            ]
        )
    )

    # MARC Local field Number tag 974
    merge_record.add_field(
        Field(
            tag='974',
            indicators=Indicators(' ', ' '),
            subfields=[
                Subfield(code='a', value=agid_value)
            ]
        )
    )

    return merge_record, field_list


def create_file_name(directory_path: str, suffix: str):
    """
    Generated filename using timestamp 
    
    Args:
        directory_path: Full path to target directory
        suffix: file's extension

    Returns:
        file_path: Full path to file in target directory

    """
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"{directory_path}/minted_handles_for_dr_{timestamp}.{suffix}"
    return file_path


def write_marc_records_to_file(marc_records: list[pymarc.Record], marc_collection_file: str):
    """
    Writes a list of MARC21 records to a MARC collection file in a given directory.

    Args:
      marc_records list[RECORD]: A list of Record objects.
      marc_collection_file Str: The path to the output MARC file.

    Returns:
        marc_collection_file Str: full path to file
    """

    with open(marc_collection_file, 'wb') as output:
        for record in marc_records:
            if isinstance(record, Record):
                output.write(record.as_marc())
            else:
                print("Receive an object that is not a MARC record\n")
    return marc_collection_file


def write_marc21xml_records_to_file(marc_records: list[Record], marc_collection_file: str):
    """
    Writes a list of MARC21 records to a MARC21XML collection file in a given directory.

    Args:
      marc_records list[RECORD]: A list of Record objects.
      marc_collection_file Str: The path to the output MARC21XML file.

    Returns:
        marc_file_name Str: full path to file
    """

    xml_writer = XMLWriter(open(marc_collection_file, 'wb'))
    for record in marc_records:
        if isinstance(record, Record):
            xml_writer.write(record)
        else:
            print("Receive an object that is not a MARC record\n")
    xml_writer.close()  # Important!
    return marc_collection_file


def setup_handle_client(config_file):
    """
    Setting up Handle minting service object

    Args:
      config_file Str: full path to the configuration file

    Returns:
        handle_client - an object performs calls to the Handle API

    Notes:

    """

    Handle_client = handle_client.new()
    return handle_client


def get_pid_from_marc_record(marc_record):
    """
    Mint Handle from existing pid from agid in Alma record
    
    Args:
        marc_record: Source record for PID

    Returns:
        pid: PID from local fields or Handle identifier, if not field with PID return an empty string

    """

    field_974 = marc_record.get_fields('974')
    if field_974:
        agid = field_974[0].get_subfields('a')[0]
        pid = agid.split(":")[1]  # get PID from agid 'agid:4004' -> 4004
        return pid

    field_024_list = marc_record.get_fields('024')
    for field_024 in field_024_list:
        code = field_024.get_subfields('2')[0]
        if code == 'hdl':
            handle_id = field_024.get_subfields('a')[0]
            handle_parts = handle_id.split('/')  # Handle: 10113/340553
            if handle_parts[0] == '10113':  # It's a NAL Handle
                pid = handle_parts[1]
                return pid

    return ''


def get_handle(marc_record, Handle_client, debug_flag):
    # The MSSID is the Alma control number require to create the Primo landing page.
    field_001 = marc_record.get_fields('001')
    mmsid = field_001[0].data
    landing_page_url = 'https://search.nal.usda.gov/permalink/01NAL_INST/27vehl/alma{0}'.format(mmsid)

    pid = get_pid_from_marc_record(marc_record)

    if debug_flag:
        minted_handle = '10113/TEST'
    elif pid:
        minted_handle = Handle_client.create_handle(pid, landing_page_url)
    else:
        pid = handle_client.mint_pid()
        minted_handle = Handle_client.create_handle( pid, landing_page_url)
    return minted_handle

def create_marc_collection_of_merge_records(record_list, Handle_client, debug_flag):
    """
    Receives a list of PyMARC MARC records and outputs a list of merge MARC records with minted Handles fields
    
    Args:
         record_list: List of Pymarc MARC record objects
         Handle_client: Object for minting Handles
         debug_flag: Debug flag - prevents minting handles

    Returns:
          marc_records: List of MARC records with newly minted Handles fields
          list_of_lists_of_fields: List of fields from each MARC record create for spreadsheet report.
    """

    merge_records = []
    list_of_lists_of_fields = []
    for marc_record in record_list:
        minted_handle = get_handle(marc_record, Handle_client, debug_flag)
        merge_record, list_of_fields = create_merge_record_with_handle(marc_record, minted_handle)
        merge_records.append(merge_record)
        list_of_lists_of_fields.append(list_of_fields)
    return merge_records, list_of_lists_of_fields


def create_spreadsheet_file(list_of_lists_of_fields: list[list], spreadsheet_file_name: str):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'New Handle assignments'
    sheet.append(['Alma MMS ID', 'Handle', 'For', 'Title'])

    for list_fields in list_of_lists_of_fields:
        sheet.append(list_fields)

    for column in sheet.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            if len(str(cell.value)) > max_length:
                max_length = len(cell.value)
        adjusted_width = (max_length + 2) * 1.2
        sheet.column_dimensions[column_letter].width = adjusted_width

    workbook.save(spreadsheet_file_name)
    return spreadsheet_file_name


def check_if_file_exist_in_amazon_s3(bucket_name, object_name):
    """Checks if a file exists in an S3 bucket.

    Args:
        bucket_name (str): The name of the S3 bucket.
        object_name (str): s3 object name to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """

    s3 = boto3.client('s3')

    try:
        s3.head_object(Bucket=bucket_name, Key=object_name)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        elif e.response['Error']['Code'] == '403':
            print(f'{bucket_name} is unauthorized or invalid')
            return False
        else:
            raise


def delete_file_in_amazon_s3(bucket_name, object_name):
    """Delete a file in an S3 bucket.

    Args:
        bucket_name (str): The name of the S3 bucket.
        object_name (str): s3 object name to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    s3 = boto3.client('s3')

    try:
        s3.delete_object(Bucket=bucket_name, Key=object_name)
        print(f"File '{object_name}' deleted successfully.")
        return True
    except ClientError as e:
        print(f"Error deleting file '{object_name}': {e}")
    return False


def upload_file_to_amazon_s3(file_name, bucket_name, object_name=None):
    """Upload a file to an S3 bucket

    Args:
        file_name: File to upload
        bucket_name: Bucket to upload to
        object_name: S3 object name. If not specified then file_name is used
    Returns
        result: True if file was uploaded, else False
    Notes
        Using Amazon s3 setup from OS level
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')

    try:
        s3_client.upload_file(file_name, bucket_name, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def send_email(email_parameters, report_path, assignment_count, message=None):
    """
    Send email with report
    Args:
        email_parameters: A dictionary with email parameters
        report_path: Path to report file
        assignment_count: Number of Handle assignments
        message: Email message body

    Returns:

    """
    if email_parameters['flag'] == 0:
        return

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")

    msg = EmailMessage()

    if assignment_count == 0:
        if message is None:
            message = """ {} {}.""".format(email_parameters["body_no_report"], date)
        msg['Subject'] = email_parameters["subject_general"]
        msg['From'] = email_parameters["from"]
        msg['To'] = email_parameters["library_staff"]
        msg['Cc'] = email_parameters["cc"]
        msg.set_content(message)
        email_status(msg, email_parameters)
    else:
        msg['Subject'] = email_parameters["subject_general"]
        msg['From'] = email_parameters["from"]
        msg['To'] = email_parameters["library_staff"]
        msg['Cc'] = email_parameters["cc"]
        msg.set_content(""" {} """.format(email_parameters["body_report"]))
        attach_file_to_send(report_path, msg)
        email_status(msg, email_parameters)
    return


def attach_file_to_send(path, msg):
    try:
        with open(path, 'rb') as fp:
            file = fp.read()
            file_name = os.path.basename(path)
            msg.add_attachment(file, maintype='application',
                               subtype='octet-stream', filename=file_name)
    except FileNotFoundError:
        print('Report file does not exist to email')
        raise SystemExit()
    except Exception as attach_file_exception:
        print(attach_file_exception)
        print('Exception occurred when opening csv file. You will not receive report email.')
        raise SystemExit()
    else:
        pass


def email_status(msg, email_parameters):
    try:
        # Send the email via our own SMTP server.
        with smtplib.SMTP(email_parameters["smtp"]) as s:
            s.send_message(msg)
            print("Email sent!")
            s.quit()
    except Exception as email_status_exception:
        print(email_status_exception)
        print('Report email is not sent!')
        raise SystemExit()


def main():
    # Setup
    config_file, debug_flag = get_command_line_parameters()
    conf = get_configuration(config_file)
    sru_endpoint = conf["sru_endpoint"]
    sru_query = conf["sru_query"]
    sru_maximum_records = conf["sru_maximum_records"]
    marc_output_directory = conf["marc_output_directory"]
    marc_output_format = conf["marc_output_format"]
    email_parameters = conf["email"]
    handle_client = setup_handle_client(config_file)
    s3_bucket_name = conf["s3_bucket_name"]
    s3_object_name = conf["s3_object_name"]

    if check_if_file_exist_in_amazon_s3(s3_bucket_name, s3_object_name):
        message = f"\n\ns3 file at \"{s3_bucket_name}{s3_object_name}\" is waiting for import into Alma\n\n"
        print(message)
        send_email(email_parameters, None, 0, message)
        return

    # Using Alma SRU API to get a list of the records for digital resources without handles
    record_list = get_digital_resources_wo_handles(sru_endpoint, sru_query, sru_maximum_records)
    if not record_list:
        # message = 'No digital resources need Handles'
        # print(message)
        # send_email(email_parameters, None, 0, message)
        return

    merge_records, list_of_lists_of_fields = create_marc_collection_of_merge_records(record_list, handle_client,
                                                                                     debug_flag)
    # Write MARC collection file
    if marc_output_format == 'xml' or marc_output_format == 'marcxml':
        marc_collection_file = create_file_name(marc_output_directory, 'xml')
        write_marc21xml_records_to_file(merge_records, marc_collection_file)
    else:
        marc_collection_file = create_file_name(marc_output_directory, 'mrc')
        write_marc_records_to_file(merge_records, marc_output_directory)

    # Write Report
    spreadsheet_file = create_file_name(marc_output_directory, 'xlsx')
    create_spreadsheet_file(list_of_lists_of_fields, spreadsheet_file)
    # Upload to Amazon s3

    upload_file_to_amazon_s3(marc_collection_file, s3_bucket_name, s3_object_name)
    # upload_file_to_amazon_s3(marc_collection_file, s3_bucket_name )
    # Email report
    send_email(email_parameters, spreadsheet_file, len(merge_records), None)

    return

def assign_handles_to_digital_resources():
    """
    Main function to assign handles to digital resources.
    """
    main()

if __name__ == "__main__":
    main()
