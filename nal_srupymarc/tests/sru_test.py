import mock
from srupymarc_test import SrupymarcTestCase
import srupymarc


class TestSru(SrupymarcTestCase):
    def test_searchretrieve(self):
        r = srupymarc.searchretrieve("http://test.com/sru/", "Test-Query",
                                     output_format="flatten")
        self.assertIsInstance(r, srupymarc.response.SearchRetrieveResponse)
        self.session_mock.return_value.get.assert_called_once_with(
            "http://test.com/sru/",
            params={
                "operation": "searchRetrieve",
                "version": "1.2",
                "query": "Test-Query",
                "startRecord": 1,
                "maximumRecords": 10,
            },
        )

    def test_searchretrieve_with_maximum_records(self):
        r = srupymarc.searchretrieve(
            "http://test.com/sru/",
            "Test-Query",
            maximum_records=100,
            output_format="flatten"
        )
        self.assertIsInstance(r, srupymarc.response.SearchRetrieveResponse)
        self.session_mock.return_value.get.assert_called_once_with(
            "http://test.com/sru/",
            params={
                "operation": "searchRetrieve",
                "version": "1.2",
                "query": "Test-Query",
                "startRecord": 1,
                "maximumRecords": 100,
            },
        )

    def test_searchretrieve_with_record_schema(self):
        r = srupymarc.searchretrieve(
            "http://test.com/sru/", "Test-Query", record_schema="isad",
            output_format="flatten"
        )
        self.assertIsInstance(r, srupymarc.response.SearchRetrieveResponse)
        self.session_mock.return_value.get.assert_called_once_with(
            "http://test.com/sru/",
            params={
                "operation": "searchRetrieve",
                "version": "1.2",
                "query": "Test-Query",
                "startRecord": 1,
                "maximumRecords": 10,
                "recordSchema": "isad",
            },
        )

    def test_searchretrieve_with_start_record(self):
        r = srupymarc.searchretrieve("http://test.com/sru/", "Test-Query",
                                     start_record=10, output_format="flatten")
        self.assertIsInstance(r, srupymarc.response.SearchRetrieveResponse)
        self.session_mock.return_value.get.assert_called_once_with(
            "http://test.com/sru/",
            params={
                "operation": "searchRetrieve",
                "version": "1.2",
                "query": "Test-Query",
                "startRecord": 10,
                "maximumRecords": 10,
            },
        )

    def test_searchretrieve_with_session(self):
        content, path = self._test_content()
        session_mock = mock.MagicMock(
            get=mock.MagicMock(return_value=mock.MagicMock(content=content))
        )  # noqa
        # session_mock.verify = False
        r = srupymarc.searchretrieve(
            "http://test.com/sru/", "Test-Query", session=session_mock,
            output_format="flatten"
        )
        self.assertIsInstance(r, srupymarc.response.SearchRetrieveResponse)
        session_mock.get.assert_called_once_with(
            "http://test.com/sru/",
            params={
                "operation": "searchRetrieve",
                "version": "1.2",
                "query": "Test-Query",
                "startRecord": 1,
                "maximumRecords": 10,
            },
        )

    def test_explain(self):
        info = srupymarc.explain("http://test.com/sru/")
        self.assertEqual(info.sru_version, "1.2"),
        self.assertEqual(info["sru_version"], "1.2")
        self.assertIsInstance(info, srupymarc.response.AttributeDict)
        self.session_mock.return_value.get.assert_called_once_with(
            "http://test.com/sru/",
            params={
                "operation": "explain",
                "version": "1.2",
            },
        )

    def test_client(self):
        client = srupymarc.Client("http://test.com/sru")
        self.assertIsInstance(client, srupymarc.client.Client)
