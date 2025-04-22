import pytest
from unittest.mock import patch, MagicMock
from pid_minter.pid_minter import pid_minter



@patch('pid_minter.connect_pid_db')
def test_pid_minter_no_pid(mock_connect, citation_object_no_pid):
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.stored_results.return_value = [MagicMock(fetchone=lambda: [5])]
    mock_connection.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_connection

    result = pid_minter(citation_object_no_pid)
    assert result == [citation_object_no_pid, "PID Assinged", 5]
    assert citation_object_no_pid.local.identifiers['pid'] == 5

@patch('pid_minter.connect_pid_db')
def test_pid_minter_with_pid(mock_connect, citation_object_with_pid):
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.stored_results.return_value = [MagicMock(fetchone=lambda: [5])]
    mock_connection.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_connection

    result = pid_minter(citation_object_with_pid)
    assert result == [citation_object_with_pid, "PID Already Assinged", None]

@patch('pid_minter.connect_pid_db')
def test_pid_minter_non_article(mock_connect, non_article_citation_object):
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.stored_results.return_value = [MagicMock(fetchone=lambda: [5])]
    mock_connection.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_connection

    result = pid_minter(non_article_citation_object)
    assert result == [non_article_citation_object, "Non Article", None]

@patch('pid_minter.connect_pid_db')
def test_pid_minter_db_connection_error(mock_connect, citation_object_no_pid):
    mock_connect.return_value = None

    result = pid_minter(citation_object_no_pid)
    assert result == [citation_object_no_pid,
                      "Database connection error occured", None]