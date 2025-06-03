import pytest
from unittest.mock import patch, MagicMock
from pid_minter import pid_minter



@patch('pid_minter.mint_pid.connect_pid_db')
def test_pid_minter_no_pid(mock_connect, citation_object_no_pid):
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = [5]
    mock_connection.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_connection

    result = pid_minter(citation_object_no_pid)
    assert result == [citation_object_no_pid, "successful", "PID Assigned", 5]
    assert citation_object_no_pid.local.identifiers['pid'] == 5


@patch('pid_minter.mint_pid.connect_pid_db')
def test_pid_minter_db_connection_error(mock_connect, citation_object_no_pid):
    mock_connect.return_value = None

    result = pid_minter(citation_object_no_pid)
    assert result == [citation_object_no_pid, "unsuccessful",
                      "Database connection error occured", None]