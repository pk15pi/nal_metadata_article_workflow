from metadata_quality_review import metadata_quality_review
import pickle

# Read in a citation object from a pickle
# This citation objects comes from a crossref article
with open('data/pickle_2500.pkl', 'rb') as f:
    cit = pickle.load(f)

# For crossref articles, we always override issue, volume and page
# Here's what happens when we don't override them. They get sent to review.
cit, msg = metadata_quality_review(cit)
print("Notes: ", cit.local.cataloger_notes)
print("Status: ", msg)

# Now we apply the necessary overrides so they don't get sent to review.
# First, remove the existing cataloguer notes, so we don't have duplicates.
cit.local.cataloger_notes = []
cit, msg = metadata_quality_review(cit, "issue, volume, page")
print("Notes: ", cit.local.cataloger_notes)
print("Status: ", msg)
