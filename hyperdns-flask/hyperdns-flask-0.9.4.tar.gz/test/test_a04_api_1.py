from flasksupport import SimpleModelTestFramework
from flask import make_response
import hyperdns.flask as web

class TestCase(SimpleModelTestFramework):
        
    def test(self):
        #for rule in self.app.url_map.iter_rules():
        #    print(rule)
        result=self.client.get("/test",headers=self.headers)
        print(result,result.data)
        raise Exception('A')