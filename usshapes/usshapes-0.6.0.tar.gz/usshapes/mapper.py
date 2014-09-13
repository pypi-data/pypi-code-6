from pyes import ES
from pyes.exceptions import IndexAlreadyExistsException


class Mapper:
    def __init__(self, es_host, num_shards, num_replicas):
        self.client = ES(es_host)
        self.num_shards = num_shards
        self.num_replicas = num_replicas

    def create_indices(self, indices=[]):
        print "creating indices: %s" % indices

        settings = dict(index=dict(
            number_of_shards=self.num_shards,
            number_of_replicas=self.num_replicas
        ))

        for index_name in indices:
            try:
                self.client.indices.create_index(index_name, settings=settings)
            except IndexAlreadyExistsException:
                print "[%s] index already exists. Skipping creation..." % index_name
                pass


    def put_shapes_mappings(self, index='shapes'):
        self.client.indices.put_mapping('neighborhood', {'properties': self.shapes_neighborhood_mapping}, [index])
        self.client.indices.put_mapping('city', {'properties': self.shapes_city_mapping}, [index])
        self.client.indices.put_mapping('state', {'properties': self.shapes_state_mapping}, [index])
        self.client.indices.put_mapping('zip', {'properties': self.shapes_zip_mapping}, [index])


    def put_suggestions_mappings(self, index='suggestions'):
        self.client.indices.put_mapping('neighborhood', {'properties': self.suggestions_mapping}, [index])
        self.client.indices.put_mapping('city', {'properties': self.suggestions_mapping}, [index])
        self.client.indices.put_mapping('zip', {'properties': self.suggestions_mapping}, [index])


    shapes_neighborhood_mapping = {
        "geometry": {
            "type": "geo_shape"
        },
        "city": {
            "type": "string"
        },
        "neighborhood": {
            "type": "string"
        },
        "state": {
            "type": "string"
        }
    }

    shapes_city_mapping = {
        "geometry": {
            "type": "geo_shape"
        },
        "city": {
            "type": "string"
        },
        "state": {
            "type": "string"
        }
    }

    shapes_state_mapping = {
        "geometry": {
            "type": "geo_shape"
        },
        "state": {
            "type": "string"
        },
        "postal": {
            "type": "string"
        }
    }

    shapes_zip_mapping = {
        "geometry": {
            "type": "geo_shape"
        },
        "zip": {
            "type": "string"
        }
    }

    suggestions_mapping = {
        "name": {
            "type": "string"
        },
        "suggest": {
            "type": "completion",
            "payloads": True
        }
    }