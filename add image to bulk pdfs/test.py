





import os
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from PIL import Image
import pathlib

def add_cover_to_all_pdfs(folder_path):
    folder = pathlib.Path(folder_path)
    if not folder.is_dir():
        print(f"Error: {folder_path} folder nahi hai.")
        return

    # Find the single image file
    image_file = None
    for file in folder.iterdir():
        if file.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
            image_file = file
            break

    if not image_file:
        print("Error: Image (PNG/JPG/WebP) folder mein nahi mili.")
        return

    pdf_files = [file for file in folder.iterdir() if file.suffix.lower() == ".pdf"]

    if not pdf_files:
        print("Error: Folder mein koi PDF nahi mili.")
        return

    print(f"Total PDFs found: {len(pdf_files)}")
    print(f"Cover image: {image_file.name}")

    # Loop through each PDF
    for pdf_file in pdf_files:
        print(f"\nProcessing: {pdf_file.name}")

        try:
            reader = PdfReader(str(pdf_file))
            first_page = reader.pages[0]
            page_width = float(first_page.mediabox.width)
            page_height = float(first_page.mediabox.height)
        except Exception as e:
            print(f"Error: {pdf_file.name} ka first page padhna fail: {e}")
            continue

        # Create temp image PDF
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
            continue

        # Merge cover + original PDF
        try:
            writer = PdfWriter()

            # Add cover
            image_reader = PdfReader(str(temp_image_pdf))
            writer.add_page(image_reader.pages[0])

            # Add original pages
            for page in reader.pages:
                writer.add_page(page)

            # Save final PDF
            output_pdf = folder / f"{pdf_file.stem}_with_cover.pdf"
            with open(output_pdf, "wb") as f:
                writer.write(f)

            # Replace original
            os.replace(output_pdf, pdf_file)

            print(f"✔ Cover added successfully to: {pdf_file.name}")

        except Exception as e:
            print(f"Error: {pdf_file.name} merge fail: {e}")

        finally:
            if temp_image_pdf.exists():
                try:
                    os.remove(temp_image_pdf)
                except:
                    pass


# Example Run
if __name__ == "__main__":
    folder_path = r"C:\Users\PCS\Downloads\Lahu se lal Novel - Copy\New folder"
    add_cover_to_all_pdfs(folder_path)
