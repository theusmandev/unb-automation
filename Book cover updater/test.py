

# import os
# from pypdf import PdfReader, PdfWriter
# from reportlab.pdfgen import canvas
# from PIL import Image
# import pathlib

# def replace_first_page(folder_path):
#     folder = pathlib.Path(folder_path)
#     if not folder.is_dir():
#         print(f"Error: {folder_path} folder nahi hai.")
#         return

#     # Find PDF and image files
#     pdf_file = None
#     image_file = None
#     for file in folder.iterdir():
#         if file.suffix.lower() == ".pdf":
#             pdf_file = file
#         elif file.suffix.lower() in (".png", ".jpg", ".jpeg",".webp"):
#             image_file = file

#     if not pdf_file or not image_file:
#         print("Error: PDF ya image file folder mein nahi mili.")
#         return

#     # Step 1: Get original PDF first page dimensions
#     try:
#         reader = PdfReader(str(pdf_file))
#         first_page = reader.pages[0]
#         page_width = float(first_page.mediabox.width)
#         page_height = float(first_page.mediabox.height)
#     except Exception as e:
#         print(f"Error: PDF page dimensions padhne mein issue: {e}")
#         return

#     # Step 2: Convert image to single-page PDF with same size
#     temp_image_pdf = folder / "temp_image.pdf"
#     try:
#         img = Image.open(image_file)
#         img_width, img_height = img.size

#         scale = min(page_width / img_width, page_height / img_height)
#         scaled_width = img_width * scale
#         scaled_height = img_height * scale

#         c = canvas.Canvas(str(temp_image_pdf), pagesize=(page_width, page_height))
#         x_offset = (page_width - scaled_width) / 2
#         y_offset = (page_height - scaled_height) / 2
#         c.drawImage(str(image_file), x_offset, y_offset, width=scaled_width, height=scaled_height)
#         c.showPage()
#         c.save()
#     except Exception as e:
#         print(f"Error: Image ko PDF mein convert karte waqt issue: {e}")
#         return

#     # Step 3: Merge image PDF + rest of original PDF
#     try:
#         writer = PdfWriter()

#         # Add image page
#         image_reader = PdfReader(str(temp_image_pdf))
#         writer.add_page(image_reader.pages[0])

#         # Add rest of PDF (skip 1st page)
#         for i in range(1, len(reader.pages)):
#             writer.add_page(reader.pages[i])

#         # Save to new file (avoid overwriting until done)
#         output_pdf = folder / f"{pdf_file.stem}_updated.pdf"
#         with open(output_pdf, "wb") as f:
#             writer.write(f)

#         print(f"PDF update ho gaya: {output_pdf}")

#         # Replace old file with updated file (overwrite original)
#         os.replace(output_pdf, pdf_file)

#     except Exception as e:
#         print(f"Error: PDF process karte waqt issue: {e}")
#     finally:
#         if temp_image_pdf.exists():
#             try:
#                 os.remove(temp_image_pdf)
#             except:
#                 pass

# # Example run
# if __name__ == "__main__":
#     folder_path = r"C:\Users\PCS\Downloads\replace"
#     replace_first_page(folder_path)













# import os
# from PyPDF2 import PdfReader, PdfWriter
# from reportlab.pdfgen import canvas
# from PIL import Image
# import pathlib

# def replace_first_page(folder_path, pdf_filename=None, image_filename=None, output_filename="output.pdf"):
#     """
#     Replace the first page of a PDF with an image converted to a PDF page.
    
#     Args:
#         folder_path (str): Path to the folder containing PDF and image.
#         pdf_filename (str, optional): Specific PDF filename to use.
#         image_filename (str, optional): Specific image filename to use.
#         output_filename (str, optional): Name of the output PDF file.
#     """
#     folder = pathlib.Path(folder_path)
#     if not folder.is_dir():
#         print(f"Error: {folder_path} is not a valid directory.")
#         return

