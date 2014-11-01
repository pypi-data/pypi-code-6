from flasksupport import SimpleModelTestFramework
from flask import make_response,json
import hyperdns.flask as web
from sqlalchemy import String,ForeignKey

class TestCase(SimpleModelTestFramework):

    def build_model(self):


        @web.api({
            })
        class ExampleThingCollectedByRoot(self.app.db.Model):
            id=self.app.db.hal.Property(String,primary_key=True)    
            container_id=self.app.db.Column(String,ForeignKey('example_root.id'))
            
        @web.api({
            })
        class ExampleComplexPartOfRoot(self.app.db.Model):
            id=self.app.db.hal.Property(String,primary_key=True)    
            owner_id=self.app.db.Column(String,ForeignKey('example_root.id'))

        @web.api({
            'root':('testobject','/test')
            })
        class ExampleRoot(self.app.db.Model):
            id=self.app.db.hal.Property(String,primary_key=True)    
            oneThing=self.app.db.hal.Resource('ExampleComplexPartOfRoot',backref='owner')    
            manyThings=self.app.db.hal.Map('ExampleThingCollectedByRoot','id',backref='container')    
            

        self.app.db.create_all()

        @staticmethod
        @web.auth.user_loader
        def load_user(payload,request):
            return ({},None,{
                'testobject':ExampleRoot.query.get(1)
            })
        
        root=ExampleRoot()._setprops({
            'id':'1'
        })
        ExampleComplexPartOfRoot()._setprops({
            'id':'1',
            'owner':root
        })
        ExampleThingCollectedByRoot()._setprops({
            'id':'1',
            'container':root
        })
        self.app.db.session.commit()

    def test(self):
        for rule in self.app.url_map.iter_rules():
            print(rule)
        result=self.client.get("/test",headers=self.headers)
        #print(result,result.data)
        result=self.client.get("/test/oneThing",headers=self.headers)
        #print(result,result.data)
        result=self.client.get("/test/manyThings/1",headers=self.headers)
        print(json.dumps(result.data,indent=4,sort_keys=True))
        raise Exception('A')