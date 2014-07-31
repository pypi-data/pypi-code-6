"""
Store mosaik simulation data in an HDF5 database.

"""
import h5py
import mosaik_api
import networkx as nx
import numpy as np


__version__ = '0.1.1'
meta = {
    'models': {
        'Database': {
            'public': True,
            'any_inputs': True,
            'params': ['filename', 'buf_size', 'dataset_opts'],
            'attrs': [],
        },
    },
}


class MosaikHdf5(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(meta)
        self.sid = None
        self.eid = 'hdf5db'
        self.step_size = None
        self.duration = None
        self.db = None
        self.rels = None
        self.series = None
        self.dataset_opts = {'compression': 'lzf'}

        self.buf_size = None
        self.data_buf = {}

    def init(self, sid, step_size, duration):
        self.sid = sid
        self.step_size = step_size
        self.duration = duration
        return self.meta

    def create(self, num, model, filename, buf_size=1000, dataset_opts=None):
        if num != 1 or self.db is not None:
            raise ValueError('Can only create one database.')
        if model != 'Database':
            raise ValueError('Unknown model: "%s"' % model)

        self.buf_size = buf_size
        if dataset_opts:
            self.dataset_opts.update(dataset_opts)

        self.db = h5py.File(filename, 'w')
        self.rels = self.db.create_group('Relations')
        self.series = self.db.create_group('Series')

        return [{'eid': self.eid, 'type': model, 'rel': []}]

    def step(self, time, inputs):
        assert len(inputs) == 1
        inputs = inputs[self.eid]

        # Store relations
        if time == 0:
            # Only do this once at the first step() call
            data = yield self.mosaik.get_related_entities()
            nxg = nx.Graph()
            nxg.add_nodes_from(data['nodes'].items())
            nxg.add_edges_from(data['edges'])
            for node, neighbors in sorted(nxg.adj.items()):
                if node == '%s.%s' % (self.sid, self.eid):
                    continue
                rels = np.array(sorted(n.encode() for n in neighbors),
                                dtype=bytes)
                self.rels.create_dataset(node, data=rels, **self.dataset_opts)

            ds_size = self.duration // self.step_size

        # Store series
        g_series = self.series
        buf_size = self.buf_size
        buf = self.data_buf
        abs_idx = time // self.step_size
        rel_idx = abs_idx % buf_size
        for attr, data in inputs.items():
            for src_id, value in data.items():
                key = '%s/%s' % (src_id, attr)
                if time == 0:
                    # Create datasets
                    try:
                        g = g_series[src_id]
                    except KeyError:
                        g = g_series.create_group(src_id)
                    dtype = np.dtype(type(value))
                    g.create_dataset(attr, (ds_size,), dtype=dtype,
                                     **self.dataset_opts)
                    buf[key] = np.empty(buf_size, dtype=dtype)

                # Buffer data to improve performance
                buf[key][rel_idx] = value

        buf_len = rel_idx + 1
        last_step = bool(time + self.step_size >= self.duration)
        if buf_len == buf_size or last_step:
            # Write and clear buffer
            start = abs_idx - rel_idx
            end = start + buf_len
            for key, val in buf.items():
                g_series[key][start:end] = buf[key][:buf_len]

        return time + self.step_size

    def get_data(self, outputs):
        raise RuntimeError('mosaik_hdf5 does not provide any outputs.')


def main():
    desc = __doc__.strip()
    mosaik_api.start_simulation(MosaikHdf5(), desc)
