from mapper import mapper
import pickle
import os

# Iterate through the files in data/jats
for filename in os.listdir('data/jats/taylor'):
    if filename.endswith('.xml'):
        # Read the JATS XML file
        with open(f'data/jats/taylor/{filename}', 'r') as f:
            jats_str = f.read()

        citation, message = mapper(jats_str, "jats_xml")
        print(message)

        # Save the citation object to a file
        with open(f'data/jats/taylor/{filename.replace(".xml", ".pkl")}', 'wb') as f:
            pickle.dump(citation, f)

# Iterate through the files in data/jats
for filename in os.listdir('data/jats/bioone'):
    if filename.endswith('.xml'):
        # Read the JATS XML file
        with open(f'data/jats/bioone/{filename}', 'r') as f:
            jats_str = f.read()

        citation, message = mapper(jats_str, "jats_xml")
        print(message)

        # Save the citation object to a file
        with open(f'data/jats/bioone/{filename.replace(".xml", ".pkl")}', 'wb') as f:
            pickle.dump(citation, f)