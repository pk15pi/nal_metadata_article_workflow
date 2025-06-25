from metadata_quality_review import (check_volume, check_issue,
                                     check_page, check_title, check_name_elems,
                                     check_primary_author, check_abstract,
                                     check_submission_manuscript,
                                     metadata_quality_review)


# Assert that the base citation usda is valid and has no quality review issues
def test_metadata_quality_review_usda(base_citation_usda):
    cit, msg = metadata_quality_review(base_citation_usda, "")
    assert msg == "active"
    assert len(cit.local.cataloger_notes) == 0

# Assert that the base citation usda is valid and has no quality review issues
def test_metadata_quality_review_non_usda(base_citation_non_usda):
    cit, msg = metadata_quality_review(base_citation_non_usda, "")
    assert msg == "active"
    assert len(cit.local.cataloger_notes) == 0


# Test behavior for valid volume, usda
def test_metadata_quality_review_valid_volume_usda(base_citation_usda):

    # Active
    cit, msg = check_volume(base_citation_usda, "active", "")
    assert msg == "active"
    assert len(cit.local.cataloger_notes) == 0

    # Review
    cit, msg = check_volume(base_citation_usda, "review", "")
    assert msg == "review"
    assert len(cit.local.cataloger_notes) == 0

    # Dropped
    cit, msg = check_volume(base_citation_usda, "dropped", "")
    assert msg == "dropped"
    assert len(cit.local.cataloger_notes) == 0

# Test behavior for valid volume, non usda
def test_metadata_quality_review_valid_volume_usda(base_citation_non_usda):

    # Active
    cit, msg = check_volume(base_citation_non_usda, "active", "")
    assert msg == "active"
    assert len(cit.local.cataloger_notes) == 0

    # Review
    cit, msg = check_volume(base_citation_non_usda, "review", "")
    assert msg == "review"
    assert len(cit.local.cataloger_notes) == 0

    # Dropped
    cit, msg = check_volume(base_citation_non_usda, "dropped", "")
    assert msg == "dropped"
    assert len(cit.local.cataloger_notes) == 0


# Test behavior for missing volume, non usda
def test_metadata_quality_review_missing_volume_non_usda(base_citation_non_usda):
    base_citation_non_usda.volume = None

    # Active, not overridden
    cit, msg = check_volume(base_citation_non_usda, "active", "")
    assert msg == "review"
    assert "No volume number" in cit.local.cataloger_notes

    # Active, overridden
    cit, msg = check_volume(base_citation_non_usda, "active", "volume")
    assert msg == "active"
    assert "No volume number" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_volume(base_citation_non_usda, "review", "")
    assert msg == "review"
    assert "No volume number" in cit.local.cataloger_notes

    # Review, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_volume(base_citation_non_usda, "review", "volume")
    assert msg == "review"
    assert "No volume number" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_volume(base_citation_non_usda, "dropped", "")
    assert msg == "dropped"
    assert "No volume number" in cit.local.cataloger_notes

    # Review, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_volume(base_citation_non_usda, "dropped", "volume")
    assert msg == "dropped"
    assert "No volume number" in cit.local.cataloger_notes

# Test behavior for missing volume, non usda
def test_metadata_quality_review_missing_volume_usda(base_citation_usda):
    base_citation_usda.volume = None

    # Active, not overridden
    cit, msg = check_volume(base_citation_usda, "active", "")
    assert msg == "active"
    assert "No volume number" in cit.local.cataloger_notes

    # Active, overridden
    cit, msg = check_volume(base_citation_usda, "active", "volume")
    assert msg == "active"
    assert "No volume number" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_volume(base_citation_usda, "review", "")
    assert msg == "review"
    assert "No volume number" in cit.local.cataloger_notes

    # Review, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_volume(base_citation_usda, "review", "volume")
    assert msg == "review"
    assert "No volume number" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_volume(base_citation_usda, "dropped", "")
    assert msg == "dropped"
    assert "No volume number" in cit.local.cataloger_notes

    # Review, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_volume(base_citation_usda, "dropped", "volume")
    assert msg == "dropped"
    assert "No volume number" in cit.local.cataloger_notes


