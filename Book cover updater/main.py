import os
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from PIL import Image
import pathlib

def replace_first_page(folder_path):
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

    # ✨ NEW FEATURE: Rename image based on PDF title
    try:
        new_image_name = f"{pdf_file.stem}_image{image_file.suffix.lower()}"
        new_image_path = folder / new_image_name

        # Agar same name ka file already hua to delete kar do
        if new_image_path.exists():
            os.remove(new_image_path)

        os.rename(image_file, new_image_path)
        image_file = new_image_path

        print(f"Image rename ho gayi: {image_file}")
    except Exception as e:
        print(f"Error: Image rename nahi ho saki: {e}")
        return

    # Step 1: Get original PDF first page dimensions
    try:
        reader = PdfReader(str(pdf_file))
        first_page = reader.pages[0]
        page_width = float(first_page.mediabox.width)
        page_height = float(first_page.mediabox.height)
    except Exception as e:
        print(f"Error: PDF page dimensions padhne mein issue: {e}")
        return

    # Step 2: Convert image to single-page PDF with same page size
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

    # Step 3: Merge image PDF + rest of file
    try:
        writer = PdfWriter()

        # Add image page
        img_reader = PdfReader(str(temp_image_pdf))
        writer.add_page(img_reader.pages[0])

        # Add remaining pages
        for i in range(1, len(reader.pages)):
            writer.add_page(reader.pages[i])

        # Save file (overwrite original)
        output_pdf = pdf_file
        with open(output_pdf, "wb") as f:
            writer.write(f)

        print(f"PDF update ho gaya: {output_pdf}")

    except Exception as e:
        print(f"Error: PDF process karte waqt issue: {e}")
    finally:
        if temp_image_pdf.exists():
            try:
                os.remove(temp_image_pdf)
            except:
                pass


# Example run
if __name__ == "__main__":
    folder_path = r"E:\unb-workstation\Writers All Novels\mediafire2\replace"
    replace_first_page(folder_path)

