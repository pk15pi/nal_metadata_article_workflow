from metadata_quality_review import metadata_quality_review
import pickle

# Read in a citation object from a pickle
# This citation objects comes from a crossref article
with open('example_data/pickle_2500.pkl', 'rb') as f:
    cit = pickle.load(f)

# For crossref articles, we always override issue, volume and page
# This record is missing the issue and page, and has a doi that does not match
# the current doi regex. We have an open issue to update the doi regex.
cit, msg = metadata_quality_review(cit, "issue, volume, page")
print("Notes: ", cit.local.cataloger_notes)
print("Status: ", msg)

# Say we also override the invalid doi check.
# First, remove the existing cataloguer notes, so we don't have duplicates.
cit.local.cataloger_notes = []
cit, msg = metadata_quality_review(cit, "doi, issue, volume, page")
print("Notes: ", cit.local.cataloger_notes)
print("Status: ", msg)
