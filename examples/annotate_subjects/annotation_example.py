from annotate_subject_terms import annotate_citation
import os
import pickle
from citation import Citation, Local, Resource, License, Author
import pprint

# Read in a citation pickle file
with open("annotation_pickles/usda_real_abstract.pkl", "rb") as f:
    citation_object: Citation = pickle.load(f)

# Get the annotations for the citation object
print("Example 1: Real USDA Abstract")
cit, msg = annotate_citation(citation_object)
pprint.pprint(cit.subjects)
print(msg)  # Successful, saves cogx files with subject cluster "USDA"
print(cit.local.indexed_by)
print("\n")

# Read in a citation pickle file
with open("annotation_pickles/non_usda_real_abstract.pkl", "rb") as f:
    citation_object: Citation = pickle.load(f)

# Get the annotations for the citation object
print("Example 2: Real Non-USDA Abstract")
cit, msg = annotate_citation(citation_object)
pprint.pprint(cit.subjects)
print(msg)  # Successful, saves cogx files with subject cluster "NO_CLUSTER"
print(cit.local.indexed_by)
print("\n")

# Read in a citation pickle file
with open("annotation_pickles/non_usda_fake_abstract.pkl", "rb") as f:
    citation_object: Citation = pickle.load(f)

# Get the annotations for the citation object
print("Example 3: Fake Non-USDA Abstract")
cit, msg = annotate_citation(citation_object)
pprint.pprint(cit.subjects)
print(msg)  # Sends to review, saves cogx files with subject cluster "NO_CLUSTER"
print(cit.local.indexed_by)
print("\n")

# Read in a citation pickle file
with open("annotation_pickles/usda_fake_abstract.pkl", "rb") as f:
    citation_object: Citation = pickle.load(f)

# Get the annotations for the citation object
print("Example 4: Fake USDA Abstract")
cit, msg = annotate_citation(citation_object)
pprint.pprint(cit.subjects)
print(cit.local.indexed_by)
print(msg)  # Successful, no subject terms added, saves cogx files with subject cluster "USDA"

# Read in a citation pickle file
with open("annotation_pickles/usda_with_geographics.pkl", "rb") as f:
    citation_object: Citation = pickle.load(f)

# Get the annotations for the citation object
print("Example 5: USDA with geographic terms")
cit, msg = annotate_citation(citation_object)
pprint.pprint(cit.subjects) # Includes geographic terms
print(msg)  # Successful, saves cogx files with subject cluster "USDA"
print(cit.local.indexed_by)
print("\n")
