from pathlib import Path
import sys
import unittest
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from parser import extracting_data_from_html

class TestExtractingDataFromHTML(unittest.TestCase):
    def setUp(self):
        self.base_dir = Path(__file__).resolve().parent.parent.parent
        self.files_dir = self.base_dir / 'files'
        self.output_path = self.files_dir / 'test-output.json'

    def run_extraction_test(self, filename):
        input_path = self.files_dir / filename

        if os.path.exists(self.output_path):
            os.remove(self.output_path)

        with open(input_path, 'r', encoding='utf-8') as f:
            html = f.read()

        result = extracting_data_from_html(html, self.output_path)

        self.assertTrue(os.path.exists(self.output_path))
        self.assertIsInstance(result, dict)
        self.assertTrue(len(result) > 0)

        first_key = list(result.keys())[0]
        self.assertIsInstance(first_key, str)

        items = result[first_key]
        self.assertIsInstance(items, list)
        self.assertTrue(len(items) > 0)

        sample = items[0]
        self.assertIn('name', sample)
        self.assertIn('extensions', sample)
        self.assertIn('link', sample)
        self.assertIn('image', sample)

    def test_van_gogh_paintings(self):
        self.run_extraction_test('van-gogh-paintings.html')

    def test_leo_painting(self):
        self.run_extraction_test('leo-da-vinci-paintings.html')

    def test_raphael_painting(self):
        self.run_extraction_test('raphael-paintings.html')

    def tearDown(self):
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

if __name__ == "__main__":
    unittest.main()
