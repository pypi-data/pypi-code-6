# -*- coding: utf-8 -*-
# :Progetto:  PatchDB -- Data loader from YAML
# :Creato:    mer 10 feb 2010 14:35:05 CET
# :Autore:    Lele Gaifax <lele@metapensiero.it>
# :Licenza:   GNU General Public License version 3 or later
#

"""
Load new instances in the database, or update existing ones, given a
data structure represented by a YAML stream, as the following::

    - entity: gam.model.Fascicolo
      key: descrizione
      # no data, just "declare" the entity

    - entity: gam.model.TipologiaFornitore
      key: tipologiafornitore
      data:
        - &tf_onesto
          tipologiafornitore: Test fornitori onesti

    - entity: gam.model.ClienteFornitore
      key: descrizione
      data:
        - descrizione: Test altro fornitore onesto
          tipologiafornitore: *tf_onesto
          partitaiva: 01234567890
        - &cf_lele
          codicefiscale: GFSMNL68C18H612V
          descrizione: Dipendente A

    - entity: gam.model.Dipendente
      key: codicefiscale
      data:
        - &lele
          codicefiscale: GFSMNL68C18H612V
          nome: Emanuele
          cognome: Gaifas
          clientefornitore: *cf_lele
          foto: !File {path: ../img/lele.jpg}

    - entity: gam.model.Attrezzature
      key: descrizione
      data:
        - &macchina
          descrizione: Fiat 500

    - entity: gam.model.Prestiti
      key:
        - dipendente
        - attrezzatura
      data:
        - dipendente: *lele
        - attrezzatura: *macchina
"""

from logging import getLogger
from os.path import abspath, dirname, join, normpath
import sys

from yaml import YAMLObject


logger = getLogger(__name__)

if sys.version_info >= (3,):
    basestring = str


class File(YAMLObject):
    """Facility to read the content of an external file.

    A field may be loaded from an external file, given its pathname
    which is interpreted as relative to the position of the YAML file
    currently loading::

        - entity: cpi.models.Document
          key: filename
          data:
            - filename: image.gif
              content: !File {path: ../image.gif}
    """

    yaml_tag = u'!File'

    basedir = None

    def __init__(self, path):
        self.path = path

    def read(self):
        fullpath = normpath(join(self.basedir, self.path))
        return open(fullpath).read()


class Entity(object):
    """Model instances factory."""

    def __init__(self, model, key, data=None):
        self.model = resolve_class_name(model)
        if isinstance(key, basestring):
            key = [key]
        self.key = key
        if isinstance(data, dict):
            data = [data]
        self.data = data

    def __repr__(self):
        return "%s(model=%r, key=%r)" % (
            self.__class__.__name__,
            self.model, self.key)

    def __call__(self, session, idmap, adaptor=None):
        """Create and or update a sequence of instances.

        :param adaptor: either None or a callable
        :rtype: an iterator over created/referenced instances
        """

        instances = self.data
        if instances is None:
            return

        for data in instances:
            if adaptor is not None:
                data = adaptor(self.model, self.key, data)
            instance = Instance(self, data, idmap)
            yield instance(session)


class Instance(object):
    """A single model instance."""

    def __init__(self, entity, data, idmap):
        self.entity = entity
        self.data = data
        self.idmap = idmap
        self.instance = None

    def __getitem__(self, key):
        item = self.data.get(key, None)
        if id(item) in self.idmap:
            return self.idmap[id(item)]
        else:
            return item

    def __call__(self, session):
        "Load an existing instance or create a new one."

        from sqlalchemy.orm import object_mapper

        if self.instance is not None:
            return self.instance

        model = self.entity.model
        key = self.entity.key

        filter = {}
        for fname in key:
            fvalue = self[fname]
            if isinstance(fvalue, basestring):
                filter[fname] = unicode(fvalue)
            elif isinstance(fvalue, Instance):
                instance = fvalue(session)

                mapper = object_mapper(instance)
                pkeyf = mapper.primary_key
                pkeyv = mapper.primary_key_from_instance(instance)
                pkey = {f.name: v for f, v in map(None, pkeyf, pkeyv)}

                for l, r in getattr(model, fname).property.local_remote_pairs:
                    filter[l.name] = pkey[r.name]
            else:
                filter[fname] = fvalue

        q = session.query(model)
        q = q.filter_by(**filter)
        obj = q.first()
        if obj is None:
            # Create a new one
            obj = model()
            session.add(obj)

        self.idmap[id(self.data)] = self
        self.instance = obj

        # Update it
        for f in self.data:
            v = self[f]
            if isinstance(v, Instance):
                v = v(session)
            elif isinstance(v, File):
                v = v.read()

            setattr(obj, f, v)

        return obj


def resolve_class_name(classname):
    """Import a particular Python class given its full dotted name.

    :param classname: full dotted name of the class,
                      such as "package.module.ClassName"
    :rtype: the Python class
    """

    modulename, _, classname = classname.rpartition('.')
    module = __import__(modulename, fromlist=[classname])
    return getattr(module, classname)