# Test behavior for valid issue
def test_metadata_quality_review_valid_issue_usda(base_citation_usda):

    # Active
    cit, msg = check_issue(base_citation_usda, "active", "")
    assert msg == "active"
    assert len(cit.local.cataloger_notes) == 0

    # Review
    cit, msg = check_issue(base_citation_usda, "review", "")
    assert msg == "review"
    assert len(cit.local.cataloger_notes) == 0

    # Dropped
    cit, msg = check_issue(base_citation_usda, "dropped", "")
    assert msg == "dropped"
    assert len(cit.local.cataloger_notes) == 0


# Test behavior for missing issue
def test_metadata_quality_review_missing_issue_usda(base_citation_usda):
    base_citation_usda.issue = None

    # Active, not overridden
    cit, msg = check_issue(base_citation_usda, "active", "")
    assert msg == "active"
    assert "No issue number" in cit.local.cataloger_notes

    # Active, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_issue(base_citation_usda, "active", "issue")
    assert msg == "active"
    assert "No issue number" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_issue(base_citation_usda, "review", "")
    assert msg == "review"
    assert "No issue number" in cit.local.cataloger_notes

    # Review, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_issue(base_citation_usda, "review", "issue")
    assert msg == "review"
    assert "No issue number" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_issue(base_citation_usda, "dropped", "")
    assert msg == "dropped"
    assert "No issue number" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_issue(base_citation_usda, "dropped", "issue")
    assert msg == "dropped"
    assert "No issue number" in cit.local.cataloger_notes

# Test behavior for missing issue
def test_metadata_quality_review_missing_issue_non_usda(base_citation_non_usda):
    base_citation_non_usda.issue = None

    # Active, not overridden
    cit, msg = check_issue(base_citation_non_usda, "active", "")
    assert msg == "review"
    assert "No issue number" in cit.local.cataloger_notes

    # Active, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_issue(base_citation_non_usda, "active", "issue")
    assert msg == "active"
    assert "No issue number" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_issue(base_citation_non_usda, "review", "")
    assert msg == "review"
    assert "No issue number" in cit.local.cataloger_notes

    # Review, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_issue(base_citation_non_usda, "review", "issue")
    assert msg == "review"
    assert "No issue number" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_issue(base_citation_non_usda, "dropped", "")
    assert msg == "dropped"
    assert "No issue number" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_issue(base_citation_non_usda, "dropped", "issue")
    assert msg == "dropped"
    assert "No issue number" in cit.local.cataloger_notes


# Test behavior for valid page info
def test_metadata_quality_review_valid_page(base_citation_usda):

    # Active
    cit, msg = check_page(base_citation_usda, "active", "")
    assert msg == "active"
    assert len(cit.local.cataloger_notes) == 0

    # Review
    cit, msg = check_page(base_citation_usda, "review", "")
    assert msg == "review"
    assert len(cit.local.cataloger_notes) == 0

    # Dropped
    cit, msg = check_page(base_citation_usda, "dropped", "")
    assert msg == "dropped"
    assert len(cit.local.cataloger_notes) == 0


# Test behavior for invalid page info
def test_metadata_quality_review_invalid_page_usda(base_citation_usda):
    base_citation_usda.page_str = None

    # Active, not overridden
    cit, msg = check_page(base_citation_usda, "active", "")
    assert msg == "active"
    assert "No page number" in cit.local.cataloger_notes

    # Active, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_page(base_citation_usda, "active", "page")
    assert msg == "active"
    assert "No page number" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_page(base_citation_usda, "review", "")
    assert msg == "review"
    assert "No page number" in cit.local.cataloger_notes

    # Review, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_page(base_citation_usda, "review", "page")
    assert msg == "review"
    assert "No page number" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_page(base_citation_usda, "dropped", "")
    assert msg == "dropped"
    assert "No page number" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_page(base_citation_usda, "dropped", "page")
    assert msg == "dropped"
    assert "No page number" in cit.local.cataloger_notes

# Test behavior for invalid page info
def test_metadata_quality_review_invalid_page_non_usda(base_citation_non_usda):
    base_citation_non_usda.page_str = None

    # Active, not overridden
    cit, msg = check_page(base_citation_non_usda, "active", "")
    assert msg == "review"
    assert "No page number" in cit.local.cataloger_notes

    # Active, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_page(base_citation_non_usda, "active", "page")
    assert msg == "active"
    assert "No page number" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_page(base_citation_non_usda, "review", "")
    assert msg == "review"
    assert "No page number" in cit.local.cataloger_notes

    # Review, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_page(base_citation_non_usda, "review", "page")
    assert msg == "review"
    assert "No page number" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_page(base_citation_non_usda, "dropped", "")
    assert msg == "dropped"
    assert "No page number" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_page(base_citation_non_usda, "dropped", "page")
    assert msg == "dropped"
    assert "No page number" in cit.local.cataloger_notes


