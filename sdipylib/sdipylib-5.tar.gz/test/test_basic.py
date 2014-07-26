import unittest

class TestBase(unittest.TestCase):
    
    
    def test_basic(self):
        from sdipylib.url import cache_url
        
        x = 's3://restricted.sandiegodata.org/manifests/134675d9-2845-458b-a153-3a3ab1d2dec7/camigrations.csv'
        
        print cache_url(x)
        
if __name__ == '__main__':
    unittest.main()