import os
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from PIL import Image
import pathlib

def add_image_as_cover(folder_path):
    folder = pathlib.Path(folder_path)
    if not folder.is_dir():
        print(f"Error: {folder_path} folder nahi hai.")
        return

    # Find PDF and image files
    pdf_file = None
    image_file = None
    for file in folder.iterdir():
        if file.suffix.lower() == ".pdf":
            pdf_file = file
        elif file.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
            image_file = file

    if not pdf_file or not image_file:
        print("Error: PDF ya image file folder mein nahi mili.")
        return

    # Step 1: Get original PDF first page dimensions (for consistency)
    try:
        reader = PdfReader(str(pdf_file))
        first_page = reader.pages[0]
        page_width = float(first_page.mediabox.width)
        page_height = float(first_page.mediabox.height)
    except Exception as e:
        print(f"Error: PDF page dimensions padhne mein issue: {e}")
        return

    # Step 2: Convert image to single-page PDF with same size
    temp_image_pdf = folder / "temp_image.pdf"
    try:
        img = Image.open(image_file)
        img_width, img_height = img.size

        scale = min(page_width / img_width, page_height / img_height)
        scaled_width = img_width * scale
        scaled_height = img_height * scale

        c = canvas.Canvas(str(temp_image_pdf), pagesize=(page_width, page_height))
        x_offset = (page_width - scaled_width) / 2
        y_offset = (page_height - scaled_height) / 2
        c.drawImage(str(image_file), x_offset, y_offset, width=scaled_width, height=scaled_height)
        c.showPage()
        c.save()
    except Exception as e:
        print(f"Error: Image ko PDF mein convert karte waqt issue: {e}")
        return

    # Step 3: Merge image PDF (first) + original PDF
    try:
        writer = PdfWriter()

        # Add image page first (cover)
        image_reader = PdfReader(str(temp_image_pdf))
        writer.add_page(image_reader.pages[0])

        # Add all original PDF pages
        for page in reader.pages:
            writer.add_page(page)

        # Save to new file
        output_pdf = folder / f"{pdf_file.stem}_with_cover.pdf"
        with open(output_pdf, "wb") as f:
            writer.write(f)

        print(f"Image cover ke sath PDF ready: {output_pdf}")

        # Agar overwrite karna hai:
        os.replace(output_pdf, pdf_file)

    except Exception as e:
        print(f"Error: PDF merge karte waqt issue: {e}")
    finally:
        if temp_image_pdf.exists():
            try:
                os.remove(temp_image_pdf)
            except:
                pass


# Example run
if __name__ == "__main__":
    folder_path = r"C:\Users\PCS\Downloads\replace"
    add_image_as_cover(folder_path)
