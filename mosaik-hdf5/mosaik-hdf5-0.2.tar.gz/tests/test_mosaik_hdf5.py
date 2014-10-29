from os.path import dirname, join

import h5py
import mosaik
import pytest

from .support import compare_hdf5
import mosaik_hdf5


DATA_DIR = join(dirname(__file__), 'data')

sim_config = {
    'Sim': {'python': 'example_sim.mosaik:ExampleSim'},
    'DB': {'python': 'mosaik_hdf5:MosaikHdf5'},
}


@pytest.yield_fixture
def world():
    world = mosaik.World(sim_config)
    yield world
    if world.srv_sock:
        world.shutdown()


def test_mosaik_hdf5(world, tmpdir):
    duration = 2
    sim_a = world.start('Sim')
    sim_b = world.start('Sim')
    a = sim_a.A(init_val=0)
    b = sim_b.B.create(2, init_val=0)
    for e in b:
        world.connect(a, e, ('val_out', 'val_in'))

    dbname = tmpdir.join('testdb.hdf5').strpath
    dbproc = world.start('DB', step_size=1, duration=duration)
    db = dbproc.Database(filename=dbname)
    for e in [a] + b:
        world.connect(e, db, 'val_out')

    # Store meta and static data:
    dbproc.set_meta_data({'a': 1, 'b': 'spam', 'c': [1, 2], 'd': {1: 2}})
    dbproc.set_static_data({e.full_id: {'type': e.type} for e in ([a] + b)})

    world.run(until=duration)

    results = h5py.File(dbname, 'r')
    expected = h5py.File(join(DATA_DIR, 'testdb.hdf5'), 'r')
    assert compare_hdf5(results, expected)


def test_series_path(tmpdir):
    # This pattern should make the following paths:
    #
    # - "Sim-0.Entity-1" -> "Sim/Sim-0/Sim-0.Entity-1"
    # - "PyPower-0.1-Node-2" -> "PyPower/PyPower-0.1/PyPower-0.1-Node-2"
    #
    # Note the special treatment for PyPower entities, because every entity
    # gets a grid-index prepend which we want to move to the sim ID for better
    # grouping.
    pattern = r'(((\w+)-(\d+.\d+|\d+))[.-](.*))'
    repl = r'\3/\2/\1'

    def _store_relations_mock(*args):
        yield

    dbname = tmpdir.join('test_paths.hdf5').strpath
    hdf5 = mosaik_hdf5.MosaikHdf5()
    hdf5._store_relations = _store_relations_mock
    hdf5.init('db-0', 1, 1, (pattern, repl))
    entities = hdf5.create(1, 'Database', dbname)
    gen = hdf5.step(0, {entities[0]['eid']: {
        'a': {'Sim-0.Entity-1': 23, 'PyPower-0.1-Node-2': 42},
        'b': {'Sim-0.Entity-1': 12, 'PyPower-0.1-Node-2': 24},
    }})
    next(gen)
    pytest.raises(StopIteration, next, gen)

    results = h5py.File(dbname, 'r')
    expected = h5py.File(join(DATA_DIR, 'test_paths.hdf5'), 'r')
    assert compare_hdf5(results, expected)
