'''
실행하기 
=====================

    $ nosetest3 
    
'''
from nose.tools import * # eq_, ok_, nottest, istest

import re , os 

def imgpath( addname , 저장위치="I" ):    
    """
    실행되는 위치마다 이미지 파일의 이름 쉽게 만들수 있다.
    ::
        < test-pixkeul-qpkimg.py  > 

        imgpath( "i01" )  -->  "_input/qp-image-i01.png"
        imgpath( "i01" , "O" )  -->  "_output/qp-image-i01.png"

    """
    ctest = os.path.basename(here(2,dirname=False ))
    #r = re.search("([^-]+).py$", ctest ,  re.I )
    r = re.search("^test\-(.*).py$", ctest ,  re.I )
    
    return os.path.join(
        { "I": "_input" , "O": "_output" }[저장위치], 
        r.group(1).lower() + "-" + addname + ".png"
        )
    

class ClsTest : 
    '''
    def test_1(self):
        eq_(2*2,4)
        
    def test_2(self):
        ok_(30+60 == 90 )
    
    #@nottest
    @istest
    def o3(self):
        eq_(2*2,4)
    '''
    
    @classmethod
    def setup_class(klass):
        """This method is run once for each class before any tests are run"""    
    @classmethod
    def teardown_class(klass):
        """This method is run once for each class _after_ all tests are run""" 
    
    def setUp(self):
        """This method is run once before _each_ test method is executed"""    
    
    def teardown(self):
        """This method is run once after _each_ test method is executed""" 
