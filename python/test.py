import argparse
import json
from parser import extracting_data_from_html

def main():
    parser = argparse.ArgumentParser(description="Extract structured JSON from HTML")
    parser.add_argument("input_file", help="Path to input HTML file")
    parser.add_argument("output_file", help="Path to output JSON file")
    args = parser.parse_args()

    # Read the HTML content
    with open(args.input_file, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Extract the structured data and create a JSON file
    extracted_data = extracting_data_from_html(html_content, args.output_file)

if __name__ == "__main__":
    main()
