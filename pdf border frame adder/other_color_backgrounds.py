import fitz  # PyMuPDF library

def add_background_to_pdf(input_pdf_path, output_pdf_path, image_path):
    print("PDF par background apply kiya ja raha hai...")
    
    # 1. Original PDF ko open karein
    doc = fitz.open(input_pdf_path)
    
    for page in doc:
        # 2. Image ko background ke tor par insert karein
        # overlay=False ka matlab hai ke image text ke peeche jayegi
        page.insert_image(page.rect, filename=image_path, keep_proportion=False, overlay=False)
        
    # 3. Final PDF save karein
    doc.save(output_pdf_path)
    doc.close()
    
    print(f"\nMukammal ho gaya! Nayi PDF yahan save hai:\n{output_pdf_path}")

# --- Aapke Paths ---
input_pdf = r"C:\Users\PCS\Downloads\Aina_Dar_submission - Google Docs.pdf"
image_frame = r"C:\Users\PCS\Downloads\Floral-Border-for-Invitation-edit-online.png" # Original image use karein
output_pdf = r"C:\Users\PCS\Downloads\Aina Dar By Mah Noor Shahzaad_output.pdf" 

add_background_to_pdf(input_pdf, output_pdf, image_frame)