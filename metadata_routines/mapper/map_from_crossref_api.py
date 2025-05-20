import json
from citation import Citation, Author, Funder, License, Local, Resource
from mapper import utils
from mapper.errors import FaultyRecordError


def value_or_none(dict, key):
    try:
        return dict[key]
    except (KeyError, TypeError):
        return None


def str_value_or_none(dict, key):
    try:
        return str(dict[key])
    except (KeyError, TypeError):
        return None


def first_value_or_none(dict, key):
    try:
        return dict[key][0]
    except (KeyError, TypeError, IndexError):
        return None


def parse_date_data(date_dict):
    out_dict = {}
    if "date_parts" in date_dict.keys():
        if len(date_dict["date_parts"]) == 1 and \
                len(date_dict["date_parts"][0]) == 3:
            out_dict["year"] = date_dict["date_parts"][0][0]
            out_dict["month"] = date_dict["date_parts"][0][1]
            out_dict["day"] = date_dict["date_parts"][0][2]
        elif len(date_dict["date_parts"]) == 1 and \
                len(date_dict["date_parts"][0]) == 1:
            out_dict["year"] = date_dict["date_parts"][0][0]
    if "date_time" in date_dict.keys():
        out_dict["string"] = date_dict["date_time"]
    elif "timestamp" in date_dict.keys():
        out_dict["string"] = date_dict["timestamp"]
    return out_dict


def map_from_crossref_api(crossref_str):
    try:
        data = json.loads(crossref_str)
    except json.JSONDecodeError as e:
        raise FaultyRecordError(f"Error decoding JSON: {e}")

    data = utils.replace_hyphens_with_underscores(data)

    if "message" in data.keys():
        data = data["message"]

    # Instantiate Citation object with high-level data
    new_citation = Citation(
        title=value_or_none(data, 'title'),
        subtitle=value_or_none(data, 'subtitle'),
        original_title=value_or_none(data, 'original_title'),
        publisher=value_or_none(data, 'publisher'),
        DOI=value_or_none(data, 'DOI'),
        container_title=value_or_none(data, 'container_title'),
        abstract=str_value_or_none(data, 'abstract'),
        volume=first_value_or_none(data, 'volume'),
        issue=value_or_none(data, 'issue'),
    )

    # If title element is a list, concatenate the strings in the list
    if isinstance(new_citation.title, list):
        new_citation.title = ' '.join(new_citation.title)

    # If subtitle element is a list, concatenate the strings in the list
    if isinstance(new_citation.subtitle, list):
        new_citation.subtitle = ' '.join(new_citation.subtitle)

    # If original_title element is a list, concatenate the strings in the list
    if isinstance(new_citation.original_title, list):
        new_citation.original_title = ' '.join(new_citation.original_title)

    # Add date data
    if "published_print" in data.keys():
        new_citation.date["published-print"] = \
            parse_date_data(data["published_print"])
    if "published" in data.keys():
        new_citation.date["published"] = parse_date_data(data["published"])
    if "published_online" in data.keys():
        new_citation.date["published-online"] = \
            parse_date_data(data["published_online"])
    if "published_other" in data.keys():
        new_citation.date["published-other"] = \
            parse_date_data(data["published_other"])

    # Specify e-issn and p-issn if provided
    if "issn_type" in data.keys():
        issn_type = data["issn_type"]
        for issn_type_dict in issn_type:
            if issn_type_dict["type"] == "print":
                new_citation.ISSN["p-issn"] = issn_type_dict["value"]
            elif issn_type_dict["type"] == "electronic":
                new_citation.ISSN["e-issn"] = issn_type_dict["value"]
    elif "ISSN" in data.keys():
        if isinstance(data["ISSN"], list):
            new_citation.ISSN["issn"] = data["ISSN"][0]
        elif isinstance(data["ISSN"], str):
            new_citation.ISSN["issn"] = data["ISSN"]

    # Set page data. Crossref provides a page string for all page data.
    if "page" in data.keys():
        new_citation.page_str = data["page"]
    else:
        new_citation.page_str = None

    # Add funder data
    if "funder" in data.keys():
        for i, funder in enumerate(data["funder"]):
            new_funder = Funder(
                name=data["funder"][i].get("name", None),
                award=data["funder"][i].get("award", None),
                DOI=data["funder"][i].get("DOI", None),
                ROR=data["funder"][i].get("ROR", None)
            )
            new_citation.funder.append(new_funder)

    # Add license data
    if "license" in data.keys():
        for i, license in enumerate(data["license"]):
            new_license = License(
                content_version=value_or_none(license, 'content-version'),
                url=value_or_none(license, 'URL')
            )
            new_citation.license.append(new_license)

    # Add author data
    if "author" in data.keys():
        for auth in data["author"]:
            affiliation_list_of_dicts = value_or_none(auth, "affiliation")
            aff_list = [aff["name"] for aff in affiliation_list_of_dicts]
            new_author = Author(
                given=value_or_none(auth, "given"),
                family=value_or_none(auth, "family"),
                orcid=value_or_none(auth, "ORCID"),
                affiliation=aff_list,
                sequence=value_or_none(auth, "sequence")
            )
            new_citation.author = new_author

    # Create dict of identifiers
    ids = {"provider_rec": new_citation.DOI}
    new_local = Local(
        identifiers=ids,
    )
    new_citation.local = new_local

    new_citation.resource = Resource(
        primary={},
        secondary=[]
    )

    return (new_citation, 'success')
