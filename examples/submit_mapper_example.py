from mapper import mapper
import json
from citation import *
import html

with open('example_data/submission_345.json', 'r') as f:
    submission_data = f.read()

cit, msg = mapper(submission_data, "submit_json")

# print submitter email and name
print(cit.local.submitter_email)
print(cit.local.submitter_name)
