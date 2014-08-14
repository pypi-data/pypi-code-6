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
Install maps on a mobile device.
"""

from __future__ import division
from __future__ import absolute_import              

import time
import os
import fnmatch
from os import path
import datetime
from itertools import cycle

from mob_map_dl.common import MapMeta
from mob_map_dl.common import TextProgressBar


#Set up logging fore useful debug output, and time stamps in UTC.
import logging
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', 
                    level=logging.DEBUG)
#Time stamps must be in UTC
logging.Formatter.converter = time.gmtime


class OsmandInstaller(object):
    """
    Install maps for Osmand on the mobile device.
    """
    def __init__(self, device_dir):
#        self.device_dir = device_dir
        self.install_dir = path.join(device_dir, "osmand")
        
        #Create Osmand directory, if it does not exist.
        if not path.exists(self.install_dir):
            os.mkdir(self.install_dir)
    
    def make_disp_name(self, file_name_path):
        """
        Create a canonical name from a file name or path of a installed map. 
        The canonical name is used in the user interface.
        
        The canonical name has the form:
            "osmand/Country_Name.obf" or
            "osmand/Language.voice"
        """
        _, file_name = path.split(file_name_path)
        disp_name = "osmand/" + file_name
        return disp_name
    
    def make_full_name(self, disp_name):
        """
        Create a path to a locally stored map from its canonical name. 
        """
        _, fname = path.split(disp_name)
        full_name = path.join(self.install_dir, fname)
        return full_name
    
    def get_map_list(self):
        """
        List the maps that are installed on the device.
        
        Maps are searched in "``self.device_dir``/osmand".
        
        Return
        -------
        
        list[MapMeta]
        """
        dir_names = os.listdir(self.install_dir)
        map_names = fnmatch.filter(dir_names, "*.obf")
        map_names.sort()
        
        map_metas = []
        for name in map_names:
            map_name = path.join(self.install_dir, name)
            disp_name = self.make_disp_name(name)
            map_size = path.getsize(map_name)
            mod_time = path.getmtime(map_name)
            map_meta = MapMeta(disp_name=disp_name, 
                               full_name=map_name, 
                               size=map_size, 
                               time=datetime.datetime.fromtimestamp(mod_time), 
                               description="", 
                               map_type="osmand")
            map_metas.append(map_meta)
        
        return map_metas
    
    
#    def install_map(self, extractor, sd_path, disp_name, size_total):
#        """
#        Install one map file in Osmand's directory on the SD card.
#        
#        Arguments
#        ---------
#        
#        extractor: file like object
#            An object that extracts the map from the zip archive. It behaves
#            like a file.
#        
#        sd_path: str
#            Path of the map on the mobile device's SD card.
#        
#        disp_name: str
#            Canonical name of the map. Used in the progress bar.
#            
#        size_total: int [Bytes]
#            The size of the map, uncompressed.
#        """
#        size_mib = round(size_total / 1024**2, 1)
#        msg = "{name} : {size} MiB".format(name=disp_name[0:50], size=size_mib)
#        progress = TextProgressBar(msg, val_max=size_total)
#        progress.update_val(0)
#        
#        fsdcard = open(sd_path, "wb")
#        
#        buff_size = 1024**2 * 10
#        size_down = 0
#        while True:
#            progress.update_val(size_down)
#            buf = extractor.read(buff_size)
#            if not buf:
#                break
#            fsdcard.write(buf)
#            size_down += len(buf)
#            
#        fsdcard.close()
#        progress.update_final(size_down, "Installed")
        
