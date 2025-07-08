from mapper import mapper
import pickle
import os

# Iterate through the files in data/springer
for filename in os.listdir('data/springer'):
    if filename.endswith('.xml'):
        # Read the PubMed XML file
        with open(os.path.join('data/springer', filename), 'r') as f:
            pubmed_str = f.read()

        citation, message = mapper(pubmed_str, "pubmed_xml")
        print(message)

        # Save the citation object to a file
        with open(os.path.join('data/springer', filename.replace('.xml', '.pkl')), 'wb') as f:
            pickle.dump(citation, f)