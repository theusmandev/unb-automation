import logging
import os
from pathlib import Path
from pypdf import PdfReader, PdfWriter

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def crop_pdf(input_path, output_path, left=0, right=0, top=0, bottom=0):
    """Har side ke liye alag mm value ke mutabiq crop karta hai."""
    try:
        mm_to_pt = 72 / 25.4
        
        reader = PdfReader(input_path)
        writer = PdfWriter()

        for page in reader.pages:
            box = page.mediabox
            
            # Har side ki calculation (mm to points conversion ke saath)
            new_left   = box.lower_left[0] + (left * mm_to_pt)
            new_bottom = box.lower_left[1] + (bottom * mm_to_pt)
            new_right  = box.upper_right[0] - (right * mm_to_pt)
            new_top    = box.upper_right[1] - (top * mm_to_pt)

            # Naye margins apply karna
            page.mediabox.lower_left = (new_left, new_bottom)
            page.mediabox.upper_right = (new_right, new_top)
            
            writer.add_page(page)

        with open(output_path, "wb") as f:
            writer.write(f)
        return True
    except Exception as e:
        logging.error(f"Error processing {input_path}: {str(e)}")
        return False

def process_folder(input_folder, output_folder, **margins):
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    pdf_files = list(input_path.glob("*.pdf"))
    if not pdf_files:
        logging.warning("Folder mein koi PDF nahi mili!")
        return

    for pdf_file in pdf_files:
        output_file = output_path / pdf_file.name
        logging.info(f"Processing: {pdf_file.name}")
        crop_pdf(str(pdf_file), str(output_file), **margins)

# --- Settings Yahan Badlein ---
if __name__ == "__main__":
    # 1. Folders ke raste
    in_dir = r"E:\unb-workstation\Writers All Novels\Uploadings\novelkiduniya"
    out_dir = r"E:\unb-workstation\Writers All Novels\Uploadings\novelkiduniya_ok"

    # 2. Apni marzi ki values (Millimeters mein)
    my_margins = {
        "left": 0,    # Left se 20mm andar
        "bottom": 29,  # Neeche se 15mm upar
        "right": 0,   # Right se 10mm andar
        "top": 31      # Upar se koi cutting nahi
    }
    
    
    