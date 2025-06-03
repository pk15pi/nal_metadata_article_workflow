from dataclasses import dataclass, field


@dataclass
class Author:
    given: str = None
    family: str = None
    orcid: str = None
    affiliation: list = field(default_factory=list)
    sequence: str = None


@dataclass
class Funder:
    name: str = None
    award: list = field(default_factory=list)
    DOI: str = None
    ROR: str = None

@dataclass
class Resource:
    primary: dict = field(default_factory=dict)
    secondary: list = field(default_factory=list)


@dataclass
class License:
    terms_of_access: str = None
    content_version: str = None
    url: str = None
    source_of_term: str = None
    start_date: str = None
    delay_in_days: int = None
    restrictions: str = None


@dataclass
class Local:
    identifiers: dict = field(default_factory=dict)
    USDA: str = "no"
    cataloger_notes: list = field(default_factory=list)
    submitter_email: str = None
    submitter_name: str = None
    indexed_by: str = None


@dataclass
class Citation:
    title: str = None
    subtitle: str = None
    original_title: str = None
    translated_title: str = None
    publisher: str = None
    DOI: str = None
    container_title: list[str] = field(default_factory=list)
    ISSN: dict = field(default_factory=dict)
    funder: list[Funder] = field(default_factory=list)
    _author: list[Author] = field(default_factory=list)
    resource: Resource = None
    type: str = "journal-article"
    abstract: str = None
    date: dict = field(default_factory=dict)
    volume: str = None
    issue: str = None
    _page: dict = field(default_factory=dict)
    license: list[License] = field(default_factory=list)
    URL: str = None
    local: Local = None
    container_DOI: str = None
    subjects: dict = field(default_factory=dict)

    def container_title_str(self):
        if isinstance(self.container_title, list):
            return ": ".join(self.container_title)
        return self.container_title

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, new_author):
        if not isinstance(new_author, Author):
            raise ValueError(
                "Can only add objects of type Author to author field"
            )
        self._author.append(new_author)

    @property
    def page(self):
        return self._page

    @page.setter
    def page_first_last(self, page_tuple):
        if page_tuple[0] not in {None, ""} and page_tuple[1] not in {None, ""}:
            page_dict = {
                'first_page': page_tuple[0],
                'last_page': page_tuple[1],
                'page_str': f'{page_tuple[0]} - {page_tuple[1]}'
            }
            self._page = page_dict
        else:
            page_dict = {
                'first_page': page_tuple[0],
                'last_page': page_tuple[1],
                'page_str': None
            }
            self._page = page_dict

    @page.setter
    def page_str(self, page_str):
        page_dict = {
            'first_page': None,
            'last_page': None,
            'page_str': page_str
        }
        self._page = page_dict

    def step3_info(self):
        obj = {}
        obj["title"] = self.title
        obj["doi"] = self.DOI
        obj["type"] = self.type
        obj["provider_rec"] = self.local.identifiers["provider_rec"]
        return obj

    def get_journal_info(self):
        journal_title = self.container_title_str()
        publisher = self.publisher
        issn = list(self.ISSN.values())
        usda = self.local.USDA
        container_doi = self.container_DOI
        journal_dict = {
            "journal_title": journal_title,
            "publisher": publisher,
            "issn": issn,
            "usda": usda,
            "container_DOI": container_doi
        }
        return journal_dict
