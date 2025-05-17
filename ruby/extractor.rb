require 'nokogiri'
require 'json'

def extracting_data_from_html(html_content, output_file = 'output.json')
# This function takes in HTML content and pulls out data from it.
# It uses Nokogiri to go through the HTML and grab things like:
#   - name
#   - extensions (like year or author)
#   - link to the Google result
#   - image (with fallback if it's just a placeholder)
# for each item in the group like paintings or books.
# Everything gets returned in a clean dictionary grouped by the category heading.
  
  doc = Nokogiri::HTML(html_content)
  results = {}

  # grab the group title like artworks
  heading_tag = doc.at_css('span.mgAbYb.OSrXXb.RES9jf.IFnjPb')
  heading = heading_tag ? heading_tag.text.strip : 'N/A'
  
  # loop through each group of items like painting or books
  doc.css('div.Cz5hV').each do |group|

    # list to store all items inside this group
    items = []

    # now grab each individual item in the group like each painting
    group.css('div.iELo6').each do |container|

      # this block holds the actual details of the item like name and year
      details_block = container.at_css('div.KHK6lb')

      # grab the name of the item
      name_tag = details_block&.at_css('div.pgNMRc')
      
      # grab the extension info like year
      extensions_tag = details_block&.at_css('div.cxzHyb')
      
      # grab the link to google search
      link_tag = container.at_css('a[href]')

      # grab the image
      image_tag = container.at_css('img.taFZJe')

      # extract the text values or set fallback if not found
      name = name_tag ? name_tag.text.strip : 'N/A'
      extensions = extensions_tag ? [extensions_tag.text.strip] : []
      link = link_tag ? "https://www.google.com#{link_tag['href']}" : 'N/A'

      thumbnail = image_tag ? image_tag['src'] : nil

      # Handle placeholder 1x1 gif and try to extract real base64
      if thumbnail&.include?('R0lGODlhAQABAIAAA')
        script_tag = container.xpath("following-sibling::script").find { |s| s.text.include?('data:image') }
        if script_tag
          match = script_tag.text.match(/data:image\/jpeg;base64,[A-Za-z0-9+\/=]+/)
          thumbnail = match[0] if match
        end
      end

      thumbnail ||= 'N/A'

      # build the final object for this item
      items << {
        name: name,
        extensions: extensions,
        link: link,
        image: thumbnail
      }
    end

    results[heading] = items unless items.empty?
  end

  # Save once at the end, with all groups
  File.write(output_file, JSON.pretty_generate(results), mode: 'w:utf-8')
  results
end
