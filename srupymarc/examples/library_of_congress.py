import srupymarc
import sys

LOC_BASE = "http://lx2.loc.gov:210/LCDB?"


def loc_search(isbn, sru_base):
    loc_lcc = None
    try:
        records = srupymarc.searchretrieve(sru_base, query=isbn, output_format="flatten")
        record = records[0]
        fields = record.get("datafield", [])
        for field in fields:
            if field["tag"] != "050":
                continue
            if len(field.get("subfield", [])) > 0:
                loc_lcc = field["subfield"][0]["text"]
                break
    except Exception as e:
        print("Error: %s" % e, file=sys.stderr)
        return None
    return loc_lcc


isbn = "0062509470"
result = loc_search(isbn, LOC_BASE)
print(f"Tag 050 of ISBN '{isbn}': {result}")
