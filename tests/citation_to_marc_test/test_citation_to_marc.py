import pytest
from citation import Citation
import pymarc
import tempfile
from citation_to_marc import citation_to_marc


@pytest.mark.parametrize(
    "citation_fixture,marc_record_fixture",
    [
        ("cit1", "marc_record1"),
        ("cit2", "marc_record2"),
        ("cit3", "marc_record3"),
        ("cit4", "marc_record4"),
        ("cit5", "marc_record5"),
        ("cit6", "marc_record6"),
    ]
)
def test_citation_to_marc(citation_fixture, marc_record_fixture, request):
    """Test the conversion of citation objects to MARC records."""
    # Get the actual fixture values
    citation = request.getfixturevalue(citation_fixture)
    expected_marc_record = request.getfixturevalue(marc_record_fixture)

    assert isinstance(citation, Citation)
    assert isinstance(expected_marc_record, pymarc.record.Record)

    # Map the citation object to a temporary file
    with tempfile.NamedTemporaryFile() as tmpfile:
        msg = citation_to_marc(citation, "xml", tmpfile.name)
        tmpfile.seek(0)
        actual_marc_record = pymarc.marcxml.parse_xml_to_array(tmpfile)[0]
        assert isinstance(actual_marc_record, pymarc.record.Record)
        assert msg == "Successful"

    # Compare the MARC records
    assert actual_marc_record.as_dict() == expected_marc_record.as_dict()