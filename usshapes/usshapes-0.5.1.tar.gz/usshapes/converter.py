from os.path import isfile
from glob import glob
from shlex import split
from subprocess import check_output


class GeoJSONConverter:
    def __init__(self, ogre_host='localhost:3000'):
        self.ogre_host = ogre_host

    def to_geojson(self, outfile, shapefile_prefix='', shapefile_ext='zip', shapefiles_dir='shapefiles'):

        if isfile(outfile):
            print "%s already exists. Skipping conversion..." % outfile
            return outfile

        print "Converting files in %s matching %s*.%s into GeoJSON. Results stored in %s" % \
              (shapefiles_dir, shapefile_prefix, shapefile_ext, outfile)

        with open(outfile, 'a') as out:
            file_pattern = "%s/%s*.%s" % (shapefiles_dir, shapefile_prefix, shapefile_ext)
            files = glob(file_pattern)

            for filename in files:
                try:
                    print "Converting %s to GeoJSON" % filename
                    raw_command = r'curl -F "upload=@%s" %s/convert' % (filename, self.ogre_host)
                    command = split(raw_command)
                    converted = check_output(command)
                    out.write("%s" % converted)
                except IOError as e:
                    print "Error converting %s" % filename
                    print "I/O error({0}): {1}".format(e.errno, e.strerror)
