import pandas as pd
import re
import os

# -----------------------------------------------------------
# 1. INPUT FILE SETTINGS
# -----------------------------------------------------------
# Apni file ka path yahan dein. 
excel_input_path = r"C:\Users\PCS\Downloads\Anisha Umar.xlsx"

# --- AUTOMATIC WRITER NAME DETECTION ---
file_name = os.path.basename(excel_input_path) 
writer_raw = os.path.splitext(file_name)[0]      
WRITER_NAME = writer_raw.title()                 

print(f"🔹 Detected Writer: {WRITER_NAME}")

# Load Excel
try:
    df = pd.read_excel(excel_input_path)
except FileNotFoundError:
    raise FileNotFoundError(f"Excel file not found at: {excel_input_path}")

df = df.rename(columns={'Name': 'Titles', 'URL': 'Links'})

# --- CLEANING FUNCTIONS ---

def quick_clean(text):
    if pd.isna(text): return "Untitled"
    text = str(text)
    text = re.sub(r'(?i)download', '', text)
    text = re.sub(r'(?i)pdf', '', text)
    text = re.sub(r'(?i)file', '', text)
    text = re.sub(r'(?i)complete', '', text)
    text = re.sub(r'(?i)urdu novel', '', text)
    return " ".join(text.split())

def fix_google_drive_link(url):
    """
    Checks if the URL is a Google Drive link.
    If yes, extracts the ID and converts it to a clean Sharing/View link.
    Ignores MediaFire or other links.
    """
    if pd.isna(url) or url == "#": return url
    url = str(url).strip()

    # Sirf Google Drive links ko process karein
    if "drive.google.com" in url or "docs.google.com" in url:
        file_id = None
        
        # Pattern A: Check for 'id=' parameter (Direct download links usually have this)
        # Example: uc?export=download&id=123ABC...
        match_id = re.search(r'[?&]id=([a-zA-Z0-9_-]+)', url)
        
        # Pattern B: Check for '/d/' path (Standard links)
        # Example: /file/d/123ABC...
        match_path = re.search(r'/d/([a-zA-Z0-9_-]+)', url)

        if match_id:
            file_id = match_id.group(1)
        elif match_path:
            file_id = match_path.group(1)
        
        # Agar ID mil gayi to Sharing Link bana do
        if file_id:
            return f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
            
    # Agar MediaFire ya koi aur link hai to waisa hi return kar do
    return url

# -----------------------------------------------------------
# 2. DYNAMIC INTRO PARAGRAPH
# -----------------------------------------------------------
intro_html = f"""
<div class="unb-intro-section">
    <p><strong><span style="font-family: inherit;"><br /></span></strong></p>
    <h2 style="text-align: center;"><strong><span style="font-family: inherit;">{WRITER_NAME}'s Novels Collection</span></strong></h2>
    <p><span><span style="font-family: inherit;">Explore the rich world of <b>Urdu literature </b>with our<b> carefully curated</b> collection of <b>{WRITER_NAME}’s best novels.</b></span></span></p>
    <p><span style="font-family: inherit;"><b><br /></b>{WRITER_NAME} is widely admired for their captivating writing style, emotionally powerful characters, and deeply engaging storylines that leave a lasting impact on readers.</span></p>
    <p><span style="font-family: inherit;"><br /></span></p>
    <p><span style="font-family: inherit;">On this page, you can easily <strong>find and download PDF versions of {WRITER_NAME}’s most popular </strong><span>and</span><strong> top-rated Urdu novels</strong>. Each download link is carefully checked and regularly updated to ensure a <strong>smooth, safe, and hassle-free reading experience</strong>.</span></p>
    <p><span style="font-family: inherit;"><br /></span></p>
    <p><span style="font-family: inherit;">Whether you are a long-time fan or discovering the author's work for the first time, this collection offers a complete gateway to enjoy <strong>high-quality Urdu novels online</strong> — anytime, anywhere.</span></p>
</div>
"""

# -----------------------------------------------------------
# 3. USER SPECIFIC LINK HTML (Fixed Code)
# -----------------------------------------------------------
middle_link_html = """
<div dir="rtl" style="text-align: right;"><br /></div><div dir="rtl" style="text-align: right;"><br /></div><div dir="rtl" style="text-align: center;"><a href="https://www.urdunovelbanks.com/2025/12/all-urdu-novel-writers-list-complete.html" target="_blank"><b><span style="font-size: medium;">👈</span></b></a><a href="https://www.urdunovelbanks.com/2025/12/all-urdu-novel-writers-list-complete.html" target="_blank"><b><span style="font-size: medium;">دیگرمصنفین کی ناولز  لسٹ دیکھیں&nbsp;</span></b></a></div>
"""

# -----------------------------------------------------------
# 4. FOOTER SECTION
# -----------------------------------------------------------
footer_html = """
<div class="unb-footer-section">
    <div dir="rtl" style="text-align: right; margin-top: 40px; background: #fdfdfd; padding: 20px; border-radius: 8px; border: 1px solid #eee;">
        <div style="text-align: center;">
            <b><span style="font-size: large; color: #dc3545;">نوٹ :</span></b>
        </div>
        <div style="text-align: center; margin-top: 10px;">
            <span style="font-size: medium; line-height: 1.8;">اگر کسی ناول کا ڈاؤن لوڈ لنک کام نہ کرے تو براہِ کرم نیچے دیے گئے فارم کے ذریعے ہمیں اطلاع دیں، تاکہ ہم جلد از جلد اسے درست کر سکیں۔ آپ کے تعاون کا شکریہ۔</span>
        </div>
    </div>

    <div style="text-align: center; margin-top: 25px; margin-bottom: 20px;">
        <a href="https://forms.gle/K3spbeeu6c7QM61u9" target="_blank" class="unb-report-btn">
            Report Dead Link ⚠️
        </a>
    </div>
</div>
"""

# -----------------------------------------------------------
# 5. CSS STYLING & GENERATION
# -----------------------------------------------------------
html_content = """
<style>
    .unb-intro-section { margin-bottom: 30px; font-family: inherit; line-height: 1.6; color: #333; }
    .unb-main-wrapper { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; max-width: 100%; margin: 0 auto; padding: 10px; box-sizing: border-box; }
    .unb-ul-list { list-style: none !important; padding: 0 !important; margin: 0 !important; }
    .unb-list-row { background-color: #fff; border-bottom: 1px solid #eee; padding: 12px 5px; display: flex; align-items: center; gap: 12px; line-height: normal; }
    .unb-list-row:last-child { border-bottom: none; }
    .unb-num-badge { font-size: 14px; font-weight: bold; color: #999; min-width: 25px; }
    h3.unb-novel-heading { flex-grow: 1; font-size: 14px !important; color: #333 !important; font-weight: 600 !important; margin: 0 !important; padding: 0 !important; line-height: 1.4 !important; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; border: none; }
    a.unb-dl-btn { background-color: #007bff !important; color: white !important; padding: 6px 10px !important; border-radius: 4px !important; font-size: 12px !important; font-weight: bold !important; text-decoration: none !important; border: none !important; display: inline-flex; align-items: center; gap: 5px; transition: background-color 0.2s ease; white-space: nowrap; height: auto !important; }
    a.unb-dl-btn:hover { background-color: #0056b3 !important; }
    a.unb-report-btn { background-color: #dc3545 !important; color: white !important; padding: 10px 20px !important; border-radius: 50px !important; font-size: 14px !important; font-weight: bold !important; text-decoration: none !important; border: none !important; display: inline-block; box-shadow: 0 4px 6px rgba(220, 53, 69, 0.2); transition: transform 0.2s; }
    a.unb-report-btn:hover { background-color: #c82333 !important; transform: translateY(-2px); }
    .unb-svg-icon { width: 12px; height: 12px; fill: currentColor; pointer-events: none; }
</style>

<svg style="display: none;">
    <symbol id="unb-arrow-icon" viewBox="0 0 24 24">
        <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
    </symbol>
</svg>

<div class="unb-main-wrapper">
"""

html_content += intro_html
html_content += """<ul class="unb-ul-list">"""

# --- GENERATING ITEMS ---

for index, row in df.iterrows():
    raw_title = str(row['Titles'])
    
    # 1. Clean Title
    display_title = quick_clean(raw_title).title()
    
    # 2. Process Link (Fix Drive Links)
    raw_link = str(row['Links']).strip() if pd.notna(row['Links']) else "#"
    final_link = fix_google_drive_link(raw_link)

    tooltip_text = f"Download {display_title}"

    if final_link == "#" or final_link == "":
        btn_html = '<span style="color:#ccc; font-size:11px;">N/A</span>'
    else:
        btn_html = f'''
        <a href="{final_link}" class="unb-dl-btn" target="_blank" rel="nofollow" title="{tooltip_text}">
            PDF Download
            <svg class="unb-svg-icon"><use href="#unb-arrow-icon"></use></svg>
        </a>'''

    html_content += f"""
        <li class="unb-list-row">
            <span class="unb-num-badge">{index + 1}.</span>
            <h3 class="unb-novel-heading">{display_title}</h3>
            {btn_html}
        </li>"""

html_content += """</ul>"""

# Adding Custom Middle Link & Footer
html_content += middle_link_html
html_content += footer_html

html_content += """</div>"""

# Save output
output_txt_path = fr"C:\Users\PCS\Downloads\\output_{writer_raw.replace(' ', '_')}_post.txt"

