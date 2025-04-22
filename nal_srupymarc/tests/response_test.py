from srupymarc_test import ResponseTestCase
from srupymarc.response import SearchRetrieveResponse, ExplainResponse
import os
import pymarc
import warnings

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class TestSearchRetrieveResponse(ResponseTestCase):
    # 1 file, 1 record, 1 query match, next record DNE
    def test_response_single(self):
        data_loader = self._data_loader_mock(["response_single.xml"])
        res = SearchRetrieveResponse(data_loader, "flatten")

        self.assertEqual(res.count, 1)
        self.assertEqual(res.__length_hint__(), 1)
        self.assertEqual(res.sru_version, "1.2")
        self.assertIsNone(res.next_start_record)

    def test_response_single_sru11(self):
        data_loader = self._data_loader_mock(["response_single_sru11.xml"])
        res = SearchRetrieveResponse(data_loader, "flatten")

        self.assertEqual(res.count, 8985)
        self.assertEqual(res.__length_hint__(), 8985)
        self.assertEqual(res.sru_version, "1.1")
        self.assertEqual(res.next_start_record, 2)

    def test_response_multi(self):
        data_loader = self._data_loader_mock(["response_multiple_1.xml"])
        res = SearchRetrieveResponse(data_loader, "flatten")

        self.assertEqual(res.count, 220)
        self.assertEqual(res.__length_hint__(), 220)
        self.assertEqual(res.sru_version, "1.2")
        self.assertEqual(res.next_start_record, 100)

    def test_response_iterator(self):
        filenames = [
            "response_multiple_1.xml",
            "response_multiple_2.xml",
            "response_multiple_3.xml",
        ]
        data_loader = self._data_loader_mock(filenames)
        res = SearchRetrieveResponse(data_loader, "flatten")

        next_res = next(iter(res))
        self.assertIsNotNone(next_res)
        self.assertIsInstance(next_res, dict)
        self.assertEqual(next_res["schema"], "isad")
        self.assertEqual(next_res["reference"], "Z 248.24")

        records = [r for r in res]
        self.assertEqual(len(records), 220)
        self.assertEqual(data_loader.load.call_count, 3)

    def test_response_index(self):
        filenames = [
            "response_multiple_1.xml",
            "response_multiple_2.xml",
            "response_multiple_3.xml",
        ]
        data_loader = self._data_loader_mock(filenames)
        res = SearchRetrieveResponse(data_loader, "flatten")
        self.assertEqual(data_loader.load.call_count, 1)

        self.assertIsNotNone(res[150])
        self.assertIsInstance(res[150], dict)
        self.assertEqual(data_loader.load.call_count, 2)

        self.assertIsNotNone(res[205])
        self.assertIsInstance(res[205], dict)
        self.assertEqual(data_loader.load.call_count, 3)

    def test_response_pymarc(self):
        data_loader = self._data_loader_mock(["alma_response.xml"])
        res = SearchRetrieveResponse(data_loader, "pymarc")
        rec1 = res[0]
        self.assertEqual(res.count, 46)
        self.assertEqual(rec1["100"]["a"], "Nakazato, Tadashi")

    def test_pymarc_schema_error(self):
        data_loader = self._data_loader_mock(["response_single.xml"])
        with self.assertRaises(ValueError):
            _ = SearchRetrieveResponse(data_loader, "pymarc")

    def test_invalid_leader(self):
        # Confirm that if we pass a record with a leader length not equal to 24,
        # that the leader field is overwritten with the default leader string
        data_loader = self._data_loader_mock(["journal_record_leader_23.xml"])
        res = SearchRetrieveResponse(data_loader, output_format="pymarc")
        rec1 = res[0]
        self.assertEqual(str(rec1.leader), "00000nam a2200289 a 4500")

    def test_valid_leader(self):
        data_loader = self._data_loader_mock(["journal_record_leader_24.xml"])
        res = SearchRetrieveResponse(data_loader, output_format="pymarc")
        rec1 = res[0]
        self.assertEqual(str(rec1.leader), "01140nas a2200349  44500")

class TestExplainResponse(ResponseTestCase):
    def test_response_simple_flatten(self):
        data_loader = self._data_loader_mock(["test_explain.xml"])
        res = ExplainResponse(data_loader)
        self.assertEqual(data_loader.load.call_count, 1)

        self.assertIsNotNone(res.server)
        self.assertIsNotNone(res.index)
        self.assertIsNotNone(res.schema)
        self.assertIsNotNone(res.database)
        self.assertIsNotNone(res.config)
