import pymarc
from pymarc import Field, Subfield, XMLWriter, JSONWriter, Indicators
from citation import Citation
import tomli
import os
import calendar
import warnings
from dateutil import parser


def title_indicator(title: str) -> str:
    # Read from the toml file
    base_path = os.path.dirname(os.path.abspath(__file__))
    title_indicator_file = os.path.join(base_path, 'title_indicator.toml')
    with open(title_indicator_file, 'rb') as f:
        data = tomli.load(f)
    first_word = title.split(" ")[0].lower().strip()
    if first_word in data:
        return data[first_word]
    return '0'

def citation_to_marc(cit: Citation, format: str, output_path: str) -> str:
    """
    Maps a Citation object to a MARC record.

    Args:
        cit (Citation): The citation object to be mapped.
        format (str): The format of the output file ('xml', 'json', or 'marc').

    Returns:
        msg (str): A message describing the success or failure of the
        operation. Returns "Success" if the MARC record was created and saved,
        and returns "Failure: <error_message>" if there was an error.

    Saves the MARC record to the specified output path in the specified format.
    """

    if format not in ["xml", "json", "marc"]:
        return "Failure: Invalid format specified. Please use 'xml', \
        'json', or 'marc'."

    try:

        # Check if there is a first author present
        has_first_author = False
        for author in cit.author:
            if author.sequence == "first":
                has_first_author = True
                break

        # Create a new MARC record
        record = pymarc.Record()

        # Set the leader
        record.leader = "00000nam a2200289 a 4500"

        # Add fields to the MARC record based on the Citation object

        # Add title and subtitle
        # Assuming that we will never have a subtitle and no title
        if cit.title:
            title_indicator_1 = "1" if has_first_author else "0"
            title_indicator_2 = title_indicator(cit.title)

            title_field = Field(
                tag='245',
                indicators=Indicators(title_indicator_1, title_indicator_2),
                subfields=[
                    Subfield(code='a', value=cit.title)
                ]
            )
            if cit.subtitle:
                title_field.add_subfield('b', cit.subtitle)
            record.add_ordered_field(title_field)

        # Add original title

        # Add DOI
        if cit.DOI:
            # Always add a field for doi, don't amend to existing 024
            record.add_ordered_field(pymarc.Field(
                tag='024',
                indicators=Indicators('7', ' '),
                subfields=[
                    Subfield(code='a', value=cit.DOI),
                    Subfield(code='2', value='doi')
                ]
            ))

        # Add container title
        # Here we assume that future updates will not implement the 773 field
        # with different indicator values
        if cit.container_title:
            if not record.get_fields("773"):
                record.add_ordered_field(
                    pymarc.Field(
                        tag="773",
                        indicators=Indicators('0', ' ')
                    )
                )
            field_773 = record.get_fields("773")[0]
            field_773.add_subfield(
                't', value=cit.container_title_str()
            )

        # Add ISSN
        if cit.ISSN:
            issn_seen = set()
            issn_list = [issn for issn in cit.ISSN.values() if not (issn in issn_seen or issn_seen.add(issn))]
            for issn in issn_list:
                if not record.get_fields("773"):
                    record.add_ordered_field(
                        pymarc.Field(
                            tag="773",
                            indicators=Indicators('0', ' ')
                        )
                    )
                field_773 = record.get_fields("773")[0]
                field_773.add_subfield(
                    'x', value=issn
                )
                if not record.get_fields("914"):
                    record.add_ordered_field(
                        pymarc.Field(
                            tag="914",
                            indicators=Indicators(' ', ' ')
                        )
                    )
                field_914 = record.get_fields("914")[0]
                field_914.add_subfield(
                    'b', value=issn
                )

        if cit.author:
            found_first_author = False
            for author in cit.author:
                if author.sequence == "first" and not found_first_author:
                    found_first_author = True
                    record.add_ordered_field(
                        pymarc.Field(
                            tag="100",
                            indicators=Indicators('1', ' '),
                            subfields=[
                                Subfield('a',
                                         value=f"{author.family}, {author.given}"),
                                Subfield('e', value="author")
                            ]
                        )
                    )
                    field_100 = record.get_fields("100")[0]
                    if author.orcid:
                        field_100.add_subfield('1', value=author.orcid)
                    if author.affiliation:
                        affiliation_list = [aff for aff in author.affiliation]
                        affiliation_str = " ``".join(affiliation_list)
                        if affiliation_str != "":
                            field_100.add_subfield('u', value=affiliation_str)
                else:
                    new_700 = pymarc.Field(
                        tag='700',
                        indicators=Indicators('1', ' '),
                        subfields=[
                            Subfield(code='a',
                                     value=f"{author.family}, {author.given}"),
                            Subfield(code='e', value="author")
                        ]
                    )
                    if author.orcid:
                        new_700.add_subfield('1', value=author.orcid)
                    if author.affiliation:
                        affiliation_list = [aff for aff in author.affiliation]
                        affiliation_str = " ``".join(affiliation_list)
                        if affiliation_str != "":
                            new_700.add_subfield('u', value=affiliation_str)
                    record.add_ordered_field(new_700)
        # Add publisher data
        if cit.publisher:
            record.add_ordered_field(pymarc.Field(
                tag='264',
                indicators=Indicators(' ', ' '),
                subfields=[
                    Subfield(code='b', value=cit.publisher)
                ]
            ))

        # Add abstract to field 520$a
        if cit.abstract:
            record.add_ordered_field(pymarc.Field(
                tag='520',
                indicators=Indicators(' ', ' '),
                subfields=[
                    Subfield(code='a', value=cit.abstract)
                ]
            ))

        # Add funder info
        for funder in cit.funder:
            if funder.award:
                for award in funder.award:
                    record.add_ordered_field(pymarc.Field(
                        tag='596',
                        indicators=Indicators(' ', ' '),
                        subfields=[
                            Subfield(code='c', value=funder.name),
                            Subfield(code='a', value=award)
                        ]
                    ))

        # Add license info
        if cit.license and len(cit.license) > 0:
            open_access = False
            for license in cit.license:
                new_506 = pymarc.Field(
                    tag='506',
                    indicators=Indicators('#', ' '),
                )
                if license.content_version:
                    new_506.add_subfield(
                        '3', value=license.content_version
                    )
                if license.terms_of_access:
                    new_506.add_subfield(
                        'a', value=license.terms_of_access
                    )
                    if license.terms_of_access == "Open Access":
                        open_access = True
                if license.source_of_term:
                    new_506.add_subfield(
                        '2', value=license.source_of_term
                    )
                if license.url:
                    new_506.add_subfield(
                        'u', value=license.url
                    )
                if license.start_date:
                    try:
                        formatted_date = parser.parse(license.start_date).strftime("%Y%m%d")
                        new_506.add_subfield(
                            'd', value=formatted_date
                        )
                    except parser._parser.ParserError:
                        pass
                if license.restrictions:
                    new_506.add_subfield(
                        'f', value=license.restrictions
                    )
                record.add_ordered_field(new_506)
            if open_access:
                record.add_ordered_field(
                    pymarc.Field(
                        tag='540',
                        indicators=Indicators(' ', ' '),
                        subfields=[
                            Subfield(code='a', value="Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License"),
                            Subfield(code='f', value="CC BY-NC-ND 4.0"),
                            Subfield(code='2', value="cc"),
                            Subfield(code='u', value="https://creativecommons.org/licenses/by-nc-nd/4.0/")
                        ]
                    )
                )

        # Add date info from submission records
        if "submission_modification" in cit.date.keys() and \
                "string" in cit.date["submission_modification"].keys():
            if cit.date["submission_modification"]["string"]:
                if not record.get_fields("961"):
                    record.add_ordered_field(
                        pymarc.Field(
                            tag="961",
                            indicators=Indicators(' ', ' ')
                        )
                    )
                field_961 = record.get_fields("961")[0]
                field_961.add_subfield(
                    'c', value=cit.date["submission_modification"]["string"]
                )
        if "submission_created" in cit.date.keys() and \
                "string" in cit.date["submission_created"].keys():
            if cit.date["submission_created"]:
                if not record.get_fields("961"):
                    record.add_ordered_field(
                        pymarc.Field(
                            tag="961",
                            indicators=Indicators(' ', ' ')
                        )
                    )
                field_961 = record.get_fields("961")[0]
                field_961.add_subfield(
                    'e', value=cit.date["submission_created"]["string"]
                )




        # Add volume to 914$c
        # Assuming that if field 914 exists, it will have indicators _ _
        if cit.volume:
            if not record.get_fields("914"):
                record.add_ordered_field(
                    pymarc.Field(
                        tag="914",
                        indicators=Indicators(' ', ' ')
                    )
                )
            field_914 = record.get_fields("914")[0]
            field_914.add_subfield(
                'c', value=cit.volume
            )

        # Add issue to 914$d
        if cit.issue:
            # Check if field 914 exists
            if not record.get_fields("914"):
                record.add_ordered_field(
                    pymarc.Field(
                        tag="914",
                        indicators=Indicators(' ', ' ')
                    )
                )
            field_914 = record.get_fields("914")[0]
            field_914.add_subfield(
                'd', value=cit.issue
            )

        # Add page info
        # Put page string in 300$a and 914$e
        # Need instructions on how to populate field 773$g
        # Update to ensure leading 'p.'
        if cit.page:
            page_str_to_record = cit.page['page_str']
            if page_str_to_record:
                if not page_str_to_record.startswith("p."):
                    page_str_to_record = "p." + page_str_to_record
                record.add_ordered_field(pymarc.Field(
                    tag='300',
                    indicators=Indicators(' ', ' '),
                    subfields=[
                        Subfield(code='a', value=page_str_to_record)
                    ]
                ))
                # Check if field 914 exists
                field_914 = record.get_fields('914')
                if field_914:
                    # Add page to existing field
                    field_914[0].add_subfield('e', value=page_str_to_record)
                else:
                    # Create new field 914 with page
                    record.add_ordered_field(pymarc.Field(
                        tag='914',
                        indicators=Indicators(' ', ' '),
                        subfields=[
                            Subfield(code='e', value=page_str_to_record)
                        ]
                    ))

        # Populate field 773$g
        # Check if field 773 exists
        volume = cit.volume
        issue = cit.issue
        page_str = cit.page.get('page_str', None)
        date = cit.date.get("published", None)
        if volume or issue or page_str or date:
            if not record.get_fields("773"):
                record.add_ordered_field(
                    pymarc.Field(
                        tag="773",
                        indicators=Indicators('0', ' ')
                    )
                )
            field_773 = record.get_fields("773")[0]
            field_773g_text = ""
            if date and "year" in date.keys() and date["year"] and \
                    "month" in date.keys() and date["month"]:
                cal_month = calendar.month_name[int(date["month"])]
                year = date["year"]
                date_str = f"{year} {cal_month}."
                field_773g_text += date_str
            elif date and "year" in date.keys() and date["year"]:
                date_str = f"{date['year']}."
                field_773g_text += date_str
            if volume and not (volume.startswith("Vol.") or
                               volume.startswith("v.")):
                volume = "Vol. " + volume
                if len(field_773g_text) > 0:
                    field_773g_text += ", "
                field_773g_text += volume
            if issue and not issue.startswith("no."):
                issue = "no. " + issue
                if len(field_773g_text) > 0:
                    field_773g_text += ", "
                field_773g_text += issue
            if page_str and not page_str.startswith("p."):
                page_str = "p." + page_str
                if len(field_773g_text) > 0:
                    field_773g_text += " "
                field_773g_text += page_str
            field_773.add_subfield(
                'g', value=field_773g_text
            )

        # Add url
        if cit.URL:
            record.add_ordered_field(pymarc.Field(
                tag='856',
                indicators=Indicators('4', '0'),
                subfields=[
                    Subfield(code='u', value=cit.URL),
                ]
            ))

        # Add subject terms to 650, 651, and 653
        if cit.subjects and cit.subjects != {}:
            if "NALT" in cit.subjects.keys():
                if isinstance(cit.subjects["NALT"], list):
                    for subject in cit.subjects["NALT"]:
                        if "topic" in subject.keys() and \
                                "term" in subject["topic"].keys():
                            new_field = pymarc.Field(
                                tag='650',
                                indicators=Indicators(' ', '3'),
                                subfields=[
                                    Subfield(code='a',
                                             value=subject["topic"]["term"]),
                                ]
                            )
                            if "uri" in subject["topic"].keys():
                                new_field.add_subfield(
                                    '0', value=subject["topic"]["uri"]
                                )
                            record.add_ordered_field(new_field)
                        elif "geographic" in subject.keys() and \
                                "term" in subject["geographic"].keys():
                            new_field = pymarc.Field(
                                tag='651',
                                indicators=Indicators(' ', '3'),
                                subfields=[
                                    Subfield(code='a',
                                             value=subject["geographic"]["term"]),
                                ]
                            )
                            if "uri" in subject["geographic"].keys():
                                new_field.add_subfield(
                                    '0', value=subject["geographic"]["uri"]
                                )
                            record.add_ordered_field(new_field)
                else:
                    warnings.warn("Citation.subjects improperly configured. \
                    NALT subject terms should be a list.")
            if "MeSH" in cit.subjects.keys():
                if isinstance(cit.subjects["MeSH"], list):
                    for subject in cit.subjects["MeSH"]:
                        if "topic" in subject.keys() and \
                                "term" in subject["topic"].keys():
                            new_field = pymarc.Field(
                                tag='650',
                                indicators=Indicators(' ', '2'),
                                subfields=[
                                    Subfield(code='a',
                                             value=subject["topic"]["term"]),
                                ]
                            )
                            if "uri" in subject["topic"].keys():
                                new_field.add_subfield(
                                    '0', value=subject["topic"]["uri"]
                                )
                            record.add_ordered_field(new_field)
                else:
                    warnings.warn("Citation.subjects improperly configured. \
                    MeSH subject terms should be a list.")
            if "Uncontrolled" in cit.subjects.keys():
                if isinstance(cit.subjects["Uncontrolled"], list):
                    for subject in cit.subjects["Uncontrolled"]:
                        if "topic" in subject.keys() and \
                                "term" in subject["topic"].keys():
                            new_field = pymarc.Field(
                                tag='653',
                                indicators=Indicators(' ', ' '),
                                subfields=[
                                    Subfield(code='a',
                                             value=subject["topic"]["term"]),
                                ]
                            )
                            record.add_ordered_field(new_field)
                else:
                    warnings.warn("Citation.subjects improperly configured. \
                    Uncontrolled subject terms should be a list.")

        if cit.container_DOI:
            # See if field 773 exists
            if not record.get_fields("773"):
                record.add_ordered_field(
                    pymarc.Field(
                        tag="773",
                        indicators=Indicators('0', ' ')
                    )
                )
            field_773 = record.get_fields("773")[0]
            field_773.add_subfield(
                'o', value=cit.container_DOI
            )

        if cit.local.USDA == "yes":
            record.add_ordered_field(pymarc.Field(
                tag='946',
                indicators=Indicators(' ', ' '),
                subfields=[
                    Subfield(code='a', value="USDA")
                ]
            ))
            if not record.get_fields("961"):
                record.add_ordered_field(
                    pymarc.Field(
                        tag="961",
                        indicators=Indicators(' ', ' ')
                    )
                )
            field_961 = record.get_fields("961")[0]
            field_961.add_subfield(
                'a', value="USDA"
            )

        if cit.local.identifiers.get("mms_id"):
            record.add_ordered_field(pymarc.Field(
                tag='001',
                data=cit.local.identifiers["mms_id"]
            ))

        if cit.local.identifiers.get("aris"):
            record.add_ordered_field(pymarc.Field(
                tag='024',
                indicators=Indicators('7', ' '),
                subfields=[
                    Subfield(code='a', value=cit.local.identifiers["aris"]),
                    Subfield(code='2', value="aris")
                ]
            ))

        if cit.local.identifiers.get("submission_node_id"):
            if not record.get_fields("961"):
                record.add_ordered_field(
                    pymarc.Field(
                        tag="961",
                        indicators=Indicators(' ', ' ')
                    )
                )
            field_961 = record.get_fields("961")[0]
            field_961.add_subfield(
                'd', value=cit.local.identifiers["submission_node_id"]
            )

        if cit.local.identifiers.get("aris_accn_no"):
            record.add_ordered_field(pymarc.Field(
                tag='024',
                indicators=Indicators('7', ' '),
                subfields=[
                    Subfield(code='a', value=cit.local.identifiers[
                        "aris_accn_no"
                    ]),
                    Subfield(code='2', value='aris_accn_no')
                ]
            ))

        if cit.local.identifiers.get("nal_journal_id"):
            # Create field 914 if DNE
            if not record.get_fields("914"):
                record.add_ordered_field(
                    pymarc.Field(
                        tag="914",
                        indicators=Indicators(' ', ' ')
                    )
                )
            field_914 = record.get_fields("914")[0]
            field_914.add_subfield(
                'a', value=cit.local.identifiers["nal_journal_id"]
            )
            # Create field 773 if DNE
            if not record.get_fields("773"):
                record.add_ordered_field(
                    pymarc.Field(
                        tag="773",
                        indicators=Indicators('0', ' ')
                    )
                )
            field_773 = record.get_fields("773")[0]
            field_773.add_subfield(
                'w', value=cit.local.identifiers["nal_journal_id"]
            )

        if cit.local.USDA == 'yes' and cit.local.identifiers.get('hdl'):
            handle = cit.local.identifiers['hdl']
            # Add handle to field 024 $a with $2 = 'hdl'
            record.add_ordered_field(pymarc.Field(
                tag='024',
                indicators=Indicators('7', ' '),
                subfields=[
                    Subfield(code='a', value=handle),
                    Subfield(code='2', value='hdl')
                ]
            ))



        if cit.local.identifiers.get("agid"):
            record.add_ordered_field(pymarc.Field(
                tag='016',
                indicators=Indicators('7', ' '),
                subfields=[
                    Subfield(code='a', value="IND60" + cit.local.identifiers["agid"]),
                    Subfield(code='2', value="DNAL")
                ]
            ))
            record.add_ordered_field(pymarc.Field(
                tag='035',
                indicators=Indicators(' ', ' '),
                subfields=[
                    Subfield(code='a',
                             value="agid:" + cit.local.identifiers["agid"] + "-01nal_inst"),
                ]
            ))
            record.add_ordered_field(pymarc.Field(
                tag='974',
                indicators=Indicators(' ', ' '),
                subfields=[
                    Subfield(code='a',
                             value="agid:" + cit.local.identifiers["agid"]),
                ]
            ))

        # Populate 008 with date published
        base_008 = "||||||||||||||||||||||||||||||||||||||||"
        if cit.date and "published" in cit.date.keys() and \
                cit.date["published"]:
            if "year" in cit.date["published"].keys() and \
                    cit.date["published"]["year"] and \
                    "month" in cit.date["published"].keys() and \
                    cit.date["published"]["month"]:
                year = str(cit.date["published"]["year"])
                month = str(cit.date["published"]["month"])
                day = str(cit.date["published"]["day"]) if "day" in cit.date["published"].keys() else "  "
                if len(year) == 4 and len(month) == 2:
                    base_008 = base_008[:6] + "e" + year + month + day + \
                        base_008[13:]
        record.add_ordered_field(pymarc.Field(
            tag='008',
            data=base_008
        ))

        # Write record based on format
        if format == "xml":
            writer = XMLWriter(open(output_path, 'wb'))
            writer.write(record)
            writer.close()
        elif format == "json":
            writer = JSONWriter(open(output_path, 'w'))
            writer.write(record)
            writer.close()
        elif format == "marc":
            with open(output_path, 'wb') as out:
                out.write(record.as_marc())
        return "Successful"
    except Exception as e:
        return f"Failure: {str(e)}"