def load_yaml(fname, session, dry_run=False, adaptor=None, show_progress=False):
    """Load a single YAML file.

    :param fname: the name of the YAML file to load
    :param session: the SQLAlchemy session
    :param dry_run: whether to commit data at the end
    :param adaptor: either None or a function
    :rtype: dict
    :returns: A dictionary with loaded data, keyed by (model class, key): each
              value is a tuple (primarykey, datadict)

    This will open the given file (that should contain a UTF-8 encoded
    YAML structure) and will load/update the data into the database.

    The `adaptor` function, if specified, will be called once for each "record"
    and has the opportunity of deliberately change its content::

        user_id = 999

        def adjust_user(cls, key, data):
            if key == ['username']:
                data['username'] = data['username'] + str(user_id)
                data['user_id'] = user_id
            return data

        load_yaml('testdata.yaml', session, adaptor=adjust_user)

    When `dry_run` is ``False`` (the default) the function performs a
    ``flush()`` on the SQLAlchemy session, but does **not** commit the
    transaction.
    """

    from codecs import open
    from yaml import Loader
    from sys import stderr
    from sqlalchemy.orm import object_mapper

    if show_progress:
        stderr.write(fname)
        stderr.write(u': ')

    stream = open(fname, 'r', 'utf-8')

    # Set the base directory: file paths will be considered relative
    # to the directory containing the YAML file
    File.basedir = dirname(abspath(fname))

    idmap = {}
    loader = Loader(stream)
    while loader.check_data():
        entities = loader.get_data()
        for data in entities:
            entity = Entity(data['entity'], data['key'], data.get('data', []))
            for e in entity(session, idmap, adaptor):
                if show_progress:
                    stderr.write('.')

        if not dry_run:
            logger.debug(u"Flushing changes")
            session.flush()

    if show_progress:
        stderr.write('\n')

    result = {}
    for i in idmap.values():
        if len(i.entity.key) == 1:
            key = getattr(i.instance, i.entity.key[0])
        else:
            key = tuple(getattr(i.instance, k) for k in i.entity.key)
        mapper = object_mapper(i.instance)
        pk = mapper.primary_key_from_instance(i.instance)
        if len(pk) == 1:
            pk = pk[0]
        result[(i.entity.model, key)] = pk, i.data

    return result


def load(uri, dry_run, echo, args):
    "Load one or more YAML file into the database."

    from sqlalchemy import create_engine
    from sqlalchemy.exc import SQLAlchemyError
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(uri, echo=echo)
    salogger = getattr(engine.logger, 'logger', None)
    if salogger is not None:
        for h in salogger.handlers:
            salogger.removeHandler(h)
    smaker = sessionmaker(autoflush=False, autocommit=False, bind=engine)

    session = smaker()

    try:
        for fname in args:
            load_yaml(fname, session, dry_run, show_progress=True)
    except SQLAlchemyError as e:
        # PG errors are UTF-8 encoded
        logger.error(u"Data couldn't be loaded: %s", str(e).decode('utf-8'))
        return 1
    except Exception:
        logger.exception(u"We are in trouble, unexpected error!")
        return 2
    else:
        if not dry_run:
            logger.info(u"Committing changes")
            session.commit()

    return 0 # OK


def main():
    import locale, logging, sys
    from argparse import ArgumentParser, RawDescriptionHelpFormatter

    locale.setlocale(locale.LC_ALL, '')

    parser = ArgumentParser(
        description="Load and/or update DB model instances.",
        epilog=__doc__, formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument("datafile", nargs="+",
                        help="The YAML data file to load.")
    parser.add_argument("-u", "--sqlalchemy-uri", type=str, metavar="URI",
                        help=u"Specify the SQLAlchemy URI.", default=None)
    parser.add_argument("-n", "--dry-run", default=False, action="store_true",
                        help=u"Don't commit the changes to the database.")
    parser.add_argument("-e", "--echo", default=False, action="store_true",
                        help=u"Activate SA engine echo")
    parser.add_argument("-w", "--unicode-warnings", default=False,
                        action="store_true",
                        help=u"Activate SA unicode warnings")

    logging.basicConfig(format='%(message)s')

    args = parser.parse_args()

    if args.sqlalchemy_uri is None:
        print(u"You must specify the SQLAlchemy URI, example:")
        print(u"  python %s -u postgres://localhost/dbname data.yaml"
              % sys.argv[0])

        return 128

    if not args.unicode_warnings:
        import warnings
        from sqlalchemy.exc import SAWarning

        warnings.filterwarnings(
            'ignore', category=SAWarning,
            message="Unicode type received non-unicode bind param value")

    return load(args.sqlalchemy_uri, args.dry_run, args.echo, args.datafile)


if __name__ == '__main__':
    from sys import exit

    exit(main())
