### Overview

This document describes the intended structure of the subelements of the 
`Citation` object that are flexible and not self-documenting. The `Subjects`
and `Resource` subelements are examples of this. These subelements of the `Citation`
object are implemented using flexible dictionaries in order to accommodate divserse
input schemas. These subelements are populated from each supported schema into
the `Citation` object via the `mapper` module. Users will not need to construct
`Resource` or `Subjects` objects manually. This documentation exists to support
future developers and library staff who interact with the `Citation` object.

### Subjects
This field is intended to include a list of subjects that are associated with the
citation. The `Subjects` object is implemented as a dict. The `Subjects` object
has the following structure:

```python
subjects = {
  "Subjects": {
    "Authority_name": [ # Authority name, e.g. NALT, MeSH, Uncontrolled, etc.
      {   
        "heading_type": {  # heading type, e.g. topic, geographic, etc.
          "term": "preferred_heading", # preferred heading term
          "uri": "headings_URI", # URI for the preferred heading (optional)
          "qualifier": "qualifier term" # Mesh heading qualifier (optional)
        }
      }  
    ]
  }
}
```

Example:

```python
citation.subjects = {
  "Subjects": {
    "NALT": [
      {
        "topic":{
          "term": "anchovies",
          "uri": "https://lod.nal.usda.gov/nalt/8615"
        },
      },
      {
        "topic":{
          "term": "protein requirement",
          "uri": "https://lod.nal.usda.gov/nalt/7762"
        },
      },
      {
        "geographic":{
          "term": "Maine",
          "uri": "https://lod.nal.usda.gov/nalt/51213"
        }
      }
],
    "MeSH": [
      {
        "topic":{
          "term": "Fish Proteins",
          "uri": "https://www.ncbi.nlm.nih.gov/mesh/68029941"
        }
      },
    ],
    "Uncontrolled": [
      {
        "topic":{
          "term": "fish"
        }
      },
      {
         "topic":{
            "term": "protein"
        }
      }
    ]
  }
}
```

### Resource
This field is intended to include files and descriptions of files that are
associated with the citation. The `Resource` object has attributes: `primary` and
`secondary`. The `primary` attribute is a dictionary with keys `'URL'`, `'title'` 
and `'label'`. The `secondary` attribute is a list of dictionaries, each with 
keys `'URL'`, `title`, and `'label'`. The `secondary` attribute is intended to 
include supporting files such as data sets, images, and other files that are not the 
primary manuscript file. The `'title'` and `'label'` elements are optional in both 
the `primary` dict and the `secondary` list of dicts.  Here is an example of 
the `Resource.primary` dictionary:

```python
citation.resource.primary = {
  "URL": "https://www.ars.usda.gov/ARSUserFiles/np/2024/2024-01-01_main.pdf",
  "label": "Accepted Manuscript"
}
```

Here is an example of a `Resource.secondary` list:
```python
citation.resource.secondary = [
      {
        "URL": "https://www.ars.usda.gov/ARSUserFiles/np/2024/2024-01-01_sup001.pdf",
        "label": "Accepted Manuscript Supporting document",
        "title": "Supporting document 1"
      },
      {
         "URL": "file:///data/digital_content/2024/2024-01-01_sup002.pdf",
         "label": "Accepted Manuscript Supporting document",
         "title": "Supporting document 2"
      }
]
```