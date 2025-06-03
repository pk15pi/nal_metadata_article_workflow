from lxml import etree as ET
from langdetect import detect
from citation import Citation, Resource, License, Author
import pickle
from annotate_subject_terms import remove_periods, replace_metacharacters, normalize_hyphens, remove_copyright_statement
import tomli
import os
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
from .nalt_lookup import validate_nalt_terms, uri_to_term
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_cogx(title, journalTitle, abstract, output_file, identifier="dummy",):
    """
    Convert title, journalTitle, and abstract strings into a COGX XML document.
    Saves the XML document to the specified output file.
    """
    # Create root and doc elements
    root = ET.Element("cogito")
    doc = ET.SubElement(root, "doc", id=str(identifier))

    # Helper for adding content zones
    def add_zone(parent, zone_type, value):
        content = ET.SubElement(parent, "content", zone=zone_type)
        text = ET.SubElement(content, "text", mimetype="text/plain")
        text.text = value

    # Helper for adding metadata values
    def add_metadata(parent, zone, name, value):
        attribs = {"zone": zone} if zone else {}
        metadata = ET.SubElement(parent, "metadata", **attribs)
        a = ET.SubElement(metadata, "a", name=name, value=value)

    # Add the article title (with carriage returns as in Perl)
    if title:
        add_zone(doc, "articleTitle", title + "\n\n")
    else:
        raise ValueError("No title found")

    # Add the journal title (with "JnlTi " prefix and carriage returns)
    if journalTitle:
        add_zone(doc, "journalTitle", f"JnlTi {journalTitle}.\n\n")
    else:
        raise ValueError("No journal title found")

    # Add the abstract (with carriage returns)
    if abstract:
        add_zone(doc, "Abstract", abstract + "\n\n")
    else:
        raise ValueError("No abstract found")

    # Add language metadata
    add_metadata(doc, None, "language", "English")
    add_metadata(doc, "articleTitle", "language", "English")
    add_metadata(doc, "journalTitle", "language", "English")
    add_metadata(doc, "Abstract", "language", "English")

    ET.ElementTree(root).write(output_file, encoding="utf-8", xml_declaration=True)

def get_title_in_english(citation_object: Citation):
    if citation_object.translated_title:
        if detect(citation_object.translated_title) == 'en':
            return citation_object.translated_title
    if citation_object.title:
        if detect(citation_object.title) == 'en':
            return citation_object.title
    return ""

def cit_to_cogx(citation_object, output_cogx_file):
    """
    Convert a Citation object to a COGX XML document.
    Save the XML document to the specified output file.
    """

    # Extract title, journal title, and abstract
    title = get_title_in_english(citation_object)
    journal_title = citation_object.container_title_str()
    abstract = citation_object.abstract

    # Clean up text
    title = remove_periods(title)
    title = replace_metacharacters(title)
    title = normalize_hyphens(title)
    title = title + "."

    journal_title = remove_periods(journal_title)
    journal_title = normalize_hyphens(journal_title)

    abstract = remove_periods(abstract)
    abstract = replace_metacharacters(abstract)
    abstract = normalize_hyphens(abstract)
    abstract = remove_copyright_statement(abstract)

    # Create COGX XML
    create_cogx(title, journal_title, abstract, output_cogx_file, identifier=citation_object.local.identifiers.get("pid", "dummy"))

def read_config():
    config_path = os.getenv("COGITO_CONFIG")
    if not config_path:
        raise ValueError("Environment variable COGITO_CONFIG is not set.")
    with open(config_path, "rb") as f:
        config = tomli.load(f)
    if not config.get("user_password"):
        raise ValueError("Configuration file does not contain user_password.")
    if len(config.get("user_password").split(':')) != 2:
        raise ValueError("user_password must be in the format 'username:password'.")
    if not config.get('indexer_url'):
        raise ValueError("Configuration file does not contain indexer_url.")
    if not config.get('annotation_plans'):
        raise ValueError("Configuration file does not contain annotation_plans.")
    if not config.get('min_num_terms'):
        raise ValueError("Configuration file does not contain min_num_terms.")
    if not config.get('cogito_path'):
        raise ValueError("Configuration files does not contain cogito_path.")
    return config

def create_file_name(id, plan, cluster):
    FILE_NAME_TEMPLATE = "A{:08d}_{:<15}_{}.cogx"
    file_name = FILE_NAME_TEMPLATE.format(int(id), plan, cluster)
    file_name = file_name.replace(" ", "_")
    return file_name


