from cassandra.cluster import Cluster
from pandas import DataFrame
import pytest
from ironeagle import get_prepared_statement, save_dataframe_to_cassandra


@pytest.fixture
def session():
    cluster = Cluster()
    session = cluster.connect("ironeagle")

    create = """
              CREATE TABLE IF NOT EXISTS simple (
              id int primary key,
              name text
              )
              """

    truncate = "truncate simple"

    queries = [create, truncate]

    for q in queries:
        session.execute(q)
    return session


@pytest.fixture
def df():
    df = DataFrame.from_records([(1, "jon"), (2, "pete")],
                                columns=['id', 'name'])
    return df



def test_get_prepared_statement(df):
    prepared = get_prepared_statement(df, "simple")
    assert "id, name" in prepared
    assert "(?,?)" in prepared

def test_insert_data(df, session):
    save_dataframe_to_cassandra(session, df, "simple")
