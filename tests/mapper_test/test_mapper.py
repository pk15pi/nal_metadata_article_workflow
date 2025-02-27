from mapper import mapper
import pytest
import pytest_datadir
pytest_plugins = ["pytest_datadir"]
from citation import *
import json
from mapper import utils
import html
import re
from mapper.errors import FaultyRecordError


def assert_equal_or_DNE(dict, dict_key, object, attribute):
    if dict_key in dict.keys():
        assert dict[dict_key] == getattr(object, attribute)
    else:
        assert getattr(object, attribute) is None

def assert_equal_or_DNE_string_cast(dict, dict_key, object, attribute):
    if dict_key in dict.keys():
        assert str(dict[dict_key]) == getattr(object, attribute)
    else:
        assert getattr(object, attribute) is None

def assert_equal_or_DNE_first_element(dict, dict_key, object, attribute):
    if dict_key in dict.keys():
        assert dict[dict_key][0] == getattr(object, attribute)
    else:
        assert getattr(object, attribute) is None

@pytest.mark.parametrize(
    'crossref_data',
    ["crossref_345", "crossref_1000", "crossref_2000", "crossref_2500",
     "crossref_2600", "crossref_sample", "crossref_2600_title_list",
     "crossref_2600_two_first_authors", "crossref_2600_no_author_names"]
)
def test_crossref_mapper(crossref_data, request):
    loaded_data = request.getfixturevalue(crossref_data)
    data_dict = json.loads(loaded_data)
    result, message = mapper(loaded_data, 'crossref_json')
    assert message == "success"
    assert type(result) == Citation
    data_dict_msg = data_dict['message']

    # Check to see how many elements there are in the title list
    if "title" in data_dict_msg.keys():
        if len(data_dict_msg["title"]) > 1:
            concatenated_titles = ' '.join(data_dict_msg["title"])
            assert concatenated_titles == result.title
        elif len(data_dict_msg["title"]) == 1:
            assert data_dict_msg["title"][0] == result.title

    assert_equal_or_DNE(data_dict_msg, 'DOI', result, 'DOI')
    assert_equal_or_DNE_string_cast(data_dict_msg, 'issue', result, 'issue')
    assert_equal_or_DNE(data_dict_msg, 'publisher', result, 'publisher')

    if "issn-type" in data_dict_msg.keys():
        for issn_type_dict in data_dict_msg["issn-type"]:
            if issn_type_dict["type"] == "print":
                assert result.ISSN['p-issn'] == issn_type_dict["value"]
            elif issn_type_dict["type"] == "electronic":
                assert result.ISSN['e-issn'] == issn_type_dict["value"]
    elif "issn-type" not in data_dict_msg.keys() and "ISSN" in data_dict_msg.keys():
        if isinstance(data_dict_msg["ISSN"], list):
            assert result.ISSN["issn"] == data_dict_msg["ISSN"][0]
        elif isinstance(data_dict_msg["ISSN"], str):
            assert result.ISSN["issn"] == data_dict_msg["ISSN"]

    # Test pages dictionary
    if "page" in data_dict_msg:
        assert data_dict_msg["page"] == result.page["page_str"]
        assert result.page["first_page"] is None
        assert result.page["last_page"] is None
    else:
        assert result.page["page_str"] is None
        assert result.page["first_page"] is None
        assert result.page["last_page"] is None

    # Test funder data
    if "funder" in data_dict_msg.keys():
        for i, funder in enumerate(data_dict_msg["funder"]):
            if "name" in funder.keys():
                assert result.funder[i].name == funder["name"]
            if "award" in funder.keys():
                assert result.funder[i].award == funder["award"]
    else:
        assert result.funder == []

    # Test authors
    if "author" in data_dict_msg.keys():
        for i, author in enumerate(data_dict_msg["author"]):
            assert_equal_or_DNE(data_dict_msg["author"][i], "given", result.author[i], "given")
            assert_equal_or_DNE(data_dict_msg["author"][i], "family", result.author[i], "family")
            assert_equal_or_DNE(data_dict_msg["author"][i], "ORCID", result.author[i], "orcid")
            assert_equal_or_DNE(data_dict_msg["author"][i], "affiliation", result.author[i], "affiliation")
            assert_equal_or_DNE(data_dict_msg["author"][i], "sequence", result.author[i], "sequence")
    else:
        assert result.author == []

    # Test licenses
    if "license" in data_dict_msg.keys():
        for i, license in enumerate(data_dict_msg["license"]):
            assert_equal_or_DNE(data_dict_msg["license"][i], "content-version", result.license[i], "version")
            assert_equal_or_DNE(data_dict_msg["license"][i], "URL", result.license[i], "url")
    else:
        assert result.license == []

    # Test local identifier
    assert "provider_rec" in result.local.identifiers
    assert data_dict_msg["DOI"] == result.local.identifiers["provider_rec"]
    assert result.local.USDA == "no"


