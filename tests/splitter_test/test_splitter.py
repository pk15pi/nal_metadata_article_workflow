import os
import pytest
import pytest_datadir
from splitter import splitter

pytest_plugins = ["pytest_datadir"]


def generic_split_test(data, expected_message, expected_length, key=None):
    """
    Generic test function for splitting different data formats.

    Args:
        data (str): The data to be split.
        expected_message (str): The expected message from the splitter.
        expected_length (int): The expected number of articles after splitting.
        key (str, optional): An optional key to check within the first article.
    """
    list_of_articles, message = splitter(data)
    assert message == expected_message
    assert len(list_of_articles) == expected_length
    if key:
        assert key in list_of_articles[0]


def test_split_crossref_json(crossref_api_response):
    generic_split_test(crossref_api_response, "successful", 1, "type")


def test_split_chorus_json(chorus_api_response):
    generic_split_test(chorus_api_response, "successful", 1, "DOI")


def test_split_submit_site_json(submission_api_collection):
    generic_split_test(submission_api_collection, "successful", 25, "submission_node_id")


def test_split_json(unknown_json):
    generic_split_test(unknown_json, "Unknown JSON metadata", 0)


def test_split_amchsoc_xml(amchsoc_jats):
    generic_split_test(amchsoc_jats, "successful", 1)


def test_split_cambridge_jats_xml(cambridge_jats):
    generic_split_test(cambridge_jats, "successful", 1)


def test_split_elsvier_consyn_xml(elsvier_consyn):
    generic_split_test(elsvier_consyn, "successful", 1)


def test_split_pagepress_jats_xml(pagepress_jats):
    generic_split_test(pagepress_jats, "successful", 1)


def test_split_springer_pubmed_xml(springer_pubmed):
    generic_split_test(springer_pubmed, "successful", 5)


def test_split_taylor_xml(taylor_jats):
    generic_split_test(taylor_jats, "successful", 1)


def test_split_wiley_xml(wiley_pubmed):
    generic_split_test(wiley_pubmed, "successful", 9)


def test_broken_xml(broken_xml):
    message = 'XML Error: Premature end of data in tag Article line 4, line 6, column 1 (<string>, line 6)'
    generic_split_test(broken_xml, message, 0)


def test_broken_json(broken_json):
    message = "JSON Error: Expecting ',' delimiter: line 4 column 1 (char 14)"
    generic_split_test(broken_json, message, 0)


def test_split_bad_txt(simple_text):
    generic_split_test(simple_text, "Unknown metadata format", 0)
