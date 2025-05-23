# -*- coding: utf-8 -*-

from collections import defaultdict
import re
import warnings
from flatten_dict import flatten
from . import xmlparse
from . import errors
import pymarc
import io


class Response(object):
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.xmlparser = xmlparse.XMLParser()
        self.records = []
        xml = self.data_loader.load()
        self._parse_content(xml)
        warnings.simplefilter('always', UserWarning)

    def maybe_int(self, s):
        try:
            return int(s)
        except (ValueError, TypeError):
            return s

    def _check_response_tag(self, xml, tag):
        sru = "{http://www.loc.gov/zing/srw/}"
        response = f"{sru}{tag}"
        if not xml.tag == response:
            # fix namespace for servers that provide the wrong namespace URI
            main_ns = self.xmlparser.namespace(xml)
            if "www.loc.gov/zing/srw" in main_ns:
                warnings.warn(
                    f"""
                    The server has the wrong namespace for SRU,
                    it should be {sru} but it's currently set to {{{main_ns}}}.
                    """,
                    errors.WrongNamespaceWarning,
                )
                self.xmlparser.namespaces["sru"] = main_ns
            else:
                raise errors.ServerIncompatibleError(
                    f"Server response did not contain a {response} tag"
                )


class SearchRetrieveResponse(Response):
    def __init__(self, data_loader, output_format, suppress_leader_warning):
        self.output_format = output_format
        self.suppress_leader_warning = suppress_leader_warning
        super(SearchRetrieveResponse, self).__init__(data_loader)

    def __repr__(self):
        try:
            return (
                "SearchRetrieveResponse("
                "sru_version=%r,"
                "count=%r,"
                "next_start_record=%r)"
            ) % (
                self.sru_version,
                self.count,
                self.next_start_record,
            )
        except AttributeError:
            return "SearchRetrieveResponse(empty)"

    def _parse_content(self, xml):
        self._check_response_tag(xml, "searchRetrieveResponse")

        record_schema = self.xmlparser.find(xml, ".//sru:recordSchema").text

        self.count = self.maybe_int(
            self.xmlparser.find(xml, "./sru:numberOfRecords").text
        )
        if self.count != 0: # Only validate record schema if there are records
            if self.output_format == "pymarc" and record_schema != "marcxml":
                raise ValueError(f'Invalid record schema for pymarc output format: {record_schema}. \n'
                                 f'Only marcxml schema is supported for pymarc output format.')

        self.sru_version = self.xmlparser.find(xml, "./sru:version").text

        self._extract_records(xml)

        next_start_record = self.xmlparser.find(xml, "./sru:nextRecordPosition").text
        if next_start_record:
            self.next_start_record = self.maybe_int(next_start_record)
        else:
            self.next_start_record = None

    def __length_hint__(self):
        return self.count

    def __iter__(self):
        # use while loop since self.records could grow while iterating
        i = 0
        while True:
            # load new data when near end
            if i == len(self.records):
                try:
                    self._load_new_data()
                except errors.NoMoreRecordsError:
                    break
            yield self.records[i]
            i += 1

    def __getitem__(self, key):
        if isinstance(key, slice):
            limit = max(key.start or 0, key.stop or self.count)
            self._load_new_data_until(limit)
            count = len(self.records)
            return [self.records[k] for k in range(*key.indices(count))]

        if not isinstance(key, int):
            raise TypeError("Index must be an integer or slice")

        limit = key
        if limit < 0:
            # if we get a negative index, load all data
            limit = self.count
        self._load_new_data_until(limit)
        return self.records[key]

    def _load_new_data_until(self, limit):
        while limit >= len(self.records):
            try:
                self._load_new_data()
            except errors.NoMoreRecordsError:
                break

    def _load_new_data(self):
        if self.next_start_record is None:
            raise errors.NoMoreRecordsError()
        xml = self.data_loader.load(startRecord=self.next_start_record)
        self._parse_content(xml)

    def _extract_records(self, xml):
        if self.output_format == "flatten":
            return self._extract_records_dict(xml)
        elif self.output_format == "pymarc":
            return self._extract_records_pymarc(xml)
        else:
            raise ValueError(f"Output format not valid: {self.output_format}")

    def _extract_records_pymarc(self, xml):
        new_records = []
        xml_recs = self.xmlparser.findall(xml, "./sru:records/sru:record")
        for xml_rec in xml_recs:
            leader_string = self.xmlparser.find(xml_rec, './sru:recordData/marc:record/marc:leader').text
            if len(leader_string) != 24:
                replacement_leader = "00000nam a2200289 a 4500" # If updated, update test in response_test.py too
                control_number = self.xmlparser.find(xml_rec, './sru:recordData/marc:record/marc:controlfield[@tag="001"]').text
                if not self.suppress_leader_warning:
                    warnings.warn(f"Invalid leader field for record with control number {control_number}")
                xml_rec = self.xmlparser.find_and_replace(xml_rec, './sru:recordData/marc:record/marc:leader', replacement_leader)
            marcxmlFile = io.BytesIO(self.xmlparser.tostring(xml_rec))
            pymarc_record = pymarc.marcxml.parse_xml_to_array(marcxmlFile)[0]
            new_records.append(pymarc_record)
        self.records.extend(new_records)

    def _extract_records_dict(self, xml):
        new_records = []

        xml_recs = self.xmlparser.findall(xml, "./sru:records/sru:record")
        for xml_rec in xml_recs:
            record = defaultdict()
            record["schema"] = self.xmlparser.find(xml_rec, "./sru:recordSchema").text
            record_data = self.xmlparser.find(xml_rec, "./sru:recordData")
            extra_data = self.xmlparser.find(xml_rec, "./sru:extraRecordData")

            record.update(self._tag_data(record_data, "sru:recordData") or {})
            record["extra"] = self._tag_data(extra_data, "sru:extraRecordData")

            record = dict(record)
            new_records.append(record)
        self.records.extend(new_records)

    def _tag_data(self, elem, parent):
        # Receives an elementTree and a tag
        # Returns a dict version of the tree from that tag's node
        if not elem:
            return None
        record_data = self.xmlparser.todict(elem, xml_attribs=True).get(parent)
        if not record_data:
            return None

        # check if there is only one element on the top level
        keys = list(record_data.keys())
        if len(record_data) == 1 and len(keys) > 0 and len(record_data[keys[0]]) > 0:
            record_data = record_data[keys[0]]

        record_data.pop("schemaLocation", None)
        record_data.pop("xmlns", None)

        def leaf_reducer(_, k2):
            # only use key of leaf element
            return k2

        try:
            flattened_data = flatten(record_data, reducer=leaf_reducer)
        except ValueError:
            # if the keys of the leaf elements are not unique
            # the dict will not be flattened
            return record_data

        return flattened_data

    def _remove_namespace(self, elem):
        ns_pattern = re.compile("{.+}")
        tag_name = ns_pattern.sub("", elem.tag)
        return tag_name


