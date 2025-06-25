import pytest
from citation import Citation, Author, License, Local, Resource


@pytest.fixture
def base_citation_usda():
    base_citation = Citation(
        title="Title",
        publisher="Publisher",
        volume="Volume",
        issue="Issue",
        type="journal-article",
        date={
            "published": {
                "year": 2000,
                "month": 1,
                "day": 1,
                "string": "2000-01-01T00:00:00Z"
            },
        },
        DOI="10.0000/000000",
        abstract="This is a valid abstract for a journal article and it is " +
                 "longer than 50 characters.",
        container_DOI="10.0000.000000",
        ISSN={"e-issn": "0000-0000", "p-issn": "1111-1111"}
    )

    author1 = Author(
        given="John",
        family="Doe",
        orcid="0000-0000-0000-0000",
        affiliation="Affiliation",
        sequence="first"
    )

    author2 = Author(
        given="John",
        family="Doe",
        orcid="0000-0000-0000-0000",
        affiliation="Affiliation",
        sequence="second"
    )

    base_citation.author = author1
    base_citation.author = author2

    base_citation.page_first_last = ("1", "10")

    license = License(
        content_version="1.0",
        url="https://www.example.com"
    )

    base_citation.license = [license]

    local = Local(
        identifiers={"mms_id": "mmsid1", "provider_rec": None},
        USDA="yes",
        cataloger_notes=[],
        submitter_email="email@email.com"
    )

    base_citation.local = local

    resource = Resource(
        primary={
            "URL": "file1.pdf"
        },
        secondary=[]
    )
    base_citation.resource = resource

    return base_citation

@pytest.fixture
def base_citation_non_usda():
    base_citation = Citation(
        title="Title",
        publisher="Publisher",
        volume="Volume",
        issue="Issue",
        type="journal-article",
        date={
            "published": {
                "year": 2000,
                "month": 1,
                "day": 1,
                "string": "2000-01-01T00:00:00Z"
            },
        },
        DOI="10.0000/000000",
        abstract="This is a valid abstract for a journal article and it is " +
                 "longer than 50 characters.",
        container_DOI="10.0000.000000",
        ISSN={"e-issn": "0000-0000", "p-issn": "1111-1111"}
    )

    author1 = Author(
        given="John",
        family="Doe",
        orcid="0000-0000-0000-0000",
        affiliation="Affiliation",
        sequence="first"
    )

    author2 = Author(
        given="John",
        family="Doe",
        orcid="0000-0000-0000-0000",
        affiliation="Affiliation",
        sequence="second"
    )

    base_citation.author = author1
    base_citation.author = author2

    base_citation.page_first_last = ("1", "10")

    license = License(
        content_version="1.0",
        url="https://www.example.com"
    )

    base_citation.license = [license]

    local = Local(
        identifiers={"mms_id": "mmsid1", "provider_rec": None},
        USDA="no",
        cataloger_notes=[],
        submitter_email="email@email.com"
    )

    base_citation.local = local

    resource = Resource(
        primary={
            "URL": "file1.pdf"
        },
        secondary=[]
    )
    base_citation.resource = resource

    return base_citation
