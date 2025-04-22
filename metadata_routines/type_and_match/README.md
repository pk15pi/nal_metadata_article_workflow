## Type and Match

The `type_and_match` module is responsible for determining the type of a citation object based on its title, and matching it against existing records. This module connects to the PubAg SOLR index and Alma to find records with matching DOIs or MMSIDs.

### Usage

To use the `type_and_match` module, import the `ArticleTyperMatcher` class and create an instance of it. You can then pass a `Citation` object to the `ArticleTyperMatcher.type_and_match()` method. This method returns a tuple of the form `(Citation, message)` where the `Citation` object has updated `type` and `mmsid` fields, and the `message` string describes whether to stop processing the record, merge the record with an existing record, create a new record, or to pass the record to library staff for review.

#### Note: The `type_and_match` function in this module requires the `SOLR_SERVER` environment variable to be set to the PubAg SOLR server URL.

```python
from type_and_match.type_and_match import ArticleTyperMatcher
from citation import Citation, Local

# Create a Citation object
# In the actual implementation, you would unpickle a Citation object from the previous step
citation = Citation()
citation.title = "A new perspective on microbial landscapes within food production"
citation.DOI = "10.1016/j.copbio.2015.12.008"
citation.local = Local()
citation.local.identifiers["mmsid"] = "9915695874407426"

# Initialize ArticleTyperMatcher
ATM = ArticleTyperMatcher()

# Call the type_and_match method
result = ATM.type_and_match(citation)
print(result)
```

### Methods

#### `type_and_match(citation)`

This method takes a `Citation` object as input and returns a tuple of the form `(Citation, message)` containing the citation and a string indicating the match type. The match type can be one of the following:
- `"dropped"`: The citation was dropped based on the identified type of the record.
- `"merge"`: The citation matches an existing record and should be merged.
- `"new"`: The citation does not match any existing records and should be treated as new.
- `"review"`: The citation requires further review.