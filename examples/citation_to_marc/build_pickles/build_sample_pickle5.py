from citation import Citation, Funder, License, Author, Local, Resource
import pickle

# Citation 1 from
cit5 = Citation(
    title="Title",
    subtitle="Subtitle",
    original_title="Original title",
    publisher="Publisher",
    DOI="DOI value",
    container_title=["Container title"],
    ISSN={"issn1": "ISSN1", "issn2": "ISSN2", "repeated issn": "ISSN1"},
    funder=[
        Funder(
            name="Funder1 name",
            award=["Award 1"],
            DOI="Funder1 doi",
            ROR="Funder1 ror"
        ),
        Funder(
            name="Funder2 name",
            award=["Award 2"]
        )
    ],
    resource=Resource(
        primary={},
        secondary=[]
    ),
    type="type",
    abstract="abstract",
    date={
        "published": {  # Taken from 949, 983, 984. Waiting for confirmation.
            "year": "2000",
            "month": "01",
            "day": "01",
            "string": "2000-01-01"
        },
        "submission_created": {
            "year": "2000",
            "month": "01",
            "day": "01",
            "string": "2000-01-01"
        },
        "submission_modification": {
            "year": "2000",
            "month": "01",
            "day": "01",
            "string": "2000-01-01"
        }
    },
    volume="volume",
    issue="issue",
    _page={"first_page": "first", "last_page": "last", "page_str": "first-last"},
    license=[
        License(
            terms_of_access="Restricted Access",
            content_version="Version of Record",
            url="https://purl.org/eprint/accessRights/RestrictedAccess",
            source_of_term="star",
        )
    ],
    URL="url",
    container_DOI="Container DOI",
    subjects={
        "NALT": [
            {
                "topic": {
                    "term": "nalt term 1",
                    "uri": "nalt uri 1"
                }
            },
            {
                "topic": {
                    "term": "nalt term 2 no uri"
                }
            },
            {
                "geographic": {
                    "term": "geographic term 1",
                    "uri": "geographic uri 1"
                }
            },
            {
                "geographic": {
                    "term": "geographic term 2 no uri"
                }
            },
        ],
        "MeSH": [
            {
                "topic": {
                    "term": "mesh term 1",
                    "uri": "mesh uri 1"
                }
            },
            {
                "topic": {
                    "term": "mesh term 2 no uri"
                }
            },
        ],
        "Uncontrolled": [
            {
                "topic": {
                    "term": "uncontrolled term 1"
                }
            },
            {
                "topic": {
                    "term": "uncontrolled term 2"
                }
            }
        ]
    }
)

cit5.author = Author(
    family="Family name 1",
    given="Given name 1",
    sequence="additional",
    orcid="orcid",
    affiliation=["Affiliation 1", "Affiliation 2"],
)

cit5.author = Author(
    family="Family name 2",
    given="Given name 2",
    sequence="additional",
    orcid="orcid",
    affiliation=["Affiliation 1", "Affiliation 2"],
)

cit5.local = Local(
    identifiers={
        "mms_id": "mmsid",
        "nal_journal_id": "nal_journal_id",
        "agid": "agid value",
        "aris": "aris value",
        "submission_node_id": "submission_node_id",
        "aris_accn_no": "aris_accn_no value",
        "pid": "pid value",
        "hdl": "hdl value",
    },
    USDA="yes"
)

# Save citation object to a pickle
with open("../data/cit5.pkl", "wb") as f:
    pickle.dump(cit5, f)
