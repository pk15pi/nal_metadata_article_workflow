import sys
from unittest.mock import MagicMock

# Mock the srupymarc module
sys.modules['srupymarc'] = MagicMock()

import pysolr
from citation import Citation, Local
from type_and_match.type_and_match import ArticleTyperMatcher
import pymarc
from pytest import MonkeyPatch


# Test type_and_match helper functions that check for article matches
def test_find_matching_records_solr(mocker):
    # Mock the SOLR_SERVER environment variable
    mp = MonkeyPatch()
    mp.setenv('SOLR_SERVER', 'http://fake_solr_server')

    mock_response = pysolr.Results({
        'response': {
            'docs': [
                {
                    'title': 'Title 1',
                    'doi': 'DOI 1',
                    'mmsid': 'MMSID 1',
                    'agid': 'agid 1'
                },
            ],
            'numFound': 1,
        }
    })

    # Create a mock Solr object
    mock_solr = mocker.MagicMock()
    mock_solr.search.return_value = mock_response

    # Patch the Solr class to return the mock Solr object
    mocker.patch('type_and_match.type_and_match.pysolr.Solr', return_value=mock_solr)

    ATM = ArticleTyperMatcher()
    result = ATM._find_matching_records_solr("DOI 1", "MMSID 1")
    print("Result: ", result)
    assert result == [
        {
            'title': 'Title 1',
            'doi': 'DOI 1',
            'mmsid': 'MMSID 1',
            'agid': 'agid 1'
        }
    ]


def test_find_matching_records_alma_doi(mocker):
    def mock_response(url, query):
        mock_srupymarc_response = mocker.MagicMock()
        mock_srupymarc_response.count = 1
        returned_record = pymarc.Record()
        returned_record.add_field(pymarc.Field(tag='245', subfields=[
            pymarc.Subfield(code='a', value='Title 2')
        ]))
        returned_record.add_field(pymarc.Field(tag='024', subfields=[
            pymarc.Subfield(code='a', value='DOI 2'),
            pymarc.Subfield(code='2', value='doi')
        ]))
        returned_record.add_field(pymarc.Field(tag='001', data='MMSID 2'))
        returned_record.add_field(pymarc.Field(tag="974", subfields=[
            pymarc.Subfield(code="a", value="agid:agid 2")
        ]))
        mock_srupymarc_response.__iter__.side_effect = \
            lambda: iter([returned_record])
        return mock_srupymarc_response

    mocker.patch('type_and_match.type_and_match.srupymarc.searchretrieve',
                 side_effect=mock_response)

    ATM = ArticleTyperMatcher()
    result = ATM._find_matching_records_alma_doi("DOI 2")
    print("Result: ", result)
    assert result == [
        {
            'title': 'Title 2',
            'doi': 'DOI 2',
            'mmsid': 'MMSID 2',
            'agid': 'agid 2'
        }
    ]


def test_find_matching_records_alma_mmsid(mocker):
    def mock_response(url, query):
        mock_srupymarc_response = mocker.MagicMock()
        mock_srupymarc_response.count = 1
        returned_record = pymarc.Record()
        returned_record.add_field(pymarc.Field(tag='245', subfields=[
            pymarc.Subfield(code='a', value='Title 2')
        ]))
        returned_record.add_field(pymarc.Field(tag='024', subfields=[
            pymarc.Subfield(code='a', value='DOI 2'),
            pymarc.Subfield(code='2', value='doi')
        ]))
        returned_record.add_field(pymarc.Field(tag='001', data='MMSID 2'))
        returned_record.add_field(pymarc.Field(tag="974", subfields=[
            pymarc.Subfield(code="a", value="agid:agid 2")
        ]))
        mock_srupymarc_response.__iter__.side_effect = \
            lambda: iter([returned_record])
        return mock_srupymarc_response

    mocker.patch('type_and_match.type_and_match.srupymarc.searchretrieve',
                 side_effect=mock_response)

    ATM = ArticleTyperMatcher()
    result = ATM._find_matching_records_alma_mmsid("MMSID 2")
    print("Result: ", result)
    assert result == [
        {
            'title': 'Title 2',
            'doi': 'DOI 2',
            'mmsid': 'MMSID 2',
            'agid': 'agid 2'
        }
    ]


# Next, test the type_and_match function for the following cases
# For brevity, "tam" is an abbreviation for "type_and_match"

