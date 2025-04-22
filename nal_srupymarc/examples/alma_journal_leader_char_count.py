import requests
from lxml import etree

def process_25_record_leaders(start_record):
    list_leader_lengths = []
    url = "https://na91.alma.exlibrisgroup.com/view/sru/01NAL_INST"
    query_journal = 'alma.local_field_990="Journal repository"'
    maximum_records = 25
    sru_version = "1.2"

    params_journal = {
        "operation": "searchRetrieve",
        "version": sru_version,
        "query": query_journal,
        "startRecord": start_record,
        "maximumRecords": maximum_records,
    }

    journal_response = requests.get(url, params=params_journal)

    parsed_journal = etree.fromstring(journal_response.content)

    records = parsed_journal.findall('.//{http://www.loc.gov/zing/srw/}records/{http://www.loc.gov/zing/srw/}record')
    for record in records:
        leader = record.find(
            './/{http://www.loc.gov/zing/srw/}recordData/{http://www.loc.gov/MARC21/slim}record/{http://www.loc.gov/MARC21/slim}leader')
        leader_len = len(leader.text)
        list_leader_lengths.append(leader_len)

    return list_leader_lengths

array_leader_counts = []
start_indicies = [1, 26, 51, 76, 101, 126, 151, 176, 201, 226, 251, 276]
for i in start_indicies:
    array_leader_counts.extend(process_25_record_leaders(i))

print("Length: ", len(array_leader_counts))
print("Unique leader lengths: ", list(set(array_leader_counts)))
print("Number of leaders of length 24: ", array_leader_counts.count(24))
print("Number of leaders of length 23: ", array_leader_counts.count(23))


