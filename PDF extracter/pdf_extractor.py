from pypdf import PdfReader, PdfWriter

def extract_pdf_pages(input_path, output_path, start_page, end_page):
    try:
        # PDF read karne aur nayi PDF write karne ke liye objects
        reader = PdfReader(input_path)
        writer = PdfWriter()

        total_pages = len(reader.pages)
        
        # Python 0-based indexing use karta hai (Page 1 ka index 0 hota hai)
        # Is liye start_page mein se 1 minus karna zaroori hai
        start_index = start_page - 1
        
        # Range function aakhri number ko exclude karta hai, is liye end_page wese hi likhenge
        end_index = end_page 

        # Validation: Check karein ke page numbers range se bahar na hon
        if start_index < 0 or end_index > total_pages or start_index >= end_index:
            print(f"Error: Invalid page numbers. Is PDF mein total {total_pages} pages hain.")
            return

        # Start se le kar end page tak loop chalayein aur pages extract karein
        for i in range(start_index, end_index):
            page = reader.pages[i]
            writer.add_page(page)

        # Nayi PDF file mein save karein
        with open(output_path, "wb") as output_file:
            writer.write(output_file)
            
        print(f"Success: Pages {start_page} se {end_page} tak '{output_path}' mein save ho gaye hain.")

    except FileNotFoundError:
        print(f"Error: '{input_path}' file nahi mili. Path check karein.")
    except Exception as e:
        print(f"Koi error aaya hai: {e}")


# ==========================================
# Yahan apni marzi ki values (Hardcoded) dein
# ==========================================
INPUT_PDF = r"C:\Users\PCS\Downloads\Khwateen digest June 2026.pdf"      # Apni asli PDF ka path (jaise 'C:/books/novel.pdf')
OUTPUT_PDF = r"C:\Users\PCS\Downloads\Khwateen digest June 2026_output.pdf"    # Jo nayi file banegi uska naam/path
START_PAGE = 158                            # Kahan se start karna hai (e.g., Page 3)
END_PAGE = 191                             # Kahan tak extract karna hai (e.g., Page 7 tak)

# Program run karna
extract_pdf_pages(INPUT_PDF, OUTPUT_PDF, START_PAGE, END_PAGE)