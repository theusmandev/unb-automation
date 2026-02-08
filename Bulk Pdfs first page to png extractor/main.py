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
            png_path = os.path.join(output_folder, f"{base_name}.png")

            try:
                doc = fitz.open(pdf_path)
                page = doc.load_page(0)  # Pehla page
                pix = page.get_pixmap(dpi=200)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img.save(png_path, "PNG")
                doc.close()
                print(f"✅ Saved: {png_path}")
            except Exception as e:
                print(f"❌ Error converting {filename}: {e}")

    print(f"\n🎯 Conversion complete! All PNGs saved in: {output_folder}")

# -------------------------------
if __name__ == "__main__":
    folder_path = r"E:\unb-workstation\Rare Books"
    pdfs_to_pngs(folder_path)
