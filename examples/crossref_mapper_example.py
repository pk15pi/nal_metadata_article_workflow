from mapper import mapper
import json
from citation import *

with open('example_data/faulty_record.json', 'r') as f:
    submission_data = f.read()

cit, msg = mapper(submission_data, "crossref_json")

print("Message: ", msg)
print("Object:", cit)