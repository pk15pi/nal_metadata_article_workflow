from metadata_quality_review import (check_volume, check_issue,
                                     check_page, check_title, check_name_elems,
                                     check_primary_author, check_abstract,
                                     check_submission_manuscript,
                                     metadata_quality_review)


# Assert that the base citation is valid and has no quality review issues
def test_metadata_quality_review(base_citation):
    cit, msg = metadata_quality_review(base_citation, "")
    assert msg == "active"
    assert len(cit.local.cataloger_notes) == 0


# Test behavior for valid volume
def test_metadata_quality_review_valid_volume(base_citation):

    # Active
    cit, msg = check_volume(base_citation, "active", "")
    assert msg == "active"
    assert len(cit.local.cataloger_notes) == 0

    # Review
    cit, msg = check_volume(base_citation, "review", "")
    assert msg == "review"
    assert len(cit.local.cataloger_notes) == 0

    # Dropped
    cit, msg = check_volume(base_citation, "dropped", "")
    assert msg == "dropped"
    assert len(cit.local.cataloger_notes) == 0


# Test behavior for missing volume
def test_metadata_quality_review_missing_volume(base_citation):
    base_citation.volume = None

    # Active, not overridden
    cit, msg = check_volume(base_citation, "active", "")
    assert msg == "review"
    assert "No volume number" in cit.local.cataloger_notes

    # Active, overridden
    cit, msg = check_volume(base_citation, "active", "volume")
    assert msg == "active"
    assert "No volume number" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_volume(base_citation, "review", "")
    assert msg == "review"
    assert "No volume number" in cit.local.cataloger_notes

    # Review, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_volume(base_citation, "review", "volume")
    assert msg == "review"
    assert "No volume number" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_volume(base_citation, "dropped", "")
    assert msg == "dropped"
    assert "No volume number" in cit.local.cataloger_notes

    # Review, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_volume(base_citation, "dropped", "volume")
    assert msg == "dropped"
    assert "No volume number" in cit.local.cataloger_notes


# Test behavior for valid issue
def test_metadata_quality_review_valid_issue(base_citation):

    # Active
    cit, msg = check_issue(base_citation, "active", "")
    assert msg == "active"
    assert len(cit.local.cataloger_notes) == 0

    # Review
    cit, msg = check_issue(base_citation, "review", "")
    assert msg == "review"
    assert len(cit.local.cataloger_notes) == 0

    # Dropped
    cit, msg = check_issue(base_citation, "dropped", "")
    assert msg == "dropped"
    assert len(cit.local.cataloger_notes) == 0


# Test behavior for missing issue
def test_metadata_quality_review_missing_issue(base_citation):
    base_citation.issue = None

    # Active, not overridden
    cit, msg = check_issue(base_citation, "active", "")
    assert msg == "review"
    assert "No issue number" in cit.local.cataloger_notes

    # Active, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_issue(base_citation, "active", "issue")
    assert msg == "active"
    assert "No issue number" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_issue(base_citation, "review", "")
    assert msg == "review"
    assert "No issue number" in cit.local.cataloger_notes

    # Review, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_issue(base_citation, "review", "issue")
    assert msg == "review"
    assert "No issue number" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_issue(base_citation, "dropped", "")
    assert msg == "dropped"
    assert "No issue number" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_issue(base_citation, "dropped", "issue")
    assert msg == "dropped"
    assert "No issue number" in cit.local.cataloger_notes


# Test behavior for valid page info
def test_metadata_quality_review_valid_page(base_citation):

    # Active
    cit, msg = check_page(base_citation, "active", "")
    assert msg == "active"
    assert len(cit.local.cataloger_notes) == 0

    # Review
    cit, msg = check_page(base_citation, "review", "")
    assert msg == "review"
    assert len(cit.local.cataloger_notes) == 0

    # Dropped
    cit, msg = check_page(base_citation, "dropped", "")
    assert msg == "dropped"
    assert len(cit.local.cataloger_notes) == 0


