# -*- coding: utf-8 -*-

import requests
from . import errors
from . import xmlparse
from . import response
import sys


class Client(object):
    def __init__(
        self,
        url=None,
        maximum_records=10,
        record_schema=None,
        sru_version="1.2",
        session=None,
        output_format="pymarc"
    ):
        self.url = url
        self.maximum_records = maximum_records
        self.sru_version = sru_version
        self.record_schema = record_schema
        self.session = session or requests.Session()

    def searchretrieve(self, query, start_record=1, output_format="pymarc", suppress_leader_warning=True):
        valid_formats = ["flatten", "pymarc"]
        if output_format not in valid_formats:
            raise ValueError(f"Invalid output format: {output_format}")
        params = {
            "operation": "searchRetrieve",
            "version": self.sru_version,
            "query": query,
            "startRecord": start_record,
            "maximumRecords": self.maximum_records,
        }

        if self.record_schema:
            params["recordSchema"] = self.record_schema

        data_loader = DataLoader(self.url, self.session, params)
        return response.SearchRetrieveResponse(data_loader, output_format, suppress_leader_warning)

    def explain(self):
        params = {
            "operation": "explain",
            "version": self.sru_version,
        }
        data_loader = DataLoader(self.url, self.session, params)
        explain_response = response.ExplainResponse(data_loader)
        return explain_response.asdict()


class DataLoader(object):
    def __init__(self, url, session, params):
        self.session = session
        self.url = url
        self.params = params
        self.response = None
        self.xmlparser = xmlparse.XMLParser()

    def load(self, **kwargs):
        self.params.update(kwargs)
        xml = self._get_content(self.url, self.params)
        self._check_errors(xml)
        return xml

    def _get_content(self, url, params):
        try:
            res = self.session.get(url, params=params)
            res.raise_for_status()
        except (OSError, requests.exceptions.ConnectTimeout) as e:
            sys.tracebacklimit = 0
            print("SRU service unavailable. Check network connection.")
            sys.exit(1)

        except requests.exceptions.HTTPError as e:
            raise errors.SrupymarcError("HTTP error: %s" % e)
        except requests.exceptions.RequestException as e:
            raise errors.SrupymarcError("Request error: %s" % e)
        except Exception as e:
            print("Failed with exception: ", e)
            sys.exit(1)


        return self.xmlparser.parse(res.content)

    def _check_errors(self, xml):
        sru = "{http://www.loc.gov/zing/srw/}"
        diag = "{http://www.loc.gov/zing/srw/diagnostic/}"
        diagnostics = self.xmlparser.find(xml, f"{sru}diagnostics/{diag}diagnostic")
        if diagnostics:
            for child in diagnostics:
                if child.text is None:
                    child.text = ""
            error_msg = ", ".join([d.text for d in diagnostics])
            raise errors.SruError(error_msg)
