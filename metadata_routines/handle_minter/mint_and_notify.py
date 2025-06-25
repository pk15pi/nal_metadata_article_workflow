import srupymarc
from citation import Citation, Local
from handle_minter.handle_client import HandleClient
import tomli
import smtplib
from email.mime.text import MIMEText
import os
import pymarc

def read_config(config_path):
    """
    Reads the configuration file and returns the configuration data.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        dict: Configuration data.
    """
    with open(config_path, 'rb') as f:
        config = tomli.load(f)

    if 'email_notification' not in config:
        raise ValueError("Configuration file must contain 'email_notification' section.")
    if 'smtp_server' not in config['email_notification']:
        raise ValueError("Configuration file must contain 'email_notification.smtp_server'.")
    if 'send_from' not in config['email_notification']:
        raise ValueError("Configuration file must contain 'email_notification.send_from'.")
    if 'subject' not in config['email_notification']:
        raise ValueError("Configuration file must contain 'email_notification.subject'.")
    if 'body_template' not in config['email_notification']:
        raise ValueError("Configuration file must contain 'email_notification.body_template'.")
    if 'debug' not in config:
        raise ValueError("Configuration file must contain 'debug'.")
    if 'testing_mode' not in config['debug']:
        raise ValueError("Configuration file must contain 'debug.testing_mode'.")
    if 'handle_service_conn' not in config['debug']:
        raise ValueError("Configuration file must contain 'debug.handle_service_conn'.")
    if 'email_submitter' not in config['debug']:
        raise ValueError("Configuration file must contain 'debug.email_submitter'.")
    if 'email_dev' not in config['debug']:
        raise ValueError("Configuration file must contain 'debug.email_dev'.")
    if 'dev_address' not in config['debug']:
        raise ValueError("Configuration file must contain 'debug.dev_address'.")
    return config


def get_matching_records(mmsid, pid, provider_rec):
    # Check for matches by mmsid

    if mmsid:
        query = f'alma.mms_id={mmsid}'
        params = {
            "url": "https://na91.alma.exlibrisgroup.com/view/sru/01NAL_INST",
            "query": query
        }
        matches = srupymarc.searchretrieve(**params)
        if len(matches.records) > 0:
            return matches.records
    # If no matches by mmsid or no mmsid present, check by pid
    query = f'alma.local_field_974=agid:{pid}'
    params = {
        "url": "https://na91.alma.exlibrisgroup.com/view/sru/01NAL_INST",
        "query": query
    }
    matches = srupymarc.searchretrieve(**params)
    if len(matches.records) > 0:
        return matches.records

    # If no matches by mmsid or pid, check by provider_rec
    query = f'alma.local_field_961={provider_rec}'
    params = {
        "url": "https://na91.alma.exlibrisgroup.com/view/sru/01NAL_INST",
        "query": query
    }
    matches = srupymarc.searchretrieve(**params)
    return matches.records

def mint_and_notify(handle_data):

    # Ensure sufficient input data and configurations
    config_file = os.getenv('HANDLE_MINTER_CONFIG')
    if config_file is None:
        raise ValueError("HANDLE_MINTER_CONFIG environment variable is not set")

    config = read_config(config_file)
    if 'pid' not in handle_data.keys() or 'provider_rec' not in handle_data.keys() or \
            'title' not in handle_data.keys():
        raise KeyError("Input handle_data dict does not have all the necessary inputs")

    # See if the record has been uploaded to Alma yet
    matching_records = get_matching_records(
        handle_data['mmsid'],
        handle_data['pid'],
        handle_data['provider_rec']
    )
    if len(matching_records) == 0:
        return 'not found in Alma', None
    if len(matching_records) > 1:
        return 'review', 'Multiple records in Alma'

    # Extract the handle field from the marc record
    pymarc_record = matching_records[0]
    fields_024 = pymarc_record.get_fields('024')
    handle_field = None
    for field in fields_024:
        if field.indicator1 == '7' and field.indicator2 == ' ':
            subfield_2 = field.get_subfields('2')
            if subfield_2 and subfield_2[0] == 'hdl':
                handle_field = field
                break
    if not handle_field:
        return 'review', 'No handle in Alma record'

    # Get handle from matched pymarc record and update local pid if necessary
    handle = handle_field.get_subfields('a')[0]
    message = ""
    pid_from_alma = handle.split("10113/")[-1]
    if pid_from_alma != handle_data['pid']:
        handle_data['pid'] = pid_from_alma
        message += "PID in Alma record does not match input PID. "

    # Construct landing page from mmsid
    mmsid_from_alma = matching_records[0].get_fields('001')[0].value() # Will throw error if mmsid DNE
    landing_page = f"https://search.nal.usda.gov/permalink/01NAL_INST/178fopj/alma{mmsid_from_alma}"

    # Create the handle using the handle service if it does not already exist
    handle_conn = config['debug']['handle_service_conn'] == 1
    testing_mode = config['debug']['testing_mode'] == 1
    hc = HandleClient(testing_mode=testing_mode)
    if not hc.check_handle_exists(handle):
        if handle_conn:
            handle_result = hc.create_handle(handle_data['pid'], landing_page)
            if handle_result is None:
                return 'review', message + 'Handle minting failed'
            if not hc.check_handle_exists(handle):
                return 'review', message + 'Handle minting failed'
        else:
            print(f"DEBUG mode: Handle would be minted here with create_handle({handle_data['pid']}, {landing_page})")
            message += "Debug mode enabled. Handle not minted - "
    if handle_data.get('submitter_email', None) is not None:
        if handle_data.get('submitter_name', None) is None:
            handle_data['submitter_name'] = 'submitter'
        body = config['email_notification']['body_template'].format(
                handle_data['submitter_name'],
                handle_data['title'],
                handle_data['pid'],
                f"11030/{handle_data['pid']}"
        )

        # Send email notification
        email_submitter = config['debug']['email_submitter'] == 1
        email_dev = config['debug']['email_dev'] == 1
        if testing_mode or (not email_submitter and not email_dev):
            print(f"DEBUG mode: Email would be sent to {handle_data['submitter_email']} with subject '{config['email_notification']['subject']}'")
            print("Email body: " + body)
        elif email_submitter: # If email_submitter is True, send email to submitter and not to dev regardless of email_dev
            msg = MIMEText(body)
            msg["Subject"] = config['email_notification']['subject']
            msg["From"] = config['email_notification']['send_from']
            msg["To"] = handle_data['submitter_email']
            smtp_server = config['email_notification']['smtp_server']

            with smtplib.SMTP(smtp_server) as server:
                server.sendmail(
                    config['email_notification']['send_from'],
                    handle_data['submitter_email'],
                    msg.as_string()
                )
        elif email_dev: # If email_dev is True, send email to developer email listed in config file
            dev_address = config['debug']['dev_address']
            print("Emailing the developer: ", dev_address)
            msg = MIMEText(body)
            msg["Subject"] = config['email_notification']['subject']
            msg["From"] = config['email_notification']['send_from']
            msg["To"] = dev_address
            smtp_server = config['email_notification']['smtp_server']

            with smtplib.SMTP(smtp_server) as server:
                server.sendmail(
                    config['email_notification']['send_from'],
                    handle_data['submitter_email'],
                    msg.as_string()
                )

    return 'success', message + 'success'