#     # Find PDF and image files if not specified
#     if pdf_filename is None:
#         pdf_files = list(folder.glob("*.pdf"))
#         if not pdf_files:
#             print("Error: No PDF file found in the folder.")
#             return
#         elif len(pdf_files) > 1:
#             print("Warning: Multiple PDFs found. Using the first one.")
#         pdf_file = pdf_files[0]
#     else:
#         pdf_file = folder / pdf_filename
#         if not pdf_file.exists():
#             print(f"Error: PDF file {pdf_filename} not found.")
#             return

#     if image_filename is None:
#         image_extensions = ("*.png", "*.jpg", "*.jpeg")
#         image_files = [f for ext in image_extensions for f in folder.glob(ext)]
#         if not image_files:
#             print("Error: No image file (PNG/JPG/JPEG) found in the folder.")
#             return
#         elif len(image_files) > 1:
#             print("Warning: Multiple images found. Using the first one.")
#         image_file = image_files[0]
#     else:
#         image_file = folder / image_filename
#         if not image_file.exists():
#             print(f"Error: Image file {image_filename} not found.")
#             return

#     # Check if output file already exists
#     output_pdf = folder / output_filename
#     if output_pdf.exists():
#         print(f"Warning: {output_filename} already exists and will be overwritten.")

#     # Step 1: Convert image to single-page PDF
#     temp_image_pdf = folder / "temp_image.pdf"
#     try:
#         img = Image.open(image_file)
#         img_width, img_height = img.size

#         c = canvas.Canvas(str(temp_image_pdf), pagesize=(img_width, img_height))
#         c.drawImage(str(image_file), 0, 0, width=img_width, height=img_height)
#         c.showPage()
#         c.save()
#     except Exception as e:
#         print(f"Error converting image to PDF: {e}")
#         return

#     # Step 2: Read original PDF and replace first page
#     try:
#         reader = PdfReader(str(pdf_file))  # Convert Path to string
#         writer = PdfWriter()

#         # Add image PDF as first page
#         image_reader = PdfReader(str(temp_image_pdf))  # Convert Path to string
#         writer.add_page(image_reader.pages[0])

#         # Add remaining pages from original PDF
#         if len(reader.pages) > 1:
#             for i in range(1, len(reader.pages)):
#                 writer.add_page(reader.pages[i])

#         # Step 3: Save output
#         with open(output_pdf, "wb") as f:
#             writer.write(f)
#         print(f"New PDF created: {output_pdf}")

#     except Exception as e:
#         print(f"Error processing PDF: {e}")
#     finally:
#         # Cleanup temporary file
#         if temp_image_pdf.exists():
#             try:
#                 os.remove(temp_image_pdf)
#             except Exception as e:
#                 print(f"Warning: Could not delete temporary file: {e}")

# # Example run
# if __name__ == "__main__":
#     folder_path = r"C:\Users\PCS\Downloads\replace"
#     replace_first_page(folder_path)

# import os
# from pypdf import PdfReader, PdfWriter
# from reportlab.pdfgen import canvas
# from PIL import Image
# import pathlib

# def replace_first_page(folder_path, pdf_password=None):
#     folder = pathlib.Path(folder_path)
#     if not folder.is_dir():
#         print(f"Error: {folder_path} folder nahi hai.")
#         return

#     # Find PDF and image files
#     pdf_file = None
#     image_file = None
#     for file in folder.iterdir():
#         if file.suffix.lower() == ".pdf":
#             pdf_file = file
#         elif file.suffix.lower() in (".png", ".jpg", ".jpeg"):
#             image_file = file

#     if not pdf_file or not image_file:
#         print("Error: PDF ya image file folder mein nahi mili.")
#         return

#     # Step 1: Convert image to single-page PDF
#     temp_image_pdf = folder / "temp_image.pdf"
#     try:
#         img = Image.open(image_file)
#         img_width, img_height = img.size
#         c = canvas.Canvas(str(temp_image_pdf), pagesize=(img_width, img_height))
#         c.drawImage(str(image_file), 0, 0, width=img_width, height=img_height)
#         c.showPage()
#         c.save()
#     except Exception as e:
#         print(f"Error: Image ko PDF mein convert karte waqt issue: {e}")
#         return

