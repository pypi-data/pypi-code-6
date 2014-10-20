from cassandra.cluster import Cluster
from pandas import DataFrame, read_fwf
import pytest
from ironeagle import get_prepared_statement, save_dataframe_to_cassandra


@pytest.fixture
def session():
    cluster = Cluster()
    session = cluster.connect("ironeagle")

    create = """
              CREATE TABLE IF NOT EXISTS simple (
              id int primary key,
              name text,
              lat float
              )
              """

    truncate = "truncate simple"

    create_station = """CREATE TABLE if not exists station (
                    station_id text primary key,
                    lat float,
                    long float,
                    elevation float,
                    state text,
                    name text,
                    gsn_flag text,
                    hcn_flag text,
                    wmo_id text
                )
                """

    trunate_station = "truncate station"

    queries = [create, truncate, create_station, trunate_station]

    for q in queries:
        session.execute(q)
    return session


@pytest.fixture
def df():
    df = DataFrame.from_records([(1, "jon", 1.1), (2, "pete", 1.2)],
                                    columns=['id', 'name', 'lat'])
    return df


@pytest.fixture
def stations():
    stations = read_fwf("tests/ghcnd-stations.txt", header=None,
                        colspecs=[(0,11), (12, 20), (21, 30), (31,37), (38,40), (41,71), (72,75), (76,79), (80,85)],
                        names=["station_id", "lat", "long", "elevation", "state", "name", "gsn_flag", "hcn_flag", "wmo_id"])

    stations['wmo_id'] = stations['wmo_id'].astype(str)
    return stations


def test_get_prepared_statement(df):
    prepared = get_prepared_statement(df, "simple")
    assert "id, name" in prepared
    assert "(?,?,?)" in prepared

def test_insert_data(df, session):
    save_dataframe_to_cassandra(session, df, "simple")



def test_station_data(session, stations):
    save_dataframe_to_cassandra(session, stations, "station")