# Test behavior for valid title
def test_metadata_quality_review_valid_title(base_citation_usda):

    # Active
    cit, msg = check_title(base_citation_usda, "active", "")
    assert msg == "active"
    assert len(cit.local.cataloger_notes) == 0

    # Review
    cit, msg = check_title(base_citation_usda, "review", "")
    assert msg == "review"
    assert len(cit.local.cataloger_notes) == 0

    # Dropped
    cit, msg = check_title(base_citation_usda, "dropped", "")
    assert msg == "dropped"
    assert len(cit.local.cataloger_notes) == 0


# Test behavior for missing title
def test_metadata_quality_review_missing_title_usda(base_citation_usda):
    base_citation_usda.title = None

    # Active, not overridden
    cit, msg = check_title(base_citation_usda, "active", "")
    assert msg == "active"
    assert "No title" in cit.local.cataloger_notes

    # Active, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_title(base_citation_usda, "active", "title")
    assert msg == "active"
    assert "No title" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_title(base_citation_usda, "review", "")
    assert msg == "review"
    assert "No title" in cit.local.cataloger_notes

    # Review, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_title(base_citation_usda, "review", "title")
    assert msg == "review"
    assert "No title" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_title(base_citation_usda, "dropped", "")
    assert msg == "dropped"
    assert "No title" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_title(base_citation_usda, "dropped", "title")
    assert msg == "dropped"
    assert "No title" in cit.local.cataloger_notes

# Test behavior for missing title
def test_metadata_quality_review_missing_title_non_usda(base_citation_non_usda):
    base_citation_non_usda.title = None

    # Active, not overridden
    cit, msg = check_title(base_citation_non_usda, "active", "")
    assert msg == "dropped"
    assert "No title" in cit.local.cataloger_notes

    # Active, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_title(base_citation_non_usda, "active", "title")
    assert msg == "review"
    assert "No title" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_title(base_citation_non_usda, "review", "")
    assert msg == "dropped"
    assert "No title" in cit.local.cataloger_notes

    # Review, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_title(base_citation_non_usda, "review", "title")
    assert msg == "review"
    assert "No title" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_title(base_citation_non_usda, "dropped", "")
    assert msg == "dropped"
    assert "No title" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_title(base_citation_non_usda, "dropped", "title")
    assert msg == "dropped"
    assert "No title" in cit.local.cataloger_notes


# Test behavior for valid author name parts
def test_metadata_quality_review_valid_author_names(base_citation_usda):

    # Active
    cit, msg = check_name_elems(base_citation_usda, "active", "")
    assert msg == "active"
    assert len(cit.local.cataloger_notes) == 0

    # Review
    cit, msg = check_name_elems(base_citation_usda, "review", "")
    assert msg == "review"
    assert len(cit.local.cataloger_notes) == 0

    # Dropped
    cit, msg = check_name_elems(base_citation_usda, "dropped", "")
    assert msg == "dropped"
    assert len(cit.local.cataloger_notes) == 0


# Test behavior for missing last author name
def test_metadata_quality_review_missing_author_names_usda(base_citation_usda):
    base_citation_usda.author[0].family = None

    # Active, not overridden
    cit, msg = check_name_elems(base_citation_usda, "active", "")
    assert msg == "active"
    assert "No name elements" in cit.local.cataloger_notes

    # Active, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_name_elems(base_citation_usda, "active", "author")
    assert msg == "active"
    assert "No name elements" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_name_elems(base_citation_usda, "review", "")
    assert msg == "review"
    assert "No name elements" in cit.local.cataloger_notes

    # Review, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_name_elems(base_citation_usda, "review", "author")
    assert msg == "review"
    assert "No name elements" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_name_elems(base_citation_usda, "dropped", "")
    assert msg == "dropped"
    assert "No name elements" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_name_elems(base_citation_usda, "dropped", "author")
    assert msg == "dropped"
    assert "No name elements" in cit.local.cataloger_notes

