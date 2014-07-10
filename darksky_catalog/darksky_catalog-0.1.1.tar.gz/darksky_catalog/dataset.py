
# These are datasets which live inside a catalog.  Note that we are not
# attempting to replicate Dublin Core here.  This is a minimal implementation,
# designed to expand at later times.

import numpy as np

dataset_type_registry = {}
import yt
from yt.utilities.sdf import load_sdf 

class DarkSkyDataset:
    name = None
    url = None
    parent = None
    children = None
    authors = None
    uuid = None
    _attrs = ('name', 'url', 'authors', 'uuid')

    class __metaclass__(type):
        def __init__(cls, name, b, d):
            type.__init__(cls, name, b, d)
            if hasattr(cls, "dataset_type"):
                dataset_type_registry[cls.dataset_type] = cls
            attrs = d['_attrs']
            for base in b:
                attrs += getattr(base, '_attrs', ())
            cls._attrs = attrs

    def __init__(self, parent, attr_dict):
        for attr in self._attrs:
            setattr(self, attr, attr_dict[attr])
        self.parent = parent
        self.attr_dict = attr_dict

    @staticmethod
    def create(parent, dataset_def):
        dataset_type = dataset_def['dataset_type']
        cls = dataset_type_registry[dataset_type]
        return cls(parent, dataset_def)

    def load(self, *args, **kwargs):
        raise NotImplementedError

    def __repr__(self):
        return "%s: %s" % (self.__class__.__name__, self.name)

    @property
    def serialized(self):
        d = {}
        if self.children is not None:
            d['children'] = [c.serialized for c in self.children]
        for attr in self._attrs:
            if attr in ("children", "parent"): continue
            d[attr] = getattr(self, attr)
        d['dataset_type'] = self.dataset_type
        return d

def _get_midx_filename(index_files, midx):
    if midx == -1:
        index_file = index_files[-1]
    elif midx is not None:
        midx_ext = ".midx%s" % midx
        index_file = [i for i in index_files
                      if i.endswith(midx_ext)][0]
    else:
        index_file = None
    return index_file

class DarkSkySDFHaloCatalog(DarkSkyDataset):
    dataset_type = "sdf_halo_catalog"
    _attrs = ('nhalos', 'sort_order', 'index_files')
    
    def load(self, bounding_box = None, midx = None):
        if midx == True:
            midx = self.index_files[0]
        index_file = _get_midx_filename(self.index_files, midx)
        ds = yt.load(self.url, midx_filename = index_file)
        return ds

class DarkSkyFilteredHaloCatalog(DarkSkyDataset):
    dataset_type = "filtered_halo_catalog"
    _attrs = ('filter_desc', 'halo_catalog')

    def load(self):
        filtered_halos = load_sdf(self.url)
        return filtered_halos

    def get_halo(self, n):
        ds = self.load()
        offset = ds['id'][n]
        catalog = self.parent[self.halo_catalog].load(midx = -1)
        halo = catalog.sdf_container.structs[-1][offset][0]
        return halo

class DarkSkySDFFullOutput(DarkSkyDataset):
    dataset_type = "sdf_full_output"
    _attrs = ('nparticles', 'sort_order', 'index_files')

    def load(self, bounding_box = None, midx = None):
        if midx == True:
            midx = self.index_files[0]
        index_file = _get_midx_filename(self.index_files, midx)
        ds = yt.load(self.url, midx_filename = index_file,
                     bounding_box=bounding_box)
        return ds
