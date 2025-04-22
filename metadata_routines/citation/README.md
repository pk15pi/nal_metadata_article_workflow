# Citation Object

## General description

- The Citation object is the main data object in the Article Citation workflow. 
It is the working expression of the article citation metadata record. 
- The structure of the Citation object's [Python dataclass](https://realpython.com/python-data-classes/) is based on the Crossref schema.
- For an interactive list of crossref elements see the Crossref's Swagger UI at: 
https://api.crossref.org/swagger-ui/index.html


## Installation

The Citation object is installed as part of the `metadata_routines` package, which is installed directly from a wheel package.

```
pip install /app/nal_metadata_article_workflow/metadata_routines/dist/metadata_routines-0.0.0-py3-none-any.whl
```

## Usage 

_Note: The functions in the mapper module instantiate Citation objects for us, 
so end users will not need to create Citation objects directly._

To use the `Citation` object, follow these steps:

1. **Import the necessary classes**:
   Ensure you have imported the `Citation` class and the relevant subfield classes from the `citation` module.

   ```python
   from citation import Citation, Author, License, Funder, Local, Resource
   ```

2. **Create a new `Citation` object**:
   Instantiate a `Citation` object and populate its fields with the relevant data.

   ```python
   new_citation = Citation(
       DOI="10.1000/xyz123",
       title="Sample Title",
       original_title="Original Sample Title",
       subtitle="Sample Subtitle",
       publisher="Sample Publisher"
       container_title="Sample Journal Name",
       abstract="This is a sample abstract.",
       volume="1",
       issue="1",
       issn={"e-issn": "1234-5678", "p-issn": "8765-4321"},
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
   Create `Author` objects and append them to the `author` field of the `Citation` object. When
adding an author, simply set `cit.author` to the author object you would like to amend. This will
add the author to the list of authors stored in the citation object.

   ```python
   author1 = Author(
       given="John",
       family="Doe",
       orcid="0000-0001-2345-6789",
       affiliation="Sample University",
       sequence="first"
   )
   new_citation.author = author1
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
   
7. **Add date information**:
   Various input schemas contain various date elements. The `date` attribute of the Citation
object is a nested dictionary. Each high-level key is the name of the date (ie 'published',
'created', 'changed', etc). Each of these keys points to a dictionary containing the keys 
'year', 'month', 'day', and 'string'.

```python
date={
    "published": {
        "year": "2016",
        "month": "03",
        "day": "14",
        "string": "2016-03-14"
    }
},
```

8. **Add local information**:
   Create a `Local` object and assign it to the `local` field of the `Citation` object.
   This field can contain additional information that is not part of the CrossRef schema.

   ```python
   local_info = Local(
       identifiers={
            "provider_rec": "10.1000/xyz123",
            "mms_id": "1234567890",
    },
       usda="no"
   )
   new_citation.local = local_info
   ```
   
9. **Add subject terms**:


The `subjects` dictionary contains structured subject terms associated with the citation.
See the `flexible_subelement_structure.md` document for more information.


10. **Add resources**:

The `resource` attribute contains an object of type `Resource`, which is designed to
support manuscript and supplemental files. See the `flexible_subelement_structure.md`
document for more information.

11. **Access and manipulate the `Citation` object**:
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

### Date

Unlike in the CrossRef schema, we implement one top-level `date` dict, which contains all dict elements.
The structure of each individual date dict also differs from the CrossRef schema's date dicts in that the
CrossRef schema's date dicts include a `date_parts` list, which is a list of integers in the form `[year, month, day]`.
The Citation object's date dicts specifically point to `day`, `month`, and `year` independently.

### Local elements for manuscript and supplementary files

Both manuscripts file and supplementary files with be stored in the `Resource` subelement.

### Local identifier element

Identifiers not included in the Crossref schema, are stored in the Citation's local identifiers dictionary, 
with the type of identifier as the key.

