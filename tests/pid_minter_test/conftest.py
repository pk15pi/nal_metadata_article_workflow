import pytest
from citation import Citation, Local

@pytest.fixture
def citation_object_no_pid():
    return Citation(
        type='journal-article',
        local=Local(
            identifiers={
                'pid': None
            }
        )
    )

@pytest.fixture
def citation_object_with_pid():
    return Citation(
        type='journal-article',
        local=Local(
            identifiers={
                'pid': 1234
            }
        )
    )
@pytest.fixture
def non_article_citation_object():
    return Citation(
        type='correction',
        local=Local(
            identifiers={
                'pid': None
            }
        )
    )