# Test behavior for missing last author name
def test_metadata_quality_review_missing_author_names_non_usda(base_citation_non_usda):
    base_citation_non_usda.author[0].family = None

    # Active, not overridden
    cit, msg = check_name_elems(base_citation_non_usda, "active", "")
    assert msg == "dropped"
    assert "No name elements" in cit.local.cataloger_notes

    # Active, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_name_elems(base_citation_non_usda, "active", "author")
    assert msg == "review"
    assert "No name elements" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_name_elems(base_citation_non_usda, "review", "")
    assert msg == "dropped"
    assert "No name elements" in cit.local.cataloger_notes

    # Review, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_name_elems(base_citation_non_usda, "review", "author")
    assert msg == "review"
    assert "No name elements" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_name_elems(base_citation_non_usda, "dropped", "")
    assert msg == "dropped"
    assert "No name elements" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_name_elems(base_citation_non_usda, "dropped", "author")
    assert msg == "dropped"
    assert "No name elements" in cit.local.cataloger_notes


# Test behavior for valid author sequence elements
def test_metadata_quality_review_valid_author_sequence(base_citation_usda):

    # Active
    cit, msg = check_primary_author(base_citation_usda, "active", "")
    assert msg == "active"
    assert len(cit.local.cataloger_notes) == 0

    # Review
    cit, msg = check_primary_author(base_citation_usda, "review", "")
    assert msg == "review"
    assert len(cit.local.cataloger_notes) == 0

    # Dropped
    cit, msg = check_primary_author(base_citation_usda, "dropped", "")
    assert msg == "dropped"
    assert len(cit.local.cataloger_notes) == 0


# Test behavior for invalid author sequence elements
def test_metadata_quality_review_invalid_author_sequence_usda(base_citation_usda):
    base_citation_usda.author[1].sequence = "first"

    # Active, not overridden
    cit, msg = check_primary_author(base_citation_usda, "active", "")
    assert msg == "active"
    assert "Multiple primary authors" in cit.local.cataloger_notes

    # Active, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_primary_author(base_citation_usda, "active", "primary")
    assert msg == "active"
    assert "Multiple primary authors" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_primary_author(base_citation_usda, "review", "")
    assert msg == "review"
    assert "Multiple primary authors" in cit.local.cataloger_notes

    # Review, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_primary_author(base_citation_usda, "review", "primary")
    assert msg == "review"
    assert "Multiple primary authors" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_primary_author(base_citation_usda, "dropped", "")
    assert msg == "dropped"
    assert "Multiple primary authors" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_primary_author(base_citation_usda, "dropped", "primary")
    assert msg == "dropped"
    assert "Multiple primary authors" in cit.local.cataloger_notes

# Test behavior for invalid author sequence elements
def test_metadata_quality_review_invalid_author_sequence_non_usda(base_citation_non_usda):
    base_citation_non_usda.author[1].sequence = "first"

    # Active, not overridden
    cit, msg = check_primary_author(base_citation_non_usda, "active", "")
    assert msg == "review"
    assert "Multiple primary authors" in cit.local.cataloger_notes

    # Active, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_primary_author(base_citation_non_usda, "active", "primary")
    assert msg == "active"
    assert "Multiple primary authors" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_primary_author(base_citation_non_usda, "review", "")
    assert msg == "review"
    assert "Multiple primary authors" in cit.local.cataloger_notes

    # Review, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_primary_author(base_citation_non_usda, "review", "primary")
    assert msg == "review"
    assert "Multiple primary authors" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_primary_author(base_citation_non_usda, "dropped", "")
    assert msg == "dropped"
    assert "Multiple primary authors" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_primary_author(base_citation_non_usda, "dropped", "primary")
    assert msg == "dropped"
    assert "Multiple primary authors" in cit.local.cataloger_notes


def test_metadata_quality_review_valid_abstract(base_citation_usda):

    # Active
    cit, msg = check_abstract(base_citation_usda, "active", "")
    assert msg == "active"
    assert len(cit.local.cataloger_notes) == 0

    # Review
    cit, msg = check_abstract(base_citation_usda, "review", "")
    assert msg == "review"
    assert len(cit.local.cataloger_notes) == 0

    # Dropped
    cit, msg = check_abstract(base_citation_usda, "dropped", "")
    assert msg == "dropped"
    assert len(cit.local.cataloger_notes) == 0


