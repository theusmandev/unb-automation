


import os
import shutil
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from PIL import Image
import pathlib

def create_pdf_from_image(image_path, target_width, target_height):
    """Image ko PDF page mein convert karne ka helper function"""
    temp_pdf = image_path.parent / f"temp_{image_path.stem}.pdf"
    img = Image.open(image_path)
    img_width, img_height = img.size

    # Aspect ratio barkarar rakhte hue scale karein
    scale = min(target_width / img_width, target_height / img_height)
    scaled_width = img_width * scale
    scaled_height = img_height * scale

    c = canvas.Canvas(str(temp_pdf), pagesize=(target_width, target_height))
    x_offset = (target_width - scaled_width) / 2
    y_offset = (target_height - scaled_height) / 2
    c.drawImage(str(image_path), x_offset, y_offset, width=scaled_width, height=scaled_height)
    c.showPage()
    c.save()
    return temp_pdf

def process_novels(folder_path):
    folder = pathlib.Path(folder_path)
    if not folder.is_dir():
        print(f"Error: {folder_path} directory nahi mili.")
        return

    # PNGs move karne ke liye folder
    processed_folder = folder / "processed_pngs"
    processed_folder.mkdir(exist_ok=True)

    pdf_files = list(folder.glob("*.pdf"))

    for pdf_path in pdf_files:
        pdf_name = pdf_path.stem
        writer = PdfWriter()
        reader = PdfReader(str(pdf_path))
        
        # Dimensions setup
        first_page = reader.pages[0]
        p_width = float(first_page.mediabox.width)
        p_height = float(first_page.mediabox.height)

        # Teeno Mumkina Image Paths
        img_cover = folder / f"{pdf_name}.png"
        img_p1 = folder / f"{pdf_name}_page_1.png"
        img_p2 = folder / f"{pdf_name}_page_2.png"

        modified = False
        used_image = None

        try:
            # CONDITION 1: Same Name (Cover Logic)
            if img_cover.exists():
                print(f"Adding COVER: {pdf_name}")
                temp_img_pdf = create_pdf_from_image(img_cover, p_width, p_height)
                img_reader = PdfReader(str(temp_img_pdf))
                
                writer.add_page(img_reader.pages[0]) # PNG as Cover
                for page in reader.pages:            # Phir puri original PDF
                    writer.add_page(page)
                
                modified = True
                used_image = img_cover
                temp_img_pdf.unlink()

            # CONDITION 2: _page_1 (Replace First Page)
            elif img_p1.exists():
                print(f"Replacing PAGE 1: {pdf_name}")
                temp_img_pdf = create_pdf_from_image(img_p1, p_width, p_height)
                img_reader = PdfReader(str(temp_img_pdf))
                
                writer.add_page(img_reader.pages[0]) 
                for i in range(1, len(reader.pages)):
                    writer.add_page(reader.pages[i])
                
                modified = True
                used_image = img_p1
                temp_img_pdf.unlink()

            # CONDITION 3: _page_2 (Remove P1, Replace P2)
            elif img_p2.exists():
                print(f"Processing PAGE 2 logic: {pdf_name}")
                temp_img_pdf = create_pdf_from_image(img_p2, p_width, p_height)
                img_reader = PdfReader(str(temp_img_pdf))

                writer.add_page(img_reader.pages[0]) # PNG as new P1
                for i in range(2, len(reader.pages)): # Skip original P1 & P2
                    writer.add_page(reader.pages[i])
                
                modified = True
                used_image = img_p2
                temp_img_pdf.unlink()

            # Agar koi condition match hui to save karein
            if modified:
                with open(pdf_path, "wb") as f:
                    writer.write(f)
                
                # PNG ko move karein
                if used_image:
                    shutil.move(str(used_image), str(processed_folder / used_image.name))
                print(f"✅ Success: {pdf_name} update ho gaya.")
            else:
                print(f"ℹ️ Skip: {pdf_name} (No matching image found)")

        except Exception as e:
            print(f"❌ Error processing {pdf_name}: {e}")

