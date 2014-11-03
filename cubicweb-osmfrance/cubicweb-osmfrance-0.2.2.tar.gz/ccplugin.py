from cubicweb.toolsutils import Command
from cubicweb.cwctl import CWCTL
from cubicweb.server.serverconfig import ServerConfiguration
from cubicweb.server.serverctl import repo_cnx

from cubes.osmfrance.import_shp import (import_shape_from_zip,
                                        import_shape_from_shp)

from cubes.osmfrance.import_osm import (import_regions,
                                        import_departements,
                                        import_arrondissements,
                                        import_epci,
                                        import_communes)


class AbstractImportCommand(Command):

    def _run(self):
        cnf = self.config
        if cnf.regions:
            self._import_shape(import_regions, cnf.regions)
        if cnf.departements:
            self._import_shape(import_departements, cnf.departements)
        if cnf.arrondissements:
            self._import_shape(import_arrondissements, cnf.arrondissements)
        if cnf.epci:
            self._import_shape(import_epci, cnf.epci)
        if cnf.communes:
            self._import_shape(import_communes, cnf.communes)
        self.session.commit()

    def run(self, args):
        appid = args.pop(0)
        config = ServerConfiguration.config_for(appid)
        repo, cnx = repo_cnx(config)
        self.session = repo._get_session(cnx.sessionid, setcnxset=True)
        try:
            self._run(*args)
        except:
            cnx.rollback()
            raise
        finally:
            cnx.close()


class OSMFranceImportCommand(AbstractImportCommand):
    '''Import shape from zip file.'''

    name = 'osmfrance_import_shp'
    arguments = '<instance>'

    options = [
        ('regions',
         {'short': 'r', 'type': 'string', 'default': None,
          'help': 'zip shape file path for "regions"',
         }),
        ('departements',
         {'short': 'd', 'type': 'string', 'default': None,
          'help': 'zip shape file path for "departements"',
         }),
        ('communes',
         {'short': 'c', 'type': 'string', 'default': None,
          'help': 'zip shape file path for "communes"',
        }),
        ('epci',
         {'short': 'e', 'type': 'string', 'default': None,
          'help': 'zip shape file path for "EPCI"',
        }),
        ('arrondissements',
         {'short': 'a', 'type': 'string', 'default': None,
          'help': 'zip shape file path for "arrondissements"',
        }),
    ]

    def _import_shape(self, importer, zippath):
        import_shape_from_zip(self.session, importer, zippath)


class IGNImportCommand(AbstractImportCommand):
    '''Import shape from SHP file.'''

    name = 'ign_import_shp'
    arguments = '<instance>'

    options = [
        ('departements',
         {'short': 'd', 'type': 'string', 'default': None,
          'help': 'SHP file path for "departements"',
         }),
        ('communes',
         {'short': 'c', 'type': 'string', 'default': None,
          'help': 'SHP file path for "communes"',
        }),
        ('arrondissements',
         {'short': 'a', 'type': 'string', 'default': None,
          'help': 'SHP file path for "arrondissements"',
        }),
    ]

    def _import_shape(self, importer, shppath):
        import_shape_from_shp(self.session, importer, shppath)


CWCTL.register(OSMFranceImportCommand)
CWCTL.register(IGNImportCommand)
