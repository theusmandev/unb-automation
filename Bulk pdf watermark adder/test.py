

#working fine with accurate watermark before adjusting watermark color and size

# import fitz  # PyMuPDF
# from pathlib import Path

# # Hard-coded paths
# INPUT_FOLDER = Path(r"C:\Users\PCS\Downloads\test")
# OUTPUT_FOLDER = INPUT_FOLDER / "Output"
# OUTPUT_FOLDER.mkdir(exist_ok=True)

# WATERMARK_TEXT = "Courtesy www.pdfbooksfree.pk"


# def add_watermark(pdf_path, output_path):
#     doc = fitz.open(pdf_path)

#     for page in doc:
#         page_width = page.rect.width

#         # ٹیکسٹ باکس کی چوڑائی پوری لائن جتنی رکھ دیتے ہیں
#         rect = fitz.Rect(0, 10, page_width, 40)

#         page.insert_textbox(
#             rect,
#             WATERMARK_TEXT,
#             fontsize=10,
#             fontname="helv",
#             color=(0, 0, 0),  # black
#             align=1           # 0 left, 1 center, 2 right
#         )

#     doc.save(output_path)
#     doc.close()


# def process_folder():
#     for file in INPUT_FOLDER.iterdir():
#         if file.suffix.lower() == ".pdf":
#             output_pdf = OUTPUT_FOLDER / f"{file.stem}_watermarked.pdf"
#             print(f"Processing: {file.name}")
#             add_watermark(str(file), str(output_pdf))

#     print("\nDone! Watermarked PDFs saved in:")
#     print(OUTPUT_FOLDER)


# process_folder()



#ok working fine but encryption error for some pdfs


# import os
# from PyPDF2 import PdfReader, PdfWriter
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# from pathlib import Path

# # ----------------------------
# # HARD CODED FOLDER PATH
# # ----------------------------
# INPUT_FOLDER = Path(r"C:\Users\PCS\Downloads\test")
# OUTPUT_FOLDER = INPUT_FOLDER / "Output"

# # Output folder create if not exists
# OUTPUT_FOLDER.mkdir(exist_ok=True)

# # ----------------------------
# # FUNCTION: watermark creator
# # ----------------------------
# def create_watermark(text, output_path):
#     c = canvas.Canvas(output_path, pagesize=letter)
#     width, height = letter

#     # Place text at top center exactly like screenshot
#     c.setFont("Helvetica", 10)
#     c.drawCentredString(width / 2, height - 20, text)
#     c.save()


# # ----------------------------
# # FUNCTION: Apply watermark to PDF
# # ----------------------------
# def add_watermark_to_pdf(pdf_path, watermark_path, output_path):
#     # Convert Path object to string (FIXED)
#     reader = PdfReader(str(pdf_path))
#     writer = PdfWriter()

#     watermark_pdf = PdfReader(str(watermark_path))
#     watermark_page = watermark_pdf.pages[0]

#     for page in reader.pages:
#         page.merge_page(watermark_page)
#         writer.add_page(page)

#     with open(str(output_path), "wb") as f:
#         writer.write(f)


# # ----------------------------
# # MAIN: Process all PDFs in folder
# # ----------------------------
# def process_folder():
#     watermark_file = INPUT_FOLDER / "watermark_temp.pdf"

#     # Watermark text
#     watermark_text = "Courtesy www.pdfbooksfree.pk"

#     # Create watermark PDF
#     create_watermark(watermark_text, str(watermark_file))

#     # Process all PDFs in input folder
#     for file in INPUT_FOLDER.iterdir():
#         if file.suffix.lower() == ".pdf":
#             output_pdf = OUTPUT_FOLDER / f"{file.stem}_watermarked.pdf"
#             print(f"Processing: {file.name}")
#             add_watermark_to_pdf(file, watermark_file, output_pdf)

#     print("\nAll PDFs processed successfully!")
#     print(f"Saved in: {OUTPUT_FOLDER}")


# # ----------------------------
# # RUN
# # ----------------------------
# process_folder()



# import os
# from pypdf import PdfReader, PdfWriter
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4

# # ============================
# # 🔧 HARD-CODED INPUT FOLDER
# # ============================
# INPUT_FOLDER = r"C:\Users\PCS\Downloads\test"  # ← Yahan apna folder path likho
# WATERMARK_TEXT = "www.urdunovelbank.com"   # ← Jo text watermark chahiye
# # ============================


# def create_watermark_pdf(watermark_path, text):
#     c = canvas.Canvas(watermark_path, pagesize=A4)
#     c.setFont("Helvetica", 40)
#     c.setFillColorRGB(0.7, 0.7, 0.7)  # Light gray
#     c.saveState()

#     # Rotate text diagonal
#     c.translate(300, 400)
#     c.rotate(45)
#     c.drawString(0, 0, text)
#     c.restoreState()
#     c.showPage()
#     c.save()


# def add_watermarks():
#     input_folder = os.path.abspath(INPUT_FOLDER)

#     # Create watermark.pdf inside input folder
#     watermark_file = os.path.join(input_folder, "watermark.pdf")
#     print(f"Creating watermark file: {watermark_file}")
#     create_watermark_pdf(watermark_file, WATERMARK_TEXT)

#     # Load watermark PDF
#     watermark_reader = PdfReader(watermark_file)
#     watermark_page = watermark_reader.pages[0]

#     # Output folder
#     output_folder = os.path.join(input_folder, "watermarked")
#     os.makedirs(output_folder, exist_ok=True)

#     # Apply watermark to all PDFs
#     for filename in os.listdir(input_folder):
#         if filename.lower().endswith(".pdf") and filename != "watermark.pdf":
#             pdf_path = os.path.join(input_folder, filename)
#             output_pdf_path = os.path.join(output_folder, filename)

#             print(f"Applying watermark to: {filename}")

#             reader = PdfReader(pdf_path)
#             writer = PdfWriter()

#             for page in reader.pages:
#                 page.merge_page(watermark_page)
#                 writer.add_page(page)

#             with open(output_pdf_path, "wb") as f:
#                 writer.write(f)

#     print("\n✔ Completed! Watermarked PDFs saved in:")
#     print(output_folder)


# # Run
# add_watermarks()
