

# import fitz  # PyMuPDF

# def pdf_page_to_png(pdf_path, page_number=1, output_name="output_page.png"):
#     doc = fitz.open(pdf_path)
#     page = doc[page_number - 1]  # 0-based index
#     pix = page.get_pixmap()
#     pix.save(output_name)
#     print(f"✅ Page {page_number} saved as {output_name}")

# # Example usage
# pdf_file = r"C:\Users\PCS\Downloads\ok pdfs\zindagi-gulzar-hai-umera-ahmad-ebooks.pdf"
# pdf_page_to_png(pdf_file, 1, "zameen_ke_ansoo_page1.png")





# import fitz  # PyMuPDF
# import os

# def pdf_page_to_png(pdf_path, page_number=1, output_name="output_page.png"):
#     # Get Downloads folder path
#     downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
#     output_path = os.path.join(downloads_folder, output_name)

#     # Open PDF and extract page
#     doc = fitz.open(pdf_path)
#     page = doc[page_number - 1]  # 0-based index
#     pix = page.get_pixmap()
#     pix.save(output_path)

#     print(f"✅ Page {page_number} from '{pdf_path}' saved as '{output_path}'")

# # Example usage
# pdf_file = r"C:\Users\PCS\Downloads\ok pdfs\surprise.pdf" # apna PDF path dalna
# pdf_page_to_png(pdf_file, 1, "zameen_ke_ansoo_page1.png")







