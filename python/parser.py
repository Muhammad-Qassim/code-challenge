import json
import re
from bs4 import BeautifulSoup

def extracting_data_from_html(html_content, output_file='output.json'):
    '''
    This function takes in HTML and pulls out data from it.
    It uses beautifulsoup to go through the html and grab things like:
        -name
        -extenstions
        -link
        -image
    for each item in the group like paintings or books.

    Everything gets returned in a nice dictionary, grouped by category heading.
    '''

    # parse the html using beautifulsoup so we can work with the file
    soup = BeautifulSoup(html_content, 'html.parser')

    # final output will be a dictionary grouped by category name
    results = {}

    # grab the group title like artworks
    heading_tag = soup.find('span', class_='mgAbYb OSrXXb RES9jf IFnjPb')
    heading = heading_tag.get_text(strip=True) if heading_tag else 'N/A'

    # list to store all items inside this group
    items = []

    # loop through each group of items like painting or books
    for group in soup.find_all('div', class_='Cz5hV'):

        # now grab each individual item in the group like each painting
        for container in group.find_all('div', class_='iELo6'):

            # this block holds the actual details of the item like name and year
            details_block = container.find('div', class_='KHK6lb')

            # grab the name of the item
            name_tag = details_block.find('div', class_='pgNMRc') if details_block else None
            
            # grab the extension info like year
            extensions_tag = details_block.find('div', class_='cxzHyb') if details_block else None
            
            # grab the link to google search
            link_tag = container.find('a', href=True)

            # grab the image
            image_tag = container.find('img', class_='taFZJe')
            
            # extract the text values or set fallback if not found
            name = name_tag.get_text(strip=True) if name_tag else 'N/A'
            extensions = [extensions_tag.get_text(strip=True)] if extensions_tag else []
            link = f"https://www.google.com{link_tag['href']}" if link_tag else 'N/A'

            # Grab placeholder image if available
            thumbnail = image_tag['src'] if image_tag and image_tag.has_attr('src') else None
            
            # If it's a 1x1 gif (placeholder), try to extract the real base64 image from nearby script
            if thumbnail and "R0lGODlhAQABAIAAA" in thumbnail:
                script_tag = container.find_next("script", string=lambda s: s and "data:image" in s)
                if script_tag:
                    match = re.search(r"data:image\/jpeg;base64,[A-Za-z0-9+/=]+", script_tag.string)
                    if match:
                        thumbnail = match.group(0)
            
            # Fallback
            thumbnail = thumbnail or 'N/A'
            
            # build the final object for this item
            items.append({
                'name': name,
                'extensions': extensions,
                'link': link,
                'image': thumbnail
            })

        # if we found any itmes, save them under this heading
        if items:
            results[heading] = items

        # saving it to a json file
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(results, json_file, indent=4)

    return results
