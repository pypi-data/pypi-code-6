# -*- coding: utf-8 -*-
###############################################################################
#    Mobile Map Downloader - Download maps for your mobile phone.             #
#                                                                             #
#    Copyright (C) 2014 by Eike Welk                                          #
#    eike.welk@gmx.net                                                        #
#                                                                             #
#    License: GPL Version 3                                                   #
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
###############################################################################
"""
Test the download functions.
"""

from __future__ import division
from __future__ import absolute_import              

#For test modules: ----------------------------------------------------------
#import pytest #contains `skip`, `fail`, `raises`, `config`

import time
import os
import os.path as path
from pprint import pprint
import shutil


#Set up logging fore useful debug output, and time stamps in UTC.
import logging
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', 
                    level=logging.DEBUG)
#Time stamps must be in UTC
logging.Formatter.converter = time.gmtime


def relative_path(*path_comps):
    "Create file paths that are relative to the location of this file."
    return path.abspath(path.join(path.dirname(__file__), *path_comps))


def test_OsmandInstaller_get_file_list():
    "OsmandInstaller: Get list of installed maps."
    from mob_map_dl.install import OsmandInstaller   
    
    device_path = relative_path("../../test_data/TEST-DEVICE1")
    
    i = OsmandInstaller(device_path)
    l = i.get_file_list()
    
    pprint(l)
    assert len(l) == 2
    assert l[0].disp_name == 'osmand/Jamaica_centralamerica_2.obf'
    assert l[0].size == 4518034
    assert l[1].disp_name == "osmand/Monaco_europe_2.obf"
    assert l[1].size == 342685

    
#def test_OsmandInstaller_install_map():
#    "OsmandInstaller: Install one map file."
#    from mob_map_dl.install import OsmandInstaller  
#    from mob_map_dl.local import OsmandManager
#    
#    download_dir = relative_path("../../test_data/maps/")
#    archive_path = relative_path("../../test_data/maps/osmand/Jamaica_centralamerica_2.obf.zip")
#    device_dir = relative_path("../../test_tmp/TEST-DEVICE1")    
#    map_path =   relative_path("../../test_tmp/TEST-DEVICE1/osmand/Jamaica_centralamerica_2.obf")
#
#    #Remove old output directory, and create new empty output directory
#    shutil.rmtree(device_dir, ignore_errors=True)
#    os.makedirs(path.join(device_dir, "osmand"))
#    
#    m = OsmandManager(download_dir)
#    i = OsmandInstaller(device_dir)
#    extractor, size_total, _ = m.get_map_extractor(archive_path)
#    i.install_map(extractor, map_path, "osmand/Jamaica_centralamerica_2", size_total)
#    
#    print "path.getsize(archive_path):", path.getsize(map_path)
#    assert path.isfile(map_path)
#    assert path.getsize(map_path) == 4518034
    

if __name__ == "__main__":
#    test_OsmandInstaller_get_file_list()
#    test_OsmandInstaller_install_map()
    
    pass
