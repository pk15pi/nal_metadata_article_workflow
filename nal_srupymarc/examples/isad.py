import srupymarc
from pprint import pprint

# check supported schemas of server
server_url = "https://suche.staatsarchiv.djiktzh.ch/SRU/"
schema = "isad"
server = srupymarc.explain(server_url)


print(20 * "=")
print("=")
print(f"= Record with schema: {schema}")
print("=")
print(20 * "=")
records = srupymarc.searchretrieve(server_url, query="Zurich", record_schema=schema, output_format="flatten")
pprint(records[0])
