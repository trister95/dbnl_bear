import os
import lxml.etree as ET
import tqdm
import glob
import re
import html
from typing import List, Dict, Optional

class DBNLParser:
    @staticmethod
    def create_if_absent(directory):
        """
        Function creates a directory if it doesn't exist already.
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
            print("Directory", directory, "created")
        else:
            print("Directory", directory, "already exists")
    
    @staticmethod
    def get_files_with_extension(directory, extension):
        """
        Gets all files with a specific extension (like .xml) from a specific directory.
        """
        try:
            # Using glob for pattern matching
            return [
                os.path.basename(file) for file in glob.glob(f"{directory}/*.{extension}")
                ]
        except OSError as e:
            print(f"Error: {e}")
            return []
    
    @staticmethod
    def clean_whitespace(text):
        """Clean unnecessary whitespaces from the text."""
        #Collapse multiple spaces and tabs
        text = re.sub(r"[ \t]+", " ", text)
        #Convert multiple newlines to a double newline for paragraph separation
        text = re.sub(r"(\s*\n\s*)+", "\n\n", text)
        return text.strip()
    
    @staticmethod
    def extract_dbnl_id(f_name):
        """
        Extract dbnl-id from a filename.
        """
        pattern = r"[a-zA-Z_]{4}\d{3}[a-zA-Z_\d]{4}\d{2}"
        regex = re.compile(pattern)
        match = regex.search(f_name)
        return match[0] if match else None
    
    def make_html_entity_dict(self):
        """
        This function makes a dict where html character entities
        (like: "&nbsp;") are coupled to xml-readable html decimal
        representations (like: "&160;").

        Note that in this function the named entities cannot
        end with a semicolon and can only have a length of 1.
        """
        html_decimal_dict = {}
        for entity, codepoint in html.entities.html5.items():
            if len(codepoint) == 1 and not entity.endswith(";"):
                html_decimal_dict[entity] = ord(codepoint)
        additional_entities = {
            'lsquo': ord('‘'),
            'rsquo': ord('’'),
            'ldquo': ord('“'),
            'rdquo': ord('”'),
            'dagger': ord('†'),
            'rarr': ord('→'),
            'phi': ord('φ'),
            'Sigma': ord('Σ'),
            'alpha': ord('α'),
            'omicron': ord('ο'),
            'rho': ord('ρ'),
            'sigmaf': ord('ς'),
            'nu': ord('ν'),
            'omega': ord('ω'),
            'eta': ord('η'),
            'nacute': ord('ń'),
            'pi': ord('π'),
            'tau': ord('τ'),
            'sigma': ord('σ'),
            'epsilon': ord('ε'),
        }
        html_decimal_dict.update(additional_entities)
        return html_decimal_dict

    def additional_declaration_str(self):
        """
        This function formulates a additional declaration string for XML documents.
        Give it the end of the old declaration (make sure this only pops up once in
        the document!) and provide a dictionary.
        Note that this function is written for conversion of html character entities
        to numerical representations. For other use, some tweaks might be needed.
        """
        html_decimal_dict = self.make_html_entity_dict()
        new_declaration = ""

        for item in html_decimal_dict.items():
            new_str = f'<!ENTITY {item[0]} "&#{item[1]};">\n'
            new_declaration += new_str

        return '.dtd"' + "\n[" + new_declaration + "]"


    def add_declaration_to_xml(self, xml_dir):
        """
        This functions adds an entity declaration. It also checks if the "new" declaration
        isn't already present.
        """
        addition = self.additional_declaration_str()

        for f_name in tqdm.tqdm(os.listdir(xml_dir)):
            if f_name.endswith(".xml"):
                with open(os.path.join(xml_dir, f_name), "r", encoding="utf-8") as f:
                    xml_text = f.read()
                    start = xml_text.find('<!DOCTYPE')
                    end = xml_text.find('.dtd"') + len('.dtd"')
                    doctype = xml_text[start:end]
                    new_doctype = doctype.replace('.dtd"', addition)
                    if new_doctype not in xml_text:
                        xml_text = xml_text[:start] + new_doctype + xml_text[end:]
                        with open(
                            os.path.join(xml_dir, f_name), "w", encoding="utf-8"
                            ) as f:
                            f.write(xml_text)

    @staticmethod
    def find_text_element(root):
        """
        Find and return the <text> element from the XML tree. If the number of text elements is not equal to 1, something fishy is going on and
        we get an error. In this case you should get to the BOTTOM of it since it is VERY unexpected.
        """
        text_elements = root.findall(".//text")
        if len(text_elements) != 1:
            raise ValueError(f"Expected exactly 1 <text> element, but found {len(text_elements)}.")
        return text_elements[0]

    def get_text_dbnl(self, xml_file, id, output_dir):
        """
        Extracts text from a dbnl xml-file and saves it as a .txt file.
        In this setup, notes in the texts (e.g. explanations, references) are not removed!
        """
        # Parse the XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()

    # Find the <text> element and extract main text
        text_element = self.find_text_element(root)
        main_text = self.clean_whitespace("".join(text_element.itertext()))

        # Save the combined text to a file
        with open(f"{output_dir}/{id}.txt", "w", encoding="utf-8") as f:
            f.write(main_text)


    def dbnl_to_txt(self, input_dir, output_dir="dbnl_txt_files"):
        """
        Puts the pieces of the pipeline together.
        """
        self.add_declaration_to_xml(input_dir)
        xml_files = self.get_files_with_extension(input_dir, "xml")
        self.create_if_absent(output_dir)
        for f in tqdm.tqdm(xml_files):
            id = self.extract_dbnl_id(f)
            p = os.path.join(input_dir, f)
            try:
                self.get_text_dbnl(p, id, output_dir)
            except Exception as e:
                error_message = f"file {id} could not be parsed because of: {e}"
                print(error_message)

parser = DBNLParser()