from mapper import mapper

# This example contains a title that cannot be converted to utf-8.
# Mapping fails
with open('data/submission_4547.json', 'r') as f:
    submission_data = f.read()

cit, msg = mapper(submission_data, "submit_json")
print(msg)
print("Cit: ", cit)
