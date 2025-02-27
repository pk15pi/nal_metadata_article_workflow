# To run this script, first install metadata_routines from the wheels included in the dist/ directory
# as described in the readme.

from mapper.map_submission_to_crossref import transform_from_submit_api_to_crossref

with open("example_data/submit_site_source.json", "r") as f:
    data_str = f.read()

result = transform_from_submit_api_to_crossref(data_str)
print("Title: ", result["title"])
print("DOI: ", result["DOI"])
print("Number of authors: ", len(result["author"]))
print("First author ORCID: ", result["author"][0]["ORCID"])
print("First author given name: ", result["author"][0]["given"])
print("First author family name: ", result["author"][0]["family"])
print("First author affiliation name: ", result["author"][0]["affiliation"][0]["name"])