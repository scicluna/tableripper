import PyPDF2
import re
import json

def barker_cleanup(items):
    pattern = re.compile(r'^\d+')
    items[:] = [re.sub(r'([A-Za-z]+\sBi\scoo\(.*?\)\d+\))', '', item) for item in items if pattern.match(item.strip())]


# Create an empty string to hold the text from all pages
all_text = ""
table_list = []
barker = True
aeg = False

# Unicode replacements
unicode_replacements = {
    '\u2013': '-',  # en dash
    '\u2014': '-',  # em dash
    '\u2019': "'",  # right single quote
    '\u201c': '"',  # left double quote
    '\u201d': '"',  # right double quote
    '\uf074': '',   # private use character
    '\uf075': '',    # private use character
    '\u2026': '.',
    'Y ou': 'You'
}

# Open the PDF file in binary mode
with open("./input/source.pdf", "rb") as file:

    # Create a PDF file reader
    reader = PyPDF2.PdfReader(file)

    # Loop over each page (zero-indexed)
    for i in range(len(reader.pages)):

        # Get the text content from the page
        page = reader.pages[i]
        text = page.extract_text()

        # Add the text from this page to the all_text string
        all_text += text

# Regular expression to match tables
aeg_table_pattern = r"(Table \d+–\d+:.*?(?=Table \d+–\d+:|$))"
barker_table_pattern = r"(d\d{1,2}.*?(?=d\d{1,2}|$))"

# Use findall to extract all tables
tables = re.findall(barker_table_pattern, all_text, re.DOTALL)

# Now tables is a list of strings, with each string being a table
for i, table in enumerate(tables):
    # Split the table into lines
    lines = table.split("\n")

    # The first line is the table header
    header = lines[0]

    # Replace Unicode characters in header
    for unicode_char, replacement in unicode_replacements.items():
        header = header.replace(unicode_char, replacement)

    # The rest of the lines are the items
    items = lines[1:]

    # Remove the numbers at the end of each item
    items = [re.sub(r"\d+\s*$", "", item).replace('\u2014', '-') for item in items]
    
    # Replace Unicode characters in items
    for unicode_char, replacement in unicode_replacements.items():
        items = [item.replace(unicode_char, replacement) for item in items]

    if barker:
        barker_cleanup(items)

    # Create a dictionary for this table
    table_dict = {"header": header, "items": items}

    # Add the dictionary to the list
    table_list.append(table_dict)

# Write the list of tables to a JSON file
with open('./output/tables.json', 'w') as f:
    json.dump(table_list, f)



