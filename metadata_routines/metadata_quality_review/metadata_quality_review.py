from citation import Citation
from langdetect import detect
import re
from typing import Tuple
import warnings

def override_phrase_to_keyword(phrase: str):
    valid_keywords = [
        "volume",
        "issue",
        "page",
        "title",
        "author",
        "primary",
        "date",
        "abstract",
        "short_abstract",
        "utf8",
        "non-english",
        "manuscript"
    ]
    phrase = phrase.lower()
    phrase = phrase.replace(".", " ")
    phrase = phrase.replace(",", " ")
    phrase = phrase.replace(";", " ")
    phrase_list = phrase.split(" ")
    keyword_list = [elem for elem in phrase_list if elem in set(valid_keywords)]
    keyword_list = list(set(keyword_list))
    keyword_str = " ".join(keyword_list)
    return keyword_str


def check_volume(cit, msg, override_str):
    override = False
    override_parts = override_str.split(" ")
    if "volume" in override_parts:
        override = True
    if cit.volume is None or cit.volume == "":
        cataloger_note = "No volume number"
        cit.local.cataloger_notes.append(cataloger_note)
        if not override and msg == "active" and cit.local.USDA == "no":
            msg = "review"
    return cit, msg


def check_issue(cit, msg, override_str):
    override = False
    override_parts = override_str.split(" ")
    if "issue" in override_parts:
        override = True
    if cit.issue is None or cit.issue == "":
        cataloger_note = "No issue number"
        cit.local.cataloger_notes.append(cataloger_note)
        if not override and msg == "active" and cit.local.USDA == "no":
            msg = "review"
    return cit, msg


def check_page(cit, msg, override_str):
    override = False
    override_parts = override_str.split(" ")
    if "page" in override_parts:
        override = True
    if cit.page is None or cit.page.get("page_str", None) is None or \
            cit.page["page_str"] == "":
        cataloger_note = "No page number"
        cit.local.cataloger_notes.append(cataloger_note)
        if not override and msg == "active" and cit.local.USDA == "no":
            msg = "review"
    return cit, msg


def check_title(cit, msg, override_str):
    override = False
    override_parts = override_str.split(" ")
    if "title" in override_parts:
        override = True
    if cit.title is None or cit.title == "":
        cataloger_note = "No title"
        cit.local.cataloger_notes.append(cataloger_note)
        if not override and cit.local.USDA == "no":
            msg = "dropped"
        elif override and msg != "dropped" and cit.local.USDA == "no":
            msg = "review"
    return cit, msg


def check_name_elems(cit, msg, override_str):
    override = False
    override_parts = override_str.split(" ")
    if "author" in override_parts:
        override = True

    # Case 1: No author element defined, or empty list of authors
    if cit.author is None or len(cit.author) == 0:
        cataloger_note = "No authors listed"
        cit.local.cataloger_notes.append(cataloger_note)
        if not override and cit.local.USDA == "no":
            msg = "dropped"
        elif override and msg == "active" and cit.local.USDA == "no":
            msg = "review"

    # Case 2: Author element defined, iterate through each element
    else:
        if cit.author[0] is None or cit.author[0].family is None or \
                cit.author[0].family == "":
            cataloger_note = "No name elements"
            cit.local.cataloger_notes.append(cataloger_note)
            if not override and cit.local.USDA == "no":
                msg = "dropped"
            elif override and msg != "dropped" and cit.local.USDA == "no":
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
            cataloger_note = "Multiple primary authors"
            cit.local.cataloger_notes.append(cataloger_note)
            if not override and msg == "active" and cit.local.USDA == "no":
                msg = "review"
            break
    return cit, msg


def check_issue_date(cit, msg, override_str):
    override = False
    override_parts = override_str.split(" ")
    if "date" in override_parts:
        override = True
    if cit.date is None or cit.date.get("published", None) is None or \
            cit.date["published"].get("year", None) is None or \
            cit.date["published"]["year"] == "":
        cataloger_note = "No issue date"
        cit.local.cataloger_notes.append(cataloger_note)
        if not override and msg != "dropped" and cit.local.USDA == "no":
            msg = "review"
    return cit, msg


def has_non_utf8_characters(text):
    try:
        text.encode('utf-8').decode('utf-8')
        return False
    except (UnicodeDecodeError, UnicodeEncodeError):
        return True


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
        cataloger_note = "missing abstract"
        cit.local.cataloger_notes.append(cataloger_note)
        if not override_missing and cit.local.USDA == "no":
            msg = "dropped"
        elif override_missing and msg != "dropped" and cit.local.USDA == "no":
            msg = "review"
        # No need to check for short, UTF8, or non-English abstract if missing
        return cit, msg

    # If not missing, check for short abstract
    if len(cit.abstract) <= 50:
        cataloger_note = "Abstract is empty or less than 50 character"
        cit.local.cataloger_notes.append(cataloger_note)
        if not override_short and cit.local.USDA == "no":
            msg = "dropped"

    if has_non_utf8_characters(cit.abstract):
        cataloger_note = "Non-UTF8 characters in abstract"
        cit.local.cataloger_notes.append(cataloger_note)
        if not override_utf8 and msg != "dropped" and cit.local.USDA == "no":
            msg = "review"

    if cit.abstract and detect(cit.abstract) != "en":
        cataloger_note = "Non-English abstract"
        cit.local.cataloger_notes.append(cataloger_note)
        if not override_non_english and msg != "dropped" and cit.local.USDA == "no":
            msg = "review"

    return cit, msg


def check_submission_manuscript(cit, msg, override_str):
    override = False
    override_parts = override_str.split(" ")
    if "manuscript" in override_parts:
        override = True
    if cit.local.USDA == "yes":
        if cit.resource.primary == {}:
            cataloger_note = "Submission article missing manuscript"
            cit.local.cataloger_notes.append(cataloger_note)
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
    override = override_phrase_to_keyword(override)

    # Generate a warning if the override string contains any unexpected substrings
    expected_override_parts = ["volume", "issue", "page", "title", "author", "primary", "date", "abstract",
                               "short_abstract", "utf8", "non-english", "manuscript"]
    override_parts = override.split(" ")
    for part in override_parts:
        if part not in expected_override_parts and part != "":
            warnings.warn(f"Override string '{part}' not recognized. Ignoring.")

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
