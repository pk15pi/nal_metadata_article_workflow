from metadata_quality_review import metadata_quality_review
import pickle

# Read in a citation object from a pickle
with open('example_data/pickle_1000.pkl', 'rb') as f:
    cit = pickle.load(f)

# Show that the article is missing the manuscript file
cit, msg = metadata_quality_review(cit)
print("Notes: ", cit.local.cataloger_notes)
print("Status: ", msg)

# Say we override the manuscript file check.
# First, remove the existing cataloguer notes so we don't have duplicates.
cit.local.cataloger_notes = []
cit, msg = metadata_quality_review(cit, "manuscript")
print("Notes: ", cit.local.cataloger_notes)
print("Status: ", msg)
