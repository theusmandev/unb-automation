



#working fine end page onk ha lakin us ma link clickable nahi ha

# import os
# import fitz  # PyMuPDF

# def add_resized_end_page(folder_path):
#     folder = os.path.abspath(folder_path)

#     if not os.path.isdir(folder):
#         print("Error: Folder exist nahi karta.")
#         return

#     end_page_path = os.path.join(folder, "endpage.pdf")
#     if not os.path.isfile(end_page_path):
#         print("Error: endpage.pdf folder ke andar nahi mila.")
#         return

#     print("End page found:", end_page_path)

#     end_doc_original = fitz.open(end_page_path)
#     end_page = end_doc_original[0]
#     end_pix = end_page.get_pixmap()

#     for file in os.listdir(folder):
#         if file.lower().endswith(".pdf") and file != "endpage.pdf":

#             pdf_path = os.path.join(folder, file)
#             print(f"\nProcessing: {file}")

#             try:
#                 novel = fitz.open(pdf_path)

#                 # Last page size same copy
#                 last_page = novel[-1]
#                 w = last_page.rect.width
#                 h = last_page.rect.height

#                 print(f"Last page size: {w} x {h}")

#                 # Create new end page
#                 new_page = novel.new_page(width=w, height=h)

#                 new_page.insert_image(
#                     new_page.rect,
#                     pixmap=end_pix,
#                     keep_proportion=False
#                 )

#                 # Temporary output path
#                 temp_path = pdf_path + ".tmp"

#                 # Save to temp file (safe overwrite)
#                 novel.save(temp_path, incremental=False)
#                 novel.close()

#                 # Replace original file
#                 os.remove(pdf_path)
#                 os.rename(temp_path, pdf_path)

#                 print("✔ End page added with exact matching size!")

#             except Exception as e:
#                 print(f"❌ Error: {e}")

#     print("\nAll files updated!")

# # Run
# add_resized_end_page(r"C:\Users\PCS\Downloads\New folder - Copy")



#working fine with endpage orignal page size 

# import os
# from pypdf import PdfReader, PdfWriter

# def add_end_page(folder_path):
#     folder = os.path.abspath(folder_path)

#     # Check folder
#     if not os.path.isdir(folder):
#         print("Error: Folder exist nahi karta.")
#         return

#     # Find endpage.pdf
#     end_page_path = os.path.join(folder, "endpage.pdf")
#     if not os.path.isfile(end_page_path):
#         print("Error: endpage.pdf folder ke andar nahi mila.")
#         return

#     print("End page found:", end_page_path)

#     end_reader = PdfReader(end_page_path)
#     end_page = end_reader.pages[0]   # assuming only first page needed

#     # Process all other PDFs
#     for file in os.listdir(folder):
#         if file.lower().endswith(".pdf") and file != "endpage.pdf":
#             pdf_path = os.path.join(folder, file)

#             try:
#                 print(f"Processing: {file}")

#                 reader = PdfReader(pdf_path)
#                 writer = PdfWriter()

#                 # Copy original pages
#                 for page in reader.pages:
#                     writer.add_page(page)

#                 # Add end page
#                 writer.add_page(end_page)

#                 # Output file (same name overwrite)
#                 out_path = os.path.join(folder, file)

#                 with open(out_path, "wb") as f:
#                     writer.write(f)

#                 print(f"✔ End page added: {file}")

#             except Exception as e:
#                 print(f"❌ Error processing {file}: {e}")

#     print("\nDone! All novels updated.")

# # Run the function (hardcoded path)
# add_end_page(r"C:\Users\PCS\Downloads\New folder - Copy")
