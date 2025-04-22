from typing import Tuple
from mapper.map_from_submit_site import map_from_submit_site
from mapper.map_from_crossref_api import map_from_crossref_api
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
        case _:
            return None, "Error: invalid source schema"


if __name__ == '__main__':
    crossref_string = '''
     {
        "indexed": {
            "title": [
                "Distribution of Apple stem grooving virus in apple \
                trees in the Czech Republic"
            ],
            "DOI": "10.17221/8360-pps"
        }
    }
    '''
    output, my_message = mapper(crossref_string, 'crossref_api_json')
    print(output)
    print(my_message)
