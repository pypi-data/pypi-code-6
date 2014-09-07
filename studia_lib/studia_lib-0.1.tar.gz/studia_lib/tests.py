import unittest

import csv_loader


class CSVLoaderTestCase(unittest.TestCase):

    def test_get_csv(self):
        questions = csv_loader.get_questions('data/test.csv')

        self.assertIsInstance(questions, list)
        self.assertEqual(len(questions), 5)
        
        self.assertIn('Testowe pytanie 1', questions[0])
        
if __name__ == '__main__':
    unittest.main()
