import tomli
import sqlite3
from rdflib import Graph, URIRef
import os
import argparse

config = os.getenv("COGITO_CONFIG")
if not config:
    raise ValueError("Environment variable COGITO_CONFIG is not set.")
with open(config, "rb") as f:
    config_data = tomli.load(f)
database_file = config_data.get("database_file", None)
if database_file is None:
    raise ValueError("Database file path not found in configuration.")
source_file = config_data.get("source_file", None)
if source_file is None:
    raise ValueError("Source file path not found in configuration.")

# Connect to the SQLite database
conn = sqlite3.connect(database_file)

# Open up the source file
g = Graph()
g.parse(source_file)

nalt_pref = "https://lod.nal.usda.gov/nalt/"

# Extract and count all the unique subjects and predicates
unique_uris = {str(s).split(nalt_pref)[1] for s, p, o in g if str(s).startswith(nalt_pref)}
unique_uris_numeric = [s for s in unique_uris if s.isnumeric()]

# Create a table in the database to hold the subjects and their preferred labels
sql_query = """SELECT name FROM sqlite_master WHERE type='table';"""
cursor = conn.cursor()
_ = cursor.execute(sql_query)
existing_tables = cursor.fetchall()
print("Existing tables: ", existing_tables)

# Drop all existing tables
for table in existing_tables:
    cursor.execute(f"DROP TABLE {table[0]}")

# Create a table called "nalt_data" to hold the subjects and their preferred labels
cursor.execute(
    """
    CREATE TABLE nalt_data (
        uri TEXT PRIMARY KEY,
        preferred_label TEXT UNIQUE,
        broader_terms TEXT,
        type TEXT
    )
    """
)

# Add subject uris, preferred labels and broader terms to the database
prefLab = URIRef("http://www.w3.org/2004/02/skos/core#prefLabel")
for uri in unique_uris_numeric:
    uriref = URIRef(f"{nalt_pref}{uri}")
    # Get the preferred label for the subject
    preferred_labels = g.objects(subject=uriref, predicate=prefLab)
    if preferred_labels:
        # Get the preferred label in English
        labels = [label for label in preferred_labels if label.language == "en"]
        if len(labels) > 1:
            print(f"Multiple preferred labels found for {uri}: {labels}")
            continue
        elif len(labels) == 0:
            continue
        label = labels[0]

        # Query all broader terms for the subject
        sparql_query = f"""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT ?broader_uri
        WHERE {{
            <{uriref}> skos:broader* ?broader_uri .

            FILTER (?broader_uri != <{uriref}>)
        }}
        """
        # Execute the SPARQL query
        results = g.query(sparql_query)
        broader_terms = ",".join([str(row[0]).split(nalt_pref)[1] for row in results])

        # Find type of the subject
        type = "T"
        type_triples = g.triples((uriref, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), None))
        for s, p, o in type_triples:
            if o == URIRef("https://lod.nal.usda.gov/naltv#Geographical"):
                type = "G"
                break

        cursor.execute(
            "INSERT INTO nalt_data (uri, preferred_label, broader_terms, type) VALUES (?, ?, ?, ?)",
            (uri, str(label), broader_terms, type)
        )
conn.commit()
conn.close()
