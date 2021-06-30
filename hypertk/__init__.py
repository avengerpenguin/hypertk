import doltcli as dolt
from rdflib import RDF, Graph, Literal


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

            iri = str(s)
            self.db.sql(
                f"insert into `{table_name}` (iri) values ('{iri}')"
                f"ON DUPLICATE KEY UPDATE iri='{iri}'"
            )

            if isinstance(o, Literal):
                col = str(p).split("/")[-1]
                col_type = type(o.toPython())
                type_map = {str: "varchar(128)"}
                self.db.sql(
                    f"""
                ALTER TABLE `{table_name}`
                ADD COLUMN `{col}` {type_map[col_type]}
                """
                )
                self.db.sql(
                    f"""
                UPDATE `{table_name}`
                SET {col} = '{o.toPython()}'
                WHERE iri='{iri}'
                """
                )
