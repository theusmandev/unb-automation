import fitz  # PyMuPDF library
import re
import os

# ==========================================
# ⚙️ MAIN SETTINGS (Yahan changes karein)
# ==========================================

# 1. Yahan apne PDF novel ka path daalein
PDF_FILE_PATH = r"C:\Users\PCS\Desktop\test1.pdf"

# 2. Header text jo ignore karna hai
HEADER_TEXT_TO_IGNORE = "Published On URDUNOVELBANKS.COM"
# HEADER_TEXT_TO_IGNORE = "Published On URDUNOVELBANKS.COM"
# ==========================================


def extract_english_from_pdf(doc, output_txt_path, header_to_ignore=""):
    # Yeh Regex pattern sirf English words aur unke darmiyan spaces/punctuation ko match karega
    eng_pattern = re.compile(r'[a-zA-Z]+(?:[\s.,!?\'-]+[a-zA-Z]+)*')

    with open(output_txt_path, 'w', encoding='utf-8') as f:
        f.write("PDF English Text Extraction Report\n")
        f.write("="*40 + "\n\n")

        total_pages = len(doc)
        print(f"[English Extraction] Total pages: {total_pages}. Processing started...")

        for page_num in range(total_pages):
            page = doc.load_page(page_num)
            text = page.get_text()

            # Agar koi header text pass kiya gaya hai, to usko page text se hata dein
            if header_to_ignore:
                text = text.replace(header_to_ignore, "")

            # Regex ke zariye English text ko find karna
            english_matches = eng_pattern.findall(text)
            english_matches = [match.strip() for match in english_matches if match.strip()]

            # Agar is page par koi English word mila hai to file mein write karein
            if english_matches:
                f.write(f"Page Number: {page_num + 1}\n")
                f.write("-" * 20 + "\n")
                for match in english_matches:
                    f.write(f"-> {match}\n")
                f.write("\n")

    print(f"[English Extraction] Done! Report '{output_txt_path}' mein save ho gayi.")

def detect_fazool_question_marks(doc, output_txt_path):
    with open(output_txt_path, 'w', encoding='utf-8') as f:
        f.write("Fazool Question Marks (?) Detection Report\n")
        f.write("="*50 + "\n\n")

        total_pages = len(doc)
        print(f"[Question Mark Detection] Scanning for '?' started...")
        
        issues_found_count = 0

        for page_num in range(total_pages):
            page = doc.load_page(page_num)
            text = page.get_text()

            lines = text.split('\n')
            page_issues = []

            for line in lines:
                if '?' in line:
                    page_issues.append(line.strip())

            if page_issues:
                issues_found_count += len(page_issues)
                f.write(f"Page Number: {page_num + 1}\n")
                f.write("-" * 20 + "\n")
                for issue in page_issues:
                    f.write(f"Line: {issue}\n")
                f.write("\n")

    print(f"[Question Mark Detection] Complete! Total {issues_found_count} fazool '?' mile hain.")
    print(f"[Question Mark Detection] Report '{output_txt_path}' mein save ho gayi.")

def analyze_pdf(pdf_path, header_text):
    # Desktop ka path dynamically nikalna aur 'reports' folder banana
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    reports_folder = os.path.join(desktop_path, "reports")

    if not os.path.exists(reports_folder):
        os.makedirs(reports_folder)
        print(f"Naya folder create ho gaya hai: {reports_folder}\n")

    # Output files ke paths set karna
    eng_output_file = os.path.join(reports_folder, "eng_word.txt")
    qmarks_output_file = os.path.join(reports_folder, "Q_marks.txt")

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error: PDF file open nahi ho saki. Details: {e}")
        return

    print("="*50)
    print("Starting PDF Analysis...")
    print("="*50 + "\n")

    # Dono functions ko call karna
    extract_english_from_pdf(doc, eng_output_file, header_to_ignore=header_text)
    print("-" * 30)
    detect_fazool_question_marks(doc, qmarks_output_file)

    # PDF close karna
    doc.close()
    
    print("\n" + "="*50)
    print(f"All tasks completed successfully! Dono reports aapke Desktop ke 'reports' folder mein mojood hain.")
    print("="*50)

# --- Execution ---
if __name__ == "__main__":
    # Top par set kiye gaye variables yahan use ho rahe hain
    analyze_pdf(PDF_FILE_PATH, HEADER_TEXT_TO_IGNORE)