#     # Step 2: Read original PDF and handle encryption
#     try:
#         reader = PdfReader(str(pdf_file))
#         if reader.is_encrypted:
#             if pdf_password:
#                 success = reader.decrypt(pdf_password)
#                 if not success:
#                     print("Error: Galat password diya hai.")
#                     return
#             else:
#                 print("Error: PDF encrypted hai, password do.")
#                 return
#         writer = PdfWriter()

#         # Add image PDF as first page
#         image_reader = PdfReader(str(temp_image_pdf))
#         writer.add_page(image_reader.pages[0])

#         # Add remaining pages from original PDF (skip first page)
#         if len(reader.pages) > 1:
#             for i in range(1, len(reader.pages)):
#                 writer.add_page(reader.pages[i])

#         # Step 3: Save output
#         output_pdf = folder / "output.pdf"
#         with open(output_pdf, "wb") as f:
#             writer.write(f)
#         print(f"Naya PDF ban gaya: {output_pdf}")

#     except Exception as e:
#         print(f"Error: PDF process karte waqt issue: {e}")
#     finally:
#         # Cleanup temporary file
#         if temp_image_pdf.exists():
#             try:
#                 os.remove(temp_image_pdf)
#             except Exception as e:
#                 print(f"Warning: Temporary file delete nahi hua: {e}")

# # Example run
# if __name__ == "__main__":
#     folder_path = r"C:\Users\PCS\Downloads\replace"
#     # If your PDF is encrypted, provide the password here
#     replace_first_page(folder_path, pdf_password="your_password_here")  # Replace with actual password or None if not encrypted








#okoomomok


# import os
# from pypdf import PdfReader, PdfWriter
# from reportlab.pdfgen import canvas
# from PIL import Image
# import pathlib

# def replace_first_page(folder_path):
#     folder = pathlib.Path(folder_path)
#     if not folder.is_dir():
#         print(f"Error: {folder_path} folder nahi hai.")
#         return

#     # Find PDF and image files
#     pdf_file = None
#     image_file = None
#     for file in folder.iterdir():
#         if file.suffix.lower() == ".pdf":
#             pdf_file = file
#         elif file.suffix.lower() in (".png", ".jpg", ".jpeg"):
#             image_file = file

#     if not pdf_file or not image_file:
#         print("Error: PDF ya image file folder mein nahi mili.")
#         return

#     # Step 1: Convert image to single-page PDF
#     temp_image_pdf = folder / "temp_image.pdf"
#     try:
#         img = Image.open(image_file)
#         img_width, img_height = img.size
#         c = canvas.Canvas(str(temp_image_pdf), pagesize=(img_width, img_height))
#         c.drawImage(str(image_file), 0, 0, width=img_width, height=img_height)
#         c.showPage()
#         c.save()
#     except Exception as e:
#         print(f"Error: Image ko PDF mein convert karte waqt issue: {e}")
#         return

#     # Step 2: Read original PDF and process
#     try:
#         reader = PdfReader(str(pdf_file))
#         writer = PdfWriter()

#         # Add image PDF as first page
#         image_reader = PdfReader(str(temp_image_pdf))
#         writer.add_page(image_reader.pages[0])

#         # Add remaining pages from original PDF (skip first page)
#         if len(reader.pages) > 1:
#             for i in range(1, len(reader.pages)):
#                 writer.add_page(reader.pages[i])

#         # Step 3: Save output
#         output_pdf = folder / "output.pdf"
#         with open(output_pdf, "wb") as f:
#             writer.write(f)
#         print(f"Naya PDF ban gaya: {output_pdf}")

#     except Exception as e:
#         print(f"Error: PDF process karte waqt issue: {e}")
#     finally:
#         # Cleanup temporary file
#         if temp_image_pdf.exists():
#             try:
#                 os.remove(temp_image_pdf)
#             except Exception as e:
#                 print(f"Warning: Temporary file delete nahi hua: {e}")

# # Example run
# if __name__ == "__main__":
#     folder_path = r"C:\Users\PCS\Downloads\replace"
#     replace_first_page(folder_path)








# import os
# from pypdf import PdfReader, PdfWriter
# from reportlab.pdfgen import canvas
# from PIL import Image
# import pathlib

