import fitz  # PyMuPDF

def add_perfect_border(input_pdf_path, output_pdf_path, transparent_image_path):
    print("Processing shuru ho gayi hai...")
    
    doc = fitz.open(input_pdf_path)
    
    for page in doc:
        # overlay=True border ko upar lagayega. 
        # Kyunke image ab naturally transparent hai, to text nahi chupega 
        # aur border ki quality bilkul original (sharp) aayegi.
        page.insert_image(page.rect, filename=transparent_image_path, overlay=True)
        
    # File size chota rakhne ke liye best optimization (Duplicate images ko rokta hai)
    doc.save(output_pdf_path, garbage=3, deflate=True)
    doc.close()
    
    print(f"\nKaam mukammal! Nayi perfect PDF yahan save ho gayi hai:\n{output_pdf_path}")


# --- Aapke Paths ---
input_pdf = r"C:\Users\PCS\Downloads\Akhi by hooria Amna khan correct file.pdf"

# YAHAN APNI NAYI TRANSPARENT PNG KA PATH DENA HAI:
transparent_frame = r"E:\unb-workstation\Writers All Novels\borders\L-3-R-3-T-4.7-B-4.7 (2)compressed-Photoroom.png"

output_pdf = r"C:\Users\PCS\Downloads\Akhi by hooria Amna khan final_perfect.pdf"

add_perfect_border(input_pdf, output_pdf, transparent_frame)









# import fitz  # PyMuPDF
# from PIL import Image
# import io

# def add_transparent_border_efficiently(input_pdf_path, output_pdf_path, image_path):
#     print("Processing shuru ho gayi hai... Image ko transparent banaya ja raha hai.")
    
#     # --- STEP 1: Border image ke white hisse ko transparent karna ---
#     img = Image.open(image_path).convert("RGBA")
#     datas = img.getdata()
#     newData = []
    
#     # Har pixel ko check karein, agar white/light color hai to transparent kar dein
#     for item in datas:
#         # RGB values check kar rahe hain (240 se upar ka matlab hai white ke qareeb)
#         if item[0] > 240 and item[1] > 240 and item[2] > 240:
#             newData.append((255, 255, 255, 0)) # Aakhri '0' ka matlab hai 100% transparent
#         else:
#             newData.append(item) # Border ke design ko waisa hi rakhein
            
#     img.putdata(newData)
    
#     # Transparent image ko temporary memory mein save karein (PNG format zaroori hai)
#     img_byte_arr = io.BytesIO()
#     img.save(img_byte_arr, format='PNG', optimize=True)
#     transparent_img_bytes = img_byte_arr.getvalue()

#     # --- STEP 2: PDF par transparent border lagana ---
#     doc = fitz.open(input_pdf_path)
    
#     for page in doc:
#         # Ab hum 'overlay=True' use karenge, kyunke image ab transparent hai
#         # Toh text nahi chupega aur border upar nazar aayega
#         page.insert_image(page.rect, stream=transparent_img_bytes, overlay=True)
        
#     # PDF ko optimize karke save karein taake size 4MB ke aas paas hi rahe
#     # garbage=3 aur deflate=True duplicate images ko ek hi baar save karte hain
#     doc.save(output_pdf_path, garbage=3, deflate=True)
#     doc.close()
    
#     print(f"\nMasla hal ho gaya! Nayi PDF yahan save ho gayi hai:\n{output_pdf_path}")

# # --- Aapke Paths ---
# input_pdf = r"C:\Users\PCS\Downloads\Akhi by hooria Amna khan correct file.pdf"
# image_frame = r"E:\unb-workstation\Writers All Novels\borders\L-3-R-3-T-4.7-B-4.7 (2)compressed.png"
# output_pdf = r"C:\Users\PCS\Downloads\Akhi by hooria Amna khan correct file_output_fixed.pdf"

# add_transparent_border_efficiently(input_pdf, output_pdf, image_frame)








# import fitz  # PyMuPDF
# from PIL import Image, ImageChops
# import io

# def apply_background_multiply(input_pdf_path, output_pdf_path, image_path):
#     print("Processing shuru ho gayi hai... Is mein thora waqt lag sakta hai kyunke hum high-quality blend kar rahe hain.")
    
#     # 1. Original background image open karein
#     bg_image = Image.open(image_path).convert("RGB")
    
#     # 2. PDF open karein
#     doc = fitz.open(input_pdf_path)
    
#     # Nayi (khali) PDF banayein jismein hum final pages daalenge
#     out_pdf = fitz.open()

#     for page_num in range(len(doc)):
#         page = doc[page_num]
        
#         # 3. PDF page ko high-resolution image (300 DPI) mein convert karein taake text blur na ho
#         pix = page.get_pixmap(dpi=300)
#         pdf_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
#         # 4. Background image ko PDF page ke size ke mutabiq resize karein
#         bg_resized = bg_image.resize((pdf_img.width, pdf_img.height))
        
#         # --- JADOO YAHAN HOTA HAI ---
#         # Multiply blend safed (white) background ko transparent kar deta hai 
#         # aur black text ko naye background par waisa hi rakhta hai
#         blended_img = ImageChops.multiply(bg_resized, pdf_img)
        
#         # 5. Blended image ko temporary memory (bytes) mein save karein
#         img_byte_arr = io.BytesIO()
#         blended_img.save(img_byte_arr, format='JPEG', quality=95)
#         img_bytes = img_byte_arr.getvalue()
        
#         # 6. Nayi PDF mein page banayein aur ye image laga dein
#         out_page = out_pdf.new_page(width=page.rect.width, height=page.rect.height)
#         out_page.insert_image(out_page.rect, stream=img_bytes)
        
#     out_pdf.save(output_pdf_path)
#     out_pdf.close()
#     doc.close()
#     print(f"\nZabardast! Nayi PDF yahan save ho gayi hai:\n{output_pdf_path}")

# # --- Aapke Paths ---
# input_pdf = r"C:\Users\PCS\Downloads\Akhi by hooria Amna khan correct file.pdf"
# image_frame = r"E:\unb-workstation\Writers All Novels\borders\L-3-R-3-T-4.7-B-4.7 (2)compressed.png"
# output_pdf = r"C:\Users\PCS\Downloads\Akhi by hooria Amna khan correct file_output.pdf"

# apply_background_multiply(input_pdf, output_pdf, image_frame)