# Citation Object

## General description

- The Citation object is main data object in the Article Citation workflow.
- It is the working expression of the article citation metadata record. 
- The structure of Citation object's [Python dataclass](https://realpython.com/python-data-classes/) will be based on the Crossref schema.
- For an interactive list of Citation elements see the in Crossref's Swagger UI at: https://api.crossref.org/swagger-ui/index.html


## Installation

The Citation object install as part of the metadata_routines package, which is installed directly from a wheel package.

```
pip install /app/nal_metadata_article_workflow/dist/metadata_routines-0.0.0-py3-none-any.whl
```

## Usage 

_Note: The functions in the mapper module instantiate Citation objects for us, 
so end users will not need to create Citation objects directly._

To use the `Citation` object, follow these steps:

1. **Import the necessary classes**:
   Ensure you have imported the `Citation` class and the relevant subfield classes from the `citation` module.

   ```python
   from citation import *
   ```

2. **Create a new `Citation` object**:
   Instantiate a `Citation` object and populate its fields with the relevant data.

   ```python
   new_citation = Citation(
       DOI="10.1000/xyz123",
       title="Sample Title",
       original_title="Original Sample Title",
       subtitle="Sample Subtitle",
       container_title="Sample Journal Name",
       abstract="This is a sample abstract.",
       volume="1",
       issue="1",
   )
   ```
   

3. **Add Page Number Information**

   To add page number information to a `Citation` object, you can either specify the first and last page numbers or provide a page string.

   **Setting Page Information by First and Last Page**

   To set the page information by specifying the first and last page numbers, use the `page_first_last` setter function. The `page_string` field will be automatically generated.

   ```python
   # Set the first and last page numbers
   new_citation.page_first_last = ("1a", "4a")

   # Access the page information
   print(new_citation.page)
   # Output: {'first_page': '1a', 'last_page': '4a', 'page_str': '1a - 4a'}
   ```

   **Setting Page Information by Page String**

   To set the page information by providing a page string, use the `page_str` setter function:

   ```python
   # Set the page string
   new_citation.page_str = "1a - 4a"

   # Access the page information
   print(new_citation.page)
   # Output: {'first_page': None, 'last_page': None, 'page_str': '1a - 4a'}
   ```

   These methods allow you to flexibly add page number information to the `Citation` object.

4. **Add authors**:
   Create `Author` objects and append them to the `author` field of the `Citation` object.

   ```python
   author1 = Author(
       given="John",
       family="Doe",
       orcid="0000-0001-2345-6789",
       affiliation="Sample University",
       sequence="first"
   )
   new_citation.author.append(author1)
   ```

5. **Add licenses**:
   Create `License` objects and append them to the `license` field of the `Citation` object.

   ```python
   license1 = License(
       version="1.0",
       url="http://example.com/license"
   )
   new_citation.license.append(license1)
   ```

6. **Add funders**:
   Create `Funder` objects and append them to the `funder` field of the `Citation` object.

   ```python
   funder1 = Funder(
       name="National Science Foundation",
       award=["NSF-123456"]
   )
   new_citation.funder.append(funder1)
   ```

7. **Add local information**:
   Create a `Local` object and assign it to the `local` field of the `Citation` object.
   This field can contain additional information that is not part of the CrossRef schema.

   ```python
   local_info = Local(
       identifiers={"provider_rec": "10.1000/xyz123"},
       files=[
           {
               "label": "manuscript",
               "location": "https://example.com/manuscript.pdf",
               "version": "pre-publication",
               "mime_type": "text/pdf"
           }
       ]
   )
   new_citation.local = local_info
   ```

8. **Access and manipulate the `Citation` object**:
   You can now access and manipulate the `Citation` object as needed.

   ```python
   print(new_citation.title)
   new_citation.title = "Updated Sample Title"
   ```

## Deviations from the Crossref schema

### title, original_title, and subtitle elements

In the Citation object, the title, original_title, and subtitle elements will be stored as a single string, 
not a list of strings. If an article record contains more than one element in its list of titles, subtitles, or original_titles, then these elements will be concatenated into one string, separated by a single space.

### ISSN elements

Instead of storing ISSN as a simple list as in the Crossref schema, the Citation will use a dictionary to track the 
types of ISSN found in a citation.

```python
ISSN = {
    'issn': '0022-538X',
    'p-issn': '0022-538X',
    'e-issn': '1098-5514'
}
```

### Page element

Crossref uses a simple string containing both the first and last page number. It also allows for non-consecutive pages.

The Citation object uses a dictionary structure for page number information. 
If a string is received for page number, we will not parse the string and only store it as text. 
If the first and last pages are received, we will construct the page_string field.

```python
page = {
   "first_page": "1a",
   "last_page": "4a",
   "page_string": "1a - 4a"
}
```

### Local elements for manuscript and supplementary files

Both manuscripts file and supplementary files with be stored in a list called `files` within `local`. The `files` list will contain one dictionary per file, and will list the file label (ie manuscript, dataset, etc), location, mime type, and if applicable, the version.

```python

local = {
    "files":[
         {
              "label": "manuscript",
              "location": 	"https://submit.nal.usda.gov/sites/default/files/manuscripts/Schumacher.pdf",
              "version": "pre-publication",
              "mime_type": "text/pdf"
         },
         {
              "label": "supplement part A",
              "location": "file://data/file_storage/a0405563a.pdf",
              "version": "publisher"     
         },
         {
              "label": "supplement part B",
              "location": "file://data/file_storage/a0405563b.pdf",
              "version": "publisher"     
         },        
    ]
}
```

### Local identifier element

Identifiers not included in the Crossref schema, are stored in the Citation's local identifiers dictionary, 
with the type of identifier as the key.