# def replace_first_page(folder_path):
#     folder = pathlib.Path(folder_path)
#     if not folder.is_dir():
#         print(f"Error: {folder_path} folder nahi hai.")
#         return

#     # Find PDF and image files
#     pdf_file = None
#     image_file = None
#     for file in folder.iterdir():
#         if file.suffix.lower() == ".pdf":
#             pdf_file = file
#         elif file.suffix.lower() in (".png", ".jpg", ".jpeg","webp"):
#             image_file = file

#     if not pdf_file or not image_file:
#         print("Error: PDF ya image file folder mein nahi mili.")
#         return

#     # Step 1: Convert image to single-page PDF with A4 scaling
#     temp_image_pdf = folder / "temp_image.pdf"
#     try:
#         img = Image.open(image_file)
#         img_width, img_height = img.size
        
#         # A4 dimensions in points (595 x 842)
#         a4_width, a4_height = 595, 842
        
#         # Calculate scaling factor to fit image within A4 while maintaining aspect ratio
#         scale = min(a4_width / img_width, a4_height / img_height)
#         scaled_width = img_width * scale
#         scaled_height = img_height * scale
        
#         # Create PDF with A4 page size
#         c = canvas.Canvas(str(temp_image_pdf), pagesize=(a4_width, a4_height))
#         # Center the image on the A4 page
#         x_offset = (a4_width - scaled_width) / 2
#         y_offset = (a4_height - scaled_height) / 2
#         c.drawImage(str(image_file), x_offset, y_offset, width=scaled_width, height=scaled_height)
#         c.showPage()
#         c.save()
#     except Exception as e:
#         print(f"Error: Image ko PDF mein convert karte waqt issue: {e}")
#         return

#     # Step 2: Read original PDF and process
#     try:
#         reader = PdfReader(str(pdf_file))
#         writer = PdfWriter()

#         # Add image PDF as first page
#         image_reader = PdfReader(str(temp_image_pdf))
#         writer.add_page(image_reader.pages[0])

#         # Add remaining pages from original PDF (skip first page)
#         if len(reader.pages) > 1:
#             for i in range(1, len(reader.pages)):
#                 writer.add_page(reader.pages[i])

#         # Step 3: Save output
#         output_pdf = folder / "output.pdf"
#         with open(output_pdf, "wb") as f:
#             writer.write(f)
#         print(f"Naya PDF ban gaya: {output_pdf}")

#     except Exception as e:
#         print(f"Error: PDF process karte waqt issue: {e}")
#     finally:
#         # Cleanup temporary file
#         if temp_image_pdf.exists():
#             try:
#                 os.remove(temp_image_pdf)
#             except Exception as e:
#                 print(f"Warning: Temporary file delete nahi hua: {e}")

# # Example run
# if __name__ == "__main__":
#     folder_path = r"C:\Users\PCS\Downloads\replace"
#     replace_first_page(folder_path)







# import os
# from pypdf import PdfReader, PdfWriter
# from reportlab.pdfgen import canvas
# from PIL import Image
# import pathlib

# def replace_first_page(folder_path):
#     folder = pathlib.Path(folder_path)
#     if not folder.is_dir():
#         print(f"Error: {folder_path} folder nahi hai.")
#         return

#     # Find PDF and image files
#     pdf_file = None
#     image_file = None
#     for file in folder.iterdir():
#         if file.suffix.lower() == ".pdf":
#             pdf_file = file
#         elif file.suffix.lower() in (".png", ".jpg", ".jpeg"):
#             image_file = file

#     if not pdf_file or not image_file:
#         print("Error: PDF ya image file folder mein nahi mili.")
#         return

#     # Step 1: Convert image to single-page PDF with A4 scaling
#     temp_image_pdf = folder / "temp_image.pdf"
#     try:
#         img = Image.open(image_file)
#         img_width, img_height = img.size
        
#         # A4 dimensions in points (595 x 842)
#         a4_width, a4_height = 595, 842
        
#         # Calculate scaling factor to fit image within A4 while maintaining aspect ratio
#         scale = min(a4_width / img_width, a4_height / img_height)
#         scaled_width = img_width * scale
#         scaled_height = img_height * scale
        
