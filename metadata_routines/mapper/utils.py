import html
from mapper import errors
from lxml import etree

def format_date(year, month=None, day=None):
    """
    Formats a date string from year, month, and day components.

    Args:
        year (str): The year as a string.
        month (str, optional): The month as a string. Defaults to None.
        day (str, optional): The day as a string. Defaults to None.

    Returns:
        str: A formatted date string in the format "YYYY-MM-DD".
    """
    if year is None:
        return None
    if month is None:
        return None
    if day is None:
        return None
    return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

def to_subscript(text):
    """
    Converts regular text to subscript format.

    Args:
        text (str): The input text string.

    Returns:
        str: The text converted to subscript format.
    """
    if not isinstance(text, str):
        return text
    subscript_map = {
        "0": "\u2080", "1": "\u2081", "2": "\u2082", "3": "\u2083", "4": "\u2084",
        "5": "\u2085", "6": "\u2086", "7": "\u2087", "8": "\u2088", "9": "\u2089",
        "a": "\u2090", "e": "\u2091", "o": "\u2092", "x": "\u2093", "h": "\u2095",
        "k": "\u2096", "l": "\u2097", "m": "\u2098", "n": "\u2099", "p": "\u209A",
        "s": "\u209B", "t": "\u209C", "+": "\u208A", "-": "\u208B", "=": "\u208C",
        "(": "\u208D", ")": "\u208E"
    }
    translation_table = str.maketrans(subscript_map)
    return text.translate(translation_table)

def to_superscript(text):
    """
    Converts regular text to superscript format.

    Args:
        text (str): The input text string.

    Returns:
        str: The text converted to superscript format.
    """
    if not isinstance(text, str):
        return text
    superscript_map = {
        "0": "\u2070", "1": "\u00B9", "2": "\u00B2", "3": "\u00B3",
        "4": "\u2074", "5": "\u2075", "6": "\u2076", "7": "\u2077",
        "8": "\u2078", "9": "\u2079", "+": "\u207A", "-": "\u207B",
        "=": "\u207C", "(": "\u207D", ")": "\u207E",
        "a": "\u1d43", "b": "\u1d47", "c": "\u1d9c", "d": "\u1d48",
        "e": "\u1d49", "f": "\u1da0", "g": "\u1d4d", "h": "\u02b0",
        "i": "\u2071", "j": "\u02b2", "k": "\u1d4f", "l": "\u02e1",
        "m": "\u1d50", "n": "\u207f", "o": "\u1d52", "p": "\u1d56",
        "r": "\u02b3", "s": "\u02e2", "t": "\u1d57", "u": "\u1d58",
        "v": "\u1d5b", "w": "\u02b7", "x": "\u02e3", "y": "\u02b8",
        "A": "\u1d2c", "B": "\u1d2e", "D": "\u1d30", "E": "\u1d31",
        "G": "\u1d33", "H": "\u1d34", "I": "\u1d35", "J": "\u1d36",
        "K": "\u1d37", "L": "\u1d38", "M": "\u1d39", "N": "\u1d3a",
        "O": "\u1d3c", "P": "\u1d3e", "R": "\u1d3f", "T": "\u1d40",
        "U": "\u1d41", "V": "\u2c7d", "W": "\u1d42"
        }
    translation_table = str.maketrans(superscript_map)
    return text.translate(translation_table)


def xml_text_cleanup(root):
    # Replace non-breaking spaces with regular spaces
    for elem in root.iter():
        if elem.text:
            elem.text = elem.text.replace('\xa0', ' ')
        if elem.tail:
            elem.tail = elem.tail.replace('\xa0', ' ')
    # Convert superscript and subscript elements
    superscript_elems = root.findall("sup")
    subscript_elems = root.findall("sub")
    for elem in superscript_elems:
        if elem.text:
            elem.text = to_superscript(elem.text)
    for elem in subscript_elems:
        if elem.text:
            elem.text = to_subscript(elem.text)
    tostring = etree.tostring(root, method="text", encoding="unicode")
    # Remove extra whitespace
    cleaned_text = ' '.join(tostring.split())
    return cleaned_text


def replace_hyphens_with_underscores(original_dict):
    """Recursively replaces hyphens with underscores in dictionary keys.

  Args:
    original_dict: The dictionary to modify.

  Returns:
    data: The modified dictionary.
  """

    new_dict = {}
    for key, value in original_dict.items():
        new_key = key.replace('-', '_')
        if isinstance(value, dict):
            new_dict[new_key] = replace_hyphens_with_underscores(value)
        else:
            new_dict[new_key] = value

    return new_dict


def to_utf8(text):
    try:
        utf8_string = text.encode('utf-8').decode('utf-8')
    except UnicodeEncodeError as e:
        raise errors.FaultyRecordError(str(e))
    return html.unescape(utf8_string)


def str_utf8_or_none(dict, key):
    try:
        text = str(dict[key])
    except KeyError:
        return None
    return to_utf8(text)


def remove_smart_quotes(text):
    """
    Removes smart quotes from the given text.

    Args:
    text: The input text string.

    Returns:
    The string without smart quotes.
    """
    if text is None:
        return None

    # Remove smart quotes (left and right single and double quotes)
    smart_quotes = ["‘", "’", "“", "”", "«", "»"]
    for quote in smart_quotes:
        text = text.replace(quote, "'")

    return text


def clean_dict_key(dict, key):
    text = str_utf8_or_none(dict, key)
    if not isinstance(text, str):
        text = str(text)
    return remove_smart_quotes(text)


def clean_str(text):
    text = to_utf8(text)
    return remove_smart_quotes(text)
