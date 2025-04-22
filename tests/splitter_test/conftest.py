import pytest

# Define data paths in a dictionary
data_paths = {
    "crossref_api_response": "crossref_api_response.json",
    "submission_api_collection": "submit_site_api_collection.json",
    "amchsoc_jats": "American_Chemical_Society_jats.xml",
    "cambridge_jats": "Cambridge_jats.xml",
    "elsvier_consyn": "Elsevier_consyn.xml",
    "pagepress_jats": "PAGEPress_jats.xml",
    "springer_pubmed": "Springer_pubmed.xml",
    "taylor_jats": "Taylor_jats.xml",
    "wiley_pubmed": "Wiley_pubmed.xml",
    "chorus_api_response": "chorus_api.json"
}


def load_data(shared_datadir, data_name):
    """Loads data from a file based on the provided name."""
    with open(shared_datadir / data_paths[data_name], "r") as file:
        return file.read()


@pytest.fixture()
def crossref_api_response(shared_datadir):
    return load_data(shared_datadir, "crossref_api_response")


@pytest.fixture()
def chorus_api_response(shared_datadir):
    return load_data(shared_datadir, "chorus_api_response")


@pytest.fixture()
def submission_api_collection(shared_datadir):
    return load_data(shared_datadir, "submission_api_collection")


@pytest.fixture()
def amchsoc_jats(shared_datadir):
    return load_data(shared_datadir, "amchsoc_jats")


@pytest.fixture()
def cambridge_jats(shared_datadir):
    return load_data(shared_datadir, "cambridge_jats")


@pytest.fixture()
def elsvier_consyn(shared_datadir):
    return load_data(shared_datadir, "elsvier_consyn")


@pytest.fixture()
def pagepress_jats(shared_datadir):
    return load_data(shared_datadir, "pagepress_jats")


@pytest.fixture()
def springer_pubmed(shared_datadir):
    return load_data(shared_datadir, "springer_pubmed")


@pytest.fixture()
def taylor_jats(shared_datadir):
    return load_data(shared_datadir, "taylor_jats")


@pytest.fixture()
def wiley_pubmed(shared_datadir):
    return load_data(shared_datadir, "wiley_pubmed")


@pytest.fixture()
def simple_text():
    return "Simple text"


@pytest.fixture(scope="session")
def broken_xml():
    text = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ArticleSet PUBLIC "-//NLM//DTD PubMed 2.8//EN" \
"https://dtd.nlm.nih.gov/ncbi/pubmed/in/PubMed.dtd">
<ArticleSet>
   <Article>
      <Journal>Journal of camping</Journal>
'''
    return text


@pytest.fixture(scope="session")
def broken_json():
    text = '''
[
  {"id":1}

'''
    return text


@pytest.fixture(scope="session")
def unknown_json():
    text = '''
[
  {"id":1}
]
'''
    return text