def test_metadata_quality_review_missing_abstract_usda(base_citation_usda):
    base_citation_usda.abstract = None

    # Active, not overridden
    cit, msg = check_abstract(base_citation_usda, "active", "")
    assert msg == "active"
    assert "missing abstract" in cit.local.cataloger_notes

    # Active, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_usda, "active", "abstract")
    assert msg == "active"
    assert "missing abstract" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_usda, "review", "")
    assert msg == "review"
    assert "missing abstract" in cit.local.cataloger_notes

    # Review, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_usda, "review", "abstract")
    assert msg == "review"
    assert "missing abstract" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_usda, "dropped", "")
    assert msg == "dropped"
    assert "missing abstract" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_usda, "dropped", "abstract")
    assert msg == "dropped"
    assert "missing abstract" in cit.local.cataloger_notes

def test_metadata_quality_review_missing_abstract_non_usda(base_citation_non_usda):
    base_citation_non_usda.abstract = None

    # Active, not overridden
    cit, msg = check_abstract(base_citation_non_usda, "active", "")
    assert msg == "dropped"
    assert "missing abstract" in cit.local.cataloger_notes

    # Active, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_non_usda, "active", "abstract")
    assert msg == "review"
    assert "missing abstract" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_non_usda, "review", "")
    assert msg == "dropped"
    assert "missing abstract" in cit.local.cataloger_notes

    # Review, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_non_usda, "review", "abstract")
    assert msg == "review"
    assert "missing abstract" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_non_usda, "dropped", "")
    assert msg == "dropped"
    assert "missing abstract" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_non_usda, "dropped", "abstract")
    assert msg == "dropped"
    assert "missing abstract" in cit.local.cataloger_notes


def test_metadata_quality_review_short_abstract_usda(base_citation_usda):
    base_citation_usda.abstract = "Short abstract"

    # Active, not overridden
    cit, msg = check_abstract(base_citation_usda, "active", "")
    assert msg == "active"
    assert "Abstract is empty or less than 50 character" in \
           cit.local.cataloger_notes

    # Active, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_usda, "active", "short_abstract")
    assert msg == "active"
    assert "Abstract is empty or less than 50 character" in \
           cit.local.cataloger_notes

    # Review, not overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_usda, "review", "")
    assert msg == "review"
    assert "Abstract is empty or less than 50 character" in \
           cit.local.cataloger_notes

    # Review, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_usda, "review", "short_abstract")
    assert msg == "review"
    assert "Abstract is empty or less than 50 character" in \
           cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_usda, "dropped", "")
    assert msg == "dropped"
    assert "Abstract is empty or less than 50 character" in \
           cit.local.cataloger_notes

    # Dropped, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_usda, "dropped", "short_abstract")
    assert msg == "dropped"
    assert "Abstract is empty or less than 50 character" in \
           cit.local.cataloger_notes

def test_metadata_quality_review_short_abstract_non_usda(base_citation_non_usda):
    base_citation_non_usda.abstract = "Short abstract"

    # Active, not overridden
    cit, msg = check_abstract(base_citation_non_usda, "active", "")
    assert msg == "dropped"
    assert "Abstract is empty or less than 50 character" in \
           cit.local.cataloger_notes

    # Active, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_non_usda, "active", "short_abstract")
    assert msg == "active"
    assert "Abstract is empty or less than 50 character" in \
           cit.local.cataloger_notes

    # Review, not overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_non_usda, "review", "")
    assert msg == "dropped"
    assert "Abstract is empty or less than 50 character" in \
           cit.local.cataloger_notes

    # Review, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_non_usda, "review", "short_abstract")
    assert msg == "review"
    assert "Abstract is empty or less than 50 character" in \
           cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_non_usda, "dropped", "")
    assert msg == "dropped"
    assert "Abstract is empty or less than 50 character" in \
           cit.local.cataloger_notes

    # Dropped, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_non_usda, "dropped", "short_abstract")
    assert msg == "dropped"
    assert "Abstract is empty or less than 50 character" in \
           cit.local.cataloger_notes


