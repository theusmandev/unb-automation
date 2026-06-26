import fitz  # PyMuPDF library

def detect_fazool_question_marks(pdf_path, output_txt_path):
    try:
        # PDF file ko open karna
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error: PDF file open nahi ho saki. Details: {e}")
        return

    # Text file create karna jisme report save hogi
    with open(output_txt_path, 'w', encoding='utf-8') as f:
        f.write("Fazool Question Marks (?) Detection Report\n")
        f.write("="*50 + "\n\n")

        total_pages = len(doc)
        print(f"Total pages: {total_pages}. Scanning for '?' started...")
        
        issues_found_count = 0

        for page_num in range(total_pages):
            page = doc.load_page(page_num)
            text = page.get_text()

            # Text ko lines mein todna taake poori line ka context mil sake
            lines = text.split('\n')
            page_issues = []

            for line in lines:
                # Agar line mein English wala question mark '?' mojood hai
                if '?' in line:
                    page_issues.append(line.strip())

            # Agar is page par koi masla mila hai to report mein likhein
            if page_issues:
                issues_found_count += len(page_issues)
                f.write(f"Page Number: {page_num + 1}\n")
                f.write("-" * 20 + "\n")
                for issue in page_issues:
                    # Line print karega taake aapko pata chale kon sa sentence hai
                    f.write(f"Line: {issue}\n")
                f.write("\n")

    print(f"\nScanning complete! Total {issues_found_count} fazool '?' mile hain.")
    print(f"Report '{output_txt_path}' mein save ho gayi hai.")

# --- Program yahan se start hoga ---

# 1. Yahan apne PDF novel ka path daalein
pdf_file = r"C:\Users\PCS\Desktop\test.pdf"

# 2. Yahan us text file ka naam likhein jisme aapko summary chahiye
output_file = r"C:\Users\PCS\Desktop\Q marks.txt"

# Function ko call karein
detect_fazool_question_marks(pdf_file, output_file)