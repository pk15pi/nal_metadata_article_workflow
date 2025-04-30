import pytest
from citation_to_marc import citation_to_marc
from citation import Citation, Local, Resource, License, Author, Funder
import pickle
import pymarc
from pathlib import Path

def load_pkl(shared_datadir, file_name):
    """Loads data from a file based on the provided name."""
    with open(shared_datadir / file_name, "rb") as file:
        # Read in pickled citation object
        citation_object = pickle.load(file)
        return citation_object

def load_marcxml(shared_datadir, file_name):
    """Loads data from a file based on the provided name into pymarc."""
    with open(shared_datadir / file_name, "r") as file:
        pymarc_record = pymarc.marcxml.parse_xml_to_array(file)[0]
        return pymarc_record

@pytest.fixture()
def cit1(shared_datadir):
    return load_pkl(shared_datadir, "cit1.pkl")

@pytest.fixture()
def cit2(shared_datadir):
    return load_pkl(shared_datadir, "cit2.pkl")

@pytest.fixture()
def cit3(shared_datadir):
    return load_pkl(shared_datadir, "cit3.pkl")

@pytest.fixture()
def cit4(shared_datadir):
    return load_pkl(shared_datadir, "cit4.pkl")

@pytest.fixture()
def cit5(shared_datadir):
    return load_pkl(shared_datadir, "cit5.pkl")

@pytest.fixture()
def cit6(shared_datadir):
    return load_pkl(shared_datadir, "cit6.pkl")

@pytest.fixture()
def marc_record1(shared_datadir):
    return load_marcxml(shared_datadir, "marc_record1.xml")

@pytest.fixture()
def marc_record2(shared_datadir):
    return load_marcxml(shared_datadir, "marc_record2.xml")

@pytest.fixture()
def marc_record3(shared_datadir):
    return load_marcxml(shared_datadir, "marc_record3.xml")

@pytest.fixture()
def marc_record4(shared_datadir):
    return load_marcxml(shared_datadir, "marc_record4.xml")

@pytest.fixture()
def marc_record5(shared_datadir):
    return load_marcxml(shared_datadir, "marc_record5.xml")

@pytest.fixture()
def marc_record6(shared_datadir):
    return load_marcxml(shared_datadir, "marc_record6.xml")