class ExplainResponse(Response):
    def __repr__(self):
        return (
            "ExplainResponse("
            "sru_version=%r,"
            "server=%r,"
            "database=%r"
            "index=%r"
            "schema=%r"
            "config=%r)"
        ) % (
            self.sru_version,
            self.server,
            self.database,
            self.index,
            self.schema,
            self.config,
        )

    def asdict(self):
        return AttributeDict(
            {
                "sru_version": self.sru_version,
                "server": self.server,
                "database": self.database,
                "index": self.index,
                "schema": self.schema,
                "config": self.config,
            }
        )

    def _parse_content(self, xml):
        self._check_response_tag(xml, "explainResponse")

        record_schema = self.xmlparser.find(xml, ".//sru:recordSchema").text
        if record_schema:
            self.xmlparser.namespaces["zr"] = record_schema

        self.sru_version = self.xmlparser.find(xml, "./sru:version").text

        self.server = self._parse_server(xml)
        self.database = self._parse_database(xml)
        self.index = self._parse_index(xml)
        self.schema = self._parse_schema(xml)
        self.config = self._parse_config(xml)

    def _parse_server(self, xml):
        server_info = {
            "host": self.xmlparser.find(
                xml, [".//zr:serverInfo/zr:host", ".//zr2:serverInfo/zr:host"]
            ).text,
            "port": self.xmlparser.find(
                xml,
                [
                    ".//zr:serverInfo/zr:port",
                    ".//zr2:serverInfo/zr:port",
                ],
            ).text,
            "database": self.xmlparser.find(
                xml,
                [
                    ".//zr:serverInfo/zr:database",
                    ".//zr2:serverInfo/zr:database",
                ],
            ).text,
        }
        server_info["port"] = self.maybe_int(server_info["port"])
        return server_info

    def _parse_schema(self, xml):
        def bool_or_none(v):
            if v is None:
                return None
            return bool(v)

        def ident(a):
            return a

        attributes = {
            "identifier": ident,
            "name": ident,
            "location": ident,
            "sort": bool_or_none,
            "retrieve": bool_or_none,
        }

        schemas = {}
        xml_schemas = self.xmlparser.findall(
            xml,
            [
                ".//zr:schemaInfo/zr:schema",
                ".//zr2:schemaInfo/zr2:schema",
            ],
        )
        for schema in xml_schemas:
            schema_info = {}
            for attr, fn in attributes.items():
                xml_attr = schema.attrib.get(attr)
                if xml_attr:
                    schema_info[attr] = fn(xml_attr)
            schema_info["title"] = self.xmlparser.find(schema, "./zr:title").text
            schemas[schema.attrib.get("name")] = schema_info
        return schemas

    def _parse_config(self, xml):
        config = {}
        settings = self.xmlparser.findall(
            xml,
            [
                ".//zr:configInfo/zr:setting",
                ".//zr2:configInfo/zr:setting",
            ],
        )
        for setting in settings:
            t = setting.attrib["type"]
            config[t] = self.maybe_int(setting.text)

        # defaults
        xml_defaults = self.xmlparser.findall(
            xml,
            [
                ".//zr:configInfo/zr:default",
                ".//zr2:configInfo/zr:default",
            ],
        )
        defaults = {}
        for default in xml_defaults:
            t = default.attrib["type"]
            defaults[t] = self.maybe_int(default.text)
        config["defaults"] = defaults
        return config

    def _parse_database(self, xml):
        db = self.xmlparser.find(xml, ".//zr:databaseInfo")
        if not db:
            return {}
        db_info = {
            "title": self.xmlparser.find(db, ["./zr:title", "./title"]).text,
            "description": self.xmlparser.find(
                db, ["./zr:description", "./description"]
            ).text,
            "contact": self.xmlparser.find(db, ["./zr:contact", "./contact"]).text,
        }
        db_info = {k: v.strip() if v else v for (k, v) in db_info.items()}
        return db_info

    def _parse_index(self, xml):
        index = defaultdict(defaultdict)
        index_sets = self.xmlparser.findall(
            xml,
            [
                ".//zr:indexInfo/zr:set",
                ".//zr2:indexInfo/zr2:set",
            ],
        )
        for index_set in index_sets:
            index[index_set.attrib["name"]] = defaultdict()

        index_fields = self.xmlparser.findall(
            xml, [".//zr:indexInfo/zr:index", ".//zr2:indexInfo/zr2:index"]
        )
        for index_field in index_fields:
            title = self.xmlparser.find(index_field, ["./zr:title", "./title"]).text
            if title:
                title = title.strip()
            names = self.xmlparser.findall(
                index_field, [".//zr:map/zr:name", ".//zr2:map/zr2:name"]
            )
            for name in names:
                index[name.attrib["set"]][name.text.strip()] = title

        return {k: dict(v) for k, v in dict(index).items()}


class AttributeDict(dict):
    def __getattr__(self, attr):
        return self[attr]
