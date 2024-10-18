import docx
from docx.shared import RGBColor
from fuzzywuzzy import fuzz

#needs changes in relevant passages logic

def highlight_relevant_passages(input_file, output_file, relevant_passages):
    # Read the original text
    with open(input_file, 'r', encoding='utf-8') as file:
        original_text = file.read()

    # Create a new Word document
    doc = docx.Document()

    # Process the text and add it to the document with highlighting
    current_pos = 0
    for passage in relevant_passages:
        # Find the best match for the passage in the remaining text
        best_match = None
        best_ratio = 0
        for i in range(current_pos, len(original_text) - len(passage) + 1):
            substring = original_text[i:i+len(passage)]
            ratio = fuzz.ratio(passage, substring)
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = (i, i + len(passage))

        if best_match:
            # Add the text before the match
            doc.add_paragraph(original_text[current_pos:best_match[0]])

            # Add the matched text with yellow highlighting
            p = doc.add_paragraph()
            run = p.add_run(original_text[best_match[0]:best_match[1]])
            run.font.highlight_color = docx.enum.text.WD_COLOR_INDEX.YELLOW

            current_pos = best_match[1]

    # Add any remaining text
    if current_pos < len(original_text):
        doc.add_paragraph(original_text[current_pos:])

    # Save the document
    doc.save(output_file)

def create_plain_text_output(output_file, document_name, relevant_passages):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(f"In this text: {document_name} the following has been found:\n")
        for passage in relevant_passages:
            file.write(f"{passage}\n")

def create_barcode_plot(input_file, output_file, relevant_passages):
    with open(input_file, 'r', encoding='utf-8') as file:
        original_text = file.read()

    barcode = [' '] * len(original_text)

    for passage in relevant_passages:
        start = original_text.find(passage)
        if start != -1:
            for i in range(start, start + len(passage)):
                barcode[i] = '|'

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(''.join(barcode))
