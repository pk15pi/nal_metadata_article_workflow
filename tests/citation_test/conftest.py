import pytest
import json
from citation import *

# Define data paths in a dictionary
data_paths = {
    "submission_2500_json": "submission_2500.json"
}


def load_data(shared_datadir, data_name):
    """Loads data from a file based on the provided name."""
    with open(shared_datadir / data_paths[data_name], "r") as file:
        return json.load(file)[0] # index because submission data is a list with one elem

@pytest.fixture()
def submission_source(shared_datadir):
    print(shared_datadir)
    return load_data(shared_datadir, "submission_2500_json")

@pytest.fixture()
def citation_object(submission_source):
    citation = Citation(
        title=submission_source['title'],
        DOI=submission_source['doi'],
        container_title=submission_source['journal'],
        ISSN={"issn": submission_source['issn']},
        abstract=submission_source['abstract'],
        type="article",
        volume=str(submission_source["volume"]),
        issue=submission_source["issue"],
    )

    citation.page_first_last = (submission_source["first_page"], submission_source["last_page"])

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
        version=submission_source["manuscript_version"]
    )
    citation.license = [new_license]

    new_local = Local(
        manuscript_file=submission_source["manuscript_file"],
        supplementary_files=submission_source["supplementary_files"],
        submission_date=str(submission_source["created"]),
        modification_date=str(submission_source["changed"]),
        date_other=str(submission_source["date_other"]),
        identifiers={
            "standard_number_aris": str(submission_source["log_number"]),
            "submission_node_id": str(submission_source["submission_node_id"]),
            "accession_number": str(submission_source["accession_number"]),
            "provider_rec": str(submission_source["submission_node_id"])
        },
        USDA="yes"
    )
    citation.local = new_local

    return citation
