import os
from PyPDF2 import PdfReader, PdfWriter

def extract_pdf_pages(input_pdf_path, start_page, end_page, output_folder, output_name="output.pdf"):
    """
    Local PC se PDF file leta hai (Google Drive nahi)
    Sirf selected pages extract karke nayi PDF banata hai.
    """

    # --- Input PDF check karein ---
    if not os.path.exists(input_pdf_path):
        raise FileNotFoundError(f"❌ File nahi mili: {input_pdf_path}")

    # --- Read PDF ---
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    total_pages = len(reader.pages)
    print(f"📄 Input PDF me total {total_pages} pages hain")

    # Agar end_page total pages se zyada ho to adjust kar do
    end_page = min(end_page, total_pages)

    if start_page > total_pages:
        raise ValueError(f"❌ Start page {start_page} total pages {total_pages} se zyada hai")

    # --- Page Extraction ---
    for i in range(start_page - 1, end_page):  # Page 1-based hotay hain
        writer.add_page(reader.pages[i])

    # --- Output Folder Create ---
    os.makedirs(output_folder, exist_ok=True)
    output_pdf = os.path.join(output_folder, output_name)

    # --- Save Output PDF ---
    with open(output_pdf, "wb") as f:
        writer.write(f)

    print(f"✅ Output PDF save ho gayi: {output_pdf}")
    return output_pdf


# -------------------------
# Example Run (Change Paths)
# -------------------------

if __name__ == "__main__":

    # Yaha apni PC wali PDF ka path likho
    input_pdf_path = r"C:\Users\PCS\Downloads\Gumshuda Mohabbat novel - Copy\7.pdf"

    # Ye folder bana diya jayega agar nahi hoga
    output_folder = r"C:\Users\PCS\Downloads\2.pdf"

    # Page range yaha change karein
    start_page = 7
    end_page = 29

    extract_pdf_pages(input_pdf_path, start_page, end_page, output_folder)
