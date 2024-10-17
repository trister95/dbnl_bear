import os
import lxml.etree as ET
import tqdm
import glob
import re

"""
These are helper functions.
"""

def create_if_absent(directory):
    """
    Function creates a directory if it doesn't exist already.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("Directory", directory, "created")
    else:
        print("Directory", directory, "already exists")
    return

def get_files_with_extension(directory, extension):
    """
    Outputs all files with a specific extension in a directory.
    """
    try:
        # Using glob for pattern matching
        return [
            os.path.basename(file) for file in glob.glob(f"{directory}/*.{extension}")
        ]
    except OSError as e:
        print(f"Error: {e}")
        return []

def clean_whitespace(text):
    """Clean unnecessary whitespaces from the text."""
    # Collapse multiple spaces and newlines
    text = re.sub(r"\s+", " ", text)
    # Optional: Convert multiple newlines to a double newline for paragraph separation
    text = re.sub(r"(\s*\n\s*)+", "\n\n", text)
    return text.strip()

def extract_dbnl_id(f_name):
    """
    Etract dbnl-id from a filename.
    """
    pattern = r"[a-zA-Z_]{4}\d{3}[a-zA-Z_\d]{4}\d{2}"
    regex = re.compile(pattern)
    match = regex.search(f_name)
    return match[0] if match else None

"""
These functions extract the actual literary texts
from a directory with dbnl-xml files.
"""

def find_text_element(root):
    """
    Find and return the <text> element from the XML tree. If the number of text elements is not equal to 1, something fishy is going on and
    we get an error. In this case you should get to the BOTTOM of it since it is VERY unexpected.
    """
    text_elements = root.findall(".//text")
    if len(text_elements) != 1:
        raise ValueError(f"Expected exactly 1 <text> element, but found {len(text_elements)}.")
    return text_elements[0]

def get_text_dbnl(xml_file, id, output_dir):
    """
    Extracts text from a dbnl xml-file and saves it as a .txt file.
    In this setup, notes are not removed!
    """
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Find the <text> element and extract main text
    text_element = find_text_element(root)
    main_text = clean_whitespace("".join(text_element.itertext()))

    # Save the combined text to a file
    with open(f"{output_dir}/{id}.txt", "w", encoding="utf-8") as f:
        f.write(main_text)


def dbnl_to_txt(input_dir, output_dir="dbnl_txt_files"):
    """
    Puts the pieces of the pipeline together.
    """
    xml_files = get_files_with_extension(input_dir, "xml")
    create_if_absent(output_dir)
    for f in tqdm.tqdm(xml_files):
        id = extract_dbnl_id(f)
        p = os.path.join(input_dir, f)
        try:
            get_text_dbnl(p, id, output_dir)
        except Exception as e:
            error_message = f"file {id} could not be parsed because of: {e}"
            print(error_message)
    return
