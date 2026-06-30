import os
from pypdf import PdfReader, PdfWriter

def replace_pdf_pages():
    # Aap ke diye gaye paths
    main_pdf_path = r"C:\Users\PCS\Desktop\test.pdf"
    output_pdf_path = r"C:\Users\PCS\Desktop\test_Final.pdf"

    # Dictionary: Original page number (1-based) map kiya ha replacement PDF paths ke sath
    replacements = {
        1: r"E:\unb-workstation\InPage DNA\DNA\InPage DNA\extracted_pages\1.pdf",
        2: r"E:\unb-workstation\InPage DNA\DNA\InPage DNA\extracted_pages\2.pdf",
        9: r"E:\unb-workstation\InPage DNA\DNA\InPage DNA\extracted_pages\9.pdf",
        255: r"E:\unb-workstation\InPage DNA\DNA\InPage DNA\extracted_pages\255.pdf"
    }

    # Main PDF reader aur output ke liye writer initialize kar rahay han
    main_reader = PdfReader(main_pdf_path)
    writer = PdfWriter()

    total_pages = len(main_reader.pages)

    # Main PDF ke har page par loop chalayen
    for i in range(total_pages):
        current_page_number = i + 1  # Python index 0 se start hota ha, is liye +1 kiya ha
        
        if current_page_number in replacements:
            # Agar ye page dictionary mein maujood ha, toh naya PDF utha lein
            replacement_pdf_path = replacements[current_page_number]
            try:
                rep_reader = PdfReader(replacement_pdf_path)
                # Naye PDF ka pehla page (index 0) output mein add kar dein
                writer.add_page(rep_reader.pages[0])
                print(f"Page {current_page_number} successfully replace ho gaya ha.")
            except Exception as e:
                print(f"Error: Page {current_page_number} ki replacement PDF load nahi hui: {e}")
                # Agar error aaye toh original page wapas dal dein
                writer.add_page(main_reader.pages[i])
        else:
            # Baqi sab pages original PDF se same copy honge
            writer.add_page(main_reader.pages[i])

    # Final PDF ko output path par save kar dein
    with open(output_pdf_path, "wb") as f_out:
        writer.write(f_out)
    
    print(f"\nKaam mukammal ho gaya! Final PDF yahan save ho gayi ha: {output_pdf_path}")

if __name__ == "__main__":
    replace_pdf_pages()