# Case 1: Incoming citation is of type 'notice'
def test_tam_notice(patch_doi_status_valid):
    ATM = ArticleTyperMatcher()
    citation = Citation()
    citation.type = "notice"
    result = ATM.type_and_match(citation)
    assert result[1] == "notice"

# Case 2: Incoming citation object matches an existing record with
# identical title
def test_tam_one_exact_match(mocker, patch_doi_status_valid):
    matches = [
        {
            'title': 'Title 1',
            'doi': 'DOI 1',
            'mmsid': 'MMSID 1',
            'agid': 'agid 1'
        }
    ]
    mocker.patch(
        'type_and_match.type_and_match.ArticleTyperMatcher.' +
        'find_matching_records', return_value=matches)

    ATM = ArticleTyperMatcher()
    citation1 = Citation()
    citation1.title = "Title 1"
    citation1.DOI = "DOI 1"
    citation1.local = Local()
    citation1.local.identifiers["mms_id"] = "MMSID 1"
    result1 = ATM.type_and_match(citation1)
    print(result1[1])
    assert result1[1] == "merge"


# Case 3: Record match identified with a similar but not identical title
def test_tam_one_fuzzy_match(mocker, patch_doi_status_valid):
    matches = [
        {
            'title': 'This is the title of a journal article with a subtitle',
            'doi': 'DOI 1',
            'mmsid': 'MMSID 1',
            'agid': 'agid 1'
        }
    ]
    mocker.patch('type_and_match.type_and_match.ArticleTyperMatcher.' +
                 'find_matching_records', return_value=matches)

    ATM = ArticleTyperMatcher()
    citation1 = Citation()
    citation1.title = "This is the title of a journal article without a " + \
                      "subtitle"
    citation1.DOI = "DOI 1"
    citation1.local = Local()
    citation1.local.identifiers["mms_id"] = "MMSID 1"
    result1 = ATM.type_and_match(citation1)
    print(result1[1])
    assert result1[1] == "merge"


# Case 4: No match found in Solr or Alma
def test_tam_no_matches(mocker, patch_doi_status_valid):
    matches = []
    mocker.patch(
        'type_and_match.type_and_match.ArticleTyperMatcher.' +
        'find_matching_records', return_value=matches)

    ATM = ArticleTyperMatcher()
    citation1 = Citation()
    citation1.title = "Title 1"
    citation1.DOI = "DOI 1"
    citation1.local = Local()
    citation1.local.identifiers["mms_id"] = "MMSID 1"
    result1 = ATM.type_and_match(citation1)
    print(result1[1])
    assert result1[1] == "new"


# Case 5: Matches found, but none of type 'journal-article'
def test_tam_no_article_type_matches(mocker, patch_doi_status_valid):
    matches = [
        {
            'title': 'Correction: Title 1',
            'doi': 'DOI 1',
            'mmsid': 'MMSID 1',
            'agid': 'agid 1'
        },
        {
            'title': 'Correction: Title 2',
            'doi': 'DOI 1',
            'mmsid': 'MMSID 2',
            'agid': 'agid 2'
        }
    ]
    mocker.patch(
        'type_and_match.type_and_match.ArticleTyperMatcher.' +
        'find_matching_records', return_value=matches)

    ATM = ArticleTyperMatcher()
    citation1 = Citation()
    citation1.title = "Title 1"
    citation1.DOI = "DOI 1"
    citation1.local = Local()
    citation1.local.identifiers["mms_id"] = "MMSID 3"
    result1 = ATM.type_and_match(citation1)
    print(result1[1])
    assert result1[1] == "new"


# Case 6: Matches found, one of type 'journal-article' with a different title
def test_tam_article_match_different_title(mocker, patch_doi_status_valid):
    matches = [
        {
            'title': 'Journal article title',
            'doi': 'DOI 1',
            'mmsid': 'MMSID 1',
            'agid': 'agid 1'
        }
    ]
    mocker.patch(
        'type_and_match.type_and_match.ArticleTyperMatcher.' +
        'find_matching_records', return_value=matches)

    ATM = ArticleTyperMatcher()
    citation1 = Citation()
    citation1.title = "A different, non-matching journal article title"
    citation1.DOI = "DOI 1"
    citation1.local = Local()
    citation1.local.identifiers["mms_id"] = "MMSID 2"
    result1 = ATM.type_and_match(citation1)
    print(result1[1])
    assert result1[1] == "review"