try:
    with open(output_txt_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✅ Full Post Generated for: {WRITER_NAME}")
    print(f"📂 Saved to: {output_txt_path}")
    print("👉 Features: Direct Google Drive links converted to Sharing links.")
except Exception as e:
    print(f"Error writing TXT file: {e}")









# import pandas as pd
# import re
# import os

# # -----------------------------------------------------------
# # 1. INPUT FILE SETTINGS
# # -----------------------------------------------------------
# # Apni file ka path yahan dein. 
# excel_input_path = r"D:\unb-workstation\writers\Alia bukhari.xlsx"

# # --- AUTOMATIC WRITER NAME DETECTION ---
# file_name = os.path.basename(excel_input_path) 
# writer_raw = os.path.splitext(file_name)[0]      
# WRITER_NAME = writer_raw.title()                 

# print(f"🔹 Detected Writer: {WRITER_NAME}")

# # Load Excel
# try:
#     df = pd.read_excel(excel_input_path)
# except FileNotFoundError:
#     raise FileNotFoundError(f"Excel file not found at: {excel_input_path}")

# df = df.rename(columns={'Name': 'Titles', 'URL': 'Links'})

# def quick_clean(text):
#     if pd.isna(text): return "Untitled"
#     text = str(text)
#     text = re.sub(r'(?i)download', '', text)
#     text = re.sub(r'(?i)pdf', '', text)
#     text = re.sub(r'(?i)file', '', text)
#     text = re.sub(r'(?i)complete', '', text)
#     text = re.sub(r'(?i)urdu novel', '', text)
#     return " ".join(text.split())

# # -----------------------------------------------------------
# # 2. DYNAMIC INTRO PARAGRAPH
# # -----------------------------------------------------------
# intro_html = f"""
# <div class="unb-intro-section">
#     <p><strong><span style="font-family: inherit;"><br /></span></strong></p>
#     <h2 style="text-align: center;"><strong><span style="font-family: inherit;">{WRITER_NAME}'s Novels Collection</span></strong></h2>
#     <p><span><span style="font-family: inherit;">Explore the rich world of <b>Urdu literature </b>with our<b> carefully curated</b> collection of <b>{WRITER_NAME}’s best novels.</b></span></span></p>
#     <p><span style="font-family: inherit;"><b><br /></b>{WRITER_NAME} is widely admired for their captivating writing style, emotionally powerful characters, and deeply engaging storylines that leave a lasting impact on readers.</span></p>
#     <p><span style="font-family: inherit;"><br /></span></p>
#     <p><span style="font-family: inherit;">On this page, you can easily <strong>find and download PDF versions of {WRITER_NAME}’s most popular </strong><span>and</span><strong> top-rated Urdu novels</strong>. Each download link is carefully checked and regularly updated to ensure a <strong>smooth, safe, and hassle-free reading experience</strong>.</span></p>
#     <p><span style="font-family: inherit;"><br /></span></p>
#     <p><span style="font-family: inherit;">Whether you are a long-time fan or discovering the author's work for the first time, this collection offers a complete gateway to enjoy <strong>high-quality Urdu novels online</strong> — anytime, anywhere.</span></p>
# </div>
# """

# # -----------------------------------------------------------
# # 3. USER SPECIFIC LINK HTML (Added Here)
# # -----------------------------------------------------------
# # Ye wo code hai jo apne diya tha
# middle_link_html = """
# <div dir="rtl" style="text-align: right;"><br /></div><div dir="rtl" style="text-align: right;"><br /></div><div dir="rtl" style="text-align: center;"><a href="https://www.urdunovelbanks.com/2025/12/all-urdu-novel-writers-list-complete.html" target="_blank"><b><span style="font-size: medium;">👈</span></b></a><a href="https://www.urdunovelbanks.com/2025/12/all-urdu-novel-writers-list-complete.html" target="_blank"><b><span style="font-size: medium;">دیگرمصنفین کی ناولز  لسٹ دیکھیں&nbsp;</span></b></a></div>
# """

# # -----------------------------------------------------------
# # 4. FOOTER SECTION (Urdu Note + Report Button)
# # -----------------------------------------------------------
# footer_html = """
# <div class="unb-footer-section">
#     <div dir="rtl" style="text-align: right; margin-top: 40px; background: #fdfdfd; padding: 20px; border-radius: 8px; border: 1px solid #eee;">
#         <div style="text-align: center;">
#             <b><span style="font-size: large; color: #dc3545;">نوٹ :</span></b>
#         </div>
#         <div style="text-align: center; margin-top: 10px;">
#             <span style="font-size: medium; line-height: 1.8;">اگر کسی ناول کا ڈاؤن لوڈ لنک کام نہ کرے تو براہِ کرم نیچے دیے گئے فارم کے ذریعے ہمیں اطلاع دیں، تاکہ ہم جلد از جلد اسے درست کر سکیں۔ آپ کے تعاون کا شکریہ۔</span>
#         </div>
#     </div>

#     <div style="text-align: center; margin-top: 25px; margin-bottom: 20px;">
#         <a href="https://forms.gle/K3spbeeu6c7QM61u9" target="_blank" class="unb-report-btn">
#             Report Dead Link ⚠️
#         </a>
#     </div>
# </div>
# """

# # -----------------------------------------------------------
# # 5. CSS STYLING
# # -----------------------------------------------------------
# html_content = """
# <style>
#     /* Intro Section */
#     .unb-intro-section { margin-bottom: 30px; font-family: inherit; line-height: 1.6; color: #333; }

#     /* Wrapper */
#     .unb-main-wrapper { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; max-width: 100%; margin: 0 auto; padding: 10px; box-sizing: border-box; }

#     /* List Styles */
#     .unb-ul-list { list-style: none !important; padding: 0 !important; margin: 0 !important; }
#     .unb-list-row { background-color: #fff; border-bottom: 1px solid #eee; padding: 12px 5px; display: flex; align-items: center; gap: 12px; line-height: normal; }
#     .unb-list-row:last-child { border-bottom: none; }

#     /* Elements */
#     .unb-num-badge { font-size: 14px; font-weight: bold; color: #999; min-width: 25px; }
#     h3.unb-novel-heading { flex-grow: 1; font-size: 14px !important; color: #333 !important; font-weight: 600 !important; margin: 0 !important; padding: 0 !important; line-height: 1.4 !important; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; border: none; }
    
#     /* Download Button (Blue) */
#     a.unb-dl-btn { background-color: #007bff !important; color: white !important; padding: 6px 10px !important; border-radius: 4px !important; font-size: 12px !important; font-weight: bold !important; text-decoration: none !important; border: none !important; display: inline-flex; align-items: center; gap: 5px; transition: background-color 0.2s ease; white-space: nowrap; height: auto !important; }
#     a.unb-dl-btn:hover { background-color: #0056b3 !important; }
    
#     /* Report Button (Red) */
#     a.unb-report-btn { background-color: #dc3545 !important; color: white !important; padding: 10px 20px !important; border-radius: 50px !important; font-size: 14px !important; font-weight: bold !important; text-decoration: none !important; border: none !important; display: inline-block; box-shadow: 0 4px 6px rgba(220, 53, 69, 0.2); transition: transform 0.2s; }
#     a.unb-report-btn:hover { background-color: #c82333 !important; transform: translateY(-2px); }

#     /* Icon */
#     .unb-svg-icon { width: 12px; height: 12px; fill: currentColor; pointer-events: none; }
# </style>

# <svg style="display: none;">
#     <symbol id="unb-arrow-icon" viewBox="0 0 24 24">
#         <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
#     </symbol>
# </svg>

# <div class="unb-main-wrapper">
# """

# html_content += intro_html
# html_content += """<ul class="unb-ul-list">"""

# # --- GENERATING ITEMS ---

# for index, row in df.iterrows():
#     raw_title = str(row['Titles'])
#     link = str(row['Links']).strip() if pd.notna(row['Links']) else "#"
    
#     display_title = quick_clean(raw_title).title()
#     tooltip_text = f"Download {display_title}"

#     if link == "#" or link == "":
#         btn_html = '<span style="color:#ccc; font-size:11px;">N/A</span>'
#     else:
#         btn_html = f'''
#         <a href="{link}" class="unb-dl-btn" target="_blank" rel="nofollow" title="{tooltip_text}">
#             PDF 
#             <svg class="unb-svg-icon"><use href="#unb-arrow-icon"></use></svg>
#         </a>'''

#     html_content += f"""
#         <li class="unb-list-row">
#             <span class="unb-num-badge">{index + 1}.</span>
#             <h3 class="unb-novel-heading">{display_title}</h3>
#             {btn_html}
#         </li>"""

# html_content += """</ul>"""

# # -----------------------------------------------------------
# # ADDING YOUR CUSTOM HTML & FOOTER
# # -----------------------------------------------------------
# html_content += middle_link_html  # List ke foran baad apka code
# html_content += footer_html       # Uske baad footer note

# html_content += """</div>"""

# # Save output
# output_txt_path = fr"C:\Users\PCS\Downloads\\output_{writer_raw.replace(' ', '_')}_post.txt"

# try:
#     with open(output_txt_path, 'w', encoding='utf-8') as f:
#         f.write(html_content)
#     print(f"✅ Full Post Generated for: {WRITER_NAME}")
#     print(f"📂 Saved to: {output_txt_path}")
#     print("👉 Includes: List + Custom Writers Link + Report Button.")
# except Exception as e:
#     print(f"Error writing TXT file: {e}")




#below code all final saima akram already uploaded 

# import pandas as pd
# import re
# import os

# # -----------------------------------------------------------
# # 1. INPUT FILE SETTINGS
# # -----------------------------------------------------------
# # Apni file ka path yahan dein. 
# excel_input_path = r"C:\Users\PCS\Downloads\Saima Akram chaudhary.xlsx"

# # --- AUTOMATIC WRITER NAME DETECTION ---
# file_name = os.path.basename(excel_input_path) 
# writer_raw = os.path.splitext(file_name)[0]      
# WRITER_NAME = writer_raw.title()                 

# print(f"🔹 Detected Writer: {WRITER_NAME}")

# # Load Excel
# try:
#     df = pd.read_excel(excel_input_path)
# except FileNotFoundError:
#     raise FileNotFoundError(f"Excel file not found at: {excel_input_path}")

# df = df.rename(columns={'Name': 'Titles', 'URL': 'Links'})

# def quick_clean(text):
#     if pd.isna(text): return "Untitled"
#     text = str(text)
#     text = re.sub(r'(?i)download', '', text)
#     text = re.sub(r'(?i)pdf', '', text)
#     text = re.sub(r'(?i)file', '', text)
#     text = re.sub(r'(?i)complete', '', text)
#     text = re.sub(r'(?i)urdu novel', '', text)
#     return " ".join(text.split())

# # -----------------------------------------------------------
# # 2. DYNAMIC INTRO PARAGRAPH
# # -----------------------------------------------------------
# intro_html = f"""
# <div class="unb-intro-section">
#     <p><strong><span style="font-family: inherit;"><br /></span></strong></p>
#     <h2 style="text-align: center;"><strong><span style="font-family: inherit;">{WRITER_NAME}'s Novels Collection</span></strong></h2>
#     <p><span><span style="font-family: inherit;">Explore the rich world of <b>Urdu literature </b>with our<b> carefully curated</b> collection of <b>{WRITER_NAME}’s best novels.</b></span></span></p>
#     <p><span style="font-family: inherit;"><b><br /></b>{WRITER_NAME} is widely admired for their captivating writing style, emotionally powerful characters, and deeply engaging storylines that leave a lasting impact on readers.</span></p>
#     <p><span style="font-family: inherit;"><br /></span></p>
#     <p><span style="font-family: inherit;">On this page, you can easily <strong>find and download PDF versions of {WRITER_NAME}’s most popular </strong><span>and</span><strong> top-rated Urdu novels</strong>. Each download link is carefully checked and regularly updated to ensure a <strong>smooth, safe, and hassle-free reading experience</strong>.</span></p>
#     <p><span style="font-family: inherit;"><br /></span></p>
#     <p><span style="font-family: inherit;">Whether you are a long-time fan or discovering the author's work for the first time, this collection offers a complete gateway to enjoy <strong>high-quality Urdu novels online</strong> — anytime, anywhere.</span></p>
# </div>
# """

# # -----------------------------------------------------------
# # 3. FOOTER SECTION (Urdu Note + Report Button)
# # -----------------------------------------------------------
# footer_html = """
# <div class="unb-footer-section">
#     <div dir="rtl" style="text-align: right; margin-top: 40px; background: #fdfdfd; padding: 20px; border-radius: 8px; border: 1px solid #eee;">
#         <div style="text-align: center;">
#             <b><span style="font-size: large; color: #dc3545;">نوٹ :</span></b>
#         </div>
#         <div style="text-align: center; margin-top: 10px;">
#             <span style="font-size: medium; line-height: 1.8;">اگر کسی ناول کا ڈاؤن لوڈ لنک کام نہ کرے تو براہِ کرم نیچے دیے گئے فارم کے ذریعے ہمیں اطلاع دیں، تاکہ ہم جلد از جلد اسے درست کر سکیں۔ آپ کے تعاون کا شکریہ۔</span>
#         </div>
#     </div>

#     <div style="text-align: center; margin-top: 25px; margin-bottom: 20px;">
#         <a href="https://forms.gle/K3spbeeu6c7QM61u9" target="_blank" class="unb-report-btn">
#             Report Dead Link ⚠️
#         </a>
#     </div>
# </div>
# """

# # -----------------------------------------------------------
# # 4. CSS STYLING
# # -----------------------------------------------------------
# html_content = """
# <style>
#     /* Intro Section */
#     .unb-intro-section { margin-bottom: 30px; font-family: inherit; line-height: 1.6; color: #333; }

#     /* Wrapper */
#     .unb-main-wrapper { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; max-width: 100%; margin: 0 auto; padding: 10px; box-sizing: border-box; }

#     /* List Styles */
#     .unb-ul-list { list-style: none !important; padding: 0 !important; margin: 0 !important; }
#     .unb-list-row { background-color: #fff; border-bottom: 1px solid #eee; padding: 12px 5px; display: flex; align-items: center; gap: 12px; line-height: normal; }
#     .unb-list-row:last-child { border-bottom: none; }

#     /* Elements */
#     .unb-num-badge { font-size: 14px; font-weight: bold; color: #999; min-width: 25px; }
#     h3.unb-novel-heading { flex-grow: 1; font-size: 14px !important; color: #333 !important; font-weight: 600 !important; margin: 0 !important; padding: 0 !important; line-height: 1.4 !important; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; border: none; }
    
#     /* Download Button (Blue) */
#     a.unb-dl-btn { background-color: #007bff !important; color: white !important; padding: 6px 10px !important; border-radius: 4px !important; font-size: 12px !important; font-weight: bold !important; text-decoration: none !important; border: none !important; display: inline-flex; align-items: center; gap: 5px; transition: background-color 0.2s ease; white-space: nowrap; height: auto !important; }
#     a.unb-dl-btn:hover { background-color: #0056b3 !important; }
    
#     /* Report Button (Red) */
#     a.unb-report-btn { background-color: #dc3545 !important; color: white !important; padding: 10px 20px !important; border-radius: 50px !important; font-size: 14px !important; font-weight: bold !important; text-decoration: none !important; border: none !important; display: inline-block; box-shadow: 0 4px 6px rgba(220, 53, 69, 0.2); transition: transform 0.2s; }
#     a.unb-report-btn:hover { background-color: #c82333 !important; transform: translateY(-2px); }

#     /* Icon */
#     .unb-svg-icon { width: 12px; height: 12px; fill: currentColor; pointer-events: none; }
# </style>

# <svg style="display: none;">
#     <symbol id="unb-arrow-icon" viewBox="0 0 24 24">
#         <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
#     </symbol>
# </svg>

# <div class="unb-main-wrapper">
# """

# html_content += intro_html
# html_content += """<ul class="unb-ul-list">"""

# # --- GENERATING ITEMS ---

# for index, row in df.iterrows():
#     raw_title = str(row['Titles'])
#     link = str(row['Links']).strip() if pd.notna(row['Links']) else "#"
    
#     display_title = quick_clean(raw_title).title()
#     tooltip_text = f"Download {display_title}"

#     if link == "#" or link == "":
#         btn_html = '<span style="color:#ccc; font-size:11px;">N/A</span>'
#     else:
#         btn_html = f'''
#         <a href="{link}" class="unb-dl-btn" target="_blank" rel="nofollow" title="{tooltip_text}">
#             PDF 
#             <svg class="unb-svg-icon"><use href="#unb-arrow-icon"></use></svg>
#         </a>'''

#     html_content += f"""
#         <li class="unb-list-row">
#             <span class="unb-num-badge">{index + 1}.</span>
#             <h3 class="unb-novel-heading">{display_title}</h3>
#             {btn_html}
#         </li>"""

# html_content += """</ul>"""

# # ADDING FOOTER
# html_content += footer_html

# html_content += """</div>"""

# # Save output
# output_txt_path = fr"C:\Users\PCS\Downloads\\output_{writer_raw.replace(' ', '_')}_post.txt"

# try:
#     with open(output_txt_path, 'w', encoding='utf-8') as f:
#         f.write(html_content)
#     print(f"✅ Full Post Generated for: {WRITER_NAME}")
#     print(f"📂 Saved to: {output_txt_path}")
#     print("👉 Includes: Intro Paragraph + List + Urdu Note + Report Button.")
# except Exception as e:
#     print(f"Error writing TXT file: {e}")









#pro working code for post use highly

# import pandas as pd
# import re
# import os # Path se naam nikalne ke liye

# # -----------------------------------------------------------
# # 1. INPUT FILE SETTINGS
# # -----------------------------------------------------------
# # Apni file ka path yahan dein. 
# # NOTE: File ka naam wahi rakhen jo Writer ka naam hai (e.g., "Umera Ahmed.xlsx")
# excel_input_path = r"D:\unb-workstation\writers\bushra saeed.xlsx" 

# # --- AUTOMATIC WRITER NAME DETECTION ---
# # Ye code file ke naam se writer ka naam nikal le ga
# file_name = os.path.basename(excel_input_path) # "nimra ahmed.xlsx"
# writer_raw = os.path.splitext(file_name)[0]      # "nimra ahmed"
# WRITER_NAME = writer_raw.title()                 # "Nimra Ahmed" (Ye variable HTML ma use hoga)

# print(f"🔹 Detected Writer: {WRITER_NAME}") # Console ma confirm kray ga

# # Load Excel
# try:
#     df = pd.read_excel(excel_input_path)
# except FileNotFoundError:
#     raise FileNotFoundError(f"Excel file not found at: {excel_input_path}")

# # Rename columns
# df = df.rename(columns={'Name': 'Titles', 'URL': 'Links'})

# def quick_clean(text):
#     if pd.isna(text): return "Untitled"
#     text = str(text)
#     text = re.sub(r'(?i)download', '', text)
#     text = re.sub(r'(?i)pdf', '', text)
#     text = re.sub(r'(?i)file', '', text)
#     text = re.sub(r'(?i)complete', '', text)
#     text = re.sub(r'(?i)urdu novel', '', text)
#     return " ".join(text.split())

# # -----------------------------------------------------------
# # 2. DYNAMIC INTRO PARAGRAPH
# # -----------------------------------------------------------
# # Maine 'Deeba Tabassum' ki jagah {WRITER_NAME} laga diya hai.
# # Ab jo bhi file hogi, uska naam yahan aa jayega.

# intro_html = f"""
# <div class="unb-intro-section">
#     <p><strong><span style="font-family: inherit;"><br /></span></strong></p>
#     <h2 style="text-align: center;"><strong><span style="font-family: inherit;">{WRITER_NAME}'s Novels Collection</span></strong></h2>
#     <p><span><span style="font-family: inherit;">Explore the rich world of <b>Urdu literature </b>with our<b> carefully curated</b> collection of <b>{WRITER_NAME}’s best novels.</b></span></span></p>
#     <p><span style="font-family: inherit;"><b><br /></b>{WRITER_NAME} is widely admired for their captivating writing style, emotionally powerful characters, and deeply engaging storylines that leave a lasting impact on readers.</span></p>
#     <p><span style="font-family: inherit;"><br /></span></p>
#     <p><span style="font-family: inherit;">On this page, you can easily <strong>find and download PDF versions of {WRITER_NAME}’s most popular </strong><span>and</span><strong> top-rated Urdu novels</strong>. Each download link is carefully checked and regularly updated to ensure a <strong>smooth, safe, and hassle-free reading experience</strong>.</span></p>
#     <p><span style="font-family: inherit;"><br /></span></p>
#     <p><span style="font-family: inherit;">Whether you are a long-time fan or discovering the author's work for the first time, this collection offers a complete gateway to enjoy <strong>high-quality Urdu novels online</strong> — anytime, anywhere.</span></p>
# </div>
# """

# # -----------------------------------------------------------
# # 3. CSS STYLING
# # -----------------------------------------------------------
# html_content = """
# <style>
#     /* Intro Section */
#     .unb-intro-section {
#         margin-bottom: 30px;
#         font-family: inherit;
#         line-height: 1.6;
#         color: #333;
#     }

#     /* List Wrapper */
#     .unb-main-wrapper {
#         font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
#         max-width: 100%;
#         margin: 0 auto;
#         padding: 10px;
#         box-sizing: border-box;
#     }

#     .unb-ul-list {
#         list-style: none !important;
#         padding: 0 !important;
#         margin: 0 !important;
#     }

#     /* List Row */
#     .unb-list-row {
#         background-color: #fff;
#         border-bottom: 1px solid #eee;
#         padding: 12px 5px;
#         display: flex;
#         align-items: center;
#         gap: 12px;
#         line-height: normal;
#     }
    
#     .unb-list-row:last-child {
#         border-bottom: none;
#     }

#     /* Numbering */
#     .unb-num-badge {
#         font-size: 14px;
#         font-weight: bold;
#         color: #999;
#         min-width: 25px;
#     }

#     /* Heading */
#     h3.unb-novel-heading {
#         flex-grow: 1;
#         font-size: 14px !important;
#         color: #333 !important;
#         font-weight: 600 !important;
#         margin: 0 !important;
#         padding: 0 !important;
#         line-height: 1.4 !important;
#         display: -webkit-box;
#         -webkit-line-clamp: 2;
#         -webkit-box-orient: vertical;
#         overflow: hidden;
#         border: none;
#     }

#     /* Button */
#     a.unb-dl-btn {
#         background-color: #007bff !important;
#         color: white !important;
#         padding: 6px 10px !important;
#         border-radius: 4px !important;
#         font-size: 12px !important;
#         font-weight: bold !important;
#         text-decoration: none !important;
#         border: none !important;
#         display: inline-flex;
#         align-items: center;
#         gap: 5px;
#         transition: background-color 0.2s ease;
#         white-space: nowrap;
#         height: auto !important;
#     }

#     a.unb-dl-btn:hover {
#         background-color: #0056b3 !important;
#     }
    
#     /* Icon */
#     .unb-svg-icon {
#         width: 12px;
#         height: 12px;
#         fill: currentColor;
#         pointer-events: none;
#     }
# </style>

# <svg style="display: none;">
#     <symbol id="unb-arrow-icon" viewBox="0 0 24 24">
#         <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
#     </symbol>
# </svg>

# <div class="unb-main-wrapper">
# """

# html_content += intro_html

# html_content += """
#     <ul class="unb-ul-list">
# """

# # --- GENERATING ITEMS ---

# for index, row in df.iterrows():
#     raw_title = str(row['Titles'])
#     link = str(row['Links']).strip() if pd.notna(row['Links']) else "#"
    
#     display_title = quick_clean(raw_title).title()
#     tooltip_text = f"Download {display_title}"

#     if link == "#" or link == "":
#         btn_html = '<span style="color:#ccc; font-size:11px;">N/A</span>'
#     else:
#         btn_html = f'''
#         <a href="{link}" class="unb-dl-btn" target="_blank" rel="nofollow" title="{tooltip_text}">
#             PDF 
#             <svg class="unb-svg-icon"><use href="#unb-arrow-icon"></use></svg>
#         </a>'''

#     html_content += f"""
#         <li class="unb-list-row">
#             <span class="unb-num-badge">{index + 1}.</span>
#             <h3 class="unb-novel-heading">{display_title}</h3>
#             {btn_html}
#         </li>"""

# html_content += """
#     </ul>
# </div>
# """

# # Save output
# # Output file ka naam bhi dynamic kar diya hai taake overwrite na ho
# output_txt_path = fr"D:\unb-workstation\output_{writer_raw.replace(' ', '_')}_post.txt"

# try:
#     with open(output_txt_path, 'w', encoding='utf-8') as f:
#         f.write(html_content)
#     print(f"✅ HTML Generated for: {WRITER_NAME}")
#     print(f"📂 Saved to: {output_txt_path}")
# except Exception as e:
#     print(f"Error writing TXT file: {e}")





#excellent use this code 


# import pandas as pd
# import re

# # 1. Load Excel File
# excel_input_path = r"D:\unb-workstation\writers\bushra saeed.xlsx"

# try:
#     df = pd.read_excel(excel_input_path)
# except FileNotFoundError:
#     raise FileNotFoundError(f"Excel file not found at: {excel_input_path}")

# # Rename columns
# df = df.rename(columns={'Name': 'Titles', 'URL': 'Links'})

# def quick_clean(text):
#     if pd.isna(text): return "Untitled"
#     text = str(text)
#     text = re.sub(r'(?i)download', '', text)
#     text = re.sub(r'(?i)pdf', '', text)
#     text = re.sub(r'(?i)file', '', text)
#     text = re.sub(r'(?i)complete', '', text)
#     text = re.sub(r'(?i)urdu novel', '', text)
#     return " ".join(text.split())

# # --- CLEANED INTRO PARAGRAPH (Data Attributes Removed) ---
# intro_html = """
# <div class="unb-intro-section">
#     <p><strong><span style="font-family: inherit;"><br /></span></strong></p>
#     <h2 style="text-align: center;"><strong><span style="font-family: inherit;">Deeba Tabassum's Novels Collection</span></strong></h2>
#     <p><span><span style="font-family: inherit;">Explore the rich world of <b>Urdu literature </b>with our<b> carefully curated</b> collection of <b>Deeba Tabassum’s best novels.</b></span></span></p>
#     <p><span style="font-family: inherit;"><b><br /></b>Deeba Tabassum is widely admired for her captivating writing style, emotionally powerful characters, and deeply engaging storylines that leave a lasting impact on readers.</span></p>
#     <p><span style="font-family: inherit;"><br /></span></p>
#     <p><span style="font-family: inherit;">On this page, you can easily <strong>find and download PDF versions of Deeba Tabassum’s most popular </strong><span>and</span><strong> top-rated Urdu novels</strong>. Each download link is carefully checked and regularly updated to ensure a <strong>smooth, safe, and hassle-free reading experience</strong>.</span></p>
#     <p><span style="font-family: inherit;"><br /></span></p>
#     <p><span style="font-family: inherit;">Whether you are a long-time fan or discovering her work for the first time, this collection offers a complete gateway to enjoy <strong>high-quality Urdu novels online</strong> — anytime, anywhere.</span></p>
# </div>
# """

# # --- CSS STYLING ---
# html_content = """
# <style>
#     /* Intro Section */
#     .unb-intro-section {
#         margin-bottom: 30px;
#         font-family: inherit;
#         line-height: 1.6;
#         color: #333;
#     }

#     /* List Wrapper */
#     .unb-main-wrapper {
#         font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
#         max-width: 100%;
#         margin: 0 auto;
#         padding: 10px;
#         box-sizing: border-box;
#     }

#     .unb-ul-list {
#         list-style: none !important;
#         padding: 0 !important;
#         margin: 0 !important;
#     }

#     /* List Row */
#     .unb-list-row {
#         background-color: #fff;
#         border-bottom: 1px solid #eee;
#         padding: 12px 5px;
#         display: flex;
#         align-items: center;
#         gap: 12px;
#         line-height: normal;
#     }
    
#     .unb-list-row:last-child {
#         border-bottom: none;
#     }

#     /* Numbering */
#     .unb-num-badge {
#         font-size: 14px;
#         font-weight: bold;
#         color: #999;
#         min-width: 25px;
#     }

#     /* Heading */
#     h3.unb-novel-heading {
#         flex-grow: 1;
#         font-size: 14px !important;
#         color: #333 !important;
#         font-weight: 600 !important;
#         margin: 0 !important;
#         padding: 0 !important;
#         line-height: 1.4 !important;
#         display: -webkit-box;
#         -webkit-line-clamp: 2;
#         -webkit-box-orient: vertical;
#         overflow: hidden;
#         border: none;
#     }

#     /* Button */
#     a.unb-dl-btn {
#         background-color: #007bff !important;
#         color: white !important;
#         padding: 6px 10px !important;
#         border-radius: 4px !important;
#         font-size: 12px !important;
#         font-weight: bold !important;
#         text-decoration: none !important;
#         border: none !important;
#         display: inline-flex;
#         align-items: center;
#         gap: 5px;
#         transition: background-color 0.2s ease;
#         white-space: nowrap;
#         height: auto !important;
#     }

#     a.unb-dl-btn:hover {
#         background-color: #0056b3 !important;
#     }
    
#     /* Icon */
#     .unb-svg-icon {
#         width: 12px;
#         height: 12px;
#         fill: currentColor;
#         pointer-events: none;
#     }
# </style>

# <svg style="display: none;">
#     <symbol id="unb-arrow-icon" viewBox="0 0 24 24">
#         <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
#     </symbol>
# </svg>

# <div class="unb-main-wrapper">
# """

# # ADDING THE INTRO HERE
# html_content += intro_html

# # STARTING THE LIST
# html_content += """
#     <ul class="unb-ul-list">
# """

# # --- GENERATING ITEMS ---

# for index, row in df.iterrows():
#     raw_title = str(row['Titles'])
#     link = str(row['Links']).strip() if pd.notna(row['Links']) else "#"
    
#     display_title = quick_clean(raw_title).title()
#     tooltip_text = f"Download {display_title}"

#     if link == "#" or link == "":
#         btn_html = '<span style="color:#ccc; font-size:11px;">N/A</span>'
#     else:
#         btn_html = f'''
#         <a href="{link}" class="unb-dl-btn" target="_blank" rel="nofollow" title="{tooltip_text}">
#             PDF 
#             <svg class="unb-svg-icon"><use href="#unb-arrow-icon"></use></svg>
#         </a>'''

#     html_content += f"""
#         <li class="unb-list-row">
#             <span class="unb-num-badge">{index + 1}.</span>
#             <h3 class="unb-novel-heading">{display_title}</h3>
#             {btn_html}
#         </li>"""

# html_content += """
#     </ul>
# </div>
# """

# # Save output
# output_txt_path = r"D:\unb-workstation\blogger_clean_intro.txt"
# try:
#     with open(output_txt_path, 'w', encoding='utf-8') as f:
#         f.write(html_content)
#     print(f"✅ HTML saved to: {output_txt_path}")
#     print("👉 'data-start' and 'data-end' attributes removed from the intro paragraph.")
# except Exception as e:
#     print(f"Error writing TXT file: {e}")





#OK use the blow one 
# import pandas as pd
# import re

# # 1. Load Excel File
# excel_input_path = r"D:\unb-workstation\writers\deeba tabassum.xlsx" 

# try:
#     df = pd.read_excel(excel_input_path)
# except FileNotFoundError:
#     raise FileNotFoundError(f"Excel file not found at: {excel_input_path}")

# # Rename columns
# df = df.rename(columns={'Name': 'Titles', 'URL': 'Links'})

# def quick_clean(text):
#     if pd.isna(text): return "Untitled"
#     text = str(text)
#     # Cleaning Logic
#     text = re.sub(r'(?i)download', '', text)
#     text = re.sub(r'(?i)pdf', '', text)
#     text = re.sub(r'(?i)file', '', text)
#     text = re.sub(r'(?i)complete', '', text)
#     text = re.sub(r'(?i)urdu novel', '', text)
#     return " ".join(text.split())

# # --- CSS STYLING (Scoped & Unique Names) ---
# html_content = """
# <style>
#     /* PREFIX: "unb-" (Urdu Novel Bank)
#        Yeh unique names hain jo Blogger ki apni CSS se takrayenge nahi.
#     */

#     /* Wrapper */
#     .unb-main-wrapper {
#         font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
#         max-width: 100%;
#         margin: 0 auto;
#         padding: 10px;
#         box-sizing: border-box;
#     }

#     .unb-ul-list {
#         list-style: none !important; /* Force remove bullets */
#         padding: 0 !important;
#         margin: 0 !important;
#     }

#     /* Single Row Card */
#     .unb-list-row {
#         background-color: #fff;
#         border-bottom: 1px solid #eee;
#         padding: 12px 5px;
#         display: flex;
#         align-items: center;
#         gap: 12px;
#         line-height: normal; /* Reset line height */
#     }
    
#     .unb-list-row:last-child {
#         border-bottom: none;
#     }

#     /* Numbering Badge */
#     .unb-num-badge {
#         font-size: 14px;
#         font-weight: bold;
#         color: #999;
#         min-width: 25px;
#     }

#     /* Title Heading */
#     h3.unb-novel-heading {
#         flex-grow: 1;
#         font-size: 14px !important; /* Force size */
#         color: #333 !important;
#         font-weight: 600 !important;
#         margin: 0 !important;
#         padding: 0 !important;
#         line-height: 1.4 !important;
        
#         /* 2 Lines CSS */
#         display: -webkit-box;
#         -webkit-line-clamp: 2;
#         -webkit-box-orient: vertical;
#         overflow: hidden;
#         border: none; /* Remove any theme borders */
#     }

#     /* Custom Button */
#     a.unb-dl-btn {
#         background-color: #007bff !important;
#         color: white !important;
#         padding: 6px 10px !important;
#         border-radius: 4px !important;
#         font-size: 12px !important;
#         font-weight: bold !important;
#         text-decoration: none !important;
#         border: none !important;
#         box-shadow: none !important;
        
#         display: inline-flex;
#         align-items: center;
#         gap: 5px;
#         transition: background-color 0.2s ease;
#         white-space: nowrap;
#         height: auto !important;
#     }

#     a.unb-dl-btn:hover {
#         background-color: #0056b3 !important;
#         color: white !important;
#     }
    
#     /* Icon Sizing */
#     .unb-svg-icon {
#         width: 12px;
#         height: 12px;
#         fill: currentColor;
#         pointer-events: none;
#     }
# </style>

# <svg style="display: none;">
#     <symbol id="unb-arrow-icon" viewBox="0 0 24 24">
#         <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
#     </symbol>
# </svg>

# <div class="unb-main-wrapper">
#     <ul class="unb-ul-list">
# """

# # --- GENERATING ITEMS ---

# for index, row in df.iterrows():
#     raw_title = str(row['Titles'])
#     link = str(row['Links']).strip() if pd.notna(row['Links']) else "#"
    
#     display_title = quick_clean(raw_title).title()
#     tooltip_text = f"Download {display_title}"

#     if link == "#" or link == "":
#         btn_html = '<span style="color:#ccc; font-size:11px;">N/A</span>'
#     else:
#         # Note: SVG uses unique ID 'unb-arrow-icon'
#         btn_html = f'''
#         <a href="{link}" class="unb-dl-btn" target="_blank" rel="nofollow" title="{tooltip_text}">
#             PDF 
#             <svg class="unb-svg-icon"><use href="#unb-arrow-icon"></use></svg>
#         </a>'''

#     html_content += f"""
#         <li class="unb-list-row">
#             <span class="unb-num-badge">{index + 1}.</span>
#             <h3 class="unb-novel-heading">{display_title}</h3>
#             {btn_html}
#         </li>"""

# html_content += """
#     </ul>
# </div>
# """

# # Save output
# output_txt_path = r"D:\unb-workstation\blogger_conflict_free.txt"
# try:
#     with open(output_txt_path, 'w', encoding='utf-8') as f:
#         f.write(html_content)
#     print(f"✅ Conflict-Free Code saved to: {output_txt_path}")
#     print("👉 All classes now start with 'unb-' (e.g., .unb-dl-btn). No conflicts with Blogger themes.")
# except Exception as e:
#     print(f"Error writing TXT file: {e}")







# import pandas as pd
# import re

# # 1. Load Excel File
# excel_input_path = r"D:\unb-workstation\writers\deeba tabassum.xlsx" 

# try:
#     df = pd.read_excel(excel_input_path)
# except FileNotFoundError:
#     raise FileNotFoundError(f"Excel file not found at: {excel_input_path}")

# # Rename columns
# df = df.rename(columns={'Name': 'Titles', 'URL': 'Links'})

# def quick_clean(text):
#     if pd.isna(text): return "Untitled"
#     text = str(text)
#     text = re.sub(r'(?i)download', '', text)
#     text = re.sub(r'(?i)pdf', '', text)
#     text = re.sub(r'(?i)file', '', text)
#     text = re.sub(r'(?i)complete', '', text)
#     text = re.sub(r'(?i)urdu novel', '', text)
#     return " ".join(text.split())

# # --- CSS STYLING ---
# html_content = """
# <style>
#     .novel-list-container {
#         font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
#         max-width: 100%;
#         margin: 0 auto;
#         padding: 10px;
#     }

#     ul.novel-list {
#         list-style: none;
#         padding: 0;
#         margin: 0;
#     }

#     li.novel-item {
#         background-color: #fff;
#         border-bottom: 1px solid #eee;
#         padding: 12px 5px;
#         display: flex;
#         align-items: center;
#         gap: 12px;
#     }
    
#     li.novel-item:last-child {
#         border-bottom: none;
#     }

#     .novel-number {
#         font-size: 14px;
#         font-weight: bold;
#         color: #999;
#         min-width: 25px;
#     }

#     h3.novel-title {
#         flex-grow: 1;
#         font-size: 14px;
#         color: #333;
#         font-weight: 600;
#         margin: 0;
#         line-height: 1.4;
#         display: -webkit-box;
#         -webkit-line-clamp: 2;
#         -webkit-box-orient: vertical;
#         overflow: hidden;
#     }

#     .download-btn {
#         background-color: #007bff;
#         color: white !important;
#         padding: 6px 10px;
#         border-radius: 4px;
#         font-size: 12px;
#         font-weight: bold;
#         text-decoration: none !important;
#         display: inline-flex;
#         align-items: center;
#         gap: 5px;
#         transition: background-color 0.2s;
#         white-space: nowrap;
#     }

#     .download-btn:hover {
#         background-color: #0056b3;
#     }
    
#     /* Icon Formatting */
#     .btn-icon {
#         width: 12px;
#         height: 12px;
#         fill: currentColor;
#     }
# </style>

# <svg style="display: none;">
#     <symbol id="icon-down" viewBox="0 0 24 24">
#         <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
#     </symbol>
# </svg>

# <div class="novel-list-container">
#     <ul class="novel-list">
# """

# # --- GENERATING ITEMS ---

# for index, row in df.iterrows():
#     raw_title = str(row['Titles'])
#     link = str(row['Links']).strip() if pd.notna(row['Links']) else "#"
    
#     display_title = quick_clean(raw_title).title()
#     tooltip_text = f"Download {display_title}"

#     if link == "#" or link == "":
#         btn_html = '<span style="color:#ccc; font-size:11px;">N/A</span>'
#     else:
#         # NOTICE: Ab yahan pura SVG nahi, sirf <use> tag hai.
#         # Yeh page size ko bohot kam rakhega.
#         btn_html = f'''
#         <a href="{link}" class="download-btn" target="_blank" rel="nofollow" title="{tooltip_text}">
#             PDF 
#             <svg class="btn-icon"><use href="#icon-down"></use></svg>
#         </a>'''

#     html_content += f"""
#         <li class="novel-item">
#             <span class="novel-number">{index + 1}.</span>
#             <h3 class="novel-title">{display_title}</h3>
#             {btn_html}
#         </li>"""

# html_content += """
#     </ul>
# </div>
# """

# # Save output
# output_txt_path = r"D:\unb-workstation\blogger_super_light.txt"
# try:
#     with open(output_txt_path, 'w', encoding='utf-8') as f:
#         f.write(html_content)
#     print(f"✅ Performance Optimized Code saved to: {output_txt_path}")
#     print("👉 Technique Used: 'SVG Symbols'. Icon code loaded ONCE, used everywhere.")
# except Exception as e:
#     print(f"Error writing TXT file: {e}")

# import pandas as pd
# import re

# # 1. Load Excel File
# excel_input_path = r"D:\unb-workstation\writers\deeba tabassum.xlsx" 

# try:
#     df = pd.read_excel(excel_input_path)
# except FileNotFoundError:
#     raise FileNotFoundError(f"Excel file not found at: {excel_input_path}")

# # Rename columns
# df = df.rename(columns={'Name': 'Titles', 'URL': 'Links'})

# # Function to clean title (removes junk words, keeps Writer Name)
# def quick_clean(text):
#     if pd.isna(text): return "Untitled"
#     text = str(text)
#     # Removing junk to keep title clean
#     text = re.sub(r'(?i)download', '', text)
#     text = re.sub(r'(?i)pdf', '', text)
#     text = re.sub(r'(?i)file', '', text)
#     text = re.sub(r'(?i)complete', '', text)
#     text = re.sub(r'(?i)urdu novel', '', text)
#     # Extra spaces remove
#     return " ".join(text.split())

# # --- CSS STYLING (Icon & Tooltip Added) ---
# html_content = """
# <style>
#     .novel-list-container {
#         font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
#         max-width: 100%;
#         margin: 0 auto;
#         padding: 10px;
#     }

#     ul.novel-list {
#         list-style: none;
#         padding: 0;
#         margin: 0;
#     }

#     /* Row Layout */
#     li.novel-item {
#         background-color: #fff;
#         border-bottom: 1px solid #eee;
#         padding: 12px 5px;
#         display: flex;
#         align-items: center; /* Vertically Center */
#         gap: 12px;
#     }
    
#     li.novel-item:last-child {
#         border-bottom: none;
#     }

#     /* 1. Numbering */
#     .novel-number {
#         font-size: 14px;
#         font-weight: bold;
#         color: #999;
#         min-width: 25px;
#     }

#     /* 2. Title (Center) */
#     h3.novel-title {
#         flex-grow: 1;
#         font-size: 14px;
#         color: #333;
#         font-weight: 600;
#         margin: 0;
#         line-height: 1.4;
        
#         /* Max 2 lines */
#         display: -webkit-box;
#         -webkit-line-clamp: 2;
#         -webkit-box-orient: vertical;
#         overflow: hidden;
#     }

#     /* 3. Button with Icon (Right) */
#     .download-btn {
#         background-color: #007bff;
#         color: white !important;
#         padding: 6px 10px;
#         border-radius: 4px;
#         font-size: 12px;
#         font-weight: bold;
#         text-decoration: none !important;
        
#         /* Flexbox for Icon Alignment */
#         display: inline-flex;
#         align-items: center;
#         gap: 5px; /* Space between Text and Icon */
        
#         transition: background-color 0.2s;
#         white-space: nowrap;
#     }

#     .download-btn:hover {
#         background-color: #0056b3;
#     }
    
#     /* SVG Icon Style */
#     .btn-icon {
#         width: 12px;
#         height: 12px;
#         fill: currentColor; /* Inherits white color */
#     }

# </style>

# <div class="novel-list-container">
#     <ul class="novel-list">
# """

# # SVG Icon Code (Simple Arrow)
# icon_svg = '<svg class="btn-icon" viewBox="0 0 24 24"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>'

# # --- GENERATING ITEMS ---

# for index, row in df.iterrows():
#     raw_title = str(row['Titles'])
#     link = str(row['Links']).strip() if pd.notna(row['Links']) else "#"
    
#     display_title = quick_clean(raw_title).title()

#     # Tooltip Logic: title="Download [Novel Name]"
#     tooltip_text = f"Download {display_title}"

#     # Button Logic
#     if link == "#" or link == "":
#         btn_html = '<span style="color:#ccc; font-size:11px;">N/A</span>'
#     else:
#         # Added 'title' attribute for tooltip and inserted icon_svg
#         btn_html = f'<a href="{link}" class="download-btn" target="_blank" rel="nofollow" title="{tooltip_text}">PDF {icon_svg}</a>'

#     html_content += f"""
#         <li class="novel-item">
#             <span class="novel-number">{index + 1}.</span>
#             <h3 class="novel-title">{display_title}</h3>
#             {btn_html}
#         </li>"""

# html_content += """
#     </ul>
# </div>
# """

# # Save output
# output_txt_path = r"D:\unb-workstation\blogger_final_v3.txt"
# try:
#     with open(output_txt_path, 'w', encoding='utf-8') as f:
#         f.write(html_content)
#     print(f"✅ Final Code saved to: {output_txt_path}")
#     print("👉 Features: Numbering + 2-Line Title + Compact Button with Icon + Hover Tooltip.")
# except Exception as e:
#     print(f"Error writing TXT file: {e}")










# import pandas as pd
# import re

# # 1. Load Excel File
# excel_input_path = r"D:\unb-workstation\writers\deeba tabassum.xlsx" 

# try:
#     df = pd.read_excel(excel_input_path)
# except FileNotFoundError:
#     raise FileNotFoundError(f"Excel file not found at: {excel_input_path}")

# # Rename columns
# df = df.rename(columns={'Name': 'Titles', 'URL': 'Links'})

# # Function to basic clean (Sirf spaces aur junk words hatane ke liye taake list gandi na lage)
# # Title ka structure "Name by Writer" wesa hi rahega.
# def quick_clean(text):
#     if pd.isna(text): return "Untitled"
#     text = str(text)
#     # Sirf "Download" aur "PDF" hataya hai taake mobile par title bohot lamba na ho
#     text = re.sub(r'(?i)download', '', text)
#     text = re.sub(r'(?i)pdf', '', text)
#     text = re.sub(r'(?i)file', '', text)
#     text = re.sub(r'(?i)complete', '', text)
#     # Extra spaces remove
#     return " ".join(text.split())

# # --- CSS STYLING (Numbered List Style) ---
# html_content = """
# <style>
#     .novel-list-container {
#         font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
#         max-width: 100%;
#         margin: 0 auto;
#         padding: 10px;
#     }

#     ul.novel-list {
#         list-style: none;
#         padding: 0;
#         margin: 0;
#     }

#     /* --- ITEM ROW LAYOUT --- */
#     li.novel-item {
#         background-color: #fff;
#         border-bottom: 1px solid #eee; /* Simple divider instead of box */
#         padding: 12px 5px;
#         display: flex;
#         align-items: center; /* Vertically Center */
#         gap: 10px;
#     }
    
#     /* Last item border remove */
#     li.novel-item:last-child {
#         border-bottom: none;
#     }

#     /* 1. NUMBER STYLE */
#     .novel-number {
#         font-size: 14px;
#         font-weight: bold;
#         color: #888;
#         min-width: 25px; /* Fixed width taake alignment out na ho */
#     }

#     /* 2. TITLE STYLE (Center) */
#     h3.novel-title {
#         flex-grow: 1; /* Baki sari jagah ye lega */
#         font-size: 14px;
#         color: #333;
#         font-weight: 600;
#         margin: 0;
#         line-height: 1.4;
        
#         /* Max 2 lines text */
#         display: -webkit-box;
#         -webkit-line-clamp: 2;
#         -webkit-box-orient: vertical;
#         overflow: hidden;
#     }

#     /* 3. BUTTON STYLE (Right) */
#     .download-btn {
#         background-color: #007bff;
#         color: white !important;
#         padding: 6px 12px;
#         border-radius: 4px; /* Thora square rakha hai */
#         font-size: 12px;
#         font-weight: bold;
#         text-decoration: none !important;
#         white-space: nowrap;
#         display: inline-block;
#     }

#     .download-btn:hover {
#         background-color: #0056b3;
#     }

# </style>

# <div class="novel-list-container">
#     <ul class="novel-list">
# """

# # --- GENERATING ITEMS ---

# for index, row in df.iterrows():
#     raw_title = str(row['Titles'])
#     link = str(row['Links']).strip() if pd.notna(row['Links']) else "#"
    
#     # Quick clean (Structure change nahi karega, bas junk words hatayega)
#     display_title = quick_clean(raw_title)
    
#     # Format: "Novel Name by Writer Name" (Proper Case)
#     display_title = display_title.title() 

#     # Button Logic
#     if link == "#" or link == "":
#         btn_html = '<span style="color:#ccc; font-size:11px;">N/A</span>'
#     else:
#         btn_html = f'<a href="{link}" class="download-btn" target="_blank" rel="nofollow">PDF</a>'

#     html_content += f"""
#         <li class="novel-item">
#             <span class="novel-number">{index + 1}.</span>
#             <h3 class="novel-title">{display_title}</h3>
#             {btn_html}
#         </li>"""

# html_content += """
#     </ul>
# </div>
# """

# # Save output
# output_txt_path = r"D:\unb-workstation\blogger_numbered_list.txt"
# try:
#     with open(output_txt_path, 'w', encoding='utf-8') as f:
#         f.write(html_content)
#     print(f"✅ Numbered List Code saved to: {output_txt_path}")
#     print("👉 Layout: [1.] [Novel Name by Writer] [PDF]")
# except Exception as e:
#     print(f"Error writing TXT file: {e}")











# import pandas as pd
# import re

# # 1. Load Excel File
# excel_input_path = r"D:\unb-workstation\writers\deeba tabassum.xlsx" 

# try:
#     df = pd.read_excel(excel_input_path)
# except FileNotFoundError:
#     raise FileNotFoundError(f"Excel file not found at: {excel_input_path}")

# # Rename columns
# df = df.rename(columns={'Name': 'Titles', 'URL': 'Links'})

# # Function to clean titles
# def clean_title_text(text):
#     if pd.isna(text): return "Untitled"
#     text = str(text)
#     # Remove junk words
#     text = re.sub(r'(?i)download', '', text)
#     text = re.sub(r'(?i)complete', '', text)
#     text = re.sub(r'(?i)pdf', '', text)
#     text = re.sub(r'(?i)file', '', text)
#     text = re.sub(r'(?i)urdu novel', '', text)
#     # Special character removal (brackets etc)
#     text = re.sub(r'[()\[\]]', '', text)
#     return " ".join(text.split())

# # --- CSS STYLING (Professional App-Like List) ---
# html_content = """
# <style>
#     /* Container Reset */
#     .novel-list-container {
#         font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
#         max-width: 100%;
#         margin: 0 auto;
#         padding: 10px;
#         background-color: #f8f9fa; /* Light background */
#     }

#     ul.novel-list {
#         list-style: none;
#         padding: 0;
#         margin: 0;
#     }

#     /* --- THE CARD (Row Layout) --- */
#     li.novel-item {
#         background-color: #ffffff;
#         border-radius: 12px; /* Smooth rounded corners */
#         padding: 12px 16px;
#         margin-bottom: 12px; /* Gap between cards */
#         box-shadow: 0 2px 8px rgba(0,0,0,0.06); /* Soft Shadow */
#         border: 1px solid #edf2f7;
        
#         /* FLEXBOX MAGIC: Text Left, Button Right */
#         display: flex;
#         align-items: center; 
#         justify-content: space-between;
#         gap: 15px; /* Space between text and button */
#         transition: transform 0.2s;
#     }

#     li.novel-item:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 5px 15px rgba(0,0,0,0.1);
#     }

#     /* --- LEFT SIDE: TEXT --- */
#     .text-content {
#         flex: 1; /* Takes all available space */
#         min-width: 0; /* Prevents text overflow issues */
#     }

#     h3.novel-title {
#         font-size: 15px;
#         color: #2d3748;
#         font-weight: 700;
#         margin: 0 0 4px 0;
#         line-height: 1.35;
        
#         /* 2 Lines Limit Logic */
#         display: -webkit-box;
#         -webkit-line-clamp: 2;
#         -webkit-box-orient: vertical;
#         overflow: hidden;
#         text-overflow: ellipsis;
#     }

#     .writer-tag {
#         font-size: 12px;
#         color: #718096;
#         display: block;
#         font-weight: 500;
#     }

#     /* --- RIGHT SIDE: BUTTON --- */
#     .download-btn {
#         background-color: #007bff; /* Bright Blue */
#         color: white !important;
#         padding: 8px 16px;
#         text-decoration: none !important;
#         border-radius: 50px; /* Pill Shape */
#         font-size: 12px;
#         font-weight: 600;
#         white-space: nowrap; /* Text won't break line */
#         box-shadow: 0 3px 6px rgba(0,123,255,0.3);
#         flex-shrink: 0; /* Button size fix rahega */
#         display: inline-flex;
#         align-items: center;
#         gap: 5px;
#     }

#     .download-btn:hover {
#         background-color: #0056b3;
#     }
    
#     /* SVG Icon inside button */
#     .download-btn svg {
#         width: 14px;
#         height: 14px;
#         fill: currentColor;
#     }

# </style>

# <div class="novel-list-container">
#     <ul class="novel-list">
# """

# # SVG Icon (Simple Down Arrow)
# icon_svg = '<svg viewBox="0 0 24 24"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>'

# # --- GENERATING ITEMS ---

# for index, row in df.iterrows():
#     raw_title = str(row['Titles'])
#     link = str(row['Links']).strip() if pd.notna(row['Links']) else "#"
    
#     clean_name = clean_title_text(raw_title)
    
#     # Writer separation logic
#     if " by " in clean_name.lower():
#         parts = re.split(r' by ', clean_name, flags=re.IGNORECASE, maxsplit=1)
#         novel_title = parts[0].strip()
#         writer_name = parts[1].strip()
#     else:
#         novel_title = clean_name
#         writer_name = "Deeba Tabassum"

#     # Button Logic
#     if link == "#" or link == "":
#         btn_html = '<span style="color:#cbd5e0; font-size:11px; font-weight:600;">Coming Soon</span>'
#     else:
#         # Button right side par hoga
#         btn_html = f'<a href="{link}" class="download-btn" target="_blank" rel="nofollow">PDF {icon_svg}</a>'

#     html_content += f"""
#         <li class="novel-item">
#             <div class="text-content">
#                 <h3 class="novel-title">{novel_title}</h3>
#                 <span class="writer-tag">{writer_name}</span>
#             </div>
#             {btn_html}
#         </li>"""

# html_content += """
#     </ul>
# </div>
# """

# # Save output
# output_txt_path = r"D:\unb-workstation\blogger_modern_ui.txt"
# try:
#     with open(output_txt_path, 'w', encoding='utf-8') as f:
#         f.write(html_content)
#     print(f"✅ Modern UI Code saved to: {output_txt_path}")
#     print("👉 Layout: [ Title+Writer (Left) ] ------ [ Small Button (Right) ]")
# except Exception as e:
#     print(f"Error writing TXT file: {e}")











# import pandas as pd
# import re

# # 1. Load Excel File
# # Path check kar lein
# excel_input_path = r"D:\unb-workstation\writers\deeba tabassum.xlsx" 

# try:
#     df = pd.read_excel(excel_input_path)
# except FileNotFoundError:
#     raise FileNotFoundError(f"Excel file not found at: {excel_input_path}")

# # Rename columns
# df = df.rename(columns={'Name': 'Titles', 'URL': 'Links'})

# # Function to clean titles
# def clean_title_text(text):
#     if pd.isna(text): return "Untitled"
#     text = str(text)
#     # Junk words removal
#     text = re.sub(r'(?i)download', '', text)
#     text = re.sub(r'(?i)complete', '', text)
#     text = re.sub(r'(?i)pdf', '', text)
#     text = re.sub(r'(?i)file', '', text)
#     text = re.sub(r'(?i)urdu novel', '', text)
#     return " ".join(text.split())

# # --- CSS STYLING (Fixed Height & Compact Button) ---
# html_content = """
# <style>
#     .novel-list-container {
#         font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
#         max-width: 100%;
#         margin: 0 auto;
#         padding: 10px 5px;
#     }

#     ul.novel-list {
#         list-style: none;
#         padding: 0;
#         margin: 0;
#         display: grid;
#         grid-template-columns: 1fr; /* Mobile par 1 column */
#         gap: 12px;
#     }

#     /* Card Design */
#     li.novel-item {
#         background-color: #fff;
#         border: 1px solid #e0e0e0;
#         border-radius: 8px;
#         padding: 12px 15px;
#         display: flex;
#         flex-direction: column; /* Content upar neechay */
#         justify-content: space-between;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.02);
#     }

#     /* --- SYMMETRY LOGIC (2 LINES FIXED) --- */
#     h3.novel-title {
#         font-size: 15px;
#         color: #333;
#         font-weight: 600;
#         margin: 0 0 8px 0;
#         line-height: 1.4; /* Line height defined */
        
#         /* Ye code title ko exactly 2 lines par restrict karega */
#         display: -webkit-box;
#         -webkit-line-clamp: 2; 
#         -webkit-box-orient: vertical;
#         overflow: hidden;
#         text-overflow: ellipsis;
#         height: 42px; /* 1.4em * 2 lines approx = Fixed Height for symmetry */
#     }

#     .meta-row {
#         display: flex;
#         justify-content: space-between;
#         align-items: center;
#         margin-top: 5px;
#     }

#     .writer-tag {
#         font-size: 12px;
#         color: #888;
#     }

#     /* --- COMPACT BUTTON STYLE --- */
#     .download-btn {
#         background-color: #007bff;
#         color: white !important;
#         padding: 6px 18px; /* Chota padding */
#         text-decoration: none !important;
#         border-radius: 20px; /* Round pill shape */
#         font-size: 13px;
#         font-weight: 500;
#         display: inline-block; /* Full width nahi hoga ab */
#         width: auto; /* Jitna text utna button */
#         border: none;
#         transition: background 0.2s;
#     }

#     .download-btn:hover {
#         background-color: #0056b3;
#     }

# </style>

# <div class="novel-list-container">
#     <ul class="novel-list">
# """

# # --- GENERATING ITEMS ---

# for index, row in df.iterrows():
#     raw_title = str(row['Titles'])
#     link = str(row['Links']).strip() if pd.notna(row['Links']) else "#"
    
#     clean_name = clean_title_text(raw_title)
    
#     # Writer Name Logic
#     if " by " in clean_name.lower():
#         parts = re.split(r' by ', clean_name, flags=re.IGNORECASE, maxsplit=1)
#         novel_title = parts[0].strip()
#         writer_name = parts[1].strip()
#     else:
#         novel_title = clean_name
#         writer_name = "Deeba Tabassum"

#     # Button Logic
#     if link == "#" or link == "":
#         btn_html = '<span style="color:#aaa; font-size:12px;">Coming Soon</span>'
#     else:
#         # Button ab div ke andar nahi, direct control hoga
#         btn_html = f'<a href="{link}" class="download-btn" target="_blank" rel="nofollow">Download PDF</a>'

#     html_content += f"""
#         <li class="novel-item">
#             <h3 class="novel-title">{novel_title}</h3>
#             <div class="meta-row">
#                 <span class="writer-tag">{writer_name}</span>
#                 {btn_html}
#             </div>
#         </li>"""

# html_content += """
#     </ul>
# </div>
# """

# # Save output
# output_txt_path = r"D:\unb-workstation\blogger_mobile_fixed.txt"
# try:
#     with open(output_txt_path, 'w', encoding='utf-8') as f:
#         f.write(html_content)
#     print(f"✅ Fixed Layout saved to: {output_txt_path}")
#     print("👉 Changes: Titles are fixed to 2 lines height. Buttons are small and compact.")
# except Exception as e:
#     print(f"Error writing TXT file: {e}")






# import pandas as pd

# # 1. Load the filtered Excel file
# excel_input_path = r"D:\unb-workstation\writers\deeba tabassum.xlsx" 

# try:
#     df = pd.read_excel(excel_input_path)
# except FileNotFoundError:
#     raise FileNotFoundError(f"Excel file not found at: {excel_input_path}")

# # Rename columns to standard names
# df = df.rename(columns={'Name': 'Titles', 'URL': 'Links'})

# # Ensure required columns exist
# if 'Titles' not in df.columns or 'Links' not in df.columns:
#     raise ValueError(f"Excel file must contain 'Titles' and 'Links' columns.")

# # --- CSS STYLING (Modern, SEO & Mobile Friendly) ---
# html_content = """
# <style>
#     :root {
#         --primary-color: #007bff; /* Professional Blue */
#         --hover-color: #0056b3;
#         --bg-color: #f8f9fa;
#         --text-color: #333;
#         --card-shadow: 0 2px 5px rgba(0,0,0,0.05);
#         --card-hover-shadow: 0 5px 15px rgba(0,0,0,0.1);
#     }

#     /* Container */
#     .novel-list-container {
#         font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
#         max-width: 800px; /* Better readability width */
#         margin: 20px auto;
#         padding: 0 10px;
#     }

#     ul.novel-list {
#         list-style: none;
#         padding: 0;
#         margin: 0;
#     }

#     /* Modern Card Item */
#     li.novel-item {
#         background-color: #fff;
#         border: 1px solid #eef0f2;
#         border-radius: 8px; /* Rounded corners */
#         padding: 15px 20px;
#         margin-bottom: 12px;
#         display: flex;
#         justify-content: space-between;
#         align-items: center;
#         transition: all 0.3s ease;
#         box-shadow: var(--card-shadow);
#     }

#     li.novel-item:hover {
#         transform: translateY(-2px); /* Subtle lift effect */
#         box-shadow: var(--card-hover-shadow);
#         border-color: #dce0e5;
#     }

#     /* Counter Styling */
#     .novel-number {
#         font-weight: 700;
#         color: #adb5bd;
#         font-size: 16px;
#         min-width: 35px;
#     }

#     /* Semantic Title for SEO (H3) */
#     h3.novel-title {
#         flex-grow: 1;
#         font-size: 16px;
#         color: var(--text-color);
#         font-weight: 600;
#         margin: 0 15px 0 0; /* Reset margins */
#         line-height: 1.5;
#     }

#     /* Status Note */
#     .note-badge {
#         font-size: 11px;
#         background-color: #fff3cd;
#         color: #856404;
#         padding: 2px 6px;
#         border-radius: 4px;
#         margin-left: 8px;
#         font-weight: normal;
#         display: inline-block;
#         vertical-align: middle;
#     }

#     /* Modern Button with Icon Support */
#     .download-btn {
#         background-color: var(--primary-color);
#         color: white !important;
#         padding: 8px 16px;
#         text-decoration: none;
#         border-radius: 50px; /* Pill shape */
#         font-size: 14px;
#         font-weight: 500;
#         display: inline-flex;
#         align-items: center;
#         gap: 8px; /* Space between icon and text */
#         transition: background-color 0.2s;
#         border: none;
#         white-space: nowrap;
#     }

#     .download-btn:hover {
#         background-color: var(--hover-color);
#         text-decoration: none;
#     }
    
#     .download-btn svg {
#         width: 16px;
#         height: 16px;
#         fill: currentColor;
#     }

#     /* Mobile Responsive */
#     @media (max-width: 600px) {
#         li.novel-item {
#             flex-direction: column;
#             align-items: flex-start;
#             padding: 15px;
#         }
        
#         h3.novel-title {
#             margin-bottom: 12px;
#             font-size: 15px;
#         }

#         .download-btn {
#             width: 100%; /* Full width on mobile */
#             justify-content: center;
#         }
        
#         .novel-number {
#             display: none; /* Hide number on small screens for cleaner look */
#         }
#     }
# </style>

# <div class="novel-list-container">
#     <ul class="novel-list">
# """

# # --- SVG ICON (Lightweight) ---
# download_icon_svg = """
# <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>
# """

# # --- GENERATING LIST ITEMS ---
# for index, row in df.iterrows():
#     # Extract data
#     raw_title = str(row['Titles']).strip() if pd.notna(row['Titles']) else "Untitled"
#     link = str(row['Links']).strip() if pd.notna(row['Links']) else "#"
    
#     # Title Formatting
#     if " by " in raw_title.lower():
#         formatted_title = raw_title.title() 
#         clean_name = raw_title.split(" by ", 1)[0].strip()
#     else:
#         clean_name = raw_title.strip()
#         formatted_title = f"{clean_name.title()} by Deeba Tabassum"
    
#     # Special Note Check
#     note_html = ""
#     if clean_name.lower() == "maala":
#         note_html = '<span class="note-badge">Episodic</span>'
    
#     # Button Logic (UX: Handle empty links)
#     if link == "#" or link == "":
#         button_html = '<span style="color:#999; font-size:13px;">Coming Soon</span>'
#     else:
#         # SEO: Added title attribute for keywords and aria-label
#         button_html = f"""
#         <a href="{link}" 
#            class="download-btn" 
#            rel="nofollow noopener noreferrer" 
#            target="_blank" 
#            title="Download {formatted_title} PDF Free"
#            aria-label="Download PDF for {formatted_title}">
#            <span>Download</span>
#            {download_icon_svg}
#         </a>
#         """

#     # HTML Structure (Used <h3> for SEO hierarchy instead of div)
#     html_content += f"""
#         <li class="novel-item">
#             <span class="novel-number">{index + 1}.</span>
#             <h3 class="novel-title">
#                 {formatted_title}
#                 {note_html}
#             </h3>
#             {button_html}
#         </li>"""

# # Close tags
# html_content += """
#     </ul>
# </div>
# """

# # Save output
# output_txt_path = r"D:\unb-workstation\novel_list_optimized.txt"
# try:
#     with open(output_txt_path, 'w', encoding='utf-8') as f:
#         f.write(html_content)
#     print(f"✅ Enhanced UI/UX & SEO HTML saved to: {output_txt_path}")
#     print("👉 Code updated with H3 tags (SEO), SVG Icons (UX), and Mobile Responsiveness.")
# except Exception as e:
#     print(f"Error writing TXT file: {e}")
















# import pandas as pd

# # 1. Load the filtered Excel file
# # Apni file ka path yahan check kar len
# excel_input_path = r"D:\unb-workstation\writers\deeba tabassum.xlsx" 

# try:
#     df = pd.read_excel(excel_input_path)
# except FileNotFoundError:
#     raise FileNotFoundError(f"Excel file not found at: {excel_input_path}")

# # Print columns for debugging
# print("Columns in Excel file:", df.columns.tolist())

# # Rename columns to 'Titles' and 'Links'
# df = df.rename(columns={'Name': 'Titles', 'URL': 'Links'})

# # Ensure required columns exist
# if 'Titles' not in df.columns or 'Links' not in df.columns:
#     raise ValueError(f"Excel file must contain 'Titles' and 'Links' columns. Found: {df.columns.tolist()}")

# # --- CSS STYLING (Lightweight & Modern) ---
# # Ye style block code ko clean rakhay ga aur bar bar inline styles nahi lagani paren gi.
# html_content = """
# <style>
#     /* Container Style */
#     .novel-list-container {
#         font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
#         max-width: 100%;
#         margin: 0 auto;
#         padding: 10px;
#     }
#     /* List Remove Bullets */
#     ul.novel-list {
#         list-style-type: none;
#         padding: 0;
#         margin: 0;
#     }
#     /* Individual Novel Card */
#     li.novel-item {
#         background-color: #fff;
#         border-bottom: 1px solid #e0e0e0;
#         padding: 15px 10px;
#         display: flex;
#         justify-content: space-between;
#         align-items: center;
#         transition: background-color 0.2s;
#     }
#     li.novel-item:hover {
#         background-color: #f9f9f9;
#     }
#     /* Numbering Style */
#     .novel-number {
#         font-weight: bold;
#         color: #555;
#         min-width: 30px;
#         font-size: 14px;
#     }
#     /* Title Style (SEO Friendly) */
#     .novel-title {
#         flex-grow: 1;
#         font-size: 15px;
#         color: #202122;
#         font-weight: 600;
#         margin-right: 10px;
#         line-height: 1.4;
#     }
#     /* Download Button Style (Call to Action) */
#     .download-btn {
#         background-color: #2ecc71; /* Green color for download */
#         color: white !important;
#         padding: 8px 15px;
#         text-decoration: none;
#         border-radius: 5px;
#         font-size: 13px;
#         font-weight: bold;
#         white-space: nowrap;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#     }
#     .download-btn:hover {
#         background-color: #27ae60;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.15);
#     }
#     .note-text {
#         font-size: 11px;
#         color: #e74c3c;
#         display: block;
#         font-weight: normal;
#         margin-top: 2px;
#     }
#     /* Mobile Responsive */
#     @media (max-width: 480px) {
#         li.novel-item {
#             flex-direction: column;
#             align-items: flex-start;
#         }
#         .download-btn {
#             margin-top: 10px;
#             width: 100%;
#             text-align: center;
#             display: block;
#         }
#     }
# </style>

# <div class="novel-list-container">
#     <ul class="novel-list">
# """

# # --- GENERATING LIST ITEMS ---

# for index, row in df.iterrows():
#     # Extract title and link
#     raw_title = str(row['Titles']).strip() if pd.notna(row['Titles']) else "Untitled"
#     link = str(row['Links']).strip() if pd.notna(row['Links']) else "#"
    
#     # Text processing logic
#     if " by " in raw_title.lower():
#         formatted_title = raw_title.title() 
#         novel_name_for_check = raw_title.split(" by ", 1)[0].strip()
#     else:
#         novel_name_for_check = raw_title.strip()
#         # Default suffix logic agar writer ka naam na ho
#         formatted_title = f"{novel_name_for_check.title()} by Deeba Tabassum" # Yahan Writer ka naam dynamic bhi ho sakta ha
    
#     # Special note logic
#     note_html = ""
#     if novel_name_for_check.lower() == "maala":
#         note_html = '<span class="note-text">(Still running in episodes)</span>'
    
#     # Clean HTML Structure (No heavy inline styles)
#     html_content += f"""
#         <li class="novel-item">
#             <span class="novel-number">{index + 1}.</span>
#             <div class="novel-title">
#                 {formatted_title}
#                 {note_html}
#             </div>
#             <a href="{link}" class="download-btn" rel="nofollow" target="_blank">Download PDF</a>
#         </li>"""

# # Close tags
# html_content += """
#     </ul>
# </div>
# """

# # Save output
# output_txt_path = r"D:\unb-workstation\novel_list_optimized.txt"
# try:
#     with open(output_txt_path, 'w', encoding='utf-8') as f:
#         f.write(html_content)
#     print(f"✅ SEO Friendly HTML saved to: {output_txt_path}")
#     print("👉 Ab is file ka content Blogger ke HTML view ma paste karen.")
# except Exception as e:
#     print(f"Error writing TXT file: {e}")