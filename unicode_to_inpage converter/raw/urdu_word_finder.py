#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import fitz  # PyMuPDF library
import os

def search_urdu_in_pdf(pdf_path, search_word):
    print("\n" + "="*50)
    print(f"  🔍 PDF Search Engine (Urdu)")
    print("="*50)
    
    if not os.path.exists(pdf_path):
        print(f"❌ File nahi mili: {pdf_path}")
        return

    print(f"📂 File   : {os.path.basename(pdf_path)}")
    print(f"🔎 Search : '{search_word}'")
    print("-" * 50)

    try:
        # PDF file open karein
        pdf_document = fitz.open(pdf_path)
        total_pages = len(pdf_document)
        print(f"📄 Total Pages: {total_pages}\n")
        
        found_pages = []

        # Har page ko scan karein
        for page_num in range(total_pages):
            page = pdf_document.load_page(page_num)
            
            # Page ka text extract karein
            text = page.get_text("text")
            
            # Agar word mil jaye (InPage PDF export mein kabhi kabhi text RTL/LTR mix hota hai, 
            # is liye hum basic string matching kar rahe hain)
            if search_word in text:
                # PDF pages 0 se shuru hote hain, is liye +1 kiya hai
                actual_page = page_num + 1
                found_pages.append(actual_page)
                print(f"  ✅ Mil gaya! -> Page Number: {actual_page}")

        print("-" * 50)
        if found_pages:
            print(f"🎉 Ye lafz total {len(found_pages)} pages par mila hai.")
            print(f"📑 Pages: {', '.join(map(str, found_pages))}")
        else:
            print("⚠️ Ye lafz is PDF mein kahin nahi mila.")
            print("Tip: InPage se PDF export karte waqt 'Save as Type' mein PDF select karein aur font theek check karein.")
            
        pdf_document.close()

    except Exception as e:
        print(f"❌ Error aaya: {e}")

# ══════════════════════════════════════════════════════════════
#  ⚙️ SETTINGS - Yahan apni file ka path aur word likhein
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    
    # Apni PDF file ka path yahan dein (Jo InPage se export ki ho)
    PDF_FILE_PATH = r"C:\Users\PCS\Desktop\test_Final.pdf"
    
    # Jo lafz search karna hai wo yahan likhein
    WORD_TO_SEARCH = "میڈیکل کا یہ"

    search_urdu_in_pdf(PDF_FILE_PATH, WORD_TO_SEARCH)