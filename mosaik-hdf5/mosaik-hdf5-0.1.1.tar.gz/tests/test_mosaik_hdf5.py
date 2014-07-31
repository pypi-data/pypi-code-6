from os.path import dirname, join

import h5py
import mosaik
import pytest

from .support import compare_hdf5


sim_config = {
    'Sim': {'python': 'example_sim.mosaik:ExampleSim'},
    'DB': {'python': 'mosaik_hdf5:MosaikHdf5'},
}


@pytest.yield_fixture
def world():
    world = mosaik.World(sim_config)
    yield world
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

    world.run(until=duration)

    results = h5py.File(dbname, 'r')
    expected = h5py.File(join(dirname(__file__), 'data', 'testdb.hdf5'), 'r')
    assert compare_hdf5(results, expected)
