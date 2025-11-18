
# from pypdf import PdfReader, PdfWriter

# def crop_pdf(input_pdf, output_pdf, crop_mm=5):
#     # mm to pt conversion
#     mm_to_pt = 72 / 25.4
#     crop_pts = crop_mm * mm_to_pt  

#     reader = PdfReader(input_pdf)
#     writer = PdfWriter()

#     for page in reader.pages:
#         # Original crop box
#         box = page.mediabox  

#         # New crop values
#         lower_left_x = box.lower_left[0]
#         lower_left_y = box.lower_left[1] + crop_pts  # bottom se crop
#         upper_right_x = box.upper_right[0]
#         upper_right_y = box.upper_right[1] - crop_pts  # top se crop

#         # Apply crop
#         page.mediabox.lower_left = (lower_left_x, lower_left_y)
#         page.mediabox.upper_right = (upper_right_x, upper_right_y)

#         writer.add_page(page)

#     with open(output_pdf, "wb") as f:
#         writer.write(f)

# # Example use
# crop_pdf(r"C:\Users\PCS\Downloads\Hashim Nadeem Novels\replace\Hashim Nadeem - Abdullah 1 (Urdueadings.com).pdf", r"C:\Users\PCS\Downloads\Hashim Nadeem Novels\replace\Hashim Nadeemokok - Abdullah 1 (Urdueadings.com).pdf", crop_mm=5)
