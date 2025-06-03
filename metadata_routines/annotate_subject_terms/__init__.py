from .nalt_lookup import validate_nalt_terms, uri_to_term
from .text_cleanup import (
    remove_periods,
    replace_metacharacters,
    normalize_hyphens,
    remove_copyright_statement,
)
from .cogito_indexer import (
    create_cogx,
    cit_to_cogx,
    get_cogito_annotations,
    annotate_citation
)