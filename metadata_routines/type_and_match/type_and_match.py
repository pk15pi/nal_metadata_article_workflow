from dataclasses import dataclass, field
from enum import Enum
import re
from typing import Dict
import tomli
import warnings
import pysolr
import os
import srupymarc
from citation import Citation
from difflib import SequenceMatcher
import doi
import urllib
import requests


class Methods(Enum):
    BEGINNING = 'beginning'
    TITLE = 'title'
    ANYWHERE = 'anywhere'


@dataclass
class ArticleTyperMatcher:
    #  imported from toml file
    correction: Dict[str, Methods] = field(default_factory=dict)
    retraction: Dict[str, Methods] = field(default_factory=dict)
    erratum: Dict[str, Methods] = field(default_factory=dict)
    corrigendum: Dict[str, Methods] = field(default_factory=dict)
    withdrawn: Dict[str, Methods] = field(default_factory=dict)
    notice: Dict[str, Methods] = field(default_factory=dict)

    def _convert_dict_to_enum(
            self,
            data: Dict[str, str]
    ) -> Dict[str, Methods]:

        return {k: Methods(v) for k, v in data.items()}

    def __post_init__(self):
        # Read in data from string_matches.toml,
        # use to populate the above dictionaries.
        # Directory of this file:
        base_path = os.path.dirname(os.path.abspath(__file__))
        string_matches_file = os.path.join(base_path, 'string_matches.toml')
        with open(string_matches_file, 'rb') as f:
            data = tomli.load(f)

        if "correction" in data:
            self.correction = self._convert_dict_to_enum(data["correction"])
        else:
            warnings.warn("No correction data found in string_matches.toml")
        if "retraction" in data:
            self.retraction = self._convert_dict_to_enum(data["retraction"])
        else:
            warnings.warn("No retraction data found in string_matches.toml")
        if "erratum" in data:
            self.erratum = self._convert_dict_to_enum(data["erratum"])
        else:
            warnings.warn("No erratum data found in string_matches.toml")
        if "corrigendum" in data:
            self.corrigendum = self._convert_dict_to_enum(data["corrigendum"])
        else:
            warnings.warn("No corrigendum data found in string_matches.toml")
        if "withdrawn" in data:
            self.withdrawn = self._convert_dict_to_enum(data["withdrawn"])
        else:
            warnings.warn("No withdrawn data found in string_matches.toml")
        if "notice" in data:
            self.notice = self._convert_dict_to_enum(data["notice"])
        else:
            warnings.warn("No notice data found in string_matches.toml")

    def get_record_type(self, title: str) -> str:
        for string, method in self.correction.items():
            if self.regx_checker(title, method, string):
                return 'correction'
        for string, method in self.retraction.items():
            if self.regx_checker(title, method, string):
                return 'retraction'
        for string, method in self.erratum.items():
            if self.regx_checker(title, method, string):
                return 'erratum'
        for string, method in self.withdrawn.items():
            if self.regx_checker(title, method, string):
                return 'withdraw'
        for string, method in self.notice.items():
            if self.regx_checker(title, method, string):
                return 'notice'
        for string, method in self.corrigendum.items():
            if self.regx_checker(title, method, string):
                return 'corrigendum'
        return 'journal-article'

    def regx_checker(self, title: str, method: Methods, string: str) -> bool:
        if method == Methods.TITLE and \
                re.fullmatch(string, title, re.IGNORECASE):
            return True
        if method == Methods.BEGINNING and \
                re.match(f'^{string}', title, re.IGNORECASE):
            return True
        if method == Methods.ANYWHERE and \
                re.search(string, title, re.IGNORECASE):
            return True
        return False

    # Utility functions to support the find_matching_records method
    def _extract_title(self, record):
        title = record.get("245")
        if title is not None:
            sub_a = title.get("a")
            sub_b = title.get("b")
            if sub_a is not None and sub_b is not None:
                return f"{sub_a}: {sub_b}"
            elif sub_a is not None:
                return sub_a
        return None

    def _extract_doi(self, record):
        fields = record.get_fields("024")
        for f in fields:
            if f is not None and f.get("2") is not None:
                if f.get("2") == "doi":
                    return f.get("a")
        return None

    def _extract_agid(self, record):
        fields = record.get_fields("974")
        for f in fields:
            if f.get("a"):
                return f.get("a").split("agid:")[1]
        return None

    def _extract_mmsid(self, record):
        return record.get("001").data

    def _find_matching_records_solr(self, doi, mmsid):

        # Read environment variable for solr server url
        solr_server = os.environ.get('SOLR_SERVER')
        if solr_server is None:
            raise ValueError("SOLR_SERVER environment variable not set")

        # Connect to Solr
        solr = pysolr.Solr(solr_server, always_commit=True)

        if doi == "":
            doi = None
        if mmsid == "":
            mmsid = None

        # First check if a record matching the doi or mmsid
        # exists in the solr index
        if doi and mmsid:
            query = f'doi:"{doi}" OR mmsid:"{mmsid}"'
        elif doi:
            query = f'doi:"{doi}"'
        elif mmsid:
            query = f'mmsid:"{mmsid}"'
        else:
            return []

        try:
            results = solr.search(query)
        except pysolr.SolrError as e:
            print("Pysolr returning network error")
            return "network error"
        if results.hits > 0:
            # Create a list of dictionaries of the results,
            # including keys 'title', 'doi', and 'mmsid'
            matching_records = []
            for result in results:
                doi_matched = result.get('doi', None)
                if isinstance(doi_matched, list):
                    doi_matched = doi_matched[0]
                title_matched = result.get('title', None)
                if isinstance(title_matched, list):
                    title_matched = title_matched[0]
                matching_records.append({
                    'title': title_matched,
                    'doi': doi_matched,
                    'mmsid': result.get('mmsid', None),
                    'agid': result.get('agid', None)
                })
            return matching_records
        else:
            return []

    def _find_matching_records_alma_mmsid(self, mmsid):

        if mmsid == "":
            mmsid = None

        if not mmsid:
            return []

        alma_query = f'alma.mms_id={mmsid}'
        params = {
            "url": "https://na91.alma.exlibrisgroup.com/view/sru/01NAL_INST",
            "query": alma_query
        }
        try:
            alma_response = srupymarc.searchretrieve(**params)
        except (OSError, requests.exceptions.ConnectTimeout, srupymarc.errors.SrupymarcError) as e:
            print("Alma returning network error")
            return "network error"

        if alma_response.count > 0:
            matching_records = []
            for record in alma_response:
                matching_records.append({
                    'title': self._extract_title(record),
                    'doi': self._extract_doi(record),
                    'mmsid': mmsid,
                    'agid': self._extract_agid(record)
                })
            return matching_records
        return []

    def _find_matching_records_alma_doi(self, doi):

        if doi == "":
            doi = None

        if not doi:
            return []

        alma_query = f'alma.digital_object_identifier={doi}'
        params = {
            "url": "https://na91.alma.exlibrisgroup.com/view/sru/01NAL_INST",
            "query": alma_query
        }
        try:
            alma_response = srupymarc.searchretrieve(**params)
        except (OSError, requests.exceptions.ConnectTimeout,
                srupymarc.errors.SrupymarcError) as e:
            return "network error"

        if alma_response.count > 0:
            matching_records = []
            for record in alma_response:
                matching_records.append({
                    'title': self._extract_title(record),
                    'doi': doi,
                    'mmsid': record.get("001").data,
                    'agid': self._extract_agid(record)
                })
            return matching_records
        return []

    # Main function to find matching records

    def find_matching_records(self, doi, mmsid):

        # If both parameters are empty, return no matching records
        # No need to check solr or alma
        if doi == "":
            doi = None
        if mmsid == "":
            mmsid = None
        if not doi and not mmsid:
            return []

        # First check if a record matching the doi or mmsid
        # exists in the solr index
        matching_records = self._find_matching_records_solr(doi, mmsid)
        if matching_records:
            return matching_records

        # If no records are matched through pubag,
        # check for Alma matches to the doi
        matching_records = self._find_matching_records_alma_mmsid(mmsid)
        if matching_records:
            return matching_records

        # If no records are matched on Alma by DOI, try by mmsid
        matching_records = self._find_matching_records_alma_doi(doi)
        if matching_records:
            return matching_records

        return []

    def doi_status(self, cit) -> str:
        # Check if the DOI is valid
        if cit.local.USDA == "yes":
            return "valid"
        doi_str = cit.DOI
        if doi_str is None or doi_str == "":
            return "missing"
        else:
            try:
                valid_doi = doi.validate_doi(doi_str)
                if not valid_doi or valid_doi == []:
                    return "invalid"
            except ValueError:
                return "invalid"
            except urllib.error.URLError as e:
                return "network error"
        return "valid"

    def type_and_match(
            self, citation_object: Citation
    ) -> tuple[Citation, str]:

        # First check if the doi is valid. If it is invalid, return the message
        # "review" and add "invalid doi" to the cataloger note.
        # If there is a network error, return the message "network error"

        status = self.doi_status(citation_object)
        if status == "missing":
            citation_object.local.cataloger_notes.append("Missing DOI")
            if citation_object.local.USDA == "no":
                return citation_object, "review"
        elif status == "invalid":
            citation_object.local.cataloger_notes.append("Invalid DOI")
            if citation_object.local.USDA == "no":
                return citation_object, "review"
        elif status == "network error":
            return citation_object, "Network error, re-run"

        ATM = ArticleTyperMatcher()

        if citation_object.type == "journal-article":
            citation_object.type = ATM.get_record_type(citation_object.title)

        if citation_object.type == "notice":
            return citation_object, "dropped"

        matching_records = ATM.find_matching_records(
            citation_object.DOI,
            citation_object.local.identifiers.get("mms_id", None)
        )

        if matching_records == "network error":
            return citation_object, "Network error, re-run"

        if citation_object.type == "journal-article":
            if len(matching_records) == 0:
                return citation_object, "new"
            else:
                matching_record_titles = [
                    record['title'] for record in matching_records
                ]
                title_match_ratios = [
                    SequenceMatcher(None, citation_object.title, title).ratio()
                    for title in matching_record_titles
                ]
                # If the incoming title matches an existing title at least 90%
                if any(ratio > 0.90 for ratio in title_match_ratios):
                    # Pick the record that matches the incoming title the most
                    matching_record = matching_records[
                        title_match_ratios.index(max(title_match_ratios))
                    ]
                    citation_object.local.identifiers["mms_id"] = \
                        matching_record['mmsid']
                    citation_object.local.identifiers["pid"] = \
                        matching_record['agid']
                    return citation_object, "merge"
                else:
                    match_types = [
                        ATM.get_record_type(title)
                        for title in matching_record_titles
                    ]
                    article_matches = [
                        title for title, match_type in
                        zip(matching_record_titles, match_types) if
                        match_type == "journal-article"
                    ]
                    if len(article_matches) == 0:
                        return citation_object, "new"
                    else:
                        matching_mmsids = [
                            record['mmsid'] for record in matching_records if
                            record['title'] in article_matches
                        ]
                        if len(matching_mmsids) > 1:
                            citation_object.cataloger_notes.append(
                                "Multiple matching article records found in \
                                Alma. See local identifiers for mmsids."
                            )
                        matching_mmsids_concat = ','.join(matching_mmsids)
                        citation_object.local.identifiers["mms_id"] = \
                            matching_mmsids_concat
                        return citation_object, "review"
        else:  # Not a journal article
            if len(matching_records) == 0:
                return citation_object, "new"
            else:
                match_titles = [record['title'] for record in matching_records]
                if citation_object.title in match_titles:
                    matching_record = matching_records[
                        match_titles.index(citation_object.title)
                    ]
                    citation_object.local.identifiers["mms_id"] = \
                        matching_record['mmsid']
                    citation_object.local.identifiers["pid"] = \
                        matching_record['agid']
                    return citation_object, "merge"
                else:
                    return citation_object, "new"
