import fitz  # PyMuPDF library
import re

def extract_english_from_pdf(pdf_path, output_txt_path, header_to_ignore=""):
    # Yeh Regex pattern sirf English words aur unke darmiyan spaces/punctuation ko match karega
    eng_pattern = re.compile(r'[a-zA-Z]+(?:[\s.,!?\'-]+[a-zA-Z]+)*')

    try:
        # PDF file ko open karna
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error: PDF file open nahi ho saki. Details: {e}")
        return

    # Text file create karna jisme report save hogi
    with open(output_txt_path, 'w', encoding='utf-8') as f:
        f.write("PDF English Text Extraction Report\n")
        f.write("="*40 + "\n\n")

        total_pages = len(doc)
        print(f"Total pages detected: {total_pages}. Processing started...")

        for page_num in range(total_pages):
            page = doc.load_page(page_num)
            text = page.get_text()

            # Agar koi header text pass kiya gaya hai, to usko page text se hata dein
            if header_to_ignore:
                # Case-insensitive replace ke liye regex ka use kar sakte hain ya direct replace
                text = text.replace(header_to_ignore, "")

            # Regex ke zariye English text ko find karna
            english_matches = eng_pattern.findall(text)

            # Khali spaces ko filter karna
            english_matches = [match.strip() for match in english_matches if match.strip()]

            # Agar is page par koi English word mila hai to file mein write karein
            if english_matches:
                f.write(f"Page Number: {page_num + 1}\n")
                f.write("-" * 20 + "\n")
                for match in english_matches:
                    # Single letters ko filter kar sakte hain agar chahein, 
                    # filhal sab save kar raha hai
                    f.write(f"-> {match}\n")
                f.write("\n")

    print(f"\nDone! Report successfully '{output_txt_path}' mein save ho gayi hai.")

# --- Program yahan se start hoga ---

# 1. Yahan apne PDF novel ka sahi path likhein
pdf_file = r"C:\Users\PCS\Desktop\test.pdf"

# 2. Yahan us text file ka naam likhein jisme report chahiye
output_file = r"C:\Users\PCS\Desktop\eng_word.txt"

# 3. Yahan wo header text likhein jo har page par hai aur aap usko ignore karna chahte hain
header_text = "DNA By Noor Rajpoot" 

# Function ko call karein
extract_english_from_pdf(pdf_file, output_file, header_to_ignore=header_text)