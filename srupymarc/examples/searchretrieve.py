import srupymarc

records = srupymarc.searchretrieve(
    "https://suche.staatsarchiv.djiktzh.ch/SRU/", query="Zurich", output_format="flatten"
)
print("SRU version:", records.sru_version)
print("Count:", records.count)
print("")

for record in records:
    # print fields from schema
    print(record["reference"])
    print(record["title"])
    print(record["date"])
    print(record["extra"]["link"])  # extra record data is available at the 'extra' key
    print("")

record = records[0]
#print(record)