# Test behavior for abstracts containing non-utf8 characters
def test_metadata_quality_review_non_utf8_abstract_usda(base_citation_usda):
    base_citation_usda.abstract = \
        "This is a sufficiently long abstract with non-utf8 characters:" + \
        "\ud835\ude17"

    # Active, not overridden
    cit, msg = check_abstract(base_citation_usda, "active", "")
    assert msg == "active"
    assert "Non-UTF8 characters in abstract" in cit.local.cataloger_notes

    # Active, overridden
    base_citation_usda.local.cataloger_notes = []  # Clear cataloger notes
    cit, msg = check_abstract(base_citation_usda, "active", "utf8")
    assert msg == "active"
    assert "Non-UTF8 characters in abstract" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_usda, "review", "")
    assert msg == "review"
    assert "Non-UTF8 characters in abstract" in cit.local.cataloger_notes

    # Review, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_usda, "review", "utf8")
    assert msg == "review"
    assert "Non-UTF8 characters in abstract" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_usda, "dropped", "")
    assert msg == "dropped"
    assert "Non-UTF8 characters in abstract" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation_usda.local.cataloger_notes = []  # Clear cataloger notes
    cit, msg = check_abstract(base_citation_usda, "dropped", "utf8")
    assert msg == "dropped"
    assert "Non-UTF8 characters in abstract" in cit.local.cataloger_notes

# Test behavior for abstracts containing non-utf8 characters
def test_metadata_quality_review_non_utf8_abstract_non_usda(base_citation_non_usda):
    base_citation_non_usda.abstract = \
        "This is a sufficiently long abstract with non-utf8 characters:" + \
        "\ud835\ude17"

    # Active, not overridden
    cit, msg = check_abstract(base_citation_non_usda, "active", "")
    assert msg == "review"
    assert "Non-UTF8 characters in abstract" in cit.local.cataloger_notes

    # Active, overridden
    base_citation_non_usda.local.cataloger_notes = []  # Clear cataloger notes
    cit, msg = check_abstract(base_citation_non_usda, "active", "utf8")
    assert msg == "active"
    assert "Non-UTF8 characters in abstract" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_non_usda, "review", "")
    assert msg == "review"
    assert "Non-UTF8 characters in abstract" in cit.local.cataloger_notes

    # Review, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_non_usda, "review", "utf8")
    assert msg == "review"
    assert "Non-UTF8 characters in abstract" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation_non_usda, "dropped", "")
    assert msg == "dropped"
    assert "Non-UTF8 characters in abstract" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation_non_usda.local.cataloger_notes = []  # Clear cataloger notes
    cit, msg = check_abstract(base_citation_non_usda, "dropped", "utf8")
    assert msg == "dropped"
    assert "Non-UTF8 characters in abstract" in cit.local.cataloger_notes

# Test behavior for non-English abstracts
def test_metadata_quality_review_non_english_abstract_usda(base_citation_usda):
    base_citation_usda.abstract = "Dies ist eine sehr wichtige wissenschaftliche Veröffentlichung."

    # Active, not overridden
    cit, msg = check_abstract(base_citation_usda, "active", "")
    assert msg == "active"
    assert "Non-English abstract" in cit.local.cataloger_notes

    # Active, overridden
    base_citation_usda.local.cataloger_notes = []  # Clear cataloger notes
    cit, msg = check_abstract(base_citation_usda, "active", "non_english")
    assert msg == "active"
    assert "Non-English abstract" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation_usda.local.cataloger_notes = []  # Clear cataloger notes
    cit, msg = check_abstract(base_citation_usda, "review", "")
    assert msg == "review"
    assert "Non-English abstract" in cit.local.cataloger_notes

    # Review, overridden
    base_citation_usda.local.cataloger_notes = []  # Clear cataloger notes
    cit, msg = check_abstract(base_citation_usda, "review", "non_english")
    assert msg == "review"
    assert "Non-English abstract" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation_usda.local.cataloger_notes = []  # Clear cataloger notes
    cit, msg = check_abstract(base_citation_usda, "dropped", "")
    assert msg == "dropped"
    assert "Non-English abstract" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation_usda.local.cataloger_notes = []  # Clear cataloger notes
    cit, msg = check_abstract(base_citation_usda, "dropped", "non_english")
    assert msg == "dropped"
    assert "Non-English abstract" in cit.local.cataloger_notes

