from citation import Citation, Funder, License, Author, Local, Resource
import pickle

# Citation 1 from
cit1 = Citation(
    title="A bibliometric study of scientific literature on obesity research in PubMed (1988-2007)",
    subtitle=None,
    original_title=None,
    publisher=None,
    DOI="10.1111/j.1467-789X.2009.00647.x",
    container_title=["Obesity reviews. "],
    ISSN={"issn": "1467-7881"},
    funder=[],
    resource=Resource(),
    type="journal-article",
    abstract="This article describes a bibliometric review of the \
    publications on obesity research in PubMed over the last 20 years. We \
    used Medline via the PubMed online service of the US National Library of \
    Medicine from 1988 to 2007. The search strategy was: ([obesity] in MesH). \
    A total of 58 325 references were retrieved, 25.5% in 1988-1997, and 74.5%\
     in 1998-2007. The growth in the number of publications showed an \
     exponential increase. The references were published in 3613 different \
     journals, with 20 journals contributing 25% of obesity literature. The \
     two journals contributing most were the International Journal of Obesity \
     (5.1%), Obesity-Obesity Research (2.9%). North America and Europe were \
     the most productive world areas with 44.1% and 37.9% of the literature, \
     respectively. The US was the predominant country in number of \
     publications, followed by the United Kingdom, Japan and Italy. The \
     ranking of production changed when the number of publications was \
     normalized by population, gross domestic product and obesity prevalence \
     by countries. The great increase of publications on obesity during the \
     period 1988-2007 was particularly evident in the second decade of the \
     period which is concordant with the worldwide obesity epidemic. USA and \
     Europe were leaders in the production of scientific articles on obesity.",
    date={
        "published": {  # Taken from 949, 983, 984. Waiting for confirmation.
            "year": "2016",
            "month": "03",
            "day": "14",
            "string": "2016-03-14"
        }
    },
    volume="11",
    issue="8",
    _page={"first_page": "603", "last_page": "611", "page_str": "603-611"},
    license=[],
    URL="http://dx.doi.org/10.1111/j.1467-789X.2009.00647.x",
    container_DOI=None,
    subjects={
        "NALT": [
            {
                "topic": {
                     "term": "Obesity",
                }
            },
            {
                "topic": {
                    "term": "National Library of Medicine"
                }
            },
            {
                "topic": {
                    "term": "gross domestic product"
                }
            },
            {
                "geographic": {
                    "term": "Italy"
                }
            },
            {
                "geographic": {
                    "term": "Japan"
                }
            },
            {
                "geographic": {
                    "term": "United Kingdom"
                }
            },
            {
                "geographic": {
                    "term": "United States"
                }
            },
        ],
        "MeSH": [
            {
                "topic": {
                    "term": "Bibliometrics"
                }
            },
            {
                "topic": {
                    "term": "Biomedical Research"
                }
            },
            {
                "topic": {
                    "term": "Humans"
                }
            },
            {
                "topic": {
                    "term": "MEDLINE"
                }
            },
            {
                "topic": {
                    "term": "Obesity"
                }
            },
            {
                "topic": {
                    "term": "PubMed"
                }
            },

        ],
        "Uncontrolled": [
            {
                "topic": {
                    "term": "literature reviews"
                }
            },
            {
                "topic": {
                    "term": "Bibliometry"
                }
            }
        ]
    }
)

# Add subjects later once mapping established:
# 650	#3$aNational Library of Medicine
# 650	#3$agross domestic product
# 650	#3$aobesity
# 650	#2$aBibliometrics
# 650	#2$aBiomedical Research $xstatistics & numerical data
# 650	#2$aHumans
# 650	#2$aMEDLINE
# 650	#2$aObesity
# 650	#2$aPubMed
# 651	#3$aItaly
# 651	#3$aJapan
# 651	#3$aUnited Kingdom
# 651	#3$aUnited States
# 653	#0$aliterature reviews
# 653	#0$aBibliometry

cit1.author = Author(
    family="Vioque",
    given="J.",
    sequence="first",
    affiliation=[],
)

cit1.author = Author(
    family="Ramos",
    given="J.M.",
    sequence="additional",
    affiliation=[],
)

cit1.author = Author(
    family="Navarrete-Muñoz",
    given="E.M.",
    sequence="additional",
    affiliation=[],
)

cit1.author = Author(
    family="García-de-la-Hera",
    given="M.",
    sequence="additional",
    affiliation=[],
)

cit1.local = Local(
    identifiers={
        "mms_id": "9915765973607426",
        "nal_journal_id": "Journal:jnl3949851",
        "agid": "2264072"
    },
    USDA="no"
)

# Save citation object to a pickle
with open("example_data/cit1.pkl", "wb") as f:
    pickle.dump(cit1, f)
