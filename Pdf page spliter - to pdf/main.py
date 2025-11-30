from PyPDF2 import PdfReader, PdfWriter

# Original PDF ka path
input_pdf_path = r"C:\Users\PCS\Downloads\ok muhammad.pdf"

reader = PdfReader(input_pdf_path)

# Har page ke liye loop
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    
    # Naya PDF ka naam
    output_pdf_path = f"page_{i+1}.pdf"
    
    # Naya PDF save karo
    with open(output_pdf_path, "wb") as output_pdf:
        writer.write(output_pdf)

    print(f"{output_pdf_path} saved successfully!")
