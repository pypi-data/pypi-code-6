try:
	import simplejson as json
except ImportError:
	import json


'''     
        given a filename (param path) or string (param str), 
        LoadJSON returns the content in json format.
'''

class LoadJSON:
        def __init__(self,path=None, str=None):
                if path:
                        self.data = json.load(self.read_file(path), encoding="utf-8")
                elif str:
                        str = str.decode('utf-8')
                        self.data = json.loads( str )
                else:
                        self.data = json.load( "{ }")


        def read_file(self,filename):
                return  open(filename,'r')

        def get_json(self):
                return self.data
                
                

''' given a json string... do pretty printing'''
def pretty_print(str):
	str =  str.encode("utf-8")
	str = str.replace(": u", ": ").replace("'", '"')
	lj = LoadJSON(str = str)
	return  json.dumps( lj.get_json(),indent=4, sort_keys=True )