import json
from citation import Citation, Author, Funder, License, Local, Resource
from mapper import utils
from mapper.errors import FaultyRecordError
from lxml import etree


def map_from_pubmed_xml(pubmed_str):
    """
    Maps a PubMed XML string to a Citation object.

    Args:
        pubmed_str (str): A string containing PubMed XML data

    Returns:
        tuple: (Citation object, str message)
    """

    # If the input string has an empty first line, remove it
    if pubmed_str.startswith("\n"):
        pubmed_str = pubmed_str[1:]
    try:
        # Parse the XML string
        root = etree.fromstring(pubmed_str.encode('utf-8'))

        # Extract article data
        article = root if root.tag == "Article" else root.find(".//Article")
        if article is None:
            raise FaultyRecordError("No Article element found")

        # Extract basic metadata
        title_elem = article.find(".//ArticleTitle")
        if title_elem is not None:
            title = utils.xml_text_cleanup(title_elem)
        else:
            title = None
        publisher = article.findtext(".//PublisherName", "")

        # Extract journal info
        journal = article.find(".//Journal")
        journal_title = journal.findtext(".//JournalTitle",
                                         "") if journal is not None else ""
        volume = journal.findtext(".//Volume", "") if journal is not None else ""
        issue = journal.findtext(".//Issue", "") if journal is not None else ""
        issn = journal.findtext(".//Issn", "") if journal is not None else ""

        # Extract publication date
        pub_date = journal.find(".//PubDate") if journal is not None else None
        year = pub_date.findtext(".//Year", "") if pub_date is not None else ""
        month = pub_date.findtext(".//Month",
                                  "") if pub_date is not None else ""
        day = pub_date.findtext(".//Day", "") if pub_date is not None else ""
        date_str = utils.format_date(year, month, day)
        date_dict = {
            "published":{
                "string": date_str,
                "year": year,
                "month": month,
                "day": day
            }
        }

        first_page = article.findtext(".//FirstPage")
        last_page = article.findtext(".//LastPage")

        # Extract DOI and other identifiers
        doi = None
        pii = None
        article_id_list = article.find("ArticleIdList")
        if article_id_list is not None:
            for article_id in article_id_list.findall(".//ArticleId"):
                if article_id.get("IdType") == "doi":
                    doi = article_id.text
                elif article_id.get("IdType") == "pii":
                    pii = article_id.text

        # Extract abstract
        abstract_elem = article.find(".//Abstract")
        if abstract_elem is not None:
            abstract = utils.xml_text_cleanup(abstract_elem)
        else:
            abstract = None
        new_local = Local()
        if pii:
            new_local.identifiers = {"pii": pii}

        # Create citation object
        new_citation = Citation(
            title=title,
            container_title=journal_title,
            ISSN={'issn': issn},
            DOI=doi,
            publisher=publisher,
            date=date_dict,
            abstract=abstract,
            volume=volume,
            issue=issue,
            local=new_local
        )

        new_citation.page_first_last = (first_page, last_page)

        # Extract authors
        author_list = article.find(".//AuthorList")
        if author_list is not None:
            for author_elem in author_list.findall(".//Author"):
                last_name = author_elem.findtext(".//LastName", "")
                first_name = author_elem.findtext(".//FirstName", "")
                affiliations = []
                for aff in author_elem.findall(".//AffiliationInfo"):
                    affiliations.append(aff.findtext(".//Affiliation", ""))
                # Find the orcid - .//Identifier with the attribute 'Source' set to 'ORCID'
                orcid = author_elem.findtext(".//Identifier[@Source='ORCID']")

                author = Author(
                    given=first_name,
                    family=last_name,
                    affiliation=", ".join(
                        affiliations) if affiliations else None,
                    orcid=orcid
                )
                new_citation.author = author

        return (new_citation, "success")

    except etree.XMLSyntaxError as e:
        raise FaultyRecordError(f"Invalid XML: {str(e)}")
    except Exception as e:
        raise FaultyRecordError(f"Error mapping PubMed XML: {str(e)}")