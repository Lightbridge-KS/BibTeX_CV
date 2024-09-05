import sys
from pybtex.database import parse_string
from pybtex.database.output.bibtex import Writer

def main():
    if len(sys.argv) != 3:
        print("Usage: python convert.py <input_bibtex_file> <output_ris_file>")
        sys.exit(1)
    
    bibtex_path = sys.argv[1]
    ris_path = sys.argv[2]
    
    bibtex_to_ris_file(bibtex_path, ris_path)


def bibtex_to_ris_file(bibtex_path, ris_path):
    # Step 1: Read the BibTeX file
    bibtex_content = read_text_file(bibtex_path)
    
    if bibtex_content is None:
        print(f"Failed to read BibTeX file from {bibtex_path}.")
        return
    
    # Step 2: Convert the BibTeX content to RIS format
    ris_content = bibtex_to_ris(bibtex_content)
    
    # Step 3: Write the RIS content to the output file
    write_text_file(ris_content, ris_path)


def bibtex_to_ris(bibtex_str):
    bib_data = parse_string(bibtex_str, 'bibtex')
    ris_entries = []
    
    for entry in bib_data.entries.values():
        ris_entry = []
        entry_type = entry.type.upper()
        
        if entry_type == 'MANUAL':
            ris_entry.append("TY  - MANUAL")
        else:
            ris_entry.append(f"TY  - {entry_type}")

        for person in entry.persons.get('author', []):
            ris_entry.append(f"AU  - {person.first_names[0]} {person.last_names[0]}")

        ris_entry.append(f"TI  - {entry.fields.get('title', '')}")
        ris_entry.append(f"PY  - {entry.fields.get('year', '')}")
        ris_entry.append(f"UR  - {entry.fields.get('url', '')}")
        ris_entry.append(f"N1  - {entry.fields.get('note', '')}")
        ris_entry.append("ER  - ")

        ris_entries.append('\n'.join(ris_entry))
    
    return '\n\n'.join(ris_entries)


def read_text_file(file_path):
    from pathlib import Path
    
    file_path = Path(file_path)
    try:
        # Open the text file in read mode
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read the entire file content into a string
            text_content = file.read()
            return text_content
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        

def write_text_file(text, file_path):
    from pathlib import Path
    
    file_path = Path(file_path)
    try:
        # Open the text file in write mode
        with open(file_path, 'w', encoding='utf-8') as file:
            # Write the string of text to the file
            file.write(text)
        print(f"Text successfully written to {file_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
        
if __name__ == "__main__":
    main()