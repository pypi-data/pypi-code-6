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
Download maps from server on the internet.
"""

from __future__ import division
from __future__ import absolute_import              

import time
import urllib2
import lxml.html
import dateutil.parser
import urlparse

from mob_map_dl.common import MapMeta
from mob_map_dl.common import TextProgressBar


#Set up logging fore useful debug output, and time stamps in UTC.
import logging
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', 
                    level=logging.DEBUG)
#Time stamps must be in UTC
logging.Formatter.converter = time.gmtime


class OsmandDownloader(object):
    """
    Download maps from the servers of the Osmand project.
    """
    list_url = "http://download.osmand.net/list.php"
    
    def __init__(self):
        pass
        
    
    def make_disp_name(self, server_name):
        """
        Create a canonical name from the name, that the server supplies.
        This canonical name is used in the user interface.
        
        The canonical name has the form:
            "osmand/Country_Name.obf" or
            "osmand/Language.voice"
        """
        #The server delivers name of the form "Country_Name.obf.zip"
        disp_name = "osmand/" + server_name.rsplit(".", 1)[0]
        return disp_name
    
    
    def get_map_list(self):
        """
        Get list of maps for Osmand that are available for download.
        
        Return
        -------
        
        list[MapMeta]
        
        Note
        ------
        
        The function parses the regular, human readable, HTML document, that
        lists the existing maps for Osmand. It has the following structure:
        
        <html>
            <head> ... </head>
            <body>
                <h1> ... </h1>
                <table>
                    <tr> ... Table headers ... </tr>
                    <tr> ... Nonsense (".gitignore") ... </tr>
                    <tr>
                        <td>
                            <A HREF="/download.php?standard=yes&file=Afghanistan_asia_2.obf.zip">Afghanistan_asia_2.obf.zip</A>
                        </td>
                        <td>03.08.2014</td>
                        <td>8.2</td>
                        <td>
                            Map, Roads, POI, Transport, Address data for 
                            Afghanistan asia
                        </td>
                    </tr>
                    <tr> ... The next map record ... </tr>
                </table>
            </body>
        </html>
        """
        #Download HTML document with list of maps from server of Osmand project
        u = urllib2.urlopen(self.list_url)
        list_html = u.read()
#        print list_html
        #Parse HTML list of maps
        root = lxml.html.document_fromstring(list_html)
        table = root.find(".//table")
        map_metas = []
        for row in table[2:]:
            link = row[0][0]
            download_url = urlparse.urljoin(self.list_url, link.get("href"))
            map_meta = MapMeta(disp_name=self.make_disp_name(link.text), 
                               full_name=download_url, 
                               size=float(row[2].text) * 1024**2, #[Byte]
                               time=dateutil.parser.parse(row[1].text), 
                               description=row[3].text, 
                               map_type="osmand")
            map_metas.append(map_meta)
            
        map_metas.sort(key=lambda m: m.disp_name)
        return map_metas
    
    
    def download_file(self, srv_url, loc_name, disp_name):
        """
        Download a file from the server and store it in the local file system.
        
        Creates a progress animation in the console window, as maps are 
        usually large files.
        
        Arguments
        ---------
        
        srv_url: str
            URL of the file on the remote server.
            
        loc_name: str
            Name of the file in the local file system.
            
        disp_name: str 
            File name for display in the progress bar.
            
        TODO: Dynamically adapt ``buff_size`` so that the animation is updated
              once per second.  
        """
        fsrv = urllib2.urlopen(srv_url)
        floc = open(loc_name, "wb")
        
        meta = fsrv.info()
        size_total = int(meta.getheaders("Content-Length")[0])
        size_mib = round(size_total / 1024**2, 1)
        msg = "{name} : {size} MiB".format(name=disp_name[0:50], size=size_mib)
        progress = TextProgressBar(msg, val_max=size_total)
        
        buff_size = 1024 * 100
        size_down = 0
        while True:
            progress.update_val(size_down)
            buf = fsrv.read(buff_size)
            if not buf:
                break
            floc.write(buf)
            size_down += len(buf)
            
        floc.close()
        progress.update_final(size_down, "Downloaded")

        
    