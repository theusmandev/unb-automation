
    
import logging
import os
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from tqdm import tqdm  # Progress bar ke liye

# Logging setup - logging ko file mein save karna behtar hai taake progress bar kharab na ho
logging.basicConfig(
    filename='pdf_crop_log.log', 
    level=logging.ERROR, 
    format='%(asctime)s - %(levelname)s: %(message)s'
)

def crop_pdf(input_path, output_path, left=0, right=0, top=0, bottom=0):
    """PDF ko mm ke hisab se crop karta hai."""
    try:
        mm_to_pt = 72 / 25.4
        reader = PdfReader(input_path)
        writer = PdfWriter()

        for page in reader.pages:
            # MediaBox (Original Page Size)
            box = page.mediabox
            
            # Naye coordinates calculate karna
            new_left   = float(box.lower_left[0]) + (left * mm_to_pt)
            new_bottom = float(box.lower_left[1]) + (bottom * mm_to_pt)
            new_right  = float(box.upper_right[0]) - (right * mm_to_pt)
            new_top    = float(box.upper_right[1]) - (top * mm_to_pt)

            # Crop apply karna
            page.mediabox.lower_left = (new_left, new_bottom)
            page.mediabox.upper_right = (new_right, new_top)
            
            writer.add_page(page)

        with open(output_path, "wb") as f:
            writer.write(f)
        return True
    except Exception as e:
        logging.error(f"Error in {input_path}: {str(e)}")
        return False

def process_folder(input_folder, output_folder, margins):
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    
    if not input_path.exists():
        print(f"❌ Error: Input folder '{input_folder}' nahi mila!")
        return

    output_path.mkdir(parents=True, exist_ok=True)
    pdf_files = list(input_path.glob("*.pdf"))

    if not pdf_files:
        print("⚠️ Folder mein koi PDF files nahi hain.")
        return

    print(f"🚀 Processing {len(pdf_files)} PDFs...\n")

    # TQDM Progress Bar ka istemal
    for pdf_file in tqdm(pdf_files, desc="Progress", unit="file", bar_format='{l_bar}{bar:30}{r_bar}{bar:-10b}'):
        output_file = output_path / pdf_file.name
        success = crop_pdf(str(pdf_file), str(output_file), **margins)
        
        if not success:
            tqdm.write(f"❌ Failed: {pdf_file.name} (Check log for details)")

    print(f"\n✅ Kaam khatam! Files yahan save hain: {output_folder}")

# --- Settings ---
if __name__ == "__main__":
    # 1. Folders ke paths
    CONFIG = {
        "in_dir": r"E:\unb-workstation\Writers All Novels\Uploadings\novelkiduniya",
        "out_dir": r"E:\unb-workstation\Writers All Novels\Uploadings\novelkiduniya_ok"
    }

    # 2. Margins (Millimeters mein)
    MY_MARGINS = {
        "left": 0,
        "bottom": 15,
        "right": 0,
        "top": 15
    }
    
    
        # 2. Apni marzi ki values (Millimeters mein)
    # my_margins = {
    #     "left": 0,    # Left se 20mm andar
    #     "bottom": 29,  # Neeche se 15mm upar
    #     "right": 0,   # Right se 10mm andar
    #     "top": 31      # Upar se koi cutting nahi
    # }
    

    process_folder(CONFIG["in_dir"], CONFIG["out_dir"], MY_MARGINS)
    