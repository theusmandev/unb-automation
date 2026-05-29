import fitz  # PyMuPDF
from PIL import Image

def process_and_add_frame(input_pdf_path, output_pdf_path, image_path):
    # --- Step 1: Frame ke white center ko transparent banana ---
    print("Frame ke white background ko transparent banaya ja raha hai...")
    
    # Image ko RGBA (Alpha/Transparency support ke sath) open karein
    img = Image.open(image_path).convert("RGBA")
    datas = img.getdata()
    
    newData = []
    for item in datas:
        # Agar color white ya almost white hai (RGB values 240 se zyada)
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            # Alpha ko 0 kar do (yani transparent kar do)
            newData.append((255, 255, 255, 0))
        else:
            # Frame ke design ko waise hi rehne do
            newData.append(item)
            
    img.putdata(newData)
    
    # Transparent image ko temporary save karein
    temp_img_path = "transparent_frame_temp.png"
    img.save(temp_img_path, "PNG")
    
    # --- Step 2: Transparent frame ko PDF ke UPAR (overlay=True) lagana ---
    print("PDF par naya frame apply kiya ja raha hai...")
    doc = fitz.open(input_pdf_path)
    
    for page in doc:
        # overlay=True text ke upar frame lagayega, lekin center transparent hone ki wajah se text nazar aayega
        page.insert_image(page.rect, filename=temp_img_path, keep_proportion=False, overlay=True)
        
    doc.save(output_pdf_path)
    doc.close()
    
    print(f"\nMukammal ho gaya! Nayi PDF yahan save hai:\n{output_pdf_path}")

# --- Aapke Paths ---
input_pdf = r"C:\Users\PCS\Downloads\Aina_Dar_submission - Google Docs.pdf"
image_frame = r"C:\Users\PCS\Downloads\czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvdjM3LXdpdC0zOGUtam9iMTI5XzEucG5n.webp"
output_pdf = r"C:\Users\PCS\Downloads\Aina Dar By Mah Noor Shahzaad_output.pdf" 

process_and_add_frame(input_pdf, output_pdf, image_frame)










# import fitz  # PyMuPDF library

# def add_frame_to_pdf(input_pdf_path, output_pdf_path, image_path):
#     # 1. Original PDF ko open karein
#     doc = fitz.open(input_pdf_path)
    
#     for page_num in range(len(doc)):
#         page = doc[page_num]
        
#         # 2. Image ko page par insert karein
#         # overlay=False ka matlab hai ke frame text ke peeche (background) jayega
#         page.insert_image(page.rect, filename=image_path, keep_proportion=False, overlay=False)
        
#     # 3. Final PDF save karein
#     doc.save(output_pdf_path)
#     doc.close()
    
#     print(f"Success! Framed PDF save ho gayi hai:\n{output_pdf_path}")

# # --- Settings ---
# input_pdf = r"C:\Users\PCS\Downloads\Aina Dar By Mah Noor Shahzaad.pdf"
# image_frame = r"C:\Users\PCS\Downloads\688414010_1833338130956305_9098373392037326606_n.png"
# output_pdf = r"C:\Users\PCS\Downloads\Aina Dar By Mah Noor Shahzaad_output.pdf" 

# add_frame_to_pdf(input_pdf, output_pdf, image_frame)















# import io
# from pypdf import PdfReader, PdfWriter
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter

# def add_frame_to_pdf(input_pdf_path, output_pdf_path, image_path):
#     # 1. Original PDF ko read karein
#     reader = PdfReader(input_pdf_path)
#     writer = PdfWriter()

#     for page in reader.pages:
#         # Page ka size lein taake frame sahi fit ho
#         page_width = float(page.mediabox.width)
#         page_height = float(page.mediabox.height)

#         # 2. Image ko background ke liye tayyar karein (In-memory)
#         packet = io.BytesIO()
#         can = canvas.Canvas(packet, pagesize=(page_width, page_height))
        
#         # Image ko poore page par draw karein
#         can.drawImage(image_path, 0, 0, width=page_width, height=page_height)
#         can.save()
#         packet.seek(0)

#         # Background (frame) wala PDF page create karein
#         frame_pdf = PdfReader(packet)
#         frame_page = frame_pdf.pages[0]

#         # 3. Frame ko original page ke saath merge karein
#         # Ham frame ko pehle rakhenge aur text ko uske upar overlay karenge
#         frame_page.merge_page(page)
        
#         # Result ko writer mein add karein
#         writer.add_page(frame_page)

#     # 4. Final PDF save karein
#     with open(output_pdf_path, "wb") as output_file:
#         writer.write(output_file)
    
#     print(f"Success! Framed PDF save ho gayi hai: {output_pdf_path}")

# # --- Settings ---
# input_pdf = r"C:\Users\PCS\Downloads\Aina Dar By Mah Noor Shahzaad.pdf"        # Aapki 15 pages wali novel file
# image_frame = r"C:\Users\PCS\Downloads\688414010_1833338130956305_9098373392037326606_n.png"        # Jo image aapne upload ki hai
# output_pdf = r"C:\Users\PCS\Downloads\Aina Dar By Mah Noor Shahzaad_output.pdf" 

# add_frame_to_pdf(input_pdf, output_pdf, image_frame)















