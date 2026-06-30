# import PyPDF2

# def find_word_in_pdf(pdf_path, txt_path, target_word):
#     pages_with_word = []
    
#     try:
#         # PDF فائل کو 'read-binary' موڈ میں کھولیں
#         with open(pdf_path, 'rb') as file:
#             reader = PyPDF2.PdfReader(file)
            
#             # PDF کے تمام صفحات کو ایک ایک کر کے چیک کریں
#             for page_num in range(len(reader.pages)):
#                 page = reader.pages[page_num]
#                 text = page.extract_text()
                
#                 # اگر صفحے پر ٹیکسٹ موجود ہے اور ہمارا مطلوبہ لفظ بھی اس میں ہے
#                 # lower() کا استعمال اس لیے کیا ہے تاکہ 'Tab', 'TAB' یا 'tab' سب کو پہچان لے
#                 if text and target_word.lower() in text.lower():
#                     # page_num 0 سے شروع ہوتا ہے، اس لیے 1 جمع کر رہے ہیں تاکہ اصل صفحہ نمبر آئے
#                     pages_with_word.append(str(page_num + 1))
        
#         # نتائج کو TXT فائل میں محفوظ کریں
#         with open(txt_path, 'w', encoding='utf-8') as txt_file:
#             if pages_with_word:
#                 txt_file.write(f"Lafz '{target_word}' in safhat par mila hai:\n")
#                 txt_file.write(", ".join(pages_with_word))
#                 print(f"✅ Kaam mukammal ho gaya! Page numbers '{txt_path}' mein save ho gaye hain.")
#             else:
#                 txt_file.write(f"Lafz '{target_word}' PDF mein kahin nahi mila.")
#                 print("❌ Yeh lafz PDF mein nahi mila.")
                
#     except FileNotFoundError:
#         print("⚠️ Error: PDF file nahi mili. Kripya path check karein.")
#     except Exception as e:
#         print(f"⚠️ Ek masla pesh aaya: {e}")

# # --- Yahan apni files ki details dein ---
# pdf_file = r"C:\Users\PCS\Desktop\test.pdf"  # Yahan apni PDF file ka path likhein
# txt_file =r"C:\Users\PCS\Desktop\tab_finder.txt"    # Jis file mein result save karna hai uska naam
# word = 'Tab5'                        # Wo lafz jo dhoondna hai

# # Function ko call karein
# find_word_in_pdf(pdf_file, txt_file, word)












import fitz  # PyMuPDF library

def find_word_in_pdf(pdf_path, txt_path, target_word):
    pages_with_word = []
    
    try:
        # PDF فائل کو کھولیں
        doc = fitz.open(pdf_path)
        
        # PDF کے تمام صفحات کو ایک ایک کر کے چیک کریں
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()  # یہ فنکشن بہت بہتر طریقے سے ٹیکسٹ نکالتا ہے
            
            # اگر صفحے پر ہمارا مطلوبہ لفظ موجود ہے (lower() سے Case Sensitivity ختم کی ہے)
            if text and target_word.lower() in text.lower():
                pages_with_word.append(str(page_num + 1))
        
        # نتائج کو TXT فائل میں محفوظ کریں
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            if pages_with_word:
                txt_file.write(f"Lafz '{target_word}' in safhat par mila hai:\n")
                txt_file.write(", ".join(pages_with_word))
                print(f"✅ Kaam mukammal ho gaya! Page numbers '{txt_path}' mein save ho gaye hain.")
            else:
                txt_file.write(f"Lafz '{target_word}' PDF mein kahin nahi mila.\n")
                print("❌ Yeh lafz is library se bhi nahi mila.")
                print("⚠️ Note: Agar aap ki PDF scanned images (tasaveer) par mushtamil hai, toh humein OCR (Tesseract) istemal karna parega.")
                
    except Exception as e:
        print(f"⚠️ Ek masla pesh aaya: {e}")

# --- Yahan apni files ki details dein ---
pdf_file = r"C:\Users\PCS\Desktop\test.pdf"  # Yahan apni PDF file ka path likhein
txt_file =r"C:\Users\PCS\Desktop\tab_finder.txt"      # Jis file mein result save karna hai uska naam
word = 'tab'                        # Wo lafz jo dhoondna hai

# Function ko call karein
find_word_in_pdf(pdf_file, txt_file, word)