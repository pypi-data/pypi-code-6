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


#Set up logging fore useful debug output, and time stamps in UTC.
import logging
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', 
                    level=logging.DEBUG)
#Time stamps must be in UTC
logging.Formatter.converter = time.gmtime


def relative_path(*path_comps):
    "Create file paths that are relative to the location of this file."
    return path.abspath(path.join(path.dirname(__file__), *path_comps))

def find_index(list_like, search_val, key=lambda x:x):
    """
    Find the index of an element in a list like container. 
    
    Accepts a custom function to compute the comparison key, like ``list.sort``.
    
    Returns
    --------
    
    int | NoneType: Index of found element or ``None`` if no element is found.
    
    TODO: Write unit test.
    """
    for i, elem in enumerate(list_like):
        comp_val = key(elem)
        if comp_val == search_val:
            return i 
    else:
        return None
    
    
def test_OsmandDownloader_get_file_list():
    "Test class OsmandDownloader: Listing of files that can be downloaded."
    from mob_map_dl.download import OsmandDownloader
    
    print "Start get_file_list"
    d = OsmandDownloader()
    l = d.get_file_list()
    
    pprint(l)
    print len(l)
    
    #Test if some files exist
    get_disp_name = lambda e: e.disp_name
    assert find_index(l, "osmand/France_rhone-alpes_europe_2.obf", 
                      key=get_disp_name) is not None
    assert find_index(l, "osmand/Germany_nordrhein-westfalen_europe_2.obf", 
                      key=get_disp_name) is not None
    assert find_index(l, "osmand/Jamaica_centralamerica_2.obf", 
                      key=get_disp_name) is not None
    assert find_index(l, "osmand/Monaco_europe_2.obf", 
                      key=get_disp_name) is not None
    #Test the names of first & last file
    assert l[0].disp_name == "osmand/Afghanistan_asia_2.obf"
    assert l[-1].disp_name == "osmand/zh_0.voice"
    #Number of files must be in certain range.
    assert 500 < len(l) < 550
    
    
def test_OsmandDownloader_download_file():
    "Test class OsmandDownloader: Downloading of files from Osmand server."
    from mob_map_dl.download import OsmandDownloader
    
    print "Start download_file"
    test_map_name = relative_path("../../test_tmp/test_1.obf.zip")
    try: os.remove(test_map_name)
    except: pass
    assert not path.exists(test_map_name)
    
#    #File size 0.2 MiB
#    url = "http://download.osmand.net/download.php?standard=yes&file=Monaco_europe_2.obf.zip"
    #File size 3.0 MiB
    url = "http://download.osmand.net/download.php?standard=yes&file=Jamaica_centralamerica_2.obf.zip"
    
    d = OsmandDownloader()
    d.download_file(url, test_map_name, "test-file-name.foo")
    
    #Test name and size of downloaded file
    assert path.isfile(test_map_name)
    file_size = path.getsize(test_map_name)/1024**2
    print "file size [MiB]:", file_size
    assert round(file_size, 1) == 3.0
    
    
if __name__ == "__main__":
    test_OsmandDownloader_get_file_list()
#    test_OsmandDownloader_download_file()
    
    pass
