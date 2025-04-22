import pytest
from mapper import mapper

# Define data paths in a dictionary
data_paths = {
    "crossref_345": "crossref_345.json",
    "submission_345": "submission_345.json",
    "crossref_1000": "crossref_1000.json",
    "submission_1000": "submission_1000.json",
    "submission_1662": "submission_1662.json",
    "submission_1192": "submission_1192.json",
    "crossref_2000": "crossref_2000.json",
    "submission_2000": "submission_2000.json",
    "submission_2015": "submission_2015.json",
    "crossref_2500": "crossref_2500.json",
    "submission_2500": "submission_2500.json",
    "crossref_2600": "crossref_2600.json",
    "crossref_sample": "crossref_sample.json",
    "crossref_2600_title_list": "crossref_2600_title_list.json",
    "submission_2600": "submission_2600.json",
    "submission_3122": "submission_3122.json",
    "submission_3491": "submission_3491.json",
    "submission_4520": "submission_4520.json",
    "submission_4545": "submission_4545.json",
    "submission_4547": "submission_4547.json",
    "crossref_2600_two_first_authors": "crossref_2600_two_first_authors.json",
    "crossref_2600_no_author_names": "crossref_2600_no_author_names.json",
    "amchsoc_jats": "American_Chemical_Society_jats_source.xml",
    "cambridge_jats": "Cambridge_jats_source.xml",
    "elsvier_consyn": "Elsevier_consyn_source.xml",
    "pagepress_jats": "PAGEPress_jats_source.xml",
    "springer_pubmed": "Springer_pubmed_source.xml",
    "taylor_jats": "Taylor_jats_source.xml",
    "wiley_pubmed": "Wiley_pubmed_source.xml",
    "faulty_record": "faulty_record.json"
}


def load_data(shared_datadir, data_name):
    """Loads data from a file based on the provided name."""
    with open(shared_datadir / data_paths[data_name], "r") as file:
        content = file.read()
        return content


@pytest.fixture()
def crossref_345(shared_datadir):
    return load_data(shared_datadir, "crossref_345")


@pytest.fixture()
def submission_345(shared_datadir):
    return load_data(shared_datadir, "submission_345")


@pytest.fixture()
def crossref_1000(shared_datadir):
    return load_data(shared_datadir, "crossref_1000")


@pytest.fixture()
def submission_1000(shared_datadir):
    return load_data(shared_datadir, "submission_1000")


@pytest.fixture()
def submission_1662(shared_datadir):
    return load_data(shared_datadir, "submission_1662")


@pytest.fixture()
def submission_1192(shared_datadir):
    return load_data(shared_datadir, "submission_1192")


@pytest.fixture()
def crossref_2000(shared_datadir):
    return load_data(shared_datadir, "crossref_2000")


@pytest.fixture()
def submission_2000(shared_datadir):
    return load_data(shared_datadir, "submission_2000")


@pytest.fixture()
def submission_2015(shared_datadir):
    return load_data(shared_datadir, "submission_2015")


@pytest.fixture()
def crossref_2500(shared_datadir):
    return load_data(shared_datadir, "crossref_2500")


@pytest.fixture()
def submission_2500(shared_datadir):
    return load_data(shared_datadir, "submission_2500")


@pytest.fixture()
def crossref_2600(shared_datadir):
    return load_data(shared_datadir, "crossref_2600")


@pytest.fixture()
def submission_2600(shared_datadir):
    return load_data(shared_datadir, "submission_2600")


@pytest.fixture()
def submission_3122(shared_datadir):
    return load_data(shared_datadir, "submission_3122")


@pytest.fixture()
def submission_3491(shared_datadir):
    return load_data(shared_datadir, "submission_3491")


@pytest.fixture()
def submission_4520(shared_datadir):
    return load_data(shared_datadir, "submission_4520")


@pytest.fixture()
def submission_4545(shared_datadir):
    return load_data(shared_datadir, "submission_4545")


@pytest.fixture()
def submission_4547(shared_datadir):
    return load_data(shared_datadir, "submission_4547")


@pytest.fixture()
def crossref_sample(shared_datadir):
    return load_data(shared_datadir, "crossref_sample")


@pytest.fixture()
def crossref_2600_title_list(shared_datadir):
    return load_data(shared_datadir, "crossref_2600_title_list")


@pytest.fixture()
def crossref_2600_two_first_authors(shared_datadir):
    return load_data(shared_datadir, "crossref_2600_two_first_authors")


@pytest.fixture()
def crossref_2600_no_author_names(shared_datadir):
    return load_data(shared_datadir, "crossref_2600_no_author_names")


@pytest.fixture()
def faulty_record(shared_datadir):
    return load_data(shared_datadir, "faulty_record")


@pytest.fixture(scope="session")
def generic_mapper_test(
        data, expected_message, expected_number_of_elements, element=None
):
    """
    Generic test function for mapping records different formats and schemas to
    a normalized Python object based on
    the Crossref schema.

    Args:
        data (str): The data to be mapped.
        expected_message (str): The expected message from the mapper.
        expected_number_of_elements (int): The expected number of top
        level elements after mapping.
        element (str, optional): An optional element to check within the
        article.
    """
    crossref_object, message = mapper(data)
    assert message == expected_message
    assert len(crossref_object) == expected_number_of_elements
    if element:
        assert element in crossref_object
