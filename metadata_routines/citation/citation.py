from dataclasses import dataclass, field


@dataclass
class Author:
    given: str = None
    family: str = None
    orcid: str = None
    affiliation: list = field(default_factory = list)
    sequence: str = None


@dataclass
class Funder:
    name: str = None
    award: list = field(default_factory = list)


@dataclass
class License:
    version: str = None
    url: str = None


@dataclass
class Local:
    manuscript_file: str = None
    supplementary_files: list = field(default_factory = list)
    submission_date: str = None
    modification_date: str = None
    date_other: str = None
    identifiers: dict = field(default_factory = dict)
    USDA: str = "no"
    cataloger_notes: list = field(default_factory = list)
    submitter_email: str = None
    submitter_name: str = None


@dataclass
class Citation:
    title: str = None
    subtitle: str = None
    original_title: str = None
    publisher: str = None
    DOI: str = None
    container_title: str = None
    ISSN: dict = field(default_factory = dict)
    funder: list[Funder] = field(default_factory = list)
    _author: list[Author] = field(default_factory = list)
    type: str = "journal-article"
    abstract: str = None
    publication_date: list = field(default_factory = list)
    volume: str = None
    issue: str = None
    _page: dict = field(default_factory = dict)
    license: list[License] = field(default_factory = list)
    URL: str = None
    local: Local = None
    container_DOI: str = None

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, new_author):
        if not isinstance(new_author, Author):
            raise ValueError("Can only add objects of type Author to author field")
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
        journal_title = self.container_title
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