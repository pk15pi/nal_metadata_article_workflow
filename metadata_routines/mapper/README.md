# mapper(source_string: str, source_schema: str) -> tuple[object, str]:

This module supports the mapping of single metadata records from thier metadata original schema or DTD into the Citation Object.

Supports both XML and JSON article citation collection documents as strings.

## Table of Contents

* [Installation](#installation)
* [Usage](#usage)

## Installation

The package installs directly from a wheel package.

```commandline
pip install /app/nal_metadata_article_workflow/dist/metadata_routines-0.0.0-py3-none-any.whl
```

## Usage

```python
from metadata_routines.splitter import mapper

crossref_string = '''
     {
        "indexed": {
            "title": [
                "Distribution of Apple stem grooving virus in apple trees in the Czech Republic"
            ],
            "DOI": "10.17221/8360-pps"
        }
    }
    '''
citation_object, my_message = mapper(crossref_string, 'crossref_api_json')

```
