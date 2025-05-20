import pytest
import sys
from unittest.mock import MagicMock
sys.modules['srupymarc'] = MagicMock()
from type_and_match.type_and_match import ArticleTyperMatcher

@pytest.fixture
def patch_doi_status_valid(mocker):
    """
    Fixture to patch the doi_status function in the ArticleTyperMatcher class.
    This will allow us to assume that the DOI is valid for various test cases.
    """
    mocker.patch.object(ArticleTyperMatcher, 'doi_status', return_value="valid")

@pytest.fixture
def patch_doi_status_invalid(mocker):
    """
    Fixture to patch the doi_status function in the ArticleTyperMatcher class.
    This will allow us to assume that the DOI is valid for various test cases.
    """
    mocker.patch.object(ArticleTyperMatcher, 'doi_status', return_value="invalid")

@pytest.fixture
def patch_doi_status_network_error(mocker):
    """
    Fixture to patch the doi_status function in the ArticleTyperMatcher class.
    This will allow us to assume that the DOI is valid for various test cases.
    """
    mocker.patch.object(ArticleTyperMatcher, 'doi_status', return_value="network error")