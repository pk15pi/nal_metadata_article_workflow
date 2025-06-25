# BEFORE RUNNING THIS EXAMPLE:
# Ensure the configuration file has [debug][handle_service_conn] set to 0

# This example mocks the connection to Alma. It performs the mint_and_notify function
# as if a matching record was found in Alma.

import sys
import pymarc
from pymarc import Indicators, Subfield
from handle_minter.mint_and_notify import mint_and_notify
from unittest import mock

handle_data = {
    "pid": "test-2222",
    "submitter_email": "noa.mills@usda.gov",
    "submitter_name": "Your Eternal Legacy",
    "mmsid": "1234",
    "provider_rec": "provider_rec",
    "title": "Super important article"
}

# Patch the function that retrieves matching records from Alma
def mock_get_matching_records(mmsid, pid, provider_rec):
    record = pymarc.Record()
    # Set field 024 with subfield '2' as 'hdl' and subfield 'a' as the handle
    record.add_field(pymarc.Field(
        tag='024',
        indicators=Indicators('7',' '),
        subfields=[
            Subfield(code='2', value='hdl'),
            Subfield(code='a', value='10113/{pid}'.format(pid=pid)),
        ])
    )
    record.add_field(pymarc.Field(
        tag='001',
        data="000000000001"
    ))
    return [record]

# Run mint_and_notify, using the mock_get_matching_records function instead of the get_matching_records function
with mock.patch('handle_minter.mint_and_notify.get_matching_records', mock_get_matching_records):
    sys.modules['srupymarc'] = mock.Mock()  # Mock srupymarc to avoid import errors
    result, message = mint_and_notify(handle_data)
print(f"Result: {result}")
print(f"Message: {message}")