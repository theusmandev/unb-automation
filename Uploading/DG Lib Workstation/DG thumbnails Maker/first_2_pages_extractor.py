import os
import fitz  # PyMuPDF
from PIL import Image

def pdfs_to_pngs(input_folder):
    output_folder = os.path.join(input_folder, "pngs")
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            base_name = os.path.splitext(filename)[0]

            try:
                doc = fitz.open(pdf_path)
                
                # Check karein ke PDF mein kitne pages hain (kam az kam 2 ya jitne available hon)
                pages_to_extract = min(2, len(doc)) 

                for page_num in range(pages_to_extract):
                    page = doc.load_page(page_num)  # Page load karein (0 for first, 1 for second)
                    pix = page.get_pixmap(dpi=200)
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    
                    # Naya filename taake page number bhi sath aaye
                    png_filename = f"{base_name}_page_{page_num + 1}.png"
                    png_path = os.path.join(output_folder, png_filename)
                    
                    img.save(png_path, "PNG")
                    print(f"✅ Saved: {png_filename}")

                doc.close()
            except Exception as e:
                print(f"❌ Error converting {filename}: {e}")

    print(f"\n🎯 Conversion complete! All PNGs saved in: {output_folder}")

# -------------------------------
if __name__ == "__main__":
    # Apna path yahan check karlein
    folder_path = r"E:\unb-workstation\Writers All Novels\Uploadings\DG workstation\3_"
    pdfs_to_pngs(folder_path)