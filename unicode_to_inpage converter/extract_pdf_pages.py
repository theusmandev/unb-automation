import PyPDF2
import os

def extract_pdf_pages(pdf_path, pages_to_extract, output_dir="extracted_pages"):
    # Agar output folder nahi hai to naya bana lo
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # Original PDF ko read mode mein open karein
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = len(reader.pages)
            
            print(f"Total pages in PDF: {total_pages}\n")

            # Har page number par loop lagayein
            for page_num in pages_to_extract:
                # PyPDF2 mein page index 0 se start hota hai, is liye (page_num - 1) kiya hai
                index = page_num - 1
                
                # Check karein ke page number PDF ki range mein hai ya nahi
                if 0 <= index < total_pages:
                    writer = PyPDF2.PdfWriter()
                    writer.add_page(reader.pages[index])
                    
                    # Nayi PDF file ka naam aur path set karein
                    output_file_path = os.path.join(output_dir, f"page_{page_num}.pdf")
                    
                    # Page ko nayi file mein save karein
                    with open(output_file_path, 'wb') as output_file:
                        writer.write(output_file)
                        
                    print(f"Success: Page {page_num} saved as {output_file_path}")
                else:
                    print(f"Skipped: Page {page_num} (Out of range)")
                    
    except FileNotFoundError:
        print("Error: PDF file nahi mili. Kripya path check karein.")
    except Exception as e:
        print(f"Koi error aagaya: {e}")

# --- Hardcoded Inputs ---

# Yahan apni PDF file ka path likhein
pdf_path = r"C:\Users\PCS\Downloads\InPage DNA\DNA Episode 1(1).pdf"

# Yahan wo page numbers likhein jo nikalne hain (Normal numbering 1, 2, 3...)
pages_to_extract = [1, 11, 532] 

# Function ko call karein
extract_pdf_pages(pdf_path, pages_to_extract)