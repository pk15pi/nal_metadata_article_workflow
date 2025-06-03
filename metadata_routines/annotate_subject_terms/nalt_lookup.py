import tomli
import sqlite3
import os

def valid_invalid_terms(uris: list[str], cursor):
    # Check if the URIs exist in the database
    valid_uris = []
    invalid_uris = []
    for uri in uris:
        cursor.execute("SELECT uri FROM nalt_data WHERE uri = ?", (uri,))
        result = cursor.fetchone()
        if result:
            valid_uris.append(uri)
        else:
            invalid_uris.append(uri)
    return valid_uris, invalid_uris

def uri_to_broader_terms(uris: list[str], cursor):
    # Create a dictionary matching each uri to its list of broader uris
    broader_terms = []
    for uri in uris:
        cursor.execute("SELECT broader_terms FROM nalt_data WHERE uri = ?", (uri,))
        result = cursor.fetchone()
        if result:
            broader_terms.extend(result[0].split(",") if result[0] else [])
    return broader_terms

def filter_broader_terms(uris, broader_terms):
    broader_terms = [uri for uri in uris if uri in broader_terms]
    narrower_terms = [uri for uri in uris if uri not in broader_terms]
    return broader_terms, narrower_terms

def split_topic_geographic(uris, cursor):
    # Split the URIs into topics and geographics
    topic_terms = []
    geographic_terms = []
    for uri in uris:
        cursor.execute("SELECT type FROM nalt_data WHERE uri = ?", (uri,))
        result = cursor.fetchone()
        if result:
            if result[0] == "T":
                topic_terms.append(uri)
            elif result[0] == "G":
                geographic_terms.append(uri)
    return topic_terms, geographic_terms

def validate_nalt_terms(uris: list[str]):
    """
    Validate NALT terms against the database.

    Args:
        terms (list[str]): List of NALT terms to validate.

    Returns:
        ... fill this in later
    """
    # Connect to the SQLite database
    config_path = os.getenv("COGITO_CONFIG")
    if not config_path:
        raise ValueError("Environment variable COGITO_CONFIG is not set.")
    with open(config_path, "rb") as f:
        config = tomli.load(f)
    db_path = config.get("database_file")
    if not db_path:
        raise ValueError("Database file path not found in configuration.")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    valid_uris, invalid_uris = valid_invalid_terms(uris, cursor)
    broader_uris, narrower_uris = filter_broader_terms(valid_uris, uri_to_broader_terms(valid_uris, cursor))

    # Lastly, we need to split narrower_uris into two lists, one for topics and one for geographics
    topics, geographics = split_topic_geographic(narrower_uris, cursor)

    return {
        "invalid_uris": invalid_uris,
        "broader_uris": broader_uris,
        "topics": topics,
        "geographics": geographics
    }

def uri_to_term(uri: str):
    """
    Convert a NALT URI to its term.

    Args:
        uri (str): The NALT URI.

    Returns:
        str: The term corresponding to the URI.
    """
    # Connect to the SQLite database
    config_path = os.getenv("COGITO_CONFIG")
    if not config_path:
        raise ValueError("Environment variable COGITO_CONFIG is not set.")
    with open(config_path, "rb") as f:
        config = tomli.load(f)
    db_path = config.get("database_file")
    if not db_path:
        raise ValueError("Database file path not found in configuration.")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT preferred_label FROM nalt_data WHERE uri = ?", (uri,))
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        return None