#         # Create PDF with A4 page size
#         c = canvas.Canvas(str(temp_image_pdf), pagesize=(a4_width, a4_height))
#         # Center the image on the A4 page
#         x_offset = (a4_width - scaled_width) / 2
#         y_offset = (a4_height - scaled_height) / 2
#         c.drawImage(str(image_file), x_offset, y_offset, width=scaled_width, height=scaled_height)
#         c.showPage()
#         c.save()
#     except Exception as e:
#         print(f"Error: Image ko PDF mein convert karte waqt issue: {e}")
#         return

#     # Step 2: Read original PDF and process
#     try:
#         reader = PdfReader(str(pdf_file))
#         writer = PdfWriter()

#         # Add image PDF as first page
#         image_reader = PdfReader(str(temp_image_pdf))
#         writer.add_page(image_reader.pages[0])

#         # Add remaining pages from original PDF (skip first page)
#         if len(reader.pages) > 1:
#             for i in range(1, len(reader.pages)):
#                 writer.add_page(reader.pages[i])

#         # Step 3: Save output with the same name as original PDF
#         output_pdf = pdf_file  # Use original PDF name
#         with open(output_pdf, "wb") as f:
#             writer.write(f)
#         print(f"PDF update ho gaya: {output_pdf}")

#     except Exception as e:
#         print(f"Error: PDF process karte waqt issue: {e}")
#     finally:
#         # Cleanup temporary file
#         if temp_image_pdf.exists():
#             try:
#                 os.remove(temp_image_pdf)
#             except Exception as e:
#                 print(f"Warning: Temporary file delete nahi hua: {e}")

# # Example run
# if __name__ == "__main__":
#     folder_path = r"C:\Users\PCS\Downloads\replace"
#     replace_first_page(folder_path)









# import os
# from pypdf import PdfReader, PdfWriter
# from reportlab.pdfgen import canvas
# from PIL import Image
# import pathlib

# def replace_first_page(folder_path):
#     folder = pathlib.Path(folder_path)
#     if not folder.is_dir():
#         print(f"Error: {folder_path} folder nahi hai.")
#         return

#     # Find PDF and image files
#     pdf_file = None
#     image_file = None
#     for file in folder.iterdir():
#         if file.suffix.lower() == ".pdf":
#             pdf_file = file
#         elif file.suffix.lower() in (".png", ".jpg", ".jpeg"):
#             image_file = file

#     if not pdf_file or not image_file:
#         print("Error: PDF ya image file folder mein nahi mili.")
#         return

#     # Step 1: Get original PDF first page dimensions
#     try:
#         reader = PdfReader(str(pdf_file))
#         first_page = reader.pages[0]
#         # Get page dimensions (width, height) in points
#         page_width = float(first_page.mediabox.width)
#         page_height = float(first_page.mediabox.height)
#     except Exception as e:
#         print(f"Error: PDF page dimensions padhne mein issue: {e}")
#         return

#     # Step 2: Convert image to single-page PDF with original page size
#     temp_image_pdf = folder / "temp_image.pdf"
#     try:
#         img = Image.open(image_file)
#         img_width, img_height = img.size
        
#         # Calculate scaling factor to fit image within original page size while maintaining aspect ratio
#         scale = min(page_width / img_width, page_height / img_height)
#         scaled_width = img_width * scale
#         scaled_height = img_height * scale
        
#         # Create PDF with original page size
#         c = canvas.Canvas(str(temp_image_pdf), pagesize=(page_width, page_height))
#         # Center the image on the page
#         x_offset = (page_width - scaled_width) / 2
#         y_offset = (page_height - scaled_height) / 2
#         c.drawImage(str(image_file), x_offset, y_offset, width=scaled_width, height=scaled_height)
#         c.showPage()
#         c.save()
#     except Exception as e:
#         print(f"Error: Image ko PDF mein convert karte waqt issue: {e}")
#         return

#     # Step 3: Read original PDF and process
#     try:
#         writer = PdfWriter()

#         # Add image PDF as first page
#         image_reader = PdfReader(str(temp_image_pdf))
#         writer.add_page(image_reader.pages[0])

