#!/usr/bin/python

import sys
from os.path import isdir
from os import mkdir
from getopt import getopt, GetoptError

from pyes import ES

from usshapes.mapper import Mapper
from usshapes.indexer import Indexer
from usshapes.builder import Builder
from usshapes.converter import GeoJSONConverter


class USShapesRunner():
    def __init__(self, args):
        es_host = 'localhost:9200'
        ogre_host = 'localhost:3000'
        batch_size = 100
        batch_mode = True
        excludes = []
        index_shapes = True
        index_suggestions = True

        try:
            opts, args = getopt(args, None, ["es-host=", "no-batch", "batch-size=", "excludes=", "skip-shapes", "skip-suggestions"])
        except GetoptError:
            print 'run.py [--es-host=<elasticsearch-host>] [[--no-batch] | [--batch-size=]] [--excludes=<excluded-types>] [--skip-shapes] [--skip-suggestions]'
            print """
                Options:
                - es-host: the elastic search host to use; default: localhost:9200
                - ogre-host: the ogre client to use; default: localhost:3000
                - no-batch: turn off batch mode
                - batch-size: how large should each batch be; default: 100
                - excludes: comma-separated list of excluded types; possible types: 'neighborhood', 'city', 'state', 'zip'
                - skip-shapes: skip creation and indexing of shapes
                - skip-suggestions: skip creation and indexing of suggestions
            """
            sys.exit(2)
        for opt, arg in opts:
            if opt == '--es-host':
                es_host = arg
            if opt == '--ogre-host':
                ogre_host = arg
            elif opt == '--no-batch':
                batch_mode = False
            elif opt == '--batch-size':
                batch_size = arg
            elif opt == '--excludes':
                excludes = [a.strip() for a in arg.split(',')]
            elif opt == '--skip-shapes':
                index_shapes = False
            elif opt == '--skip-suggestions':
                index_suggestions = False

        print "Running shapes and suggestions indexing with the following options:"
        print "* elasticsearch host: %s" % es_host
        print "* ogre host: %s" % ogre_host
        print "* batch mode: %s" % batch_mode
        print "* batch size: %s" % (batch_size if batch_mode else 'n/a')
        print "* excluded types: %s" % excludes
        print "* indexing shapes? %s" % index_shapes
        print "* indexing suggestions? %s" % index_suggestions

        es_client = ES(es_host)
        mapper = Mapper(es_client)
        indexer = Indexer(es_client, batch_size=batch_size, batch_mode=batch_mode)
        converter = GeoJSONConverter(ogre_host=ogre_host)
        builder = Builder(converter=converter)

        self.shapes_index = 'shapes_tmp'
        self.suggest_index = 'suggestions_tmp'

        self.initialize_mappings(mapper)

        if index_shapes:
            self.index_shapes(builder, indexer, excludes=excludes)
        if index_suggestions:
            self.index_suggestions(builder, indexer, excludes=excludes)

    def initialize_mappings(self, mapper):
        # Create indices and put mappings

        print 'Creating indices'
        mapper.create_indices(indices=[self.shapes_index, self.suggest_index])
        mapper.put_shapes_mappings(index=self.shapes_index)
        mapper.put_suggestions_mappings(index=self.suggest_index)

    def index_shapes(self, builder, indexer, excludes):
        # Download and format shapefiles, if they don't exist

        shapes_dir = 'shapes'
        neighborhood_shapes_file = '%s/shapes_neighborhood.json' % shapes_dir
        city_shapes_file = '%s/shapes_city.json' % shapes_dir
        state_shapes_file = '%s/shapes_state.json' % shapes_dir
        zip_shapes_file = '%s/shapes_zip.json' % shapes_dir

        if not isdir(shapes_dir):
            mkdir(shapes_dir)

        if 'neighborhood' not in excludes:
            builder.build_neighborhood_shapes(outfile=neighborhood_shapes_file)
            indexer.bulk_index(self.shapes_index, 'neighborhood', neighborhood_shapes_file)
        if 'city' not in excludes:
            builder.build_city_shapes(outfile=city_shapes_file)
            indexer.bulk_index(self.shapes_index, 'city', city_shapes_file)
        if 'state' not in excludes:
            builder.build_state_shapes(outfile=state_shapes_file)
            indexer.bulk_index(self.shapes_index, 'state', state_shapes_file)
        if 'zip' not in excludes:
            builder.build_zip_shapes(outfile=zip_shapes_file)
            indexer.bulk_index(self.shapes_index, 'zip', zip_shapes_file)

    def index_suggestions(self, builder, indexer, excludes):
        # Generate suggestion files, if they don't exist

        suggestions_dir = 'suggestions'
        neighborhood_suggestions_file = '%s/suggestions_neighborhood.json' % suggestions_dir
        city_suggestions_file = '%s/suggestions_city.json' % suggestions_dir
        zip_suggestions_file = '%s/suggestions_zip.json' % suggestions_dir

        shapes_dir = 'shapes'
        neighborhood_geofile = '%s/shapes_neighborhood.json' % shapes_dir
        city_geofile = '%s/shapes_city.json' % shapes_dir
        zip_geofile = '%s/shapes_zip.json' % shapes_dir

        if not isdir(suggestions_dir):
            mkdir(suggestions_dir)

        if 'neighborhood' not in excludes:
            builder.build_neighborhood_suggestions(outfile=neighborhood_suggestions_file,
                                                   neighborhood_geofile=neighborhood_geofile)
            indexer.bulk_index(self.suggest_index, 'neighborhood', neighborhood_suggestions_file)

        if 'city' not in excludes:
            builder.build_city_suggestions(outfile=city_suggestions_file, city_geofile=city_geofile)
            indexer.bulk_index(self.suggest_index, 'city', city_suggestions_file)

        if 'zip' not in excludes:
            builder.build_zip_suggestions(outfile=zip_suggestions_file, zip_geofile=zip_geofile)
            indexer.bulk_index(self.suggest_index, 'zip', zip_suggestions_file)


if __name__ == "__main__":
    USShapesRunner(sys.argv[1:])
