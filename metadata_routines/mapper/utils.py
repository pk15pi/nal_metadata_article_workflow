import html
from mapper import errors


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