#         # Add remaining pages from original PDF (skip first page)
#         if len(reader.pages) > 1:
#             for i in range(1, len(reader.pages)):
#                 writer.add_page(reader.pages[i])

#         # Step 4: Save output with the same name as original PDF
#         output_pdf = pdf_file  # Use original PDF name
#         with open(output_pdf, "wb") as f:
#             writer.write(f)
#         print(f"PDF update ho gaya: {output_pdf}")

#     except Exception as e:
#         print(f"Error: PDF process karte waqt issue: {e}")
#     finally:
#         # Cleanup temporary file
#         if temp_image_pdf.exists():
#             try:
#                 os.remove(temp_image_pdf)
#             except Exception as e:
#                 print(f"Warning: Temporary file delete nahi hua: {e}")

# # Example run
# if __name__ == "__main__":
#     folder_path = r"C:\Users\PCS\Downloads\replace"
#     replace_first_page(folder_path)




# import os
# from pypdf import PdfReader, PdfWriter
# from reportlab.pdfgen import canvas
# from PIL import Image
# import pathlib

# def replace_first_page(folder_path):
#     folder = pathlib.Path(folder_path)
#     if not folder.is_dir():
#         print(f"Error: {folder_path} folder nahi hai.")
#         return

#     # Find PDF and image files
#     pdf_file = None
#     image_file = None
#     for file in folder.iterdir():
#         if file.suffix.lower() == ".pdf":
#             pdf_file = file
#         elif file.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
#             image_file = file

#     if not pdf_file or not image_file:
#         print("Error: PDF ya image file folder mein nahi mili.")
#         return

#     # Step 1: Get original PDF first page dimensions
#     try:
#         reader = PdfReader(str(pdf_file))
#         first_page = reader.pages[0]
#         # Get page dimensions (width, height) in points
#         page_width = float(first_page.mediabox.width)
#         page_height = float(first_page.mediabox.height)
#     except Exception as e:
#         print(f"Error: PDF page dimensions padhne mein issue: {e}")
#         return

#     # Step 2: Convert image to single-page PDF with original page size
#     temp_image_pdf = folder / "temp_image.pdf"
#     try:
#         img = Image.open(image_file)
#         img_width, img_height = img.size
        
#         # Calculate scaling factor to fit image within original page size while maintaining aspect ratio
#         scale = min(page_width / img_width, page_height / img_height)
#         scaled_width = img_width * scale
#         scaled_height = img_height * scale
        
#         # Create PDF with original page size
#         c = canvas.Canvas(str(temp_image_pdf), pagesize=(page_width, page_height))
#         # Center the image on the page
#         x_offset = (page_width - scaled_width) / 2
#         y_offset = (page_height - scaled_height) / 2
#         c.drawImage(str(image_file), x_offset, y_offset, width=scaled_width, height=scaled_height)
#         c.showPage()
#         c.save()
#     except Exception as e:
#         print(f"Error: Image ko PDF mein convert karte waqt issue: {e}")
#         return

#     # Step 3: Read original PDF and process
#     try:
#         writer = PdfWriter()

#         # Add image PDF as first page
#         image_reader = PdfReader(str(temp_image_pdf))
#         writer.add_page(image_reader.pages[0])

#         # Add remaining pages from original PDF (skip first page)
#         if len(reader.pages) > 1:
#             for i in range(1, len(reader.pages)):
#                 writer.add_page(reader.pages[i])

#         # Step 4: Save output with the same name as original PDF
#         output_pdf = pdf_file  # Use original PDF name
#         with open(output_pdf, "wb") as f:
#             writer.write(f)
#         print(f"PDF update ho gaya: {output_pdf}")

#     except Exception as e:
#         print(f"Error: PDF process karte waqt issue: {e}")
#     finally:
#         # Cleanup temporary file
#         if temp_image_pdf.exists():
#             try:
#                 os.remove(temp_image_pdf)
#             except Exception as e:
#                 print(f"Warning: Temporary file delete nahi hua: {e}")

# # Example run
# if __name__ == "__main__":
#     folder_path = r"C:\Users\PCS\Downloads\replace"
#     replace_first_page(folder_path)




