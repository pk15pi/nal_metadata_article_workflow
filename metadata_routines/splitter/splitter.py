import json
import lxml
from lxml import etree


def split_json(json_data) -> tuple[list[str], str]:
    """ Splits JSON data into a list of articles as JSON strings.

    Args:
        json_data: JSON object

    Returns
        :returns: result (tuple)
            article_json_list (list[str]) - list of strings:
            message (str) - if successful returns 'successful',
            otherwise JSON parsing error message

    """

    result = ([], 'Unknown JSON metadata')

    if isinstance(json_data, dict) and 'message' in json_data:
        """ Crossref article single"""
        article_json = json_data['message']
        article_json_str = json.dumps(article_json)
        result = ([article_json_str], 'successful')
    elif isinstance(json_data, dict) and 'DOI' in json_data:
        """ Chorus article single"""
        article_json_str = json.dumps(json_data)
        result = ([article_json_str], 'successful')
    elif isinstance(json_data, list) and len(json_data) > 0 and \
            'submission_node_id' in json_data[0]:
        """submit site article collection"""
        submission_string_list: list[str] = []
        for submission in json_data:
            submission_json_str = json.dumps(submission)
            submission_string_list.append(submission_json_str)
        result = (submission_string_list, 'successful')

    return result


def split_pubmed(xml_data) -> tuple[list[str], str]:
    """ Splits PubMed XML data into a list of articles as JSON strings.

    Args:
        xml_data (lxml.etree.ElementTree) collection of PubMed articles

    Returns
            :returns: result (tuple)
                article_xml_list (list[str]) - list of strings:
                message (str) - if successful returns 'successful'

    """
    pubmed_doctype = ''''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Article PUBLIC "-//NLM//DTD PubMed 3.0//EN" \
"https://dtd.nlm.nih.gov/ncbi/pubmed/in/PubMed.dtd">
'''

    list_of_articles: list[str] = []
    for article in xml_data:
        doc_string = etree.tostring(article, pretty_print=True)
        article_xml_str = pubmed_doctype + doc_string.decode('utf-8')
        list_of_articles.append(article_xml_str)
    result = (list_of_articles, 'successful')
    return result


def split_xml(xml_data, document_string) -> tuple[list[str], str]:
    """Read an article collection in XML document string and split it into a
    list of single record XML strings.
    The XML namespaces and declaration are preserved.

    Args
        :param xml_data (lxml.etree.ElementTree) - XML document
        :param document_string (str) - XML document string
    Returns
         :returns: result (tuple)
            article_xml_list (list) - list of strings:
            message - if successful, otherwise error message
    """

    result = ([], 'Unknown XML metadata')

    root = xml_data.tag

    if root == 'article' or root == 'Article':
        # single PubMED or JATS record:
        result = ([document_string], 'successful')
    elif root == '{http://www.elsevier.com/xml/document/schema}document':
        # single Elsevier CONSYS record:
        result = ([document_string], 'successful')
    elif root == 'ArticleSet':
        # collection of PubMED articles:
        list_of_articles, message = split_pubmed(xml_data)
        result = (list_of_articles, message)
    return result


def get_json(my_string: str) -> tuple[dict, str]:
    try:
        data_json = json.loads(my_string)
        result = (data_json, 'successful')
    except (json.decoder.JSONDecodeError, ValueError) as err:
        result = (None, 'JSON Error: ' + str(err))
    return result


def get_xml(my_string: str) -> tuple[lxml.etree.ElementTree, str]:
    try:
        data_xml = etree.fromstring(my_string.encode('utf-8'))
        result = (data_xml, 'successful')
    except etree.XMLSyntaxError as err:
        result = (None, 'XML Error: ' + str(err))
    return result


def splitter(document_string: str) -> tuple[list[str], str]:
    """Receives a JSON or XML document string containing a single or
       collection of article records and returns a list of strings
       with a message string.

    Args
        :param document_string (str) - String containing the JSON or XML
        document
    Returns
        :returns result (tuple):
            list_of_articles (list): list of article strings with JSON or
            XML documents
            message (str) - if successful is 'successful', otherwise error
            message
    Notes
        :note Requires XML strings to start with "<?xml version="1.0"
        encoding="UTF-8"?>"
        :note Requires JSON strings to start with "{" or "["
    """

    document_string = document_string.lstrip()

    result = ([], 'Unknown metadata format')

    if document_string[:5] == "<?xml":
        # If XML string
        data_xml, message = get_xml(document_string)
        if message == "successful":
            list_of_articles, message = split_xml(data_xml, document_string)
            result = (list_of_articles, message)
        else:
            result = ([], message)
    elif document_string[:1] in "{[":
        # If JSON string
        data_json, message = get_json(document_string)
        if message == "successful":
            list_of_articles, message = split_json(data_json)
            result = (list_of_articles, message)
        else:
            result = ([], message)

    return result
