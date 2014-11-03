import os
import tempfile
import zipfile
import shutil

from osgeo import ogr


def import_shape_from_zip(session, importer, zippath):
    tempdir = tempfile.mkdtemp()
    try:
        # all files must be extracted as they are inspected by the shape file reader
        with zipfile.ZipFile(zippath) as zobj:
            zobj.extractall(tempdir)
        # there is only one .shp file
        shpname = (x for x in os.listdir(tempdir) if x.lower().endswith('.shp')).next()
        shppath = os.path.join(tempdir, shpname)
        importer(session, shppath)
    finally:
        shutil.rmtree(tempdir)


def import_shape_from_shp(session, importer, shppath):
    importer(session, shppath)


class _CollectionProperties(object):
    def __init__(self, feature):
        self.feature = feature

    def __getitem__(self, name):
        value = self.feature[name]
        if isinstance(value, str):
            return value.decode('latin1')
        else:
            return unicode(value)

    def GetGeometryRef(self):
        return self.feature.GetGeometryRef()


class _Collection(object):

    def __init__(self, filepath):
        self.collection = ogr.Open(filepath)
        self.layer = self.collection.GetLayer()


    def __enter__(self):
        return self

    def __exit__(self, *args):
        return

    def __iter__(self):
        for idx in xrange(self.layer.GetFeatureCount()):
            yield _CollectionProperties(self.layer.GetFeature(idx))

