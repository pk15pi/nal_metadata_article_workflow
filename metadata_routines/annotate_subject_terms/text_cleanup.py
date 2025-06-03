import re
import unicodedata

REPLACE_WITH_PERIOD = {
    'subsp': ' subsp',
    'ssp': ' ssp',
    'cv': ' cv',
    'var': ' var',
    'pv': ' pv',
    'St': ' St',
    '(St': '(St',
}

REGX_HASH = {
    r'U\.S\.D\.A\.\s': 'USDA ',
    r'U\.S\.\s': 'US ',
    r'U\.S\.$': 'US ',
    r'U\.S\.,': 'US,',
    r'f\.\s*sp\.': 'fsp',
}

COPYRIGHT_CLEANUP = [
    r'©.*',                         # Copyright sign
    r'\(c\)\s+\d{4}.*',             # (c) 2002 or (C) 1998
    r'copyright.*',                 # [Cc]opyright ....
    r'published\s+by\s+elsevier',   # Published by Elsevier
    r'all\s+rights',                # [Aa]ll rights .....
]

def remove_periods(text):
    # REGX_HASH replacements
    for pattern in sorted(REGX_HASH, reverse=True):
        text = re.sub(pattern, REGX_HASH[pattern], text, flags=re.MULTILINE)
    # Check each word ending with a period against the hash.
    def repl(match):
        word = match.group(2)
        return REPLACE_WITH_PERIOD.get(word, match.group(1))
    text = re.sub(r'(\s([\(\w]+)\.?)', repl, text)
    # Replace multiple spaces with one
    text = re.sub(r'\s+', ' ', text)
    return text

def replace_metacharacters(text):
    # Replace < with «, > with »
    text = text.replace('<', '«').replace('>', '»')
    return text

# Define hyphen/minus/dash unicode code points
HYPHENS = [
    'HYPHEN', 'SOFT HYPHEN', 'NON-BREAKING HYPHEN', 'HYPHEN BULLET',
    'SMALL HYPHEN-MINUS', 'FULLWIDTH HYPHEN-MINUS', 'TAG HYPHEN-MINUS'
]
MINUS = ['MINUS SIGN', 'HEAVY MINUS SIGN', 'ROMAN UNCIA SIGN']
DASHES = [
    'FIGURE DASH', 'EN DASH', 'EM DASH', 'TWO-EM DASH', 'THREE-EM DASH', 'SMALL EM DASH'
]
def get_unicode_chars(names):
    return ''.join([unicodedata.lookup(name) for name in names])

def normalize_hyphens(text):
    hyphens = get_unicode_chars(HYPHENS)
    minus = get_unicode_chars(MINUS)
    dashes = get_unicode_chars(DASHES)
    hyphen_minus = unicodedata.lookup('HYPHEN-MINUS')
    for group in [hyphens, minus, dashes]:
        text = re.sub(rf'[{re.escape(group)}]', hyphen_minus, text)
    return text

def remove_copyright_statement(text):
    for pattern in COPYRIGHT_CLEANUP:
        new_text, n = re.subn(pattern, '', text, flags=re.IGNORECASE)
        if n:
            text = new_text
            break
    text = re.sub(r'\s+\Z', '', text)
    return text

# Example usage:
if __name__ == "__main__":
    sample_text = f"U.S.D.A. subsp. (c) 2020 published by Elsevier <hello> {unicodedata.lookup('FULLWIDTH HYPHEN-MINUS')}"
    print("Original text: ", sample_text)
    print("Removed periods: ", remove_periods(sample_text))
    print("Replaced metadata chars: ", replace_metacharacters(sample_text))
    print("Normalized hyphens: ", normalize_hyphens(sample_text))
    print("Removed copyright: ", remove_copyright_statement(sample_text))