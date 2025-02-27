from citation import *
import pytest
import pytest_datadir
pytest_plugins = ["pytest_datadir"]
import json


def test_citation_creation(citation_object):
    assert citation_object.title == "A diverse diet increases animal growth performance and carcass yield of grazing lambs "
    assert citation_object.DOI == '10.1093/tas/txae103'
    assert citation_object.container_title == 'Translational Animal Science'
    assert citation_object.ISSN == {"issn": "2573-2102"}
    assert citation_object.type == "article"
    assert citation_object.abstract[0:23] == "The current experiments"
    # assert citation_object.publication_date == ??? <-- fill in once we have the appropriate mapping
    assert citation_object.volume == "8"
    assert citation_object.issue == ""
    assert len(citation_object.author) == 4
    assert citation_object.author[0].given == "Matthew R."
    assert citation_object.author[1].given == "Konagh"
    assert citation_object.author[2].given == "Cameron J."
    assert citation_object.author[3].given == "Pablo"
    assert citation_object.funder[0].name == 'Agricultural Research Service (ARS)'
    assert citation_object.funder[0].award == ['']
    assert citation_object.license[0].version == 'accepted_manuscript'
    assert citation_object.page["first_page"] == "txae103"
    assert citation_object.page["last_page"] == ""
    assert citation_object.page["page_str"] == None
    #assert citation_object.local.standard_number_aris == "413627"
    #assert citation_object.local.submission_node_id == "2500"
    assert citation_object.local.manuscript_file == 'https://submit.nal.usda.gov/sites/default/files/manuscripts/Log%20413627%20-%2003%20413627.Accepted%20Manuscript.Beck.2024-03-07.pdf'
    assert citation_object.local.supplementary_files == ""
    assert citation_object.local.submission_date == "1723556153"
    assert citation_object.local.modification_date == "1727109137"
    assert citation_object.local.date_other == ""
    assert citation_object.local.USDA == "yes"
    assert citation_object.local.cataloger_notes == []
    assert citation_object.local.identifiers == {
        "standard_number_aris": "413627",
        "submission_node_id": "2500",
        "accession_number": "441154",
        "provider_rec": "2500"
    }
    #assert citation_object.local.accession_number == "441154"
    assert citation_object.step3_info() == {'title': 'A diverse diet increases animal growth performance and carcass yield of grazing lambs ', 'doi': '10.1093/tas/txae103', 'type': 'article', 'provider_rec': "2500"}
    assert citation_object.get_journal_info() == {'container_DOI': None, 'journal_title': "Translational Animal Science", 'publisher': None,'issn': ['2573-2102'], "usda": "yes"}


