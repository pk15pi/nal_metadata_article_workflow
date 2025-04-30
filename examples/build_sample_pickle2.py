from citation import Citation, Funder, License, Author, Local, Resource
import pickle

# Citation 1 from
cit2 = Citation(
    title="The Same Source of Microbes has a Divergent Assembly Trajectory Along a Hot Spring Flowing Path ",
    subtitle=None,
    original_title=None,
    publisher=None,
    DOI="10.1111/mec.17727",
    container_title=[""],
    ISSN={"issn": "0962-1083"},
    resource=Resource(),
    type="journal-article",
    abstract="Hot spring microbial mats represent intricate biofilms that \
    establish self‐sustaining ecosystems, hosting diverse microbial \
    communities which facilitate a range of biochemical processes and \
    contribute to the structural and functional complexity of these systems. \
    While community structuring across mat depth has received substantial \
    attention, mechanisms shaping horizontal spatial composition and \
    functional structure of these communities remain understudied. Here, we \
    explored the contributions of species source, local environment and \
    species interaction to microbial community assembly processes in six \
    microbial mat regions following a flow direction with a temperature \
    decreasing from 73.3°C to 52.8°C. Surprisingly, we found that despite \
    divergent community structures and potential functions across different \
    microbial mats, large proportions of the community members \
    (45.50%–80.29%) in the recipient mat communities originated from the same \
    source community at the upper limit of temperature for photosynthetic \
    life. This finding indicated that the source species were dispersed with \
    water and subsequently filtered and shaped by local environmental \
    factors. Furthermore, critical species with specific functional \
    attributes played a pivotal role in community assembly by influencing \
    potential interactions with other microorganisms. Therefore, species \
    dispersal via water flow, environmental variables, and local species \
    interaction jointly governed microbial assembly, elucidating assembly \
    processes in the horizontal dimension of hot spring microbial mats and \
    providing insights into microbial community assembly within extreme \
    biospheres. ",
    date={
        "published": {  # Taken from 949, 983, 984. Waiting for confirmation.
            "year": "2025",
            "month": "04",
            "day": "08",
            "string": "2025-04-08"
        }
    },
    volume="34",
    issue="8",
    _page={"first_page": "", "last_page": "", "page_str": "e17727-"},
    license=[],
    URL="https://dx.doi.org/10.1111/mec.17727",
    container_DOI=None,
    subjects={
        "NALT": [
            {
                "topic": {
                    "term": "biofilm",
                    "uri": "https://lod.nal.usda.gov/nalt/17347"
                },
            },
            {
                "topic": {
                    "term": "hot springs",
                    "uri": "https://lod.nal.usda.gov/nalt/196124"
                },
            },
            {
                "topic": {
                    "term": "microbial communities",
                    "uri": "https://lod.nal.usda.gov/nalt/196371"
                },
            },
            {
                "topic": {
                    "term": "photosynthesis",
                    "uri": "https://lod.nal.usda.gov/nalt/14059"
                },
            },
            {
                "topic": {
                    "term": "species",
                    "uri": "https://lod.nal.usda.gov/nalt/350021"
                },
            },
            {
                "topic": {
                    "term": "species dispersal",
                    "uri": "https://lod.nal.usda.gov/nalt/188673"
                },
            },
            {
                "topic": {
                    "term": "temperature",
                    "uri": "https://lod.nal.usda.gov/nalt/5861"
                },
            },
            {
                "topic": {
                    "term": "water flow",
                    "uri": "https://lod.nal.usda.gov/nalt/43956"
                },
            },
        ],
    },
)


cit2.author = Author(
    family="He",
    given="Qing",
    sequence="first",
    affiliation=["CAS Key Laboratory for Environmental Biotechnology, \
    Research Center for Eco‐Environmental Sciences, Chinese Academy of \
    Sciences (CAS), Beijing, China"],
)

cit2.author = Author(
    family="Wang",
    given="Shang",
    sequence="additional",
    affiliation=["CAS Key Laboratory for Environmental Biotechnology, \
    Research Center for Eco‐Environmental Sciences, Chinese Academy of \
    Sciences (CAS), Beijing, China"]
)

cit2.author = Author(
    family="Feng",
    given="Kai",
    sequence="additional",
    affiliation=["CAS Key Laboratory for Environmental Biotechnology, \
    Research Center for Eco‐Environmental Sciences, Chinese Academy of \
    Sciences (CAS), Beijing, China"]
)

cit2.author = Author(
    family="Hou",
    given="Weiguo",
    sequence="additional",
    affiliation=["State Key Laboratory of Biogeology and Environmental \
    Geology, China University of Geosciences, Beijing, China "]
)

cit2.author = Author(
    family="Zhang",
    given="Wenhui",
    sequence="additional",
    affiliation=["State Key Laboratory of Biogeology and Environmental \
    Geology, China University of Geosciences, Beijing, China "]
)

cit2.author = Author(
    family="Li",
    given="Fangru",
    sequence="additional",
    affiliation=["State Key Laboratory of Biogeology and Environmental \
    Geology, China University of Geosciences, Beijing, China "]
)

cit2.author = Author(
    family="Zhang",
    given="Yidi",
    sequence="additional",
    affiliation=["State Key Laboratory of Biogeology and Environmental \
    Geology, China University of Geosciences, Beijing, China "]
)

cit2.author = Author(
    family="Hai",
    given="Wanming",
    sequence="additional",
    affiliation=["State Key Laboratory of Biogeology and Environmental \
    Geology, China University of Geosciences, Beijing, China "]
)

cit2.author = Author(
    family="Sun",
    given="Yuxuan",
    sequence="additional",
    affiliation=["State Key Laboratory of Biogeology and Environmental \
    Geology, China University of Geosciences, Beijing, China "]
)

cit2.author = Author(
    family="Deng",
    given="Ye",
    sequence="additional",
    affiliation=["CAS Key Laboratory for Environmental Biotechnology, \
    Research Center for Eco‐Environmental Sciences, Chinese Academy of \
    Sciences (CAS), Beijing, China"]
)

cit2.funder = [
    Funder(
        name="National Nature Science Foundation of China",
        award=["92351303", "U23A2043"]
    )
]

cit2.local = Local(
    identifiers={
        "mms_id": "9916798845507426",
        "nal_journal_id": "Journal:jnl48811",
        "agid": "8994725"
    },
    USDA="no"
)

# Save citation object to a pickle
with open("example_data/cit2.pkl", "wb") as f:
    pickle.dump(cit2, f)
