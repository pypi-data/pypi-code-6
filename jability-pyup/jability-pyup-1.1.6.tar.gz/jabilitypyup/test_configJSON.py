#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright 2010 ROMAND Fabrice <fabrom@jability.org>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.


import configJSON
from configJSON import *


import os.path
test_cfg_file = os.path.join(   os.path.dirname(__file__),
                                'tests/test.json')
notexisting_cfg_file = os.path.join(    os.path.dirname(__file__),
                                        'tests/notexisting.json')
dir_cfg_file = os.path.join(    os.path.dirname(__file__), 'tests/')
temp_cfg_file = os.path.join(   os.path.dirname(__file__),
                                'tests/temp/test.json')

def test_exists():
    cfg = ConfigJSON(test_cfg_file)
    assert cfg.exists() == True

    cfg = ConfigJSON(notexisting_cfg_file)
    assert cfg.exists() == False

    cfg = ConfigJSON(dir_cfg_file)
    assert cfg.exists() == False


def test_load():
    cfg = ConfigJSON(test_cfg_file)
    assert not cfg.load() == None

    cfg = ConfigJSON(dir_cfg_file)
    assert cfg.load() == None

def test_parse():
    cfg = ConfigJSON(test_cfg_file)
    conf = cfg.load()
    assert conf['configuration1']['liste1'] == [u'a', u'b', u'c']

def test_save():
    cfg = ConfigJSON(test_cfg_file)
    conf = cfg.load()
    conf['configuration1']['key1'] = 'NewValue'
    cfg.save(conf, temp_cfg_file)

    cfg2 = ConfigJSON(temp_cfg_file)
    assert cfg2.exists() == True

    conf2 = cfg2.load()
    assert conf2['configuration1']['key1'] == 'NewValue'

    os.remove(temp_cfg_file)
    assert cfg2.exists() == False

def test_update():
    cfg = ConfigJSON(test_cfg_file)
    assert cfg.exists() == True
    conf = cfg.load()
    cfg.save(conf, temp_cfg_file)
    
    assert cfg.version == u'0.1'
    assert conf['configuration1'].has_key('foo2') == False
    assert conf['configuration1'].has_key('todelete') == True
    
    cfg.update()
    assert cfg.version == '1.2.0'
    print conf['configuration1']['foo2']
    assert conf['configuration1']['foo2'] == [ 1,2,3 ]
    assert conf['configuration1'].has_key('todelete') == False


if __name__ == '__main__':
    import doctest
    doctest.testmod(configJSON)
    try:
        import nose
        nose.main()
    except ImportError:
        pass