# Test behavior for invalid page info
def test_metadata_quality_review_invalid_page(base_citation):
    base_citation.page_str = None

    # Active, not overridden
    cit, msg = check_page(base_citation, "active", "")
    assert msg == "review"
    assert "No page number" in cit.local.cataloger_notes

    # Active, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_page(base_citation, "active", "page")
    assert msg == "active"
    assert "No page number" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_page(base_citation, "review", "")
    assert msg == "review"
    assert "No page number" in cit.local.cataloger_notes

    # Review, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_page(base_citation, "review", "page")
    assert msg == "review"
    assert "No page number" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_page(base_citation, "dropped", "")
    assert msg == "dropped"
    assert "No page number" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_page(base_citation, "dropped", "page")
    assert msg == "dropped"
    assert "No page number" in cit.local.cataloger_notes


# Test behavior for valid title
def test_metadata_quality_review_valid_title(base_citation):

    # Active
    cit, msg = check_title(base_citation, "active", "")
    assert msg == "active"
    assert len(cit.local.cataloger_notes) == 0

    # Review
    cit, msg = check_title(base_citation, "review", "")
    assert msg == "review"
    assert len(cit.local.cataloger_notes) == 0

    # Dropped
    cit, msg = check_title(base_citation, "dropped", "")
    assert msg == "dropped"
    assert len(cit.local.cataloger_notes) == 0


# Test behavior for missing title
def test_metadata_quality_review_missing_title(base_citation):
    base_citation.title = None

    # Active, not overridden
    cit, msg = check_title(base_citation, "active", "")
    assert msg == "dropped"
    assert "No title" in cit.local.cataloger_notes

    # Active, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_title(base_citation, "active", "title")
    assert msg == "review"
    assert "No title" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_title(base_citation, "review", "")
    assert msg == "dropped"
    assert "No title" in cit.local.cataloger_notes

    # Review, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_title(base_citation, "review", "title")
    assert msg == "review"
    assert "No title" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_title(base_citation, "dropped", "")
    assert msg == "dropped"
    assert "No title" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_title(base_citation, "dropped", "title")
    assert msg == "dropped"
    assert "No title" in cit.local.cataloger_notes


# Test behavior for valid author name parts
def test_metadata_quality_review_valid_author_names(base_citation):

    # Active
    cit, msg = check_name_elems(base_citation, "active", "")
    assert msg == "active"
    assert len(cit.local.cataloger_notes) == 0

    # Review
    cit, msg = check_name_elems(base_citation, "review", "")
    assert msg == "review"
    assert len(cit.local.cataloger_notes) == 0

    # Dropped
    cit, msg = check_name_elems(base_citation, "dropped", "")
    assert msg == "dropped"
    assert len(cit.local.cataloger_notes) == 0


# Test behavior for missing last author name
def test_metadata_quality_review_missing_author_names(base_citation):
    base_citation.author[0].family = None

    # Active, not overridden
    cit, msg = check_name_elems(base_citation, "active", "")
    assert msg == "dropped"
    assert "No name elements" in cit.local.cataloger_notes

    # Active, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_name_elems(base_citation, "active", "author")
    assert msg == "review"
    assert "No name elements" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_name_elems(base_citation, "review", "")
    assert msg == "dropped"
    assert "No name elements" in cit.local.cataloger_notes

    # Review, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_name_elems(base_citation, "review", "author")
    assert msg == "review"
    assert "No name elements" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_name_elems(base_citation, "dropped", "")
    assert msg == "dropped"
    assert "No name elements" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_name_elems(base_citation, "dropped", "author")
    assert msg == "dropped"
    assert "No name elements" in cit.local.cataloger_notes


# Test behavior for valid author sequence elements
def test_metadata_quality_review_valid_author_sequence(base_citation):

    # Active
    cit, msg = check_primary_author(base_citation, "active", "")
    assert msg == "active"
    assert len(cit.local.cataloger_notes) == 0

    # Review
    cit, msg = check_primary_author(base_citation, "review", "")
    assert msg == "review"
    assert len(cit.local.cataloger_notes) == 0

    # Dropped
    cit, msg = check_primary_author(base_citation, "dropped", "")
    assert msg == "dropped"
    assert len(cit.local.cataloger_notes) == 0


