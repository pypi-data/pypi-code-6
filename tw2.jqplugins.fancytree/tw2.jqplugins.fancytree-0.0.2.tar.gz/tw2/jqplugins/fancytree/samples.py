""""""
try:
    import simplejson as json
except:
    import json

import uuid
from collections import defaultdict

import tw2.core as twc

from widgets import FancyTreeWidget

# see taxonomy_tree() docstring
tree = lambda: defaultdict(tree)

# provide a uuid as a (json-ifiable)_string
key = lambda: str(uuid.uuid4())


def dicts(t):
    '''recursive function to provide keys/values with children,
    unique key and `folder` flagged as True/False as appropriate.
    '''
    return [
        {'title': k,
         'children': dicts(t[k]),
         'key': key(),
         'folder': True if dicts(t[k]) else False
         } for k in t
    ]


def taxonomy_tree():
    '''

    methodology:  based upon the "One-line Tree in python" using
                  python's built-in `defaultdict`. See this gist:
                  https://gist.github.com/hrldcpr/2012250

    rationale: nested structures are by their nature a bit messy, so
               we provide a nice, easy-to-read block of data for what
               would otherwise be a lengthy nested dict.

    The `dicts()` function (above) converts the tree structure to a
    standard dict, recursively, in the format required by the fancytree
    ie a title, unique key, folder (boolean) and children (a list of
    dicts).  And it's a neat demonstration of the technique(!)

    note: this intentionally not PEP8'ed...

    ... and our structure
    Kingdom/Phylum/Class/Order/Family/Genus/Species
    '''
    taxonomy = tree()
    taxonomy['Animalia']['Chordata']['Mammalia']['Carnivora']['Felidae']['Felis']['cat']
    taxonomy['Animalia']['Chordata']['Mammalia']['Carnivora']['Felidae']['Panthera']['lion']
    taxonomy['Animalia']['Chordata']['Mammalia']['Carnivora']['Felidae']['Panthera']['snow leopard']
    taxonomy['Animalia']['Chordata']['Mammalia']['Carnivora']['Canidae']['Canis']['dog']
    taxonomy['Animalia']['Chordata']['Mammalia']['Monotremata']['Ornithorhynchidae']['Ornithorhynchus']['duck-billed platypus']
    taxonomy['Animalia']['Chordata']['Myxini']['Myxiniforms']['Myxinidae']['Eptatretus']['Pacific hagfish']
    taxonomy['Plantae']['Solanales']['Solanaceae']['Solanum']['tomato']
    taxonomy['Plantae']['Solanales']['Solanaceae']['Solanum']['potato']
    taxonomy['Plantae']['Solanales']['Convolvulaceae']['Ipomoea']['sweet potato']

    return dicts(taxonomy)


class DemoFancyTreeWidget(FancyTreeWidget):
    '''
    The `source` parameter below shows three valid definitions.
    Comment/uncomment the code to explore...
    '''
    options = {
        'activate': twc.js_callback('''
            function(event, data) {
                var node = data.node;
                console.log('activated:', node.title);
            }
        '''),

        # 1.  the simplest data source format -- a plain list of dicts
        # 'source': [
        #     {"title": "Node 1", "key": "1"},
        #     {"title": "Folder 2", "key": "2", "folder": True,
        #         "children": [
        #             {"title": "Node 2.1", "key": "3"},
        #             {"title": "Node 2.2", "key": "4"},
        #             {"title": "Node 2.3", "key": "5"}
        #         ]
        #      },
        # ]
        #
        # 2. drawing the data directly from taxonomy_tree(), the data
        #    will be rendererd directly within the page's html
        #'source': taxonomy_tree()
        #
        # 3. simulated ajax call
        'source': {'url': 'jsonsource', 'cache': False},
    }

    @classmethod
    def request(cls, req):
        import webob
        import time
        # the artificial delay demos that `loading` is displayed by
        # the widget
        time.sleep(1)
        resp = webob.Response(request=req, content_type="application/json")
        resp.body = json.dumps(taxonomy_tree())
        return resp

# register the widget's request
twc.register_controller(DemoFancyTreeWidget, 'jsonsource')
