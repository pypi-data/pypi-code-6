"""
"""

# Should this be part of client?? It's an interactive thing


class SchemaInspector:

    def __init__(self, client, profile_type):
        self.profile_type = profile_type
        urn = "urn:collectiondoc:query:schemas"
        query_params = {'text': self.profile_type}


# Possibility of looking up a schema and using its validation to
# Create a profile. Question: how to look-up a schema based on a profile


# Querying a schema

client = None  # for this example only
schema_doc = client.query("urn:collectiondoc:query:schemas",
                          params={'text': 'Story'})
# OR FRAGILE, something like:
schema_doc = client.get(client.entry_point + 'schemas/story')
# Hopefully something in between

schema = schema_doc.attributes
schema['schema']  # this is the actual schema
schema['schema']['definitions']  # validator located here
# and here are the attributes to be found in this profile
schema['schema']['definitions']['attributes']
{'type': 'object', 'description': 'Story metadata object', 'properties': {'contentencoded': {'type': 'string', 'description': 'A representation of the content which can be used literally as HTML-encoded content'}, 'teaser': {'type': 'string', 'description': 'A short description, appropriate for showing in small spaces'}, 'contenttemplated': {'type': 'string', 'description': 'A representation of the content which has placeholders for rich-media assets'}, 'description': {'type': 'string', 'description': 'A representation of the content of this document without HTML'}}, 'id': '#attributes'}
schema['schema']['definitions']['attributes']['properties'].keys()
['contentencoded', 'teaser', 'contenttemplated', 'description']

# However, this schema inherits from base, so you also need to do
schema['schema']['allOf']  # which returns:
[{'$ref': 'https://api-sandbox.pmp.io/schemas/base'}, {'$ref': '#storySchema'}]
# So we can get that one too
base = client.get('https://api-sandbox.pmp.io/schemas/base')
base_schema = base.attributes['schema']
base_schema['definitions']['attributes']
{'required': ['title'], 'type': 'object', 'description': 'Document metadata object', 'properties': {'byline': {'type': 'string', 'description': 'Rendered byline as suggested by document distributor'}, 'description': {'type': 'string', 'description': 'Document synopsis'}}, 'id': '#attributes'}
bscheme['definitions']['attributes']['properties'].keys()
dict_keys(['byline', 'description'])
bscheme['definitions']['attributes'].get('required')
['title']

# Unfortunately, this one too references a further base...
bottom = client.get('https://api-sandbox.pmp.io/schemas/pmpcore')


# So, to generate an actual profile, we'd need to do the following:

# 1 Look up the schema
# 2 Look up all base schemas
# 3 find required items
# 4 find optional items
# 5 assemble attributes for profile
# 6 add links


# And then we just need a generic "links" object which contains stuff generic to all objects...