# Test behavior for invalid author sequence elements
def test_metadata_quality_review_invalid_author_sequence(base_citation):
    base_citation.author[1].sequence = "first"

    # Active, not overridden
    cit, msg = check_primary_author(base_citation, "active", "")
    assert msg == "review"
    assert "Multiple primary authors" in cit.local.cataloger_notes

    # Active, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_primary_author(base_citation, "active", "primary")
    assert msg == "active"
    assert "Multiple primary authors" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_primary_author(base_citation, "review", "")
    assert msg == "review"
    assert "Multiple primary authors" in cit.local.cataloger_notes

    # Review, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_primary_author(base_citation, "review", "primary")
    assert msg == "review"
    assert "Multiple primary authors" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_primary_author(base_citation, "dropped", "")
    assert msg == "dropped"
    assert "Multiple primary authors" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_primary_author(base_citation, "dropped", "primary")
    assert msg == "dropped"
    assert "Multiple primary authors" in cit.local.cataloger_notes


def test_metadata_quality_review_valid_abstract(base_citation):

    # Active
    cit, msg = check_abstract(base_citation, "active", "")
    assert msg == "active"
    assert len(cit.local.cataloger_notes) == 0

    # Review
    cit, msg = check_abstract(base_citation, "review", "")
    assert msg == "review"
    assert len(cit.local.cataloger_notes) == 0

    # Dropped
    cit, msg = check_abstract(base_citation, "dropped", "")
    assert msg == "dropped"
    assert len(cit.local.cataloger_notes) == 0


def test_metadata_quality_review_missing_abstract(base_citation):
    base_citation.abstract = None

    # Active, not overridden
    cit, msg = check_abstract(base_citation, "active", "")
    assert msg == "dropped"
    assert "missing abstract" in cit.local.cataloger_notes

    # Active, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation, "active", "abstract")
    assert msg == "review"
    assert "missing abstract" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation, "review", "")
    assert msg == "dropped"
    assert "missing abstract" in cit.local.cataloger_notes

    # Review, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation, "review", "abstract")
    assert msg == "review"
    assert "missing abstract" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation, "dropped", "")
    assert msg == "dropped"
    assert "missing abstract" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation, "dropped", "abstract")
    assert msg == "dropped"
    assert "missing abstract" in cit.local.cataloger_notes


def test_metadata_quality_review_short_abstract(base_citation):
    base_citation.abstract = "Short abstract"

    # Active, not overridden
    cit, msg = check_abstract(base_citation, "active", "")
    assert msg == "dropped"
    assert "Abstract is empty or less than 50 character" in \
           cit.local.cataloger_notes

    # Active, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation, "active", "short_abstract")
    assert msg == "active"
    assert "Abstract is empty or less than 50 character" in \
           cit.local.cataloger_notes

    # Review, not overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation, "review", "")
    assert msg == "dropped"
    assert "Abstract is empty or less than 50 character" in \
           cit.local.cataloger_notes

    # Review, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation, "review", "short_abstract")
    assert msg == "review"
    assert "Abstract is empty or less than 50 character" in \
           cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation, "dropped", "")
    assert msg == "dropped"
    assert "Abstract is empty or less than 50 character" in \
           cit.local.cataloger_notes

    # Dropped, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation, "dropped", "short_abstract")
    assert msg == "dropped"
    assert "Abstract is empty or less than 50 character" in \
           cit.local.cataloger_notes


