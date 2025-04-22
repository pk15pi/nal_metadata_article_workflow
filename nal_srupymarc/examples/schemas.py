import srupymarc
from pprint import pprint

# check supported schemas of server
server = srupymarc.explain("http://lx2.loc.gov:210/LCDB?")

print(f"Supported schemas: {', '.join(server.schema.keys())}")


for schema in server.schema.keys():
    print(20 * "=")
    print("=")
    print(f"= Record with schema: {schema}")
    print("=")
    print(20 * "=")
    records = srupymarc.searchretrieve(
        "http://lx2.loc.gov:210/LCDB?", query="human", record_schema=schema,
        output_format="flatten"
    )
    pprint(records[0])
    print("")
    print("")
