import json
from citation import Citation, Funder, License, Author, Local, Resource
from mapper import utils
from mapper.errors import FaultyRecordError
from datetime import datetime
import dateutil


def value_or_none(dict, key):
    try:
        return dict[key]
    except (KeyError, TypeError):
        return None


def date_string_to_dict(date: str):
    out_dict = {"string": date}
    try:
        dt = datetime.strptime(date, "%Y-%m-%d")
        out_dict["year"] = dt.year
        out_dict["month"] = dt.month
        out_dict["day"] = dt.day
    except ValueError:
        pass
    return out_dict


def date_timestamp_to_dict(date: str):
    out_dict = {"string": date}
    try:
        dt = datetime.fromtimestamp(int(date))
        out_dict["year"] = dt.year
        out_dict["month"] = dt.month
        out_dict["day"] = dt.day
    except ValueError:
        pass
    return out_dict


def parse_ambiguous_date_to_dict(date: str):
    out_dict = {"string": date}
    if len(date) == 4 and date.isdigit():
        out_dict["year"] = date
        return out_dict
    date_char_set = {
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-",
        "T", "Z", ":", ".", "/"
    }
    if set(date) <= date_char_set:
        try:
            dt = dateutil.parser.parse(date)
            out_dict["year"] = dt.year
            out_dict["month"] = dt.month
            out_dict["day"] = dt.day
        except dateutil.parser.ParserError:
            pass
    else:
        seasons = ("Spring", "Summer", "Fall", "Autumn", "Winter")
        months = ("January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November",
                  "December", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Sept", "Oct", "Nov", "Dec")
        if date.startswith(seasons):
            year = date.split(" ")[1]
            if len(year) == 4 and year.isdigit():
                out_dict["year"] = year
            return out_dict
        elif date.startswith(months):
            dt = dateutil.parser.parse(date)
            out_dict["year"] = dt.year
            out_dict["month"] = dt.month
            return out_dict
        else:
            # Remove leading non-date characters and attempt parse
            date = ''.join(char for char in date if char in date_char_set)
            try:
                dt = dateutil.parser.parse(date)
                out_dict["year"] = dt.year
                out_dict["month"] = dt.month
                out_dict["day"] = dt.day
            except dateutil.parser.ParserError:
                pass
    return out_dict


def map_from_submit_site(submit_str):
    try:
        submit_str_unicode_unescaped = \
            submit_str.encode('utf-8').decode('unicode_escape')
    except UnicodeError as e:
        raise FaultyRecordError(f"Unicode Error: {e}")
    try:
        data = json.loads(submit_str_unicode_unescaped)
    except json.JSONDecodeError as e:
        raise FaultyRecordError(f"Error decoding JSON: {e}")

    try:

        # Submit site api returns a list, so index first and only element
        if isinstance(data, list):
            if len(data) == 1:
                data = data[0]
            else:
                raise FaultyRecordError(
                    "Submit site data is a list with multiple elements"
                )

        data = utils.replace_hyphens_with_underscores(data)

        # Instantiate Citation object with high-level data
        new_citation = Citation(
            title=utils.clean_dict_key(data, 'title'),
            DOI=utils.clean_dict_key(data, "doi"),
            container_title=[utils.clean_dict_key(data, "journal")],
            abstract=utils.clean_dict_key(data, "abstract"),
            volume=utils.clean_dict_key(data, "volume"),
            issue=utils.clean_dict_key(data, "issue")
        )
        if "issn" in data.keys():
            new_citation.ISSN["issn"] = data["issn"]

        # Set date data
        publication_datestring = utils.clean_dict_key(data, "publication_date")
        if publication_datestring and publication_datestring != "":
            new_citation.date["published"] = \
                date_string_to_dict(publication_datestring)

        modification_datestring = utils.clean_dict_key(data, "changed")
        if modification_datestring and modification_datestring != "":
            new_citation.date["submission_modification"] = \
                date_timestamp_to_dict(modification_datestring)

        creation_datestring = utils.clean_dict_key(data, "created")
        if creation_datestring and creation_datestring != "":
            new_citation.date["submission_created"] = \
                date_timestamp_to_dict(creation_datestring)

        # Add page data. Submit site provides first and last pages.
        new_citation.page_first_last = (
            utils.clean_dict_key(data, "first_page"),
            utils.clean_dict_key(data, "last_page")
        )

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
        ids = {"provider_rec": None}
        if "log_number" in data.keys():
            ids["aris"] = utils.clean_dict_key(
                data, "log_number"
            )
        if "submission_node_id" in data.keys():
            ids["submission_node_id"] = utils.clean_dict_key(
                data, "submission_node_id"
            )
            ids["provider_rec"] = utils.clean_dict_key(
                data, "submission_node_id"
            )
        if "accession_number" in data.keys():
            ids["aris_accn_no"] = utils.clean_dict_key(
                data, "accession_number"
            )
        if "mms_id" in data.keys():
            ids["mms_id"] = utils.clean_dict_key(data, "mms_id")

        # Add local data
        new_local = Local(
            identifiers=ids,
            USDA="yes",
            submitter_email=utils.clean_dict_key(data, "submitter_email"),
            submitter_name=utils.clean_dict_key(data, "submitter_name")
        )

        new_citation.local = new_local

        new_resource = Resource(
            primary={},
            secondary=[]
        )
        if "manuscript_file" in data.keys():
            new_resource.primary["URL"] = utils.clean_dict_key(
                data,
                "manuscript_file"
            )
            new_resource.primary["label"] = "Accepted Manuscript"
        if "supplementary_files" in data.keys() and \
                data["supplementary_files"] != "":
            supplementary_files = utils.clean_dict_key(
                data,
                "supplementary_files"
            )
            split_files = supplementary_files.split(", ")
            for i, file in enumerate(split_files):
                new_resource.secondary.append(
                    {
                        "URL": file,
                        "label": "Accepted Manuscript Supporting document",
                        "title": "Supporting document " + str(i + 1)
                    }
                )

        new_citation.resource = new_resource

        return (new_citation, 'success')
    except FaultyRecordError as e:
        return None, "Faulty record: " + str(e)
