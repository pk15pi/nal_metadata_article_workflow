from citation import Citation, Author, Funder, License, Local, Resource
import json

'''
This provides an example of how to construct a Citation object.
The creation of Citation objects is implemented by the mapper module.
'''

with open('data/submission_2500.json', 'r') as f:
    submission_data = json.load(f)

cit = Citation(
    title=submission_data['title'],
    DOI=submission_data['doi'],
    container_title=submission_data["journal"],
    ISSN=submission_data['issn'],
    abstract=submission_data['abstract'],
    type="article",
    volume=str(submission_data["volume"]),
    issue=submission_data["issue"],
)

cit.page_first_last = (
    submission_data["first_page"],
    submission_data["last_page"]
)
print("Page info: \n ", cit.page, "\n")

# Create Author objects, add to list
for auth in submission_data["authors"]:
    new_author = Author(
        given=auth["first_name"],
        family=auth["last_name"],
        orcid=auth["orcid"],
        affiliation=[auth["affiliation"]],
    )
    cit.author = new_author
print("Author info: \n", cit.author, "\n")

# Create Funder objects, add to list
for funder in submission_data["funding_agencies"]:
    new_funder = Funder(
        name=funder["name"],
        award=[funder["award_number"]]
    )
    cit.funder.append(new_funder)

print("Funder info: \n", cit.funder, "\n")

new_license = License(
    content_version=submission_data["manuscript_version"]
)
cit.license = [new_license]
print(cit.license)

new_local = Local(
    identifiers={
        "standard_number_aris": str(submission_data["log_number"]),
        "submission_node_id": str(submission_data["submission_node_id"]),
        "accession_number": submission_data["accession_number"],
        "provider_rec": str(submission_data["submission_node_id"])
    }
)
cit.local = new_local

new_resource = Resource(
    primary={
        "URL": submission_data["manuscript_file"],
        "label": "Accepted Manuscript"
    },
    secondary=[]

)
print("Citation object: \n ", cit)
