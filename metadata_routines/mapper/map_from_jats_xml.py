"""
Parse a JATS XML file and map it to a citation.
"""

from lxml import etree
from citation import Citation, Local, Author
from mapper import utils
import re


def map_from_jats_xml(xml_string):
    """
    Map data from JATS XML to a Citation object.

    Args:
        xml_string: XML string containing JATS data

    Returns:
        Citation: Citation object containing data from JATS XML
    """
    # Parse XML
    try:
        root = etree.fromstring(xml_string.encode('utf-8') if isinstance(xml_string, str) else xml_string)

        # Create citation object
        citation = Citation()

        # Extract article title
        title_elem = root.find(".//article-title")
        if title_elem is not None:
            citation.title = utils.xml_text_cleanup(title_elem)

        # Extract abstract (preserve <sup> tags if needed)
        abstract_elem = root.find(".//abstract")
        if abstract_elem is not None:
            citation.abstract = utils.xml_text_cleanup(abstract_elem)

        # Extract authors
        contrib_group = root.findall(".//contrib-group/contrib[@contrib-type='author']")
        for contrib in contrib_group:
            new_author = Author()
            new_author.given = contrib.findtext(".//given-names")
            new_author.family = contrib.findtext(".//surname")
            orcid = contrib.findtext(".//contrib-id[@contrib-id-type='orcid']")
            if orcid:
                new_author.orcid = orcid.strip()
            # Find xref aff
            aff_list = contrib.findall(".//xref[@ref-type='aff']")
            if aff_list:
                new_author.affiliation = []
                for aff in aff_list:
                    rid_value = aff.get("rid")
                    if rid_value:
                        aff_elem = root.find(f".//aff[@id='{rid_value}']")
                        if aff_elem is not None:
                            aff_children = list(aff_elem)
                            aff_str = ""
                            for elem in aff_children:
                                if elem.text is not None:
                                    if elem.tag != "label":
                                        if len(aff_str) > 0:
                                            aff_str += ", "
                                        aff_str += re.sub(r'\n\s*', ' ', elem.text.strip())
                                    else:
                                        aff_str += re.sub(r'\n\s*', ' ', elem.tail.strip())


                            new_author.affiliation.append(aff_str)
            citation.author = new_author

        # Extract DOI
        doi_elem = root.find(".//article-id[@pub-id-type='doi']")
        if doi_elem is not None and doi_elem.text:
            citation.DOI = doi_elem.text.strip()

        citation.local = Local()

        pub_id_elem = root.find(".//article-id[@pub-id-type='publisher-id']")
        if pub_id_elem is not None and pub_id_elem.text:
            citation.local.identifiers['publisher-id'] = pub_id_elem.text.strip()

        # Extract journal info
        journal_title = root.find(".//journal-title")
        if journal_title is not None:
            citation.container_title = journal_title.text.strip()

        # Extract ISSN
        citation.ISSN = {'issn': None, 'e-issn': None, 'p-issn': None}
        p_issn = root.find(".//issn[@pub-type='ppub']")
        if p_issn is None:
            p_issn = root.find(".//issn[@publication-format='print']")
        if p_issn is not None and p_issn.text:
            citation.ISSN['p-issn'] = p_issn.text.strip()
        e_issn = root.find(".//issn[@pub-type='epub']")
        if e_issn is None:
            e_issn = root.find(".//issn[@publication-format='online']")
        if e_issn is not None and e_issn.text:
            citation.ISSN['e-issn'] = e_issn.text.strip()

        # Extract publisher name
        publisher_elem = root.find(".//publisher")
        if publisher_elem is not None:
            publisher_name = publisher_elem.findtext(".//publisher-name")
            citation.publisher = publisher_name.strip() if publisher_name else None

        # Extract publication date
        pub_date = root.find(".//pub-date[@pub-type='ppub']")
        if pub_date is None:
            pub_date = root.find(".//pub-date[@pub-type='epub']")
        if pub_date is None:
            history = root.find(".//history")
            if history is not None:
                accepted_date = history.find(".//date[@date-type='accepted']")
                if accepted_date is not None:
                    pub_date = accepted_date
        date_dict = {}
        if pub_date is not None:
            year = pub_date.find("year").text.strip() if pub_date.find("year") is not None else None
            month = pub_date.find("month").text.strip() if pub_date.find("month") is not None else None
            day = pub_date.find("day").text.strip() if pub_date.find("day") is not None else None

            date_dict = {
                "string": utils.format_date(year, month, day),
                "year": year if year is not None else None,
                "month": month if month is not None else None,
                "day": day if day is not None else None
            }
        else:
            pub_date = root.findtext(".//copyright-year")
            if pub_date is not None:
                date_dict = {"string": pub_date.strip(), "year": pub_date.strip(), "month": None, "day": None}

        citation.date = {"published": date_dict}

        # Extract volume, issue, pages
        volume = root.find(".//volume")
        if volume is not None and volume.text:
            citation.volume = volume.text.strip()

        issue = root.find(".//issue")
        if issue is not None and issue.text:
            citation.issue = issue.text.strip()


        fpage = root.findtext(".//fpage")
        lpage = root.findtext(".//lpage")
        citation.page_first_last = (fpage.strip() if fpage is not None else None, lpage.strip() if lpage is not None else None)

        # Add subjects
        # Some subject terms may be italicized (ie species names).
        # We assume that keywords are either entirely italicized or not at all.
        author_subjects = root.findall(".//kwd-group[@kwd-group-type='author']/kwd")
        if len(author_subjects) > 0:
            uncontrolled_subjects = []
            for kwd in author_subjects:
                if len(kwd) == 0 and kwd.text:
                    uncontrolled_subjects.append({"topic": {"term": kwd.text.strip()}})
                # else if kwd has a child element with the tag 'italic':
                elif kwd.find("italic") is not None and kwd.find("italic").text:
                    uncontrolled_subjects.append({"topic": {"term": kwd.find("italic").text.strip()}})

            citation.subjects = {"Uncontrolled": uncontrolled_subjects}

        return citation, "success"
    except Exception as e:
        return None, "Faulty record: " + str(e)
