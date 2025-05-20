# `citation_to_marc` Module

The `citation_to_marc` module is designed to map citation objects into marc MARC (Machine-Readable Cataloging) format. This module supports marcxml, json, and marc21 formats, allowing for the conversion of citation metadata into a standardized format used in libraries and information systems.

The main function in this module, `citation_to_marc`, takes in a citation object, a file format code (either `"xml"`, `"json"`, or `"marc"`), and an output file path. It converts the citation object into the specified MARC format and saves it to the provided file path. This function returns a message indicating the success or failure of the operation. If the conversion fails, the message describes the error encountered.

## Installation

Ensure that the required dependencies are installed in your Python environment. You can install them using `pip`:

First build and activate your virtual environment if you haven't already:
```bash
python -m venv venv
source venv/bin/activate
```

Then, install the required packages:
```
pip install -r requirements.txt
```

## Usage

### Example: Converting a Citation Object to MARCXML

Below is an example of how to use the `citation_to_marc` subpackage to convert a citation object into a MARCXML record:

```python
from citation_to_marc import citation_to_marc
import pickle

# Load a citation object from a pickle file
with open('example_data/cit1.pkl', 'rb') as f:
    cit1 = pickle.load(f)

# Convert the citation object to MARCXML and save it to a file
output_path = "example_data/marc_record1.xml"
format = "xml"
msg = citation_to_marc(cit1, format, output_path)

# Print the result message
print(msg)
```