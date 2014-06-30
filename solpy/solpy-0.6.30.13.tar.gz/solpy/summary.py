import argparse
#from solpy import pv
import pv
import os
import datetime
parser = argparse.ArgumentParser()
parser.add_argument('--verbose', '-v', action='count')
parser.add_argument('files', nargs='*')
args = parser.parse_args()
#print args.files

total_dc = 0
sdate = datetime.datetime(2014,6,1)

for i in args.files:
    try:
        plant = pv.fileToSystem(i)
        ctime = os.path.getmtime(i)
        cdt = datetime.datetime.fromtimestamp(ctime)
        if cdt > sdate:
            total_dc += plant.Pdc(1000)/1000.
            print '%s, %s - %s, %s KW DC, %s KW AC' % (cdt, plant.systemName , \
                    plant.phase, round(plant.Pdc(1000)/1000,1), \
                    round(plant.Pac(1000)/1000,1))
    except:
        print "error in %s" % i
    #print datetime.datetime.fromtimestamp(ctime,est)

print 'total: %s' % total_dc
