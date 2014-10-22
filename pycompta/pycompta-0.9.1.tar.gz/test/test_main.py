# -*- coding: iso-8859-1 -*-

"""
PyCompta

Ce module rassemble les tests unitaires.
"""

__revision__ = "$Id: test_main.py,v 1.5 2006-04-23 13:58:09 nico Exp $"

from logilab.common import testlib
from pycompta import main, Date, RelativeDateTime
import StringIO

class ConfigDictTC(testlib.TestCase) :
    """Test du dictionnaire de config"""

    def read_config(self) :
        CF_FILE = """key = value
            key2 = value2 # comment
            # comment

            key3 = value3
            """
        cf = main.read_config(StringIO.StringIO(CF_FILE))
        self.assertEqual(cf['key'], 'value')
        self.assertEqual(cf['key2'], 'value2')
        self.assertEqual(cf['key3'], 'value3')
        self.assertEqual(len(cf), 3)

    def test_normalize(self) :
        self.skipTest('fix or remove this')
        CF = {'repertoire_cible':'cible',
              'exercice_precedent':'ex_prec',
              'repertoire_source':'source',
              'exercice':'EXERC',
              }
        cf = main.ConfigDict('/tmp/')
        cf.update(CF)
        cf.normalize_paths()
        self.assertEqual(cf['repertoire_cible'],'/tmp/cible')

    def test_normalize2(self):
        self.skipTest('fix or remove this')
        CF = {'repertoire_cible':'comptes',
              'repertoire_source':'data',
              'exercice':'2003',
              'exercice_precedent':'../2002',
              }
        cf = main.ConfigDict('/tmp/')
        cf.update(CF)
        cf.normalize_paths()
        self.assertEqual(cf['repertoire_cible'],'/tmp/comptes')
        self.assertEqual(cf['repertoire_source'],'/tmp/data')
        self.assertEqual(cf['repertoire_ecritures'],'/tmp/data/2003/ecritures')

if __name__ == '__main__':
    testlib.unittest_main()
