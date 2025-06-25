from citation_to_marc import citation_to_marc
import pickle

# Read in pickle 1
with open('data/cit1.pkl', 'rb') as f:
    cit1 = pickle.load(f)

# Map the citation object to a marcxml record
output_path = "data/marc_record1.xml"
format = "xml"
msg1 = citation_to_marc(cit1, format, output_path)
print(msg1)

# Read in pickle 2
with open('data/cit2.pkl', 'rb') as f:
    cit2 = pickle.load(f)

# Map the citation object to a marcxml record
output_path = "data/marc_record2.xml"
format = "xml"
msg2 = citation_to_marc(cit2, format, output_path)
print(msg2)

# Read in pickle 3
with open('data/cit3.pkl', 'rb') as f:
    cit3 = pickle.load(f)

# Map the citation object to a marcxml record
output_path = "data/marc_record3.xml"
format = "xml"
msg3 = citation_to_marc(cit3, format, output_path)
print(msg3)

# Read in pickle 4
with open('data/cit4.pkl', 'rb') as f:
    cit4 = pickle.load(f)

# Map the citation object to a marcxml record
output_path = "data/marc_record4.xml"
format = "xml"
msg4 = citation_to_marc(cit4, format, output_path)
print(msg4)

# Read in pickle 5
with open('data/cit5.pkl', 'rb') as f:
    cit5 = pickle.load(f)

# Map the citation object to a marcxml record
output_path = "data/marc_record5.xml"
format = "xml"
msg5 = citation_to_marc(cit5, format, output_path)
print(msg5)

# Read in pickle 6
with open('data/cit6.pkl', 'rb') as f:
    cit6 = pickle.load(f)

# Map the citation object to a marcxml record
output_path = "data/marc_record6.xml"
format = "xml"
msg6 = citation_to_marc(cit6, format, output_path)
print(msg6)
