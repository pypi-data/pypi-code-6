# -*- coding: utf-8 -*-
"""
NOCH NICHT VERWENDET -> ERSTELLUNG VON ICONS
"""


from PIL import Image
import random
import math
import md5

class utils():


     
    def generate_voronoi_diagram(width, height, num_cells, unique_identifier):
        """
        """
        image = Image.new("RGB", (width, height))
        putpixel = image.putpixel
        imgx, imgy = image.size
        nx = []
        ny = []
        nr = []
        ng = []
        nb = []
        for i in range(num_cells):
            #nx.append(random.randrange(imgx))
            #ny.append(random.randrange(imgy))
            #nr.append(random.randrange(255))
            #ng.append(random.randrange(255))
            #nb.append(random.randrange(255))

            # --- #LM
            # determinierte Farbwerte
            hui = md5.new(unique_identifier).hexdigest()

            print "----------------------------"
            print i
            #print int('0x' + hui[ 1+(i+1):3+(i+1)], 16), int('0x' + hui[ 1+(i+2):3+(i+2)], 16), int('0x' + hui[ 1+(i+3):3+(i+3)], 16)

            nx.append( int('0x0' + hui[ 1+(i+1):3+(i+1) ], 16) % width )
            ny.append( int('0x0' + hui[ 1+(i+2):3+(i+2) ], 16) % height )
            nr.append( int('0x0' + hui[ 1+(i+1):3+(i+1) or 1], 16) )
            ng.append( int('0x0' + hui[ 1+(i+2):3+(i+2) or 1], 16) )
            nb.append( int('0x0' + hui[ 1+(i+3):3+(i+3) or 1], 16) )
            # --- /#LM

        for y in range(imgy):
            for x in range(imgx):
                dmin = math.hypot(imgx-1, imgy-1)
                j = -1
                for i in range(num_cells):
                    d = math.hypot(nx[i]-x, ny[i]-y)
                    if d < dmin:
                        dmin = d
                        j = i
                putpixel((x, y), (nr[j], ng[j], nb[j]))

        #TODO --> save to filesystem
        image.save("VoronoiDiagram.png", "PNG")
        image.show()


# ----------------------------------------------------    
#generate_voronoi_diagram(48, 48, 3, 'lmuller@ityou.de')
#generate_voronoi_diagram(48, 48, 4, 'test@ityou.de')
#generate_voronoi_diagram(48, 48, 5, 'info@ityou.de')

