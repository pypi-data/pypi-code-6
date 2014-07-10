
# This is a top-level object that will contain links to multiple datasets
# within it.
import json
import thingking
from .dataset import DarkSkyDataset

darksky = {}

class DarkSkyCatalog:
    name = None
    authors = None
    datasets = None
    catalog_url = None
    
    def __init__(self, name, catalog_url, authors, datasets):
        darksky[name] = self
        self.name = name
        self.authors = authors
        self.catalog_url = catalog_url
        self.datasets = []
        for dataset in datasets:
            # Each dataset will be a deserialized JSON entry
            self.datasets.append(DarkSkyDataset.create(self, dataset))

    def __getitem__(self, key):
        candidates = []
        for item in self.datasets:
            if key in (item.name, item.uuid):
                candidates.append(item)
        if len(candidates) != 1:
            raise KeyError(key, len(candidates))
        return candidates[0]

    @classmethod
    def from_manifest_url(self, url):
        f = thingking.httpfile(url)

    @property
    def serialized(self):
        d = {}
        d['name'] = self.name
        d['authors'] = self.authors
        d['catalog_url'] = self.catalog_url
        d['datasets'] = [ds.serialized for ds in self.datasets]
        return d

    def load(self, *args, **kwargs):
        candidate = None
        for ds in self.datasets:
            if "full_output" in ds.dataset_type:
                if candidate is not None:
                    raise RuntimeError
                candidate = ds
        if candidate is None:
            raise KeyError
        ds = candidate.load(*args, **kwargs)
        return ds

    def __repr__(self):
        return "%s: %s" % (self.__class__.__name__, self.name)

_root = "http://darksky.slac.stanford.edu/simulations/"
_authors = (["Dark Sky Simulations"],)

_ds14_a = {'name': 'ds14_a',
          'authors': _authors,
          'catalog_url': _root + 'ds14_a/',
          'datasets': [],
}

_ds14_a['datasets'] = [
    {'name': 'halos_a_1.0000',
     'authors': _authors,
     'dataset_type': 'sdf_halo_catalog',
     'url': _root + 'ds14_a/halos/ds14_a_halos_1.0000',
     'uuid': 'some_uuid',
     'nhalos': 100,
     'sort_order': 'mass',
     'authors': _authors,
     'index_files': [_root + 'ds14_a/halos/ds14_a_halos_1.0000.midx' + str(i)
                     for i in (7,8,9)],
     'filter_files': [_root + 'ds14_a/halos/ds14_a_halos_filter_1e15_1.0000'],
     },
    {'name': 'full_data_a_1.0000',
     'authors': _authors,
     'dataset_type': 'sdf_full_output',
     'url': _root + 'ds14_a/ds14_a_1.0000',
     'uuid': 'some_other_uuid',
     'nparticles': 10240**3,
     'sort_order': 'morton',
     'index_files': [_root + 'ds14_a/ds14_a_1.0000.midx10'],
     },
    {'name': 'filtered_1e15_a_1.0000',
     'authors': _authors,
     'dataset_type': 'filtered_halo_catalog',
     'halo_catalog': 'halos_a_1.0000',
     'url': _root + 'ds14_a/halos/ds14_a_halos_filter_1e15_1.0000',
     'uuid': 'another_uuid',
     'filter_desc': 'mb_200 > 1e15',
     },
]

_ds14_g = {
    'name': 'ds14_g',
    'authors': _authors,
    'catalog_url': _root + 'ds14_g/',
    'datasets': [],
}

ds14_g_params = [
    ('ds14_g_100_2048', 2048, 8),
    ('ds14_g_200_2048', 2048, 8),
    ('ds14_g_800_4096', 4096, 9),
    ('ds14_g_1600_4096', 4096, 9)
]
for (dname, np, midx_level) in ds14_g_params:
    _ds14_g['datasets'].append(
        {'name': '%s_1.0000' % dname,
         'authors': _authors,
         'dataset_type': 'sdf_full_output',
         'url': _root + 'ds14_g/%s/%s_1.0000' % (dname, dname),
         'uuid': 'uuid0',
         'nparticles': np**3,
         'sort_order': 'morton_xyz',
         'authors': _authors,
         'index_files': [
             _root + 'ds14_g/' + dname + '/' + dname + '_1.0000.midx' + str(midx_level)],
         }
    )

DarkSkyCatalog(**_ds14_a)
DarkSkyCatalog(**_ds14_g)
