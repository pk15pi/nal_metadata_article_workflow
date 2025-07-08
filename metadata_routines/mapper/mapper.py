from typing import Tuple
from mapper.map_from_submit_site import map_from_submit_site
from mapper.map_from_crossref_api import map_from_crossref_api
from mapper.map_from_pubmed_xml import map_from_pubmed_xml
from mapper.map_from_jats_xml import map_from_jats_xml
from mapper.errors import FaultyRecordError


def mapper(source_string: str, source_schema: str) -> Tuple[str, str]:
    match source_schema:
        case 'submit_json':
            try:
                (citation_object, message) = \
                    map_from_submit_site(source_string)
            except FaultyRecordError as e:
                return None, "Faulty record: " + str(e)
            return citation_object, message
        case 'crossref_json':
            try:
                (citation_object, message) = \
                    map_from_crossref_api(source_string)
            except FaultyRecordError as e:
                return None, "Faulty record: " + str(e)
            return citation_object, message
        case 'pubmed_xml':
            try:
                (citation_object, message) = \
                    map_from_pubmed_xml(source_string)
            except FaultyRecordError as e:
                return None, "Faulty record: " + str(e)
            return citation_object, message
        case 'jats_xml':
            try:
                (citation_object, message) = \
                    map_from_jats_xml(source_string)
            except FaultyRecordError as e:
                return None, "Faulty record: " + str(e)
            return citation_object, message
        case _:
            return None, "Error: invalid source schema"
