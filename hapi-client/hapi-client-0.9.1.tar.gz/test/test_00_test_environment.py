import flasksupport
from hyperdns.hapi.flask import (
    app,
    System
    )
from hyperdns.hapi.client import HAPI

class TestCase(flasksupport.SimpleTestCase):

    # #### first test the database environment
    def test_a00_init_and_destroy_db(self):
        with app.app_context():
            app.db.drop_all()
            app.db.create_all()

    def test_a01_create_system(self):

        with app.app_context():
            app.db.drop_all()
            app.db.create_all()
            System()
    
    def test_a02_create_basic_objects(self):

        with app.app_context():
            self.initialize_db()
            self.create_vendor('vtst_1')
            self.create_vendor('vtst_2')
            self.add_vendor('vtst_1')

    def test_a03_create_basic_objects(self):

        with app.app_context():
            self.initialize_db()
            self.create_vendor('vtst_1')
            self.create_vendor('vtst_2')
            self.add_vendor('vtst_1')
            #self.assertRaises(Exception,self.create_vendor,'vtst_1')
            self.assertRaises(Exception,self.add_vendor,'vtst_1')
            self.assertRaises(Exception,self.add_vendor,'vtst_3')
             
    # test HAPI
    def test_b00_HAPI_sanity(self):
        with app.app_context():
            self.standard_context()
        H=self.hapi
        
        assert str(H.id)==str(self.account.id)
        print(H.zones.keys())
        print(H.vendors.keys())
        assert list(H.zones.keys())==[]
        assert list(H.vendors.keys())==['vtst_1']
                
    def notest_b01_monkeypatch(self):
        import httpretty.core
        with app.app_context():
            self.standard_context()
        H=self.hapi
        V=H.vendors['vtst_1']
        print(V.scan)
        print("X",getattr(httpretty.core.FakeSockFile,'close'))
        self.assertRaises(ValueError,V.startScan)
            
        print(V.scan)
        result=V.startScan()
        def fake_close(self):
            print("Fake Closing")
            pass
        setattr(httpretty.core.FakeSockFile,'close',fake_close)
        result=V.startScan()

        print(result)
        assert 1==3
        
    def test_b01_monkeypatch(self):
        """Testing the monkeypatch - this typically results in a
        ValueError when making the second requests, which, in this case takes
        place in V.startScan, but any request will do.
        """
        with app.app_context():
            self.standard_context()
        H=self.hapi
        V=H.vendors['vtst_1']
        assert V.scan==None        
        result=V.startScan()
        assert result==True
        
        V._refresh_from_server()
        assert V.scan!=None
        
        result=V.startScan()
        assert result==False



        
        
