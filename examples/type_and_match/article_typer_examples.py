# Note: ensure you are connected to the VPN

from type_and_match.type_and_match import ArticleTyperMatcher
from citation import Citation, Local


ATM = ArticleTyperMatcher()


# Print out record types with strings designed to match regex
print(ATM.get_record_type("Correction: title"))
print(ATM.get_record_type("Retraction: title"))
print(ATM.get_record_type("Erratum: title"))
print(ATM.get_record_type("Corrigendum: title"))
print(ATM.get_record_type("Withdrawn: title"))
print(ATM.get_record_type("Editorial: title"))
print(ATM.get_record_type("title"))

# Create sample citation objects
citation1 = Citation()
citation1.title = "A new perspective on microbial landscapes within food " + \
                  "production"
citation1.DOI = "10.1016/j.copbio.2015.12.008"
citation1.local = Local()
citation1.local.identifiers["mms_id"] = "9915695874407426"

citation2 = Citation()
citation2.title = "A new journal article that doesn't match any existing " + \
                  "records"
citation2.DOI = "10.1234/5678-fake-doi"
citation2.local = Local()
citation2.local.identifiers["mms_id"] = "1234567890"

# Record that matches an existing record, but upper case to avoid string matching
# This shows what happens when there is an ID match, but the titles are too different.
# String comparison ratio = 0.14, which is less than the threshold of 0.5.
citation3 = Citation()
citation3.title = "A new perspective on microbial landscapes within food ".upper() + \
                  "production".upper()
citation3.DOI = "10.1016/j.copbio.2015.12.008"
citation3.local = Local()
citation3.local.identifiers["mms_id"] = "9915695874407426"

# Record that matches an existing record with a small enough change to the
# title that it is considered a merge. String comparison ration = 0.99
citation4 = Citation()
citation4.title = "A new perspective on microbial landscapes within food " + \
                  "production."
citation4.DOI = "10.1016/j.copbio.2015.12.008"
citation4.local = Local()
citation4.local.identifiers["mms_id"] = "9915695874407426"

# Record with no DOI
citation5 = Citation()
citation5.local = Local()
citation5.DOI = None

# Record with an invalid DOI
citation6 = Citation()
citation6.local = Local()
citation6.DOI = "invalid_doi"


# Find records matching the citation1 object
# Note - the find_matching_records method is a helper method called by
# type_and_match. It is not designed to be called directly in the django app.
matching_records = ATM.find_matching_records(
    citation1.DOI, citation1.local.identifiers["mms_id"]
)
print("Matching records for citation 1: ", matching_records)

# Type and match all four records, print out associated message
print("Citation 1 message: ", ATM.type_and_match(citation1)[1])  # returns merge
print("Citation 2 message: ", ATM.type_and_match(citation2)[1])  # returns review because missing doi
print("Citation 3 message: ", ATM.type_and_match(citation3)[1])  # returns review because titles are too different
print("Citation 4 message: ", ATM.type_and_match(citation4)[1])  # returns merge
print("Citation 5 message: ", ATM.type_and_match(citation5)[1])  # returns review because missing doi
print("Citation 6 message: ", ATM.type_and_match(citation6)[1])  # returns review because invalid doi
