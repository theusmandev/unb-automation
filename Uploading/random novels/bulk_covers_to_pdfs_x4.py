import os
import shutil
import pathlib
import re
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from PIL import Image

def process_all_pdf_covers(folder_path):
    folder = pathlib.Path(folder_path)
    if not folder.is_dir():
        print(f"Error: {folder_path} directory nahi hai.")
        return

    # Folders Setup
    missing_folder = folder / "Missing_Covers"
    processed_folder = folder / "Processed_PDFs"
    
    missing_folder.mkdir(exist_ok=True)
    processed_folder.mkdir(exist_ok=True)
    
    valid_extensions = [".png", ".jpg", ".jpeg", ".webp"]
    
    processed_count = 0
    missing_count = 0
    error_count = 0

    print(f"Processing started in: {folder}\n" + "-"*40)

    for pdf_file in folder.glob("*.pdf"):
        base_name = pdf_file.stem.strip().lower()
        matching_image = None

        # Robust Image Search: Handling -4x, 2x, etc. suffixes
        for file in folder.iterdir():
            if file.is_file() and file.suffix.lower() in valid_extensions:
                # Image ke naam se -4x, 2x, -2x, _4x waghera hatana
                image_stem_clean = re.sub(r'[- _]?\d+x$', '', file.stem.strip().lower())
                
                if image_stem_clean == base_name:
                    matching_image = file
                    break

        if not matching_image:
            print(f"⚠️ Image missing: '{pdf_file.name}' -> Moving to Missing_Covers")
            try:
                shutil.move(str(pdf_file), str(missing_folder / pdf_file.name))
                missing_count += 1
            except Exception as e:
                print(f"❌ Move failed for {pdf_file.name}: {e}")
            continue

        print(f"🔄 Processing: '{pdf_file.name}' with cover '{matching_image.name}'")
        temp_image_pdf = folder / f"temp_{pdf_file.stem}.pdf"
        output_pdf = processed_folder / pdf_file.name
        
        try:
            # 1. Safely open original PDF using 'with' to ensure it closes properly
            with open(pdf_file, "rb") as pdf_in:
                reader = PdfReader(pdf_in)
                reference_page = reader.pages[1] if len(reader.pages) > 1 else reader.pages[0]
                
                page_width = float(reference_page.mediabox.width)
                page_height = float(reference_page.mediabox.height)

                # 2. Safely open Image using 'with' so it doesn't lock the file
                with Image.open(matching_image) as img:
                    img_width, img_height = img.size

                # Draw canvas
                scale = min(page_width / img_width, page_height / img_height)
                scaled_width = img_width * scale
                scaled_height = img_height * scale

                c = canvas.Canvas(str(temp_image_pdf), pagesize=(page_width, page_height))
                x_offset = (page_width - scaled_width) / 2
                y_offset = (page_height - scaled_height) / 2
                
                c.drawImage(str(matching_image), x_offset, y_offset, width=scaled_width, height=scaled_height)
                c.showPage()
                c.save()

                # 3. Merge New Cover and Old Pages safely
                writer = PdfWriter()
                
                # Open temp image pdf safely
                with open(temp_image_pdf, "rb") as temp_in:
                    img_reader = PdfReader(temp_in)
                    writer.add_page(img_reader.pages[0]) # Add new cover

                    for i in range(1, len(reader.pages)): # Add remaining pages
                        writer.add_page(reader.pages[i])

                    # Save directly to Processed_PDFs
                    with open(output_pdf, "wb") as f_out:
                        writer.write(f_out)

            # --- YAHAAN TAK SAB FILES CLOSE HO CHUKI HAIN ---
            # Ab hum inko araam se delete aur move kar sakte hain
            os.remove(pdf_file)
            shutil.move(str(matching_image), str(processed_folder / matching_image.name))

            print(f"✅ Success: '{pdf_file.name}' -> Moved to Processed_PDFs")
            processed_count += 1

        except Exception as e:
            print(f"❌ Error processing '{pdf_file.name}': {e}")
            error_count += 1
            
        finally:
            # Har haal mein temporary file remove karni hai
            if temp_image_pdf.exists():
                try:
                    os.remove(temp_image_pdf)
                except:
                    pass

    # Final Report
    print("-" * 40)
    print("Processing Complete!")
    print(f"Successfully Processed & Moved: {processed_count}")
    print(f"Missing Images (Moved): {missing_count}")
    print(f"Errors: {error_count}")

if __name__ == "__main__":
    folder_path = r"E:\unb-workstation\Writers All Novels\Uploadings\random novels"
    process_all_pdf_covers(folder_path)