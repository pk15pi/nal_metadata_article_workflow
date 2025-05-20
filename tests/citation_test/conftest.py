import pytest
import json
from citation import Citation, Author, Funder, License, Local, Resource
from datetime import datetime

# Define data paths in a dictionary
data_paths = {
    "submission_2500_json": "submission_2500.json"
}


def load_data(shared_datadir, data_name):
    """Loads data from a file based on the provided name."""
    with open(shared_datadir / data_paths[data_name], "r") as file:
        # index because submission data is a list with one elem
        return json.load(file)[0]


@pytest.fixture()
def submission_source(shared_datadir):
    print(shared_datadir)
    return load_data(shared_datadir, "submission_2500_json")


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


@pytest.fixture()
def citation_object(submission_source):
    citation = Citation(
        title=submission_source['title'],
        DOI=submission_source['doi'],
        container_title=[submission_source['journal']],
        ISSN={"issn": submission_source['issn']},
        abstract=submission_source['abstract'],
        type="article",
        volume=str(submission_source["volume"]),
        issue=submission_source["issue"],
    )

    citation.date["published"] = date_string_to_dict(
        submission_source["publication_date"]
    )

    citation.page_first_last = (
        submission_source["first_page"],
        submission_source["last_page"]
    )

    for auth in submission_source["authors"]:
        new_author = Author(
            given=auth["first_name"],
            family=auth["last_name"],
            orcid=auth["orcid"],
            affiliation=[auth["affiliation"]],
        )
        citation.author = new_author

    for funder in submission_source["funding_agencies"]:
        new_funder = Funder(
            name=funder["name"],
            award=[funder["award_number"]]
        )
        citation.funder.append(new_funder)

    new_license = License(
        content_version=submission_source["manuscript_version"]
    )
    citation.license = [new_license]

    new_local = Local(
        identifiers={
            "standard_number_aris": str(submission_source["log_number"]),
            "submission_node_id": str(submission_source["submission_node_id"]),
            "accession_number": str(submission_source["accession_number"]),
            "provider_rec": str(submission_source["submission_node_id"])
        },
        USDA="yes"
    )
    citation.local = new_local

    new_resource = Resource(
        primary={
            "URL": submission_source["manuscript_file"]
        },
        secondary=[]
    )
    citation.resource = new_resource

    return citation
