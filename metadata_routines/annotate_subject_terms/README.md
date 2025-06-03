# Annotate Subject Terms

The `annotate_subject_terms` module provides tools for working with NALT 
(National Agricultural Library Thesaurus) terms. This includes populating a 
sqlite database with NALT data and validating terms against the database.

## Prerequisites

Before using this module, ensure the following:
1. You have a configuration file that includes all the variables defined in the sample 
configuration file, `cogito_config.toml`. This includes the following variables:
- `source_file`: The path to the source file of the NALT thesaurus, used by `populate_nalt_db.py`.
- `database_file`: The path to the SQLite database file, used by both `populate_nalt_db.py` and 
`nalt_lookup.py`. Note that if this file does not yet exist, `populate_nalt_db.py` will create it.
If it does exist, `populate_nalt_db.py` will overwrite it.
- `user_password`: The username and password for connecting to cogito, separated by a full colon.
- `annotation_plans`: A list of the annotation plans used by cogito.
- `indexer_url`: The URL for connecting to cogito.
- `min_num_terms`: The minimum number of terms required for a valid annotation.
- `cogito_path`: The path to the base directory where COGX files should be saved.
2. The `COGITO_CONFIG` environment variable is set to the path of the configuration 
file.
   ```bash
   export COGITO_CONFIG=/path/to/cogito_config.toml
   ```
   
To make this environment variable permanent, save the export command in your .bashrc file:
```bash
echo 'export NALT_DB=/path/to/cogito_config.toml' >> ~/.bashrc
```
Then, run the following command to apply the changes:
```bash
source ~/.bashrc
```
2. The required Python dependencies are installed. It is recommended to use a virtual
environment, and to create one if you do not yet have one.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
   You can install the required dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

---

## The `populate_nalt_db.py` script

The `populate_nalt_db.py` script is used to populate the SQLite database with 
NALT data from a source thesaurus file.

### Usage

Run the script from the command line:

```bash
python populate_nalt_db.py
```

This will populate the database file specified by the `database_file` variable in the configuration file
with the data from `source_file`.

---

## The `nalt_lookup` module

The `nalt_lookup` module provides a function to validate NALT terms against the 
database and retrieve related information. The `validate_nalt_terms` function
takes a list of NALT URIs and returns a dictionary containing invalid uris, broader
uris that were filtered out, valid topic uris, and valid geographic uris.

### Example Usage

In this example, we use the following uris:
- `00000`, an invlaid URI
- `106155`, the URI for Ashley National Forest (geographic)
- `105883`, a broader URI for Ashley National Forest
- `25222101`, the URI for 'rat tickling' (topic)
- `9054` and `332`, two broader URIs for 'rat tickling'

```python
from annotate_subject_terms import validate_nalt_terms

# Validate a list of NALT URIs
result = validate_nalt_terms(["00000", "106155", "105883", "25222101", "9054", "332"])

# Output the result
print(result)
```
This will output a dictionary with the following structure:

```python
{
    "invalid_uris": ["00000"],
    "broader_uris": ["105883", "9054", "332"],
    "topics": ["25222101"],
    "geographics": ["106155"]
}
```

## The `text_cleanup` Module

The `text_cleanup` module provides functions for standardizing and cleaning text data. Import the functions as follows:

```python
from annotate_subject_terms import (
    remove_periods,
    replace_metacharacters, 
    normalize_hyphens,
    remove_copyright_statement
)
```

### Functions

### `remove_periods(text)`
Removes and standardizes periods in text, including special handling for:
- USDA/US abbreviations
- Taxonomic notation (subsp., var., etc.)
- Multiple spaces

```python
>>> remove_periods("U.S.D.A. subsp. name")
"USDA subsp name"
```

### `replace_metacharacters(text)`
Replaces angle brackets with guillemets:
- `<` becomes `«`
- `>` becomes `»`

```python
>>> replace_metacharacters("text <here>")
"text «here»"
```

### `normalize_hyphens(text)`
Standardizes various Unicode hyphens, minuses and dashes to the ASCII hyphen-minus character (`-`):
- Converts Unicode hyphens (soft, non-breaking, etc.)
- Converts Unicode minus signs
- Converts Unicode dashes (em dash, en dash, etc.)

```python
>>> normalize_hyphens("text—with—dashes")  # using em dashes
"text-with-dashes"
```

### `remove_copyright_statement(text)`
Removes copyright statements and related text:
- Copyright symbols and "(c)" notices
- Publisher statements
- Rights reservations

```python
>>> remove_copyright_statement("Text © 2024 All rights reserved")
"Text"
```

## The `cogito_indexer` Module

The `cogito_indexer.py` module provides functionality for annotating citation objects with NALT terms using the Cogito 
indexer. It interacts with the Cogito API to generate annotations, updates the citation object with valid NALT terms,
and filters out any uncontrolled subject terms in the citation object that match NALT terms. This module applies the 
text_cleanup module to clean up text before it is sent to Cogito for annotation, and it validates the uris that Cogito 
returns against the NALT database created by the `populate_nalt_db.py` script.

### Example Usage

To use the `cogito_indexer` module, follow these steps:

1. Ensure you have a valid configuration file (`cogito_config.toml`) as described in the prerequisites section. 
   This file should include all necessary variables such as `source_file`, `database_file`, `user_password`, 
   `annotation_plans`, `indexer_url`, `min_num_terms`, and `cogito_path`. See the sample configuration file for an example.

2. Ensure the `COGITO_CONFIG` environment variable is set to the path of the configuration file:
   ```bash
   export COGITO_CONFIG=/path/to/cogito_config.toml
   ```

3. Use the `annotate_citation()` function to annotate a citation object:

### Example Code

```python
from annotate_subject_terms import annotate_citation
import pickle
import pprint

# Load a citation object from a pickle file
with open("path/to/citation_pickle.pkl", "rb") as f:
    citation_object = pickle.load(f)

# Annotate the citation object
annotated_citation, message = annotate_citation(citation_object, subject_cluster="sample_subject")

# Print the updated subjects and the status message
pprint.pprint(annotated_citation.subjects)
print(message)
```

If the `annotate_citation()` function encounters a network error when trying to connect to the Cogito API, it will return 
a message of `"network error"` and the original citation object. If the annotation is successful, it will return a message 
of "successful" and the updated citation object with the annotated subjects. If there are insufficient terms returned by
Cogito for all of the annotation plans specified, it will return a message of 'review'.

The `annotate_citation()` function will save intermediary cogx files in the directory specified by the `cogito_path` 
variable in the configuration file. It will save files to a subdirectory named after the current date.

The subject cluster passed to the annotate_citation() function is used to name the intermediary cogx files that are
saved to the database. If the subject cluster is not specified, it defaults to "NO_CLUSTER". If the subject cluster 
contains digits, it is assumed to be faulty and replaced with "NO_CLUSTER". If the article is USDA funded or authored,
then the subject cluster is set to "USDA".

## Notes

- The NALT SKOS file can be downloaded from the bottom of this webpage: https://lod.nal.usda.gov/nalt/en/