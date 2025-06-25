import sys
from unittest.mock import MagicMock
sys.modules['srupymarc'] = MagicMock()
from pytest import MonkeyPatch
import pymarc
from pymarc import Indicators, Subfield
from handle_minter.mint_and_notify import mint_and_notify
import os

current_file_directory = __file__.rsplit('/', 1)[0]

# Case 1: No records in Alma
def test_no_records_in_alma(monkeypatch: MonkeyPatch):
    # Mock the environment variable
    monkeypatch.setenv('HANDLE_MINTER_CONFIG', os.path.join(current_file_directory, 'test_config.toml'))
    monkeypatch.setenv('HANDLE_API_HEADERS', 'fake_value')

    handle_data = {
        'pid': 'test-0000',
        'mmsid': '000000000000',
        'provider_rec': '1234',
        'title': 'Super important article'
    }

    # Mock the get_matching_records function to return an empty list
    def mock_get_matching_records(mmsid, pid, provider_rec):
        return []

    monkeypatch.setattr('handle_minter.mint_and_notify.get_matching_records', mock_get_matching_records)

    result, message = mint_and_notify(handle_data)
    assert result == 'not found in Alma'
    assert message is None

def test_multiple_records_in_alma(monkeypatch: MonkeyPatch):
    # Mock the environment variable
    monkeypatch.setenv('HANDLE_MINTER_CONFIG', os.path.join(current_file_directory, 'test_config.toml'))
    monkeypatch.setenv('HANDLE_API_HEADERS', 'fake_value')

    handle_data = {
        'pid': 'test-0000',
        'mmsid': '000000000001',
        'provider_rec': '1234',
        'title': 'Super important article'
    }

    # Mock the get_matching_records function to return multiple records
    def mock_get_matching_records(mmsid, pid, provider_rec):
        return [pymarc.Record(), pymarc.Record()]

    monkeypatch.setattr('handle_minter.mint_and_notify.get_matching_records', mock_get_matching_records)

    result, message = mint_and_notify(handle_data)
    assert result == 'review'
    assert message == 'Multiple records in Alma'

def test_successful_handle_creation(monkeypatch: MonkeyPatch):
    monkeypatch.setenv('HANDLE_MINTER_CONFIG', os.path.join(current_file_directory, 'test_config.toml'))
    monkeypatch.setenv('HANDLE_API_HEADERS', 'fake_value')

    handle_data = {
        'pid': 'test-0000',
        'mmsid': '000000000001',
        'provider_rec': '1234',
        'title': 'Super important article'
    }

    def mock_get_matching_records(mmsid, pid, provider_rec):
        record = pymarc.Record()
        # Set field 024 with subfield '2' as 'hdl' and subfield 'a' as the handle
        record.add_field(pymarc.Field(
            tag='024',
            indicators=Indicators('7', ' '),
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

    monkeypatch.setattr('handle_minter.mint_and_notify.get_matching_records', mock_get_matching_records)
    result, message = mint_and_notify(handle_data)
    assert result == 'success'
    assert message == 'Debug mode enabled. Handle not minted - success'

def test_handle_minter_failure(monkeypatch: MonkeyPatch):
    monkeypatch.setenv('HANDLE_MINTER_CONFIG', os.path.join(current_file_directory, 'test_config_handle_conn.toml'))
    monkeypatch.setenv('HANDLE_API_HEADERS', 'fake_value')

    handle_data = {
        'pid': 'test-0000',
        'mmsid': '000000000001',
        'provider_rec': '1234',
        'title': 'Super important article'
    }

    def mock_get_matching_records(mmsid, pid, provider_rec):
        record = pymarc.Record()
        # Set field 024 with subfield '2' as 'hdl' and subfield 'a' as the handle
        record.add_field(pymarc.Field(
            tag='024',
            indicators=Indicators('7', ' '),
            subfields=[
                Subfield(code='2', value='hdl'),
                Subfield(code='a', value='10113/{pid}'.format(pid=pid)),
            ])
        )
        record.add_field(pymarc.Field(
            tag='001',
            data="000000000001"
            )
        )
        return [record]

    monkeypatch.setattr('handle_minter.mint_and_notify.get_matching_records', mock_get_matching_records)

    # Mock the create_handle function to simulate a failure
    def mock_create_handle(self, pid, landing_page_url):
        return None  # Simulate failure

    monkeypatch.setattr('handle_minter.handle_client.HandleClient.create_handle', mock_create_handle)

    result, message = mint_and_notify(handle_data)
    assert result == 'review'
    assert message == 'Handle minting failed'
