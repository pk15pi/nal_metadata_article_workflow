import pymarc
from srupymarc import xmlparse
import io
import requests

url = "https://na91.alma.exlibrisgroup.com/view/sru/01NAL_INST"
query_journal = 'alma.local_field_990="Journal repository"'
query_article = "alma.issn=1365-6937"
maximum_records = 1
sru_version = "1.2"
start_record = 8
# Errors on records: 4, 5,

params_journal = {
    "operation": "searchRetrieve",
    "version": sru_version,
    "query": query_journal,
    "startRecord": start_record,
    "maximumRecords": maximum_records,
}

journal_response = requests.get(url, params=params_journal)

parser = xmlparse.XMLParser()

parsed_journal = parser.parse(journal_response.content)

def _extract_records_pymarc(xml):
    new_records = []
    xml_recs = parser.findall(xml, "./sru:records/sru:record")
    for xml_rec in xml_recs:
        marcxmlFile = io.BytesIO(parser.tostring(xml_rec))
        pymarc_record = pymarc.marcxml.parse_xml_to_array(marcxmlFile)[0]
        new_records.append(pymarc_record)
    return new_records

journal_records = _extract_records_pymarc(parsed_journal)



