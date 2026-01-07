import fitz  # PyMuPDF
from PIL import Image
from fpdf import FPDF
import os

def change_pdf_background(input_pdf, bg_color=(173, 216, 230)):  # light blue
    folder = os.path.dirname(input_pdf)
    base_name = os.path.splitext(os.path.basename(input_pdf))[0]
    output_pdf = os.path.join(folder, f"{base_name}_bgchanged.pdf")

    doc = fitz.open(input_pdf)
    pdf = FPDF()

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # Render page as PNG (no alpha channel)
        pix = page.get_pixmap(dpi=200)
        img_path = os.path.join(folder, f"page_{page_num+1}.png")
        pix.save(img_path)

        # Open image
        img = Image.open(img_path).convert("RGBA")
        datas = img.getdata()

        new_data = []
        for item in datas:
            # If pixel is almost white, make it transparent
            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                new_data.append((0, 0, 0, 0))
            else:
                new_data.append(item)

        img.putdata(new_data)

        # Create background
        bg = Image.new("RGBA", img.size, bg_color)

        # Merge page onto background
        combined = Image.alpha_composite(bg, img)

        # Save final image
        final_img = os.path.join(folder, f"bg_{page_num+1}.jpg")
        combined.convert("RGB").save(final_img, "JPEG", quality=90)

        # Add into PDF
        pdf.add_page()
        pdf.image(final_img, 0, 0, 210, 297)

        # Cleanup
        os.remove(img_path)
        os.remove(final_img)

    pdf.output(output_pdf, "F")
    print(f"✅ Background changed PDF saved: {output_pdf}")


# Run
change_pdf_background(r"E:\pdf color change\sheeshe-ke-ghar-qurratulain-hyder-ebooks-1.pdf")
