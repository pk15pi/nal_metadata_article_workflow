import json
import pprint
from citation import *
from mapper import utils
from mapper.errors import FaultyRecordError

def value_or_none(dict, key):
    try:
        return dict[key]
    except:
        return None

def str_value_or_none(dict, key):
    try:
        return str(dict[key])
    except:
        return None

def first_value_or_none(dict, key):
    try:
        return dict[key][0]
    except:
        return None

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
        title=value_or_none(data,'title'),
        subtitle=value_or_none(data,'subtitle'),
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
                award=data["funder"][i].get("award", None)
            )
            new_citation.funder.append(new_funder)

    # Add license data
    if "license" in data.keys():
        for i, license in enumerate(data["license"]):
            new_license = License(
                version = value_or_none(license, 'content-version'),
                url = value_or_none(license, 'URL')
            )
            new_citation.license.append(new_license)

    # Add author data
    if "author" in data.keys():
        for auth in data["author"]:
            new_author = Author(
                given=value_or_none(auth, "given"), # Required, throws key error if DNE
                family=value_or_none(auth, "family"), # Required, throws key error if DNE
                orcid=value_or_none(auth, "ORCID"),
                affiliation=value_or_none(auth, "affiliation"),
                sequence=value_or_none(auth,"sequence")
            )
            new_citation.author = new_author

    # Create dict of identifiers
    ids = {"provider_rec": new_citation.DOI}
    new_local = Local(
        identifiers=ids,
    )
    new_citation.local = new_local


    return (new_citation, 'success')