# Case 7: Citation is not of type 'journal-article', no record matches
def test_tam_non_article_no_matches(mocker, patch_doi_status_valid):
    matches = []
    mocker.patch(
        'type_and_match.type_and_match.ArticleTyperMatcher.' +
        'find_matching_records', return_value=matches)

    ATM = ArticleTyperMatcher()
    citation1 = Citation()
    citation1.title = "Correction: Title 1"
    citation1.DOI = "DOI 1"
    citation1.local = Local()
    citation1.local.identifiers["mms_id"] = "MMSID 1"
    result1 = ATM.type_and_match(citation1)
    print(result1[1])
    assert result1[1] == "new"


# Case 8: Citation is not of type 'journal-article', exact match found
def test_tam_non_article_match(mocker, patch_doi_status_valid):
    matches = [
        {
            'title': 'Correction: Title 1',
            'doi': 'DOI 1',
            'mmsid': 'MMSID 1',
            'agid': 'agid 1'
        }
    ]
    mocker.patch(
        'type_and_match.type_and_match.ArticleTyperMatcher.' +
        'find_matching_records', return_value=matches)

    ATM = ArticleTyperMatcher()
    citation1 = Citation()
    citation1.title = "Correction: Title 1"
    citation1.DOI = "DOI 1"
    citation1.local = Local()
    citation1.local.identifiers["mms_id"] = "MMSID 1"
    result1 = ATM.type_and_match(citation1)
    print(result1[1])
    assert result1[1] == "merge"


# Case 9: Citation is not of type 'journal-article',
# record matches but no title matches
def test_tam_non_article_no_title_matches(mocker, patch_doi_status_valid):
    matches = [
        {
            'title': 'Correction: the first correction to the journal article',
            'doi': 'DOI 1',
            'mmsid': 'MMSID 1',
            'agid': 'agid 1'
        }
    ]
    mocker.patch(
        'type_and_match.type_and_match.ArticleTyperMatcher.' +
        'find_matching_records', return_value=matches)

    ATM = ArticleTyperMatcher()
    citation1 = Citation()
    citation1.title = "Correction: The second correction to the journal " + \
                      "article"
    citation1.DOI = "DOI 1"
    citation1.local = Local()
    citation1.local.identifiers["mms_id"] = "MMSID 1"
    result1 = ATM.type_and_match(citation1)
    print(result1[1])
    assert result1[1] == "new"

# Case 10: No mmsid, no DOI matches
def test_tam_no_mmsid(mocker, patch_doi_status_valid):
    # Show that if there is no mmsid, and no DOI matches, there are no matches

    matches_solr = []
    matches_alma_doi = []

    mocker.patch(
        'type_and_match.type_and_match.ArticleTyperMatcher.' +
        '_find_matching_records_solr', return_value=matches_solr)

    mocker.patch(
        'type_and_match.type_and_match.ArticleTyperMatcher.' +
        '_find_matching_records_alma_doi', return_value=matches_alma_doi)

    ATM = ArticleTyperMatcher()
    citation1 = Citation()
    citation1.title = "Title 1"
    citation1.DOI = "DOI 1"
    citation1.local = Local()
    citation1.local.identifiers["mms_id"] = ""
    result1 = ATM.type_and_match(citation1)
    print(result1[1])
    assert result1[1] == "new"

# Case 11: Missing DOI
def test_tam_doi_missing():
    ATM = ArticleTyperMatcher()
    citation1 = Citation()
    citation1.DOI = None
    citation1.local = Local()
    cit, msg = ATM.type_and_match(citation1)
    assert msg == "Missing DOI, review"
    assert cit.local.cataloger_notes == ["Missing DOI"]

# Case 12: Invalid DOI
def test_tam_doi_invalid(patch_doi_status_invalid):
    ATM = ArticleTyperMatcher()
    citation1 = Citation()
    citation1.DOI = "invalid_doi"
    citation1.local = Local()
    cit, msg = ATM.type_and_match(citation1)
    assert msg == "Invalid DOI, review"
    assert cit.local.cataloger_notes == ["Invalid DOI"]

# Case 13: Network error when attempting to resolve DOI
def test_tam_doi_network_error(patch_doi_status_network_error):
    ATM = ArticleTyperMatcher()
    citation1 = Citation()
    citation1.DOI = "placeholder"
    citation1.local = Local()
    cit, msg = ATM.type_and_match(citation1)
    assert msg == "Network error, re-run"




