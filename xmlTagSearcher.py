# Description: python command line script to search an xml file for a specific tag that contains a value, and export out any matching tags and their parent structures to a new xml file which is a subset of the original
import sys
import xml.etree.ElementTree as ET

def search_and_extract(filename, search_tag_name, search_tag_contents):
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
    except FileNotFoundError:
        print("Error: File not found.")
        return
    except ET.ParseError:
        print("Error: Invalid XML file.")
        return
    except Exception as e:
        print("Error:", e)
        return

    found_tags = []
    for parent in root.iter():
        for child in parent:
            if child.tag == search_tag_name and child.text == search_tag_contents:
                found_tags.append(parent)
                break

    if not found_tags:
        print("No matching tags found.")
        return

    new_filename = filename.split('.')[0] + "-searchedTagExport.xml"
    with open(new_filename, 'w', encoding='utf-8') as f:  # Specify UTF-8 encoding
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        f.write("<{}>\n".format(root.tag))
        for tag in found_tags:
            f.write(ET.tostring(tag, encoding='unicode'))
        f.write("\n</{}>".format(root.tag))  # Added line break and indentation
    print("Tags extracted and written to {}.".format(new_filename))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <filename> <search_tag_name> <search_tag_contents>")
    else:
        filename = sys.argv[1]
        search_tag_name = sys.argv[2]
        search_tag_contents = sys.argv[3]
        search_and_extract(filename, search_tag_name, search_tag_contents)
