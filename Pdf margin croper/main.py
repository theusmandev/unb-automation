
# import logging
# import os
# from pathlib import Path
# from pypdf import PdfReader, PdfWriter

# # Logging configuration
# logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# def crop_pdf(input_path, output_path, crop_mm=5, crop_left=0, crop_right=0, crop_top=0, crop_bottom=0):
#     """Crops a single PDF file."""
#     try:
#         mm_to_pt = 72 / 25.4
#         crop_pts = crop_mm * mm_to_pt

#         reader = PdfReader(input_path)
#         writer = PdfWriter()

#         for page in reader.pages:
#             box = page.mediabox
            
#             # Naye coordinates calculate karna
#             lower_left_x = box.lower_left[0] + (crop_pts if crop_left else 0)
#             lower_left_y = box.lower_left[1] + (crop_pts if crop_bottom else 0)
#             upper_right_x = box.upper_right[0] - (crop_pts if crop_right else 0)
#             upper_right_y = box.upper_right[1] - (crop_pts if crop_top else 0)

#             page.mediabox.lower_left = (lower_left_x, lower_left_y)
#             page.mediabox.upper_right = (upper_right_x, upper_right_y)
#             writer.add_page(page)

#         with open(output_path, "wb") as f:
#             writer.write(f)
#         return True
#     except Exception as e:
#         logging.error(f"Error processing {input_path}: {str(e)}")
#         return False

# def process_all_pdfs_in_folder(input_folder, output_folder, crop_mm=5, **kwargs):
#     """Folders scan karta hai aur har PDF ko crop karta hai."""
    
#     # Check if input folder exists
#     input_path = Path(input_folder)
#     if not input_path.exists():
#         logging.error(f"Input folder nahi mila: {input_folder}")
#         return

#     # Create output folder if it doesn't exist
#     output_path = Path(output_folder)
#     output_path.mkdir(parents=True, exist_ok=True)

#     # PDF files ki list nikalna
#     pdf_files = list(input_path.glob("*.pdf"))
#     logging.info(f"Total {len(pdf_files)} PDF files mili hain.")

#     for pdf_file in pdf_files:
#         output_file_path = output_path / pdf_file.name
#         logging.info(f"Processing: {pdf_file.name}...")
        
#         success = crop_pdf(str(pdf_file), str(output_file_path), crop_mm=crop_mm, **kwargs)
        
#         if success:
#             logging.info(f"Done: {pdf_file.name} -> Saved in output folder.")



# # --- Istemal Karne Ka Tariqa ---
# if __name__ == "__main__":
#     # Apne folders ke raste yahan likhein
#     src_folder = r"C:\Users\PCS\Downloads\New folder"
#     dst_folder = r"C:\Users\PCS\Downloads\New folderok"

#     # Cropping parameters
#     params = {
#         "crop_mm": 93,
#         "crop_top": 0,
#         "crop_bottom": 1,
#         "crop_left": 0,
#         "crop_right": 0
#     }

#     process_all_pdfs_in_folder(src_folder, dst_folder, **params)














# import logging
# from pypdf import PdfReader, PdfWriter

# # Configure logging for better debugging
# logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# def crop_pdf(input_pdf, output_pdf, crop_mm=5, crop_left=0, crop_right=0, crop_top=0, crop_bottom=0):
#     """
#     Crop a PDF file by specified margins in millimeters.
    
#     Args:
#         input_pdf (str): Path to input PDF file
#         output_pdf (str): Path to output PDF file
#         crop_mm (float): Crop amount in millimeters
#         crop_left (int): 1 to crop left side, 0 to skip
#         crop_right (int): 1 to crop right side, 0 to skip
#         crop_top (int): 1 to crop top, 0 to skip
#         crop_bottom (int): 1 to crop bottom, 0 to skip
#     """
#     try:
#         # Validate inputs
#         if not input_pdf.endswith('.pdf') or not output_pdf.endswith('.pdf'):
#             raise ValueError("Input and output files must be PDF files")
#         if crop_mm < 0:
#             raise ValueError("Crop amount cannot be negative")
#         if not all(isinstance(x, int) and x in [0, 1] for x in [crop_left, crop_right, crop_top, crop_bottom]):
#             raise ValueError("Crop parameters must be 0 or 1")

#         # Convert mm to points (1 mm = 72/25.4 points)
#         mm_to_pt = 72 / 25.4
#         crop_pts = crop_mm * mm_to_pt

#         # Initialize reader and writer
#         reader = PdfReader(input_pdf)
#         writer = PdfWriter()

#         # Log number of pages
#         logging.info(f"Processing {len(reader.pages)} pages from {input_pdf}")

#         for page in reader.pages:
#             # Get original media box
#             box = page.mediabox

#             # Calculate new coordinates
#             lower_left_x = box.lower_left[0] + (crop_pts if crop_left else 0)
#             lower_left_y = box.lower_left[1] + (crop_pts if crop_bottom else 0)
#             upper_right_x = box.upper_right[0] - (crop_pts if crop_right else 0)
#             upper_right_y = box.upper_right[1] - (crop_pts if crop_top else 0)

#             # Apply crop
#             page.mediabox.lower_left = (lower_left_x, lower_left_y)
#             page.mediabox.upper_right = (upper_right_x, upper_right_y)

#             writer.add_page(page)

#         # Write output PDF
#         with open(output_pdf, "wb") as f:
#             writer.write(f)
#         logging.info(f"Successfully saved cropped PDF to {output_pdf}")

#     except FileNotFoundError:
#         logging.error(f"Input file {input_pdf} not found")
#         raise
#     except Exception as e:
#         logging.error(f"Error processing PDF: {str(e)}")
#         raise

# # Example usage
# if __name__ == "__main__":
#     try:
#         # Crop only top
#         crop_pdf(r"E:\unb- workstations\94.pdf", r"E:\unb- workstations\94ok.pdf",crop_mm=93, crop_top=0, crop_bottom=1, crop_left=0, crop_right=0)
        
#         # # Crop only bottom
#         # crop_pdf("input.pdf", "output_bottom.pdf", crop_mm=5, crop_top=0, crop_bottom=1, crop_left=0, crop_right=0)
        
#         # # Crop both top and bottom
#         # crop_pdf("input.pdf", "output_both.pdf", crop_mm=5, crop_top=1, crop_bottom=1, crop_left=0, crop_right=0)
        
#         # # No cropping (as is)
#         # crop_pdf("input.pdf", "output_same.pdf", crop_mm=5, crop_top=0, crop_bottom=0, crop_left=0, crop_right=0)
        
#         # # Crop all sides
#         # crop_pdf("input.pdf", "output_all_sides.pdf", crop_mm=5, crop_top=1, crop_bottom=1, crop_left=1, crop_right=1)
#     except Exception as e:
#         logging.error(f"Failed to process PDF: {str(e)}")