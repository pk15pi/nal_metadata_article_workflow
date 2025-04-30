from citation import Citation, Funder, License, Author, Local, Resource
import pickle

# Citation 1 from
cit4 = Citation(
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
        }
    },
    volume="volume",
    issue="issue",
    _page={"first_page": "first", "last_page": "last", "page_str": "first-last"},
    license=[
        License(
            version="License1 version",
            url="License1 url"
        ),
        License(
            version="License2 version",
            url="License2 url"
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

cit4.author = Author(
    family="Family name",
    given="Given name",
    sequence="first",
    orcid="orcid",
    affiliation=["Affiliation 1", "Affiliation 2"],
)

cit4.author = Author(
    family="Family name",
    given="Given name",
    sequence="additional",
    orcid="orcid",
    affiliation=["Affiliation 1", "Affiliation 2"],
)

cit4.local = Local(
    identifiers={
        "mms_id": "mmsid",
        "nal_journal_id": "nal_journal_id",
        "agid": "agid value",
        "aris": "aris value",
        "aris_accn_no": "aris_accn_no value",
    },
    USDA="no"
)

# Save citation object to a pickle
with open("example_data/cit4.pkl", "wb") as f:
    pickle.dump(cit4, f)
