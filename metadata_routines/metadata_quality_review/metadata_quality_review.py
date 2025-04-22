from citation import Citation
from langdetect import detect
import re
from typing import Tuple
import warnings


def check_doi(cit, msg, override_str):
    override = False
    override_parts = override_str.split(" ")
    if "doi" in override_parts:
        override = True
    if cit.DOI is None or cit.DOI == "":
        cataloguer_note = "No DOI"
        cit.local.cataloger_notes.append(cataloguer_note)
        if not override and msg == "active":
            msg = "review"
    elif not is_doi(cit.DOI):
        cataloguer_note = "Invalid DOI"
        cit.local.cataloger_notes.append(cataloguer_note)
        if not override and msg == "active":
            msg = "review"
    return cit, msg


def check_volume(cit, msg, override_str):
    override = False
    override_parts = override_str.split(" ")
    if "volume" in override_parts:
        override = True
    if cit.volume is None or cit.volume == "":
        cataloguer_note = "No volume number"
        cit.local.cataloger_notes.append(cataloguer_note)
        if not override and msg == "active":
            msg = "review"
    return cit, msg


def check_issue(cit, msg, override_str):
    override = False
    override_parts = override_str.split(" ")
    if "issue" in override_parts:
        override = True
    if cit.issue is None or cit.issue == "":
        cataloguer_note = "No issue number"
        cit.local.cataloger_notes.append(cataloguer_note)
        if not override and msg == "active":
            msg = "review"
    return cit, msg


def check_page(cit, msg, override_str):
    override = False
    override_parts = override_str.split(" ")
    if "page" in override_parts:
        override = True
    if cit.page is None or cit.page.get("page_str", None) is None or \
            cit.page["page_str"] == "":
        cataloguer_note = "No page number"
        cit.local.cataloger_notes.append(cataloguer_note)
        if not override and msg == "active":
            msg = "review"
    return cit, msg


def check_title(cit, msg, override_str):
    override = False
    override_parts = override_str.split(" ")
    if "title" in override_parts:
        override = True
    if cit.title is None or cit.title == "":
        cataloguer_note = "No title"
        cit.local.cataloger_notes.append(cataloguer_note)
        if not override:
            msg = "dropped"
        elif override and msg != "dropped":
            msg = "review"
    return cit, msg


def check_name_elems(cit, msg, override_str):
    override = False
    override_parts = override_str.split(" ")
    if "author" in override_parts:
        override = True

    # Case 1: No author element defined, or empty list of authors
    if cit.author is None or len(cit.author) == 0:
        cataloguer_note = "No authors listed"
        cit.local.cataloger_notes.append(cataloguer_note)
        if not override:
            msg = "dropped"
        elif override and msg == "active":
            msg = "review"

    # Case 2: Author element defined, iterate through each element
    else:
        if cit.author[0] is None or cit.author[0].family is None or \
                cit.author[0].family == "":
            cataloguer_note = "No name elements"
            cit.local.cataloger_notes.append(cataloguer_note)
            if not override:
                msg = "dropped"
            elif override and msg != "dropped":
                msg = "review"
    return cit, msg


def check_primary_author(cit, msg, override_str):
    override = False
    override_parts = override_str.split(" ")
    if "primary" in override_parts:
        override = True
    found_primary = False
    for author in cit.author:
        if author.sequence == "first" and found_primary is False:
            found_primary = True
        elif author.sequence == "first" and found_primary is True:
            cataloguer_note = "Multiple primary authors"
            cit.local.cataloger_notes.append(cataloguer_note)
            if not override and msg == "active":
                msg = "review"
    return cit, msg


def check_issue_date(cit, msg, override_str):
    override = False
    override_parts = override_str.split(" ")
    if "date" in override_parts:
        override = True
    if cit.date is None or cit.date.get("published", None) is None or \
            cit.date["published"].get("year", None) is None or \
            cit.date["published"]["year"] == "":
        cataloguer_note = "No issue date"
        cit.local.cataloger_notes.append(cataloguer_note)
        if not override and msg != "dropped":
            msg = "review"
    return cit, msg


def has_non_utf8_characters(text):
    try:
        text.encode('utf-8').decode('utf-8')
        return False
    except (UnicodeDecodeError, UnicodeEncodeError):
        return True


def is_doi(text):
    pattern = r'10\.[a-zA-Z0-9]{4}\/[a-zA-Z0-9]{6}'
    match = re.match(pattern, text)
    if match:
        return True
    return False


def check_abstract(cit, msg, override_str):
    override_missing = False
    override_short = False
    override_utf8 = False
    override_non_english = False
    override_parts = override_str.split(" ")
    if "abstract" in override_parts:
        override_missing = True
    if "short_abstract" in override_parts:
        override_short = True
    if "utf8" in override_parts:
        override_utf8 = True
    if "non_english" in override_parts:
        override_non_english = True

    # Check for missing abstract
    if cit.abstract is None:
        cataloguer_note = "missing abstract"
        cit.local.cataloger_notes.append(cataloguer_note)
        if not override_missing:
            msg = "dropped"
        elif override_missing and msg != "dropped":
            msg = "review"
        # No need to check for short, UTF8, or non-English abstract if missing
        return cit, msg

    # If not missing, check for short abstract
    if len(cit.abstract) <= 50:
        cataloguer_note = "Abstract is empty or less than 50 character"
        cit.local.cataloger_notes.append(cataloguer_note)
        if not override_short:
            msg = "dropped"

    if has_non_utf8_characters(cit.abstract):
        cataloguer_note = "Non-UTF8 characters in abstract"
        cit.local.cataloger_notes.append(cataloguer_note)
        if not override_utf8 and msg != "dropped":
            msg = "review"

    if cit.abstract and detect(cit.abstract) != "en":
        cataloguer_note = "Non-English abstract"
        cit.local.cataloger_notes.append(cataloguer_note)
        if not override_non_english and msg != "dropped":
            msg = "review"

    return cit, msg


def check_submission_manuscript(cit, msg, override_str):
    override = False
    override_parts = override_str.split(" ")
    if "manuscript" in override_parts:
        override = True
    if cit.local.USDA:
        if cit.resource.primary == {}:
            cataloguer_note = "Submission article missing manuscript"
            cit.local.cataloger_notes.append(cataloguer_note)
            if not override and msg == "active":
                msg = "review"
    return cit, msg


def metadata_quality_review(
        cit: Citation,
        override: str = None
) -> Tuple[Citation, str]:
    message = "active"
    if not override:
        override = ""
    override = override.lower()
    print(override)

    # Generate a warning if the override string contains any unexpected substrings
    expected_override_parts = ["doi", "volume", "issue", "page", "title", "author", "primary", "date", "abstract",
                               "short_abstract", "utf8", "non-english", "manuscript"]
    override_parts = override.split(" ")
    for part in override_parts:
        if part not in expected_override_parts and part != "":
            warnings.warn(f"Override string '{part}' not recognized. Ignoring.")

    cit, message = check_doi(cit, message, override)
    cit, message = check_volume(cit, message, override)
    cit, message = check_issue(cit, message, override)
    cit, message = check_page(cit, message, override)
    cit, message = check_title(cit, message, override)
    cit, message = check_name_elems(cit, message, override)
    cit, message = check_primary_author(cit, message, override)
    cit, message = check_issue_date(cit, message, override)
    cit, message = check_abstract(cit, message, override)
    cit, message = check_submission_manuscript(cit, message, override)

    return cit, message
