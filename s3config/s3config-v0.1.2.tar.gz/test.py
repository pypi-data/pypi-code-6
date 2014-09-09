import unittest
from s3config import S3Config, Parser

class TestParser(unittest.TestCase):
    
    def setUp(self):
        self.end_data = {
            'name': 'Vorlin Laruknuzum', 
            'gold': 423, 
            'float': 42.3, 
            'title': 'Acolyte', 
            'sp': [1, 13], 
            'inventory': [
                'a Holy Book of Prayers (Words of Wisdom)', 
                'an Azure Potion of Cure Light Wounds', 
                'a Silver Wand of Wonder'],
            }
        
    def test_invalid_schema(self):
        parser = Parser(schema="an_invalid_schema")
        with self.assertRaises(ValueError):
            parser.parse('123')
            
    def test_json(self):
        data = """
        {
            "name": "Vorlin Laruknuzum", 
            "gold": 423, 
            "float": 42.3,
            "title": "Acolyte", 
            "sp": [1, 13], 
            "inventory": [
                "a Holy Book of Prayers (Words of Wisdom)", 
                "an Azure Potion of Cure Light Wounds", 
                "a Silver Wand of Wonder"
            ]
        }
        """
        parser = Parser(schema="json")
        self.assertTrue(parser.parse(data) == self.end_data)
        
    def test_yaml(self):
        data = """
        name: Vorlin Laruknuzum
        title: Acolyte
        sp: [1, 13]
        gold: 423
        float: 42.3
        inventory:
        - a Holy Book of Prayers (Words of Wisdom)
        - an Azure Potion of Cure Light Wounds
        - a Silver Wand of Wonder
        """
        parser = Parser(schema="yaml")
        self.assertTrue(parser.parse(data) == self.end_data)
        

class TestS3Config(unittest.TestCase):
    def test_urls(self):
        self.assertEqual(S3Config("s3://asd_backer/mi/ofile.json").parse_url(), ("asd_backer","mi/ofile.json"))
        self.assertEqual(S3Config("s3://asdbacker/mi_ofile.json").parse_url(), ("asdbacker","mi_ofile.json"))
        self.assertEqual(S3Config("s3://asd-backer/mi-ofile").parse_url(),("asd-backer","mi-ofile"))
        self.assertRaises(ValueError,S3Config,"invalid://s3sd-backer")
        
    def test_schema(self):
        self.assertEqual(S3Config.schema_from_key("key.json"), "json")
        self.assertEqual(S3Config.schema_from_key("key.yaml"), "yaml")
        self.assertEqual(S3Config.schema_from_key("key..test"), "test")
        self.assertEqual(S3Config.schema_from_key("key"), "")
        
    def test_s3config(self):
        config = S3Config("s3://s3config/config.json").read()
        self.assertIsInstance(config,dict)
        self.assertTrue(len(config.keys())==6)
        config = S3Config("s3://s3config/config.yaml").read()
        self.assertIsInstance(config,dict)
        self.assertTrue(len(config.keys())==6)

if __name__ == '__main__':
    unittest.main()
    