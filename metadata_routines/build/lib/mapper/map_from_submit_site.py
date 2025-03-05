import json
from citation import *
from mapper import utils
import html
from mapper.errors import FaultyRecordError

def value_or_none(dict, key):
    try:
        return dict[key]
    except:
        return None


def map_from_submit_site(submit_str):
    try:
        data = json.loads(submit_str)
    except json.JSONDecodeError as e:
        raise FaultyRecordError(f"Error decoding JSON: {e}")

    # Submit site api returns a list, so index first and only element
    if isinstance(data, list):
        if len(data) == 1:
            data = data[0]
        else:
            raise FaultyRecordError("Submit site data is a list with multiple elements")

    data = utils.replace_hyphens_with_underscores(data)

    # Instantiate Citation object with high-level data
    new_citation = Citation(
        title=utils.clean_dict_key(data, 'title'),
        DOI=utils.clean_dict_key(data, "doi"),
        container_title=utils.clean_dict_key(data, "journal"),
        abstract=utils.clean_dict_key(data, "abstract"),
        # add publication date once we hear back from David about mapping
        volume=utils.clean_dict_key(data, "volume"),
        issue=utils.clean_dict_key(data, "issue")
    )
    if "issn" in data.keys():
        new_citation.ISSN["issn"] = data["issn"]

    # Add page data. Submit site provides first and last pages.
    new_citation.page_first_last = (utils.clean_dict_key(data, "first_page"), utils.clean_dict_key(data, "last_page"))

    # Add funder data
    if "funding_agencies" in data.keys():
        for funder in data["funding_agencies"]:
            new_funder = Funder(
                name=utils.clean_dict_key(funder, "name"),
                award=[utils.clean_dict_key(funder, "award_number")]
            )
            new_citation.funder.append(new_funder)

    # Add license data
    new_license = License(
        version=utils.clean_dict_key(data, "manuscript_version")
    )
    if new_license.version is not None:
        new_citation.license = [new_license]

    # Add author data
    if "authors" in data.keys():
        for auth in data["authors"]:
            # Affiliation may be a string or a list of strings
            if "affiliation" in auth.keys():
                affiliation = utils.clean_dict_key(auth, "affiliation")
                if isinstance(affiliation, str):
                    affiliation = [affiliation]
            else:
                affiliation = None

            new_author = Author(
                given=utils.clean_dict_key(auth, "first_name"),
                family=utils.clean_dict_key(auth, "last_name"),
                orcid=utils.clean_dict_key(auth, "orcid"),
                affiliation=affiliation,
                sequence=None
            )
            new_citation.author = new_author

    # Create dict of identifiers
    ids = {"provider_rec":None}
    if "log_number" in data.keys():
        ids["standard_number_aris"] = utils.clean_dict_key(data, "log_number")
    if "submission_node_id" in data.keys():
        ids["submission_node_id"] = utils.clean_dict_key(data, "submission_node_id")
        ids["provider_rec"] = utils.clean_dict_key(data, "submission_node_id")
    if "accession_number" in data.keys():
        ids["accession_number"] = utils.clean_dict_key(data, "accession_number")
    if "mms_id" in data.keys():
        ids["mms_id"] = utils.clean_dict_key(data, "mms_id")

    # Add local data
    new_local = Local(
        manuscript_file=utils.clean_dict_key(data, "manuscript_file"),
        supplementary_files=utils.clean_dict_key(data,"supplementary_files"),
        submission_date=utils.clean_dict_key(data,"created"),
        modification_date=utils.clean_dict_key(data,"changed"),
        date_other=utils.clean_dict_key(data,"date_other"),
        identifiers=ids,
        USDA="yes",
        submitter_email=utils.clean_dict_key(data, "submitter_email"),
        submitter_name=utils.clean_dict_key(data, "submitter_name")
    )

    new_citation.local = new_local

    return (new_citation, 'success')