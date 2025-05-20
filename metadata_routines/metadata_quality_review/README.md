# metadata_quality_review

The `metadata_quality_review` package provides functions to review and validate the quality of metadata in citation records. It includes checks for various fields such as volume, issue, page, title, author, primary author, issue date, and abstract. The package ensures that the metadata meets certain quality standards and provides feedback through cataloguer notes. If a field fails a check, the citation object's cataloguer notes will contain a message indicating the issue, and the status of the record will be returned as either "review" or "dropped". 

The `metadata_quality_review(cit: Citation, override: str = None)` function returns a tuple of the form `(Citation, message)` where `Citation` is the reviewed citation object and `message` is a string indicating the review status.
The reviewed status is either "active", "review", or "dropped" depending on whether the citation passed or failed the review. The `override` parameter is a space-separated string that specifies which checks to override. For example, `"volume issue"` will override the checks for volume and issue. See the table at the bottom of this documentation for a full description of the checks performed, the statuses triggered by various checks, and the override behavior.

## Usage

To use the `metadata_quality_review` package, follow these steps:

1. **Import the necessary functions:**

    ```python
    from metadata_quality_review import metadata_quality_review
    ```

2. **Create a `Citation` object:**

    Ensure you have a `Citation` object that contains the metadata you want to review.

    ```python
    from citation import Citation
   
    with open('example_data/pickle_1000.pkl', 'rb') as f:
        citation = pickle.load(f)
    ```

3. **Run the metadata quality review:**

   Call the `metadata_quality_review` function with the `Citation` object and an optional override string.

    ```python
    reviewed_citation, message = metadata_quality_review(citation, override="volume issue")
    ```

4. **Check the results:**

    The function returns a tuple containing the reviewed `Citation` object and a message indicating the review status.

    ```python
    print(reviewed_citation.local.cataloger_notes)
    print(message)
    ```

### Conditions override words, status, and notes

| Condition                                | Override word  | failed status | if overridden | local Catalog Note Text                     |
|------------------------------------------|----------------|---------------|---------------|---------------------------------------------|
| No volume number                         | volume         | review        | active        | No volume number                            |
| No issue number                          | issue          | review        | active        | No issue number                             |
| No page number                           | page           | review        | active        | No page number                              |
| No main title                            | title          | dropped       | review        | No main title                               |
| No names elements                        | author         | dropped       | review        | No name elements                            |
| Two or more primary author               | primary        | review        | active        | Two or more primary author                  |
| No issue date                            | date           | review        | active        | No issue date                               |
| missing abstract                         | abstract       | dropped       | review        | missing abstract                            |
| Abstract empty or less than 50 character | short_abstract | dropped       | active        | Abstract is empty or less than 50 character |
| Non-UTF8 characters in abstract          | UTF8           | review        | active        | Non-UTF8 characters in abstract             |
| Abstract **may** not be in English       | non-English    | review        | active        | Non-English abstract                        |
| Submission article missing manuscript    | manuscript     | review        | active        | Submission article missing manuscript       |