import fitz  # PyMuPDF
from PIL import Image, ImageChops
import io

def apply_background_multiply(input_pdf_path, output_pdf_path, image_path):
    print("Processing shuru ho gayi hai... Is mein thora waqt lag sakta hai kyunke hum high-quality blend kar rahe hain.")
    
    # 1. Original background image open karein
    bg_image = Image.open(image_path).convert("RGB")
    
    # 2. PDF open karein
    doc = fitz.open(input_pdf_path)
    
    # Nayi (khali) PDF banayein jismein hum final pages daalenge
    out_pdf = fitz.open()

    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # 3. PDF page ko high-resolution image (300 DPI) mein convert karein taake text blur na ho
        pix = page.get_pixmap(dpi=300)
        pdf_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # 4. Background image ko PDF page ke size ke mutabiq resize karein
        bg_resized = bg_image.resize((pdf_img.width, pdf_img.height))
        
        # --- JADOO YAHAN HOTA HAI ---
        # Multiply blend safed (white) background ko transparent kar deta hai 
        # aur black text ko naye background par waisa hi rakhta hai
        blended_img = ImageChops.multiply(bg_resized, pdf_img)
        
        # 5. Blended image ko temporary memory (bytes) mein save karein
        img_byte_arr = io.BytesIO()
        blended_img.save(img_byte_arr, format='JPEG', quality=95)
        img_bytes = img_byte_arr.getvalue()
        
        # 6. Nayi PDF mein page banayein aur ye image laga dein
        out_page = out_pdf.new_page(width=page.rect.width, height=page.rect.height)
        out_page.insert_image(out_page.rect, stream=img_bytes)
        
    out_pdf.save(output_pdf_path)
    out_pdf.close()
    doc.close()
    print(f"\nZabardast! Nayi PDF yahan save ho gayi hai:\n{output_pdf_path}")

# --- Aapke Paths ---
input_pdf = r"C:\Users\PCS\Downloads\Aina_Dar_submission - Google Docs.pdf"
image_frame = r"C:\Users\PCS\Downloads\Vintage-Page-Border-Template-edit-online.png"
output_pdf = r"C:\Users\PCS\Downloads\Aina Dar By Mah Noor Shahzaad_output.pdf" 

apply_background_multiply(input_pdf, output_pdf, image_frame)