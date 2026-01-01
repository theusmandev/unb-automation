
import os

# ---------------- CONFIGURATION ----------------
INPUT_FILE = r"C:\Users\PCS\Downloads\writers_all_novels_list_urls.txt"
OUTPUT_FILE = r"C:\Users\PCS\Downloads\upload.txt"
# -----------------------------------------------

def clean_text_from_url(url):
    # URL کی صفائی اور ٹائٹل بنانے کا عمل
    filename = url.split("/")[-1]
    slug = filename.replace(".html", "")
    
    suffixes_to_remove = ["-read-online", "-read", "-online"]
    for suffix in suffixes_to_remove:
        if slug.endswith(suffix):
            slug = slug[:-len(suffix)]
            break
            
    if "-e-" in slug:
        clean_name = slug.replace("-e-", " E ").replace("-", " ").title()
        clean_name = clean_name.replace(" E ", "-e-")
    else:
        clean_name = slug.replace("-", " ").title()
        
    return clean_name

def generate_html_file():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: '{INPUT_FILE}' not found.")
        return

    # ڈیٹا اسٹور کرنے کے لیے لسٹ
    books_data = [] 
    author_name = "Unknown Writer"
    author_found = False

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    # 1. تمام لنکس سے ڈیٹا نکالنا
    for url in urls:
        book_title = clean_text_from_url(url)
        
        # مصنف کا نام نکالنا
        if " By " in book_title and not author_found:
            parts = book_title.split(" By ")
            if len(parts) > 1:
                author_name = parts[1].strip()
                author_found = True
        
        # ٹائٹل اور لنک کو عارضی طور پر محفوظ کر لیں
        books_data.append((book_title, url))

    # 2. یہاں چھانٹی (Sorting) ہو رہی ہے (Alphabetical Order)
    # یہ لسٹ کو ٹائٹل کے لحاظ سے A to Z ترتیب دے دے گا
    books_data.sort(key=lambda x: x[0])

    # 3. ترتیب شدہ ڈیٹا سے HTML بنانا
    links_list = []
    for title, url in books_data:
        list_item = f'        <li><a href="{url}"><span style="font-family: arial;">{title}</span></a></li>'
        links_list.append(list_item)

    # فائنل HTML سٹرکچر
    html_content = f""" <br />
 <div>
    <h2><span style="font-family: arial;">Read More Books by {author_name}</span></h2><ol>
{chr(10).join(links_list)}
    </ol>
</div>"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Success! Sorted HTML list saved to '{OUTPUT_FILE}'")
    print(f"Detected Author: {author_name}")

if __name__ == "__main__":
    generate_html_file()


# import os

# # ---------------- CONFIGURATION ----------------
# # اپنی ان پٹ فائل کا نام یہاں لکھیں
# INPUT_FILE = r"C:\Users\PCS\Downloads\writers_all_novels_list_urls.txt"
# # آؤٹ پٹ فائل کا نام یہاں لکھیں
# OUTPUT_FILE = r"C:\Users\PCS\Downloads\upload.txt"
# # -----------------------------------------------

# def clean_text_from_url(url):
#     # 1. URL میں سے آخری حصہ (Slug) نکالنا
#     filename = url.split("/")[-1]
    
#     # 2. .html کو ہٹانا
#     slug = filename.replace(".html", "")
    
#     # 3. فالتو الفاظ (-read-online وغیرہ) کو ہٹانا
#     suffixes_to_remove = ["-read-online", "-read", "-online"]
#     for suffix in suffixes_to_remove:
#         if slug.endswith(suffix):
#             slug = slug[:-len(suffix)]
#             break
            
#     # 4. ہائفن (-) کو اسپیس میں بدلنا اور ہر لفظ کا پہلا حرف بڑا کرنا (Title Case)
#     # خاص طور پر 'e' والے ناموں کے لیے (جیسے Kulliyat-e-Parveen)
#     if "-e-" in slug:
#         # اگر نام میں -e- ہے تو اسے محفوظ رکھیں
#         clean_name = slug.replace("-e-", " E ").replace("-", " ").title()
#         clean_name = clean_name.replace(" E ", "-e-") # واپس -e- کر دیں
#     else:
#         clean_name = slug.replace("-", " ").title()
        
#     return clean_name

# def generate_html_file():
#     # چیک کریں کہ ان پٹ فائل موجود ہے یا نہیں
#     if not os.path.exists(INPUT_FILE):
#         print(f"Error: '{INPUT_FILE}' not found. Please create the file and paste URLs in it.")
#         return

#     links_list = []
#     author_name = "Unknown Writer" # ڈیفالٹ نام
#     author_found = False

#     with open(INPUT_FILE, "r", encoding="utf-8") as f:
#         urls = [line.strip() for line in f if line.strip()]

#     # تمام لنکس کو پروسیس کرنا
#     for url in urls:
#         book_title = clean_text_from_url(url)
        
#         # مصنف کا نام نکالنے کی کوشش (Detect Writer Name)
#         # یہ "By" کے بعد والے حصے کو مصنف کا نام سمجھے گا
#         if " By " in book_title and not author_found:
#             parts = book_title.split(" By ")
#             if len(parts) > 1:
#                 author_name = parts[1].strip() # Writer Name detected
#                 author_found = True
        
#         # HTML لسٹ آئٹم بنانا
#         list_item = f'        <li><a href="{url}"><span style="font-family: arial;">{book_title}</span></a></li>'
#         links_list.append(list_item)

#     # مکمل HTML سٹرکچر بنانا
#     html_content = f""" <br />
#  <div>
#     <h2><span style="font-family: arial;">Read More Books by {author_name}</span></h2><ol>
# {chr(10).join(links_list)}
#     </ol>
# </div>"""

#     # آؤٹ پٹ فائل میں لکھنا
#     with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
#         f.write(html_content)

#     print(f"Success! HTML code has been saved to '{OUTPUT_FILE}'")
#     print(f"Detected Author: {author_name}")

# if __name__ == "__main__":
#     generate_html_file()