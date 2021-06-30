import doltcli as dolt

from hypertk import Ingest


def test_create_table_from_class(tmp_path):
    ingest = Ingest(tmp_path)
    triples = """
    <http://example.com/thing/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.com/classes/Thing> .
    """.splitlines()
    ingest.ingest(triples)

    db = dolt.Dolt(tmp_path)
    assert ["thing"] == [table.name for table in db.ls()]


def test_create_table_idempotent(tmp_path):
    ingest = Ingest(tmp_path)
    triples = """
    <http://example.com/thing/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.com/classes/Thing> .
    <http://example.com/thing/1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.com/classes/Thing> .
    """.splitlines()
    ingest.ingest(triples)

    db = dolt.Dolt(tmp_path)
    assert ["thing"] == [table.name for table in db.ls()]
