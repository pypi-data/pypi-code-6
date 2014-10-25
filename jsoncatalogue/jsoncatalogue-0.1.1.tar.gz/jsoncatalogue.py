import json
import os

class Catalogue():
    """Catalogue of JSON documents (e.g. for JSON Schema validation)
    >>> catalogue = Catalogue()
    >>> catalogue.add_directory("catalog")
    >>> catalogue.add_directory("../other/catalog")
    >>> catalogue.store
    {"http://exam.ple/schema/one.json": {...},
     "http://exam.ple/schema/two.json": {...},
     "http://wordnik.github.io/schema/v1.2/apiAuthentication.json": {...}
     "http://no.extensi.on/schema/pets": {...}
     }

    This catalogue.store can be assigned e.g. to `jsonschema` validator

    >>> from jsonschema import Draft4Validator
    >>> validator = Draft4Validator()
    >>> validator.resolver.store = catalogue.store

    From now on, validator will know about schemas from catalogue
    """
    def __init__(self, rootdir=None, fail_callback=None):
        """
        `rootdir` .. path to directory, where are files located.
        first subdirectory is typically "http", "https" and servers
        as protocol name.
        for rootdir "../catalogue" we might find
            - ../catalogue/http/wordnik.github.io/schemas/v1.2/apiDeclaration.json
            - ../catalogue/http/wordnik.github.io/schemas/v1.2/infoObject.json

        `fail_callback` is callable called at json load failure
        getting three parameters: rootpath, file_path, exception
        e.g. fail_callback("../catalogue", "http/wordnik.github.io/schemas/v1.2/apiDeclaration.json",
        Exception(...))
        """

        self.store = {}
        self.fail_callback = fail_callback
        if rootdir:
            self.add_directory(rootdir)

    def add_directory(self, rootdir):
        for path in self._find_all_files(rootdir):
            fullpath = os.path.join(rootdir, path)
            uri = self._path2uri(path)
            try:
                with open(fullpath) as f:
                    self.store[uri] = json.load(f)
            except Exception as e:
                if self.fail_callback:
                    self.fail_callback(rootdir, path, e)
                else:
                    raise e

    @staticmethod
    def _path2uri(pth):
        pth = pth.replace("\\", "/")
        pth = pth.strip("./")
        proto, rest = pth.split("/", 1)
        return proto + "://" + rest

    @staticmethod
    def _find_all_files(directory):
        dirlen = len(directory)
        for root, dirs, files in os.walk(directory):
            for basename in files:
                res = os.path.join(root, basename)[dirlen+1:]
                yield res