# Test behavior for abstracts containing non-utf8 characters
def test_metadata_quality_review_non_utf8_abstract(base_citation):
    base_citation.abstract = \
        "This is a sufficiently long abstract with non-utf8 characters:" + \
        "\ud835\ude17"

    # Active, not overridden
    cit, msg = check_abstract(base_citation, "active", "")
    assert msg == "review"
    assert "Non-UTF8 characters in abstract" in cit.local.cataloger_notes

    # Active, overridden
    base_citation.local.cataloger_notes = []  # Clear cataloger notes
    cit, msg = check_abstract(base_citation, "active", "utf8")
    assert msg == "active"
    assert "Non-UTF8 characters in abstract" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation, "review", "")
    assert msg == "review"
    assert "Non-UTF8 characters in abstract" in cit.local.cataloger_notes

    # Review, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation, "review", "utf8")
    assert msg == "review"
    assert "Non-UTF8 characters in abstract" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_abstract(base_citation, "dropped", "")
    assert msg == "dropped"
    assert "Non-UTF8 characters in abstract" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation.local.cataloger_notes = []  # Clear cataloger notes
    cit, msg = check_abstract(base_citation, "dropped", "utf8")
    assert msg == "dropped"
    assert "Non-UTF8 characters in abstract" in cit.local.cataloger_notes

# Test behavior for non-English abstracts
def test_metadata_quality_review_non_english_abstract(base_citation):
    base_citation.abstract = "Dies ist eine sehr wichtige wissenschaftliche Veröffentlichung."

    # Active, not overridden
    cit, msg = check_abstract(base_citation, "active", "")
    assert msg == "review"
    assert "Non-English abstract" in cit.local.cataloger_notes

    # Active, overridden
    base_citation.local.cataloger_notes = []  # Clear cataloger notes
    cit, msg = check_abstract(base_citation, "active", "non_english")
    assert msg == "active"
    assert "Non-English abstract" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation.local.cataloger_notes = []  # Clear cataloger notes
    cit, msg = check_abstract(base_citation, "review", "")
    assert msg == "review"
    assert "Non-English abstract" in cit.local.cataloger_notes

    # Review, overridden
    base_citation.local.cataloger_notes = []  # Clear cataloger notes
    cit, msg = check_abstract(base_citation, "review", "non_english")
    assert msg == "review"
    assert "Non-English abstract" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation.local.cataloger_notes = []  # Clear cataloger notes
    cit, msg = check_abstract(base_citation, "dropped", "")
    assert msg == "dropped"
    assert "Non-English abstract" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation.local.cataloger_notes = []  # Clear cataloger notes
    cit, msg = check_abstract(base_citation, "dropped", "non_english")
    assert msg == "dropped"
    assert "Non-English abstract" in cit.local.cataloger_notes

def test_metadata_quality_review_manuscript_file(base_citation):
    base_citation.resource.primary = {}
    base_citation.local.USDA = "yes"

    # Active, not overridden
    cit, msg = check_submission_manuscript(base_citation, "active", "")
    assert msg == "review"
    assert "Submission article missing manuscript" in cit.local.cataloger_notes

    # Review, not overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_submission_manuscript(base_citation, "review", "")
    assert msg == "review"
    assert "Submission article missing manuscript" in cit.local.cataloger_notes

    # Dropped, not overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_submission_manuscript(base_citation, "dropped", "")
    assert msg == "dropped"
    assert "Submission article missing manuscript" in cit.local.cataloger_notes

    # Active, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_submission_manuscript(base_citation, "active",
                                           "manuscript")
    assert msg == "active"
    assert "Submission article missing manuscript" in cit.local.cataloger_notes

    # Review, overridden
    base_citation.local.cataloger_notes = []
    cit, msg = check_submission_manuscript(base_citation, "review",
                                           "manuscript")
    assert msg == "review"
    assert "Submission article missing manuscript" in cit.local.cataloger_notes

    # Dropped, overridden
    base_citation.local.cataloger_notes = []

    cit, msg = check_submission_manuscript(base_citation, "dropped",
                                           "manuscript")
    assert msg == "dropped"
    assert "Submission article missing manuscript" in cit.local.cataloger_notes
