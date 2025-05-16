from pathlib import Path
import sys
import unittest
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from parser import extracting_data_from_html
class TestExtractingDataFromHTML(unittest.TestCase):
    def setUp(self):
        base_dir = Path(__file__).resolve().parent.parent.parent
        self.input_path = base_dir / 'files' / 'van-gogh-paintings.html'
        self.output_path = base_dir / 'files' / 'test-output.json'
        
        # Clean up old file if it exists
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

    def test_extracting_data_from_html_and_json_output(self):
        with open(self.input_path, 'r', encoding='utf-8') as f:
            html = f.read()

        result = extracting_data_from_html(html, self.output_path)

        # Check that output file was created
        self.assertTrue(os.path.exists(self.output_path))

        # Check structure of the result
        self.assertIsInstance(result, dict)
        self.assertTrue(len(result.keys()) > 0)
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

    def tearDown(self):
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

if __name__ == "__main__":
    unittest.main()
