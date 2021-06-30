import doltcli as dolt
from rdflib import RDF, Graph


class Ingest:
    def __init__(self, path):
        self.db = dolt.Dolt.init(path)

    def ingest(self, triples):
        for t in triples:
            t = t.strip()
            if not t:
                continue
            g = Graph()
            g.parse(data=t, format="nt")
            s, p, o = list(g)[0]

            if p == RDF.type:
                table_name = o.split("/")[-1].lower()
                self.db.sql(
                    f"create table if not exists `{table_name}` ("
                    "    iri varchar(30), primary key (iri)"
                    ")"
                )
