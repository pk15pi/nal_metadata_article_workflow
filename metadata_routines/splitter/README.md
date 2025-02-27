# splitter(document_string: str) -> tuple[list[str], str]:

This module supports the splitting of metadata collection documents into single record documents preserving the 
metadata original schema or DTD.

Supports both XML and JSON article citation collection documents as strings.

## Table of Contents

* [Installation](#installation)
* [Usage](#usage)
* [Schemas](#schemas)


## Installation

The package installs directly from a wheel package.

```commandline
pip install /app/nal_metadata_article_workflow/dist/metadata_routines-0.0.0-py3-none-any.whl
```

## Usage

```python
from metadata_routines.splitter import splitter

my_str = """
[
   {  "submission_node_id":345,
      "title":"A New Method to Calculate Cotton Fiber Length"
   },
   {  "submission_node_id":346,
      "title":"Characterization of the seed virome of alfalfa"
   }
]   
"""

( list_of_records, status ) = splitter(my_str) 

```

## Schemas

Supported formats and schemas

| Source          | format | schemas    | Notes                                                                |
|-----------------|--------|------------|----------------------------------------------------------------------|
| CrossRef API    | JSON   | Crossref   | [CrossRef JSON](https://github.com/CrossRef/rest-api-doc/blob/master/api_format.md) |
| Submit site API | JSON   | custom     | [Submit site API](https://github.com/USDA-REE-ARS/nal-library-systems-support/wiki/Submission-Export-API) |
| JATS            | XML    | JATS 3.0   | [Tags](https://dtd.nlm.nih.gov/archiving/tag-library/3.0/index.html) |
| PubMed          | XML    | PubMed 2.8 | [PubMed XML](https://www.ncbi.nlm.nih.gov/books/NBK3828/#publisherhelp.PubMed_XML_Tagged_Format) |
| Elsevier ConSyn | XML    | Elesvier   | [ConSyn Schemas](https://supportcontent.elsevier.com/Support%20Hub/DaaS/36178_ConSyn_Schemas_Document.pdf) |