# Test behavior for non-English abstracts
def test_metadata_quality_review_non_english_abstract_non_usda(base_citation_non_usda):
    base_citation_non_usda.abstract = "Dies ist eine sehr wichtige wissenschaftliche Veröffentlichung."

    # Active, not overridden
    cit, msg = check_abstract(base_citation_non_usda, "active", "")
    assert msg == "review"
    assert "Non-English abstract" in cit.local.cataloger_notes

    # Active, overridden
    base_citation_non_usda.local.cataloger_notes = []  # Clear cataloger notes
    cit, msg = check_abstract(base_citation_non_usda, "active", "non_english")
    assert msg == "active"
    assert "Non-English abstract" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation_non_usda.local.cataloger_notes = []  # Clear cataloger notes
    cit, msg = check_abstract(base_citation_non_usda, "review", "")
    assert msg == "review"
    assert "Non-English abstract" in cit.local.cataloger_notes

    # Review, overridden
    base_citation_non_usda.local.cataloger_notes = []  # Clear cataloger notes
    cit, msg = check_abstract(base_citation_non_usda, "review", "non_english")
    assert msg == "review"
    assert "Non-English abstract" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation_non_usda.local.cataloger_notes = []  # Clear cataloger notes
    cit, msg = check_abstract(base_citation_non_usda, "dropped", "")
    assert msg == "dropped"
    assert "Non-English abstract" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation_non_usda.local.cataloger_notes = []  # Clear cataloger notes
    cit, msg = check_abstract(base_citation_non_usda, "dropped", "non_english")
    assert msg == "dropped"
    assert "Non-English abstract" in cit.local.cataloger_notes

def test_metadata_quality_review_manuscript_file_usda(base_citation_usda):
    base_citation_usda.resource.primary = {}
    base_citation_usda.local.USDA = "yes"

    # Active, not overridden
    cit, msg = check_submission_manuscript(base_citation_usda, "active", "")
    assert msg == "review"
    assert "Submission article missing manuscript" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_submission_manuscript(base_citation_usda, "review", "")
    assert msg == "review"
    assert "Submission article missing manuscript" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_submission_manuscript(base_citation_usda, "dropped", "")
    assert msg == "dropped"
    assert "Submission article missing manuscript" in cit.local.cataloger_notes

    # Active, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_submission_manuscript(base_citation_usda, "active",
                                           "manuscript")
    assert msg == "active"
    assert "Submission article missing manuscript" in cit.local.cataloger_notes

    # Review, overridden
    base_citation_usda.local.cataloger_notes = []
    cit, msg = check_submission_manuscript(base_citation_usda, "review",
                                           "manuscript")
    assert msg == "review"
    assert "Submission article missing manuscript" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation_usda.local.cataloger_notes = []

    cit, msg = check_submission_manuscript(base_citation_usda, "dropped",
                                           "manuscript")
    assert msg == "dropped"
    assert "Submission article missing manuscript" in cit.local.cataloger_notes

def test_metadata_quality_review_manuscript_file_non_usda(base_citation_non_usda):
    base_citation_non_usda.resource.primary = {}
    base_citation_non_usda.local.USDA = "no"

    # Active, not overridden
    cit, msg = check_submission_manuscript(base_citation_non_usda, "active", "")
    assert msg == "active"
    assert "Submission article missing manuscript" not in cit.local.cataloger_notes

    # Review, not overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_submission_manuscript(base_citation_non_usda, "review", "")
    assert msg == "review"
    assert "Submission article missing manuscript" not in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_submission_manuscript(base_citation_non_usda, "dropped", "")
    assert msg == "dropped"
    assert "Submission article missing manuscript" not in cit.local.cataloger_notes

    # Active, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_submission_manuscript(base_citation_non_usda, "active",
                                           "manuscript")
    assert msg == "active"
    assert "Submission article missing manuscript" not in cit.local.cataloger_notes

    # Review, overridden
    base_citation_non_usda.local.cataloger_notes = []
    cit, msg = check_submission_manuscript(base_citation_non_usda, "review",
                                           "manuscript")
    assert msg == "review"
    assert "Submission article missing manuscript" not in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation_non_usda.local.cataloger_notes = []

    cit, msg = check_submission_manuscript(base_citation_non_usda, "dropped",
                                           "manuscript")
    assert msg == "dropped"
    assert "Submission article missing manuscript" not in cit.local.cataloger_notes