if __name__ == "__main__":
    # Apna path yahan check kar lein
    target_folder = r"E:\unb-workstation\Writers All Novels\Uploadings\DG workstation\2"
    process_novels(target_folder)
















# import os
# from pypdf import PdfReader, PdfWriter
# from reportlab.pdfgen import canvas
# from PIL import Image
# import pathlib

# def create_pdf_from_image(image_path, target_width, target_height):
#     """Image ko PDF page mein convert karne ka helper function"""
#     temp_pdf = image_path.parent / f"temp_{image_path.stem}.pdf"
#     img = Image.open(image_path)
#     img_width, img_height = img.size

#     scale = min(target_width / img_width, target_height / img_height)
#     scaled_width = img_width * scale
#     scaled_height = img_height * scale

#     c = canvas.Canvas(str(temp_pdf), pagesize=(target_width, target_height))
#     x_offset = (target_width - scaled_width) / 2
#     y_offset = (target_height - scaled_height) / 2
#     c.drawImage(str(image_path), x_offset, y_offset, width=scaled_width, height=scaled_height)
#     c.showPage()
#     c.save()
#     return temp_pdf

# def process_novels(folder_path):
#     folder = pathlib.Path(folder_path)
#     if not folder.is_dir():
#         print(f"Error: {folder_path} directory nahi mili.")
#         return

#     # Folder mein sari PDF files check karein
#     pdf_files = list(folder.glob("*.pdf"))

#     for pdf_path in pdf_files:
#         pdf_name = pdf_path.stem
#         writer = PdfWriter()
#         reader = PdfReader(str(pdf_path))
        
#         # Dimensions nikalne ke liye
#         first_page = reader.pages[0]
#         p_width = float(first_page.mediabox.width)
#         p_height = float(first_page.mediabox.height)

#         # Image paths check karein
#         img_p1 = folder / f"{pdf_name}_page_1.png"
#         img_p2 = folder / f"{pdf_name}_page_2.png"

#         modified = False

#         try:
#             # CONDITION 1: Agar _page_1 wali image hai
#             if img_p1.exists():
#                 print(f"Processing Page 1 replacement for: {pdf_name}")
#                 temp_img_pdf = create_pdf_from_image(img_p1, p_width, p_height)
#                 img_reader = PdfReader(str(temp_img_pdf))
                
#                 writer.add_page(img_reader.pages[0]) # New Image Page
#                 for i in range(1, len(reader.pages)): # Baqi sari pages
#                     writer.add_page(reader.pages[i])
                
#                 modified = True
#                 temp_img_pdf.unlink() # Delete temp file

#             # CONDITION 2: Agar _page_2 wali image hai
#             elif img_p2.exists():
#                 print(f"Processing Page 2 logic (Remove P1, Replace P2) for: {pdf_name}")
#                 temp_img_pdf = create_pdf_from_image(img_p2, p_width, p_height)
#                 img_reader = PdfReader(str(temp_img_pdf))

#                 # User logic: P1 remove karo, P2 ko PNG se replace karo
#                 # Iska matlab result mein [PNG] + [Original P3 onwards] ayenge
#                 writer.add_page(img_reader.pages[0]) # PNG image as new first page
                
#                 for i in range(2, len(reader.pages)): # 3rd page se agay tak
#                     writer.add_page(reader.pages[i])
                
#                 modified = True
#                 temp_img_pdf.unlink()

#             # Agar modification hui hai to file save karein
#             if modified:
#                 output_path = pdf_path # Original ko overwrite karega
#                 with open(output_path, "wb") as f:
#                     writer.write(f)
#                 print(f"✅ Success: {pdf_name} update ho gaya.")
#             else:
#                 print(f"ℹ️ Skip: {pdf_name} ke liye koi matching image nahi mili.")

#         except Exception as e:
#             print(f"❌ Error processing {pdf_name}: {e}")

# if __name__ == "__main__":
#     # Apna path yahan set karein
#     target_folder = r"E:\unb-workstation\Writers All Novels\DG workstation\create"
#     process_novels(target_folder)