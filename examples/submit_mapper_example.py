from mapper import mapper

with open('example_data/submission_2015.json', 'r') as f:
    submission_data = f.read()

cit, msg = mapper(submission_data, "submit_json")

print(msg)

print(cit.resource)
