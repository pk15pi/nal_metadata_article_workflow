from mapper import mapper

with open('example_data/crossref_2600.json', 'r') as f:
    crossref_data = f.read()

cit, msg = mapper(crossref_data, "crossref_json")

print("Message: ", msg)
print("Citation: ", cit)