def get_cogito_annotations(
        xml: bytes,
        indexer_url: str,
        annotation_plans: list,
        username: str,
        password: str,
        todays_path: str,
        id: str,
        min_num_terms: int,
        subject: str):

    for annotation in annotation_plans:
        endpoint = f"v1/annotation/annotateCogx/{annotation}"
        url = f"{indexer_url}/{endpoint}"
        headers = {'Content-type': 'application/xml'}
        auth = HTTPBasicAuth(username, password)
        try:
            response = requests.post(url, headers=headers, data=xml, auth=auth, verify=False)
        except requests.exceptions.RequestException:
            return [], "network error"
        if not response.ok:
            return [], "network error"
        response.raise_for_status()
        # Read xml content into an etree
        xml_data = ET.fromstring(response.content)
        # Save xml data to directory specified by cogito_path
        output_name = create_file_name(id, annotation, subject)
        # Save the XML file with the annotation name
        output_file = os.path.join(todays_path, output_name)
        with open(output_file, "wb") as f:
            f.write(response.content)

        # Get annotations from the XML data
        doc_node = xml_data.xpath("/cogito/doc")[0]
        terms = get_NALT_uri_from_mi_annotations(doc_node)
        if len(terms) >= min_num_terms:
            return terms, annotation
    return [], "no annotations"

def get_NALT_uri_from_mi_annotations(doc_node):
    """
    Get NALT URIs from the machine indexing doc node into a list.
    Args:
        doc_node (lxml.etree._Element): The <doc> node from a COGITO XML document.
    Returns:
        List of unique NALT URIs (could be int strings or labels). Returns empty list if none found.
    """
    # Find all annotation elements under knowledge/annotations/annotation
    annotation_nodes = doc_node.xpath("knowledge/annotations/annotation")
    uri_hash = {}

    for annotation_node in annotation_nodes:
        annotation_type = annotation_node.get("type")
        # Only pull NALT URIs
        if annotation_type in ["/Entity/NALTerm", "/Thesaurus/Concept"]:
            uri = annotation_node.get("name")
            # If 'name' doesn't look like an int (has non-digits), use the 'label' attribute
            if uri is not None and not uri.isdigit():
                uri = annotation_node.get("label")
            if uri:
                uri_hash[uri] = True

    return list(uri_hash.keys())

def annotate_citation(citation_object: Citation, subject_cluster: str = None):

    if subject_cluster is None or subject_cluster == "none" or \
            any(char.isdigit() for char in subject_cluster):
        subject_cluster = "NO_CLUSTER"

    if citation_object.local.USDA == 'yes':
        subject_cluster = "USDA"

    config = read_config()

    # Create cogx file from citation object
    cogito_path = config.get('cogito_path')
    if not os.path.exists(cogito_path):
        os.makedirs(cogito_path)
    todays_date = datetime.now().strftime("%Y-%m-%d")
    # Make a subdirectory with todays date
    todays_path = os.path.join(cogito_path, todays_date)
    if not os.path.exists(cogito_path):
        os.makedirs(cogito_path)
    if not os.path.exists(todays_path):
        os.makedirs(todays_path)

    # Create file name
    file_name = create_file_name(citation_object.local.identifiers.get("pid", "dummy"), "source", subject_cluster)
    output_file = os.path.join(todays_path, file_name)
    # Create cogx file in the output file location
    cit_to_cogx(citation_object, output_file)

    # Pass the cogx file to the cogito indexer and get a list of URIs back
    with open(output_file, "rb") as f:
        xml_content = f.read()
    uris, message = get_cogito_annotations(
        xml=xml_content,
        indexer_url=config.get('indexer_url'),
        annotation_plans=config.get('annotation_plans'),
        username=config.get('user_password').split(':')[0],
        password=config.get('user_password').split(':')[1],
        todays_path=todays_path,
        id=citation_object.local.identifiers.get("pid", "dummy"),
        min_num_terms=config.get('min_num_terms'),
        subject=subject_cluster
    )

    if message == "network error":
        return citation_object, "network error"

    if message == "no annotations":
        citation_object.local.indexed_by = "unable to annotate"
        if citation_object.local.USDA == 'no':
            return citation_object, "review"
        elif citation_object.local.USDA == 'yes':
            return citation_object, "successful, no annotations"

    if len(uris) > 0:
        citation_object.local.indexed_by = message

    valid_uris = validate_nalt_terms(uris)
    valid_topic_uris = valid_uris['topics']
    valid_geographic_uris = valid_uris['geographics']
    all_labels = [uri_to_term(uri) for uri in valid_topic_uris + valid_geographic_uris]

    # Update the NALT subject terms of the citation object
    if not "Subjects" in citation_object.subjects:
        citation_object.subjects["Subjects"] = {}
    nalt_subjects = []
    for uri in valid_topic_uris:
        nalt_subjects.append({"topic": {"term": uri_to_term(uri), "uri": uri}})
    for uri in valid_geographic_uris:
        nalt_subjects.append({"geographic": {"term": uri_to_term(uri), "uri": uri}})
    if len(nalt_subjects) > 0:
        citation_object.subjects["Subjects"]["NALT"] = nalt_subjects

    # Remove uncontrolled terms that match NALT terms
    if "uncontrolled" in citation_object.subjects["Subjects"].keys() and \
        len(citation_object.subjects["Subjects"]["uncontrolled"]) > 0:
        for term_dict in citation_object.subjects["Subjects"]["uncontrolled"]:
            term = term_dict["topic"]["term"] if "topic" in term_dict else term_dict["geographic"]["term"]
            if term in all_labels:
                citation_object.subjects["Subjects"]["uncontrolled"].remove(term_dict)

    # Return the citation object and message
    return citation_object, "successful"