import json
# from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
import jsonrpclib
from corenlp import batch_parse
from pprint import pprint


results = batch_parse("sample_raw_text")
for i in results:
    print i

# class StanfordNLP:
#     def __init__(self, port_number=8080):
#         self.server = jsonrpclib.Server("http://localhost:%d" % port_number)

#     def parse(self, text):
#         return json.loads(self.server.parse(text))

# nlp = StanfordNLP()
# result = nlp.parse("Hello world!  It is so beautiful.")
# pprint(result)

# from nltk.tree import Tree
# tree = Tree.parse(result['sentences'][0]['parsetree'])
# pprint(tree)