@pytest.mark.parametrize(
    'submit_data',
    ["submission_345", "submission_1000", "submission_2000", "submission_2500", "submission_2600", "submission_1662",
     "submission_3122"]
)
def test_submit_site_mapper(submit_data, request):
    loaded_data = request.getfixturevalue(submit_data)
    data_dict = json.loads(loaded_data)

    def update_dict_str_encodings(input):
        if isinstance(input, dict):
            for key, value in input.items():
                if isinstance(value, int):
                    input[key] = str(value)
                if isinstance(value, str):
                    input[key] = utils.clean_str(value)
                elif isinstance(value, dict):
                    update_dict_str_encodings(value)
                elif isinstance(value, list):
                    for i, item in enumerate(value):
                        if isinstance(item, str):
                            value[i] = utils.clean_str(value[i])
                        elif isinstance(item, list) or isinstance(item, dict):
                            update_dict_str_encodings(item)
        elif isinstance(input, list):
            for i, item in enumerate(input):
                if isinstance(item, str):
                    input[i] = utils.clean_str(input[i])
                else:
                    update_dict_str_encodings(item)
        return input

    if isinstance(data_dict, list):
        data_dict = data_dict[0]

    data_dict = update_dict_str_encodings(data_dict)

    data_dict = utils.replace_hyphens_with_underscores(data_dict)

    result, message = mapper(loaded_data, 'submit_json')
    assert message == "success"
    assert type(result) == Citation

    # Test high-level Citation attributes
    assert_equal_or_DNE(data_dict, 'title', result, 'title')
    assert_equal_or_DNE(data_dict, 'doi', result, 'DOI')
    assert_equal_or_DNE(data_dict, 'journal', result, 'container_title')
    assert_equal_or_DNE(data_dict, 'abstract', result, 'abstract')
    assert_equal_or_DNE(data_dict, 'abstract', result, 'abstract')
    assert_equal_or_DNE_string_cast(data_dict, 'issue', result, 'issue')

    if 'issn' in data_dict:
        assert data_dict['issn'] == result.ISSN['issn']

    # Test pages dictionary
    if "first_page" in data_dict.keys():
        assert data_dict["first_page"] == result.page["first_page"]
    else:
        assert result.page["first_page"] == None

    if "last_page" in data_dict.keys():
        assert data_dict["last_page"] == result.page["last_page"]
    else:
        assert result.page["last_page"] == None

    if (
            "first_page" in data_dict.keys() and data_dict["first_page"] not in {None, ""} and
            "last_page" in data_dict.keys() and data_dict["last_page"] not in {None, ""}
    ):
        page_str = f'{data_dict["first_page"]} - {data_dict["last_page"]}'
        assert result.page["page_str"] == page_str
    else:
        assert result.page["page_str"] == None

    # Test funders
    if "funding_agencies" in data_dict.keys():
        for i, funder in enumerate(data_dict["funding_agencies"]):
            assert funder["name"] == result.funder[i].name
            if 'award_number' in funder.keys():
                if isinstance(funder["award_number"], list):
                    assert funder["award_number"] == result.funder[i].award
                else:
                    assert [funder["award_number"]] == result.funder[i].award
            else:
                assert result.funder[i].award == [""]

    # Test authors
    for i, author in enumerate(data_dict["authors"]):
        assert_equal_or_DNE(data_dict["authors"][i], "first_name", result.author[i], "given")
        assert_equal_or_DNE(data_dict["authors"][i], "last_name", result.author[i], "family")
        assert_equal_or_DNE(data_dict["authors"][i], "orcid", result.author[i], "orcid")
        if "affiliation" in data_dict["authors"][i].keys():
            assert [data_dict["authors"][i]["affiliation"]] == result.author[i].affiliation
        else:
            assert result.author[i].affiliation == [""]
        assert_equal_or_DNE(data_dict["authors"][i], "sequence", result.author[i], "sequence")

    # Test license
    if "manuscript_version" in data_dict.keys():
        assert data_dict["manuscript_version"] == result.license[0].version

    # Test local
    assert_equal_or_DNE(data_dict, "manuscript_file", result.local, "manuscript_file")
    assert_equal_or_DNE(data_dict, "supplementary_files", result.local, "supplementary_files")
    assert_equal_or_DNE_string_cast(data_dict, "created", result.local, "submission_date")
    assert_equal_or_DNE_string_cast(data_dict, "changed", result.local, "modification_date")
    assert_equal_or_DNE_string_cast(data_dict, "date_other", result.local, "date_other")
    assert result.local.USDA == "yes"
    # Test identifiers
    if "log_number" in data_dict.keys():
        assert data_dict["log_number"] == result.local.identifiers["standard_number_aris"]
    if "submission_node_id" in data_dict.keys():
        assert data_dict["submission_node_id"] == result.local.identifiers["submission_node_id"]
    if "accession_number" in data_dict.keys():
        assert data_dict["accession_number"] == result.local.identifiers["accession_number"]
    if "mms_id" in data_dict.keys():
        assert data_dict["mms_id"] == result.local.identifiers["mms_id"]
    assert "provider_rec" in result.local.identifiers
    assert data_dict["submission_node_id"] == result.local.identifiers["provider_rec"]

# Test error handling of faulty records
def test_faulty_record_submit_json(faulty_record):
    loaded_data = faulty_record
    result, message = mapper(loaded_data, 'submit_json')
    assert result is None
    error_pattern = r"Faulty record: *"
    assert re.search(error_pattern, message) is not None

def test_faulty_record_crossref_json(faulty_record):
    loaded_data = faulty_record
    result, message = mapper(loaded_data, 'crossref_json')
    assert result is None
    error_pattern = r"Faulty record: *"
    assert re.search(error_pattern, message) is not None
