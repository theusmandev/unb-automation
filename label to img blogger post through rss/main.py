import requests
import json
import os
import re
import xml.etree.ElementTree as ET

# --- 1. CONFIGURATION ---
# Yahan wo Link dalen jis label ka page ap banana chahtay hain
LABEL_URL = "https://www.urdunovelbanks.com/search/label/Romantic%20Urdu%20Novels"

# Output file kahan save ho? (Downloads folder)
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
output_file_path = os.path.join(downloads_path, "blogger_auto_feed_code.txt")

# --- 2. HELPER FUNCTIONS ---

def get_feed_url(label_url):
    """
    Normal Label URL ko RSS Feed URL ma convert krta ha.
    Example: .../search/label/Name -> .../feeds/posts/default/-/Name?alt=rss
    """
    # URL clean up
    label_url = label_url.split('?')[0] # remove query params like ?m=1
    
    if "/search/label/" in label_url:
        label_part = label_url.split("/search/label/")[-1]
        # URL encoding fix (Space ko %20 banana)
        label_part = requests.utils.quote(requests.utils.unquote(label_part))
        feed_url = f"https://www.urdunovelbanks.com/feeds/posts/default/-/{label_part}?alt=rss&max-results=500"
        return feed_url
    else:
        print("Error: Ye URL sahi Label URL nahi lag raha.")
        return None

def clean_title(title):
    """ Title ma se 'Read Online' waghaira remove krta ha """
    if not title: return ""
    # Normalize dash
    title = title.replace('–', '-').replace('—', '-').replace('|', '-')
    # Remove unwanted phrases
    clean_text = re.sub(r'\s*-\s*(Read Online|Download|PDF|Free PDF).*', '', title, flags=re.IGNORECASE)
    return clean_text.strip()

def optimize_google_url(url):
    """ Image URL ko WebP aur Small Size ma convert krta ha """
    if not url: return ""
    
    # Agar image choti (s72-c) ha to usay bara (w300) kro
    if '/s72-c/' in url:
        return url.replace('/s72-c/', '/w300-h450-c-rw/')
        
    if 'blogger.googleusercontent.com' in url or 'bp.blogspot.com' in url:
        if re.search(r'\/s\d+.*\/', url):
            return re.sub(r'\/s\d+.*\/', '/w300-h450-c-rw/', url)
        elif re.search(r'=s\d+', url):
            return re.sub(r'=s\d+.*', '=w300-h450-c-rw', url)
    return url

# --- 3. MAIN PROCESS ---

print(f"Target Label: {LABEL_URL}")
feed_url = get_feed_url(LABEL_URL)

if not feed_url:
    exit()

print(f"Fetching RSS Feed: {feed_url} ...")

try:
    response = requests.get(feed_url)
    if response.status_code != 200:
        print(f"Error: Feed fetch nahi ho saki. Status Code: {response.status_code}")
        exit()
        
    # XML Parsing
    root = ET.fromstring(response.content)
    
    novels_list = []
    
    # XML namespace handling (Atom feeds k liye)
    # Blogger RSS (alt=rss) simple XML hota ha
    
    for item in root.findall('channel/item'):
        title_raw = item.find('title').text
        link = item.find('link').text
        
        # Image extract krna (Media Thumbnail ya Content se)
        img_url = ""
        
        # 1. Try Media Thumbnail
        media_thumb = item.find('{http://search.yahoo.com/mrss/}thumbnail')
        if media_thumb is not None:
            img_url = media_thumb.attrib['url']
        
        # 2. Agar thumbnail na milay to Description/Content se nikalo
        if not img_url:
            description = item.find('description').text
            if description:
                img_match = re.search(r'src="(https://[^"]+)"', description)
                if img_match:
                    img_url = img_match.group(1)
        
        # Agar phir bhi image na milay to placeholder
        if not img_url:
            img_url = "https://via.placeholder.com/300x450?text=No+Image"

        # Processing
        final_title = clean_title(title_raw)
        final_img = optimize_google_url(img_url)
        
        novels_list.append({
            "title": final_title,
            "link": link,
            "img": final_img
        })

    print(f"Total Novels Found: {len(novels_list)}")

    # JSON Data Generation
    json_data = json.dumps(novels_list, ensure_ascii=False)

    # --- 4. HTML TEMPLATE ---
    html_template = r"""<style>
/* --- CONTAINER --- */
.novels-box { 
    margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px; 
    contain: content; 
}
.novels-head { font-size: 18px; font-weight: bold; color: #333; margin-bottom: 15px; border-left: 4px solid #e74c3c; padding-left: 10px; text-transform: uppercase; }

/* --- GRID --- */
.novels-grid {
    display: grid; 
    grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)); 
    gap: 12px;
    min-height: 300px;
    content-visibility: auto; 
}

/* --- CARD --- */
.novel-card { 
    background: #fff; border: 1px solid #ddd; border-radius: 6px; overflow: hidden; 
    text-decoration: none; display: flex; flex-direction: column; 
    position: relative; 
    contain-intrinsic-size: 110px 240px; 
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.novel-card:hover { transform: translateY(-4px); box-shadow: 0 6px 12px rgba(0,0,0,0.15); }

/* --- IMAGE --- */
.novel-card img {
    width: 100%; 
    height: auto;
    aspect-ratio: 2 / 3; 
    object-fit: cover; 
    display: block; 
    background: #f0f0f0;
}

/* --- TITLE --- */
.novel-title { 
    padding: 8px 5px;          
    font-size: 12px;           
    font-weight: 700; 
    color: #333; 
    text-align: center; 
    line-height: 1.4;
    display: -webkit-box; 
    -webkit-line-clamp: 3;     
    -webkit-box-orient: vertical; 
    overflow: hidden;
    height: 52px;              
    display: flex;             
    align-items: center;
    justify-content: center;
}

/* --- BUTTONS --- */
.load-more-area { text-align: center; margin-top: 25px; width: 100%; display: none; }
.load-btn {
    background: #e74c3c; color: white; border: none; padding: 12px 40px;
    font-size: 14px; font-weight: bold; cursor: pointer; border-radius: 50px;
    transition: background 0.3s;
}
.load-btn:hover { background: #c0392b; }
.end-msg {
    text-align: center; margin-top: 20px; padding: 10px; font-weight: bold; 
    font-size: 13px; color: #e74c3c; display: none;
}
</style>

<div class="novels-box">
  <div class="novels-head">Writers Novels Library</div>
  
  <div class="novels-grid" id="libGrid">
    </div>

  <div class="load-more-area" id="libBtnArea">
    <button class="load-btn" onclick="renderNextBatch()">Load More Novels</button>
  </div>
  <div class="end-msg" id="libEndMsg">All novels loaded. Keep in touch!</div>
</div>

<script>
// --- STATIC DATA ---
var staticNovels = __DATA_HERE__;

var renderedCount = 0;
var batchSize = 30; 
var grid = document.getElementById("libGrid");

(function initLibrary() {
    staticNovels.sort(function(a, b) {
        return a.title.localeCompare(b.title);
    });
    renderNextBatch();
})();

function renderNextBatch() {
    var fragment = document.createDocumentFragment(); 
    
    var limit = renderedCount + batchSize;
    if (limit > staticNovels.length) limit = staticNovels.length;

    for (var i = renderedCount; i < limit; i++) {
        var post = staticNovels[i];
        
        var isLCP = (i < 4);
        var loadAttr = isLCP ? 'loading="eager" fetchpriority="high"' : 'loading="lazy" decoding="async"';
        var safeTitle = post.title.replace(/"/g, '&quot;');

        var linkEl = document.createElement('a');
        linkEl.className = 'novel-card';
        linkEl.href = post.link;
        linkEl.title = safeTitle;

        linkEl.innerHTML = `
            <img src="${post.img}" ${loadAttr} alt="${safeTitle}" width="300" height="450">
            <div class="novel-title"><span>${post.title}</span></div>
        `;
        fragment.appendChild(linkEl);
    }

    grid.appendChild(fragment);
    renderedCount = limit;
    
    var btn = document.getElementById("libBtnArea");
    var msg = document.getElementById("libEndMsg");
    
    if (renderedCount >= staticNovels.length) {
        if(btn) btn.style.display = 'none';
        if(msg) msg.style.display = 'block';
    } else {
        if(btn) btn.style.display = 'block';
        if(msg) msg.style.display = 'none';
    }
}
</script>
"""
    # Merge
    final_html = html_template.replace('__DATA_HERE__', json_data)

    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print("--------------------------------------------------")
    print("SUCCESS! Auto-Fetch Complete.")
    print(f"File Saved: {output_file_path}")
    print("--------------------------------------------------")

except Exception as e:
    print(f"Error aa gaya: {e}")
 
 
 
 
 #super class
 
# import pandas as pd
# import json
# import os
# import re

# # --- 1. INPUT FILE PATH ---
# input_csv_path = r"C:\Users\PCS\Downloads\urdunovelbanks_image_urls.csv"

# # --- 2. OUTPUT FILE PATH ---
# downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
# output_file_path = os.path.join(downloads_path, "blogger_final_v3.txt")

# print(f"Reading CSV from: {input_csv_path} ...")

# # --- 3. LOAD CSV ---
# try:
#     df = pd.read_csv(input_csv_path, encoding='cp1252')
# except UnicodeDecodeError:
#     try:
#         df = pd.read_csv(input_csv_path, encoding='latin1')
#     except:
#         print("Error: Encoding issue. CSV check karein.")
#         exit()
# except FileNotFoundError:
#     print("Error: File nahi mili.")
#     exit()

# # --- 4. TITLE CLEANING FUNCTION ---
# def clean_title(title):
#     if not isinstance(title, str): return ""
#     # Normalize dash
#     title = title.replace('–', '-').replace('—', '-').replace('|', '-')
#     # Remove unwanted phrases
#     clean_text = re.sub(r'\s*-\s*(Read Online|Download|PDF|Free PDF).*', '', title, flags=re.IGNORECASE)
#     return clean_text.strip()

# # --- 5. IMAGE OPTIMIZER FUNCTION ---
# def optimize_google_url(url):
#     if not isinstance(url, str): return ""
#     url = url.strip()
#     if 'blogger.googleusercontent.com' in url or 'bp.blogspot.com' in url:
#         if re.search(r'\/s\d+.*\/', url):
#             return re.sub(r'\/s\d+.*\/', '/w300-h450-c-rw/', url)
#         elif re.search(r'=s\d+', url):
#             return re.sub(r'=s\d+.*', '=w300-h450-c-rw', url)
#     return url

# # --- 6. PREPARE DATA ---
# novels_list = []
# for index, row in df.iterrows():
#     try:
#         original_title = str(row['Title'])
#         original_img = str(row['Image URL'])
        
#         final_title = clean_title(original_title)
#         final_img = optimize_google_url(original_img)
        
#         novel = {
#             "title": final_title,
#             "link": str(row['Post URL']).strip(),
#             "img": final_img
#         }
#         novels_list.append(novel)
#     except KeyError:
#         continue

# # JSON Data Generation
# json_data = json.dumps(novels_list, ensure_ascii=False)

# # --- 7. OPTIMIZED HTML TEMPLATE (Taller Cards) ---
# html_template = r"""<style>
# /* --- CONTAINER --- */
# .novels-box { 
#     margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px; 
#     contain: content; 
# }
# .novels-head { font-size: 18px; font-weight: bold; color: #333; margin-bottom: 15px; border-left: 4px solid #e74c3c; padding-left: 10px; text-transform: uppercase; }

# /* --- GRID --- */
# .novels-grid {
#     display: grid; 
#     grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)); /* Thora sa width barhaya */
#     gap: 12px;
#     min-height: 300px;
#     content-visibility: auto; 
# }

# /* --- CARD --- */
# .novel-card { 
#     background: #fff; border: 1px solid #ddd; border-radius: 6px; overflow: hidden; 
#     text-decoration: none; display: flex; flex-direction: column; 
#     position: relative; 
#     contain-intrinsic-size: 110px 240px; /* Height barha di ta k glitch na ho */
#     transition: transform 0.2s ease, box-shadow 0.2s ease;
# }
# .novel-card:hover { transform: translateY(-4px); box-shadow: 0 6px 12px rgba(0,0,0,0.15); }

# /* --- IMAGE --- */
# .novel-card img {
#     width: 100%; 
#     height: auto;
#     aspect-ratio: 2 / 3; 
#     object-fit: cover; 
#     display: block; 
#     background: #f0f0f0;
# }

# /* --- TITLE (UPDATED HEIGHT) --- */
# .novel-title { 
#     padding: 8px 5px;          /* Padding barhai */
#     font-size: 12px;           /* Font size 11px se 12px kia */
#     font-weight: 700; 
#     color: #333; 
#     text-align: center; 
#     line-height: 1.4;
#     display: -webkit-box; 
#     -webkit-line-clamp: 3;     /* Ab 2 ki bajaye 3 lines allow hain */
#     -webkit-box-orient: vertical; 
#     overflow: hidden;
#     height: 52px;              /* Height 30px se barha kar 52px kar di */
#     display: flex;             /* Centering k liye */
#     align-items: center;
#     justify-content: center;
# }

# /* --- BUTTONS --- */
# .load-more-area { text-align: center; margin-top: 25px; width: 100%; display: none; }
# .load-btn {
#     background: #e74c3c; color: white; border: none; padding: 12px 40px;
#     font-size: 14px; font-weight: bold; cursor: pointer; border-radius: 50px;
#     transition: background 0.3s;
# }
# .load-btn:hover { background: #c0392b; }
# .end-msg {
#     text-align: center; margin-top: 20px; padding: 10px; font-weight: bold; 
#     font-size: 13px; color: #e74c3c; display: none;
# }
# </style>

# <div class="novels-box">
#   <div class="novels-head">Writers Novels Library</div>
  
#   <div class="novels-grid" id="libGrid">
#     </div>

#   <div class="load-more-area" id="libBtnArea">
#     <button class="load-btn" onclick="renderNextBatch()">Load More Novels</button>
#   </div>
#   <div class="end-msg" id="libEndMsg">All novels loaded. Keep in touch!</div>
# </div>

# <script>
# // --- STATIC DATA ---
# var staticNovels = __DATA_HERE__;

# var renderedCount = 0;
# var batchSize = 30; 
# var grid = document.getElementById("libGrid");

# (function initLibrary() {
#     staticNovels.sort(function(a, b) {
#         return a.title.localeCompare(b.title);
#     });
#     renderNextBatch();
# })();

# function renderNextBatch() {
#     var fragment = document.createDocumentFragment(); 
    
#     var limit = renderedCount + batchSize;
#     if (limit > staticNovels.length) limit = staticNovels.length;

#     for (var i = renderedCount; i < limit; i++) {
#         var post = staticNovels[i];
        
#         // LCP Optimization
#         var isLCP = (i < 4);
#         var loadAttr = isLCP ? 'loading="eager" fetchpriority="high"' : 'loading="lazy" decoding="async"';
        
#         var safeTitle = post.title.replace(/"/g, '&quot;');

#         var linkEl = document.createElement('a');
#         linkEl.className = 'novel-card';
#         linkEl.href = post.link;
#         linkEl.title = safeTitle;

#         linkEl.innerHTML = `
#             <img src="${post.img}" ${loadAttr} alt="${safeTitle}" width="300" height="450">
#             <div class="novel-title"><span>${post.title}</span></div>
#         `;
        
#         fragment.appendChild(linkEl);
#     }

#     grid.appendChild(fragment);
#     renderedCount = limit;
    
#     var btn = document.getElementById("libBtnArea");
#     var msg = document.getElementById("libEndMsg");
    
#     if (renderedCount >= staticNovels.length) {
#         if(btn) btn.style.display = 'none';
#         if(msg) msg.style.display = 'block';
#     } else {
#         if(btn) btn.style.display = 'block';
#         if(msg) msg.style.display = 'none';
#     }
# }
# </script>
# """

# # --- 8. MERGE & SAVE ---
# final_html = html_template.replace('__DATA_HERE__', json_data)

# with open(output_file_path, 'w', encoding='utf-8') as f:
#     f.write(final_html)

# print("--------------------------------------------------")
# print("SUCCESS! Card Height Increased.")
# print(f"File Location: {output_file_path}")
# print("Changes: Title area height 30px -> 52px, Font 11px -> 12px.")
# print("--------------------------------------------------")


#top class

# import pandas as pd
# import json
# import os
# import re

# # --- 1. INPUT FILE PATH ---
# # Apni CSV file ka path yahan check kar len
# input_csv_path = r"C:\Users\PCS\Downloads\urdunovelbanks_image_urls.csv"

# # --- 2. OUTPUT FILE PATH ---
# # Ye file apke Downloads folder ma "blogger_clean_code.txt" ke naam se banay ga
# downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
# output_file_path = os.path.join(downloads_path, "blogger_clean_code.txt")

# print(f"Reading CSV from: {input_csv_path} ...")

# # --- 3. LOAD CSV ---
# try:
#     df = pd.read_csv(input_csv_path, encoding='cp1252')
# except UnicodeDecodeError:
#     try:
#         df = pd.read_csv(input_csv_path, encoding='latin1')
#     except:
#         print("Error: Encoding issue. CSV check karein.")
#         exit()
# except FileNotFoundError:
#     print("Error: File nahi mili.")
#     exit()

# # --- 4. TITLE CLEANING FUNCTION (NEW) ---
# def clean_title(title):
#     if not isinstance(title, str): return ""
    
#     # Ye REGEX pattern dhondta hai: " - Read Online..." ya " – Read Online..."
#     # Aur usay remove kar deta hai
#     clean_text = re.sub(r'\s*[–-]\s*(Read Online|Download).*', '', title, flags=re.IGNORECASE)
    
#     return clean_text.strip()

# # --- 5. IMAGE OPTIMIZER FUNCTION ---
# def optimize_google_url(url):
#     if not isinstance(url, str): return ""
#     url = url.strip()
    
#     # Google Images ko WebP (-rw) aur Fixed Size (w300-h450) ma convert krna
#     if 'blogger.googleusercontent.com' in url or 'bp.blogspot.com' in url:
#         if re.search(r'\/s\d+.*\/', url):
#             return re.sub(r'\/s\d+.*\/', '/w300-h450-c-rw/', url)
#         elif re.search(r'=s\d+', url):
#             return re.sub(r'=s\d+.*', '=w300-h450-c-rw', url)
            
#     return url

# # --- 6. PREPARE DATA ---
# novels_list = []
# for index, row in df.iterrows():
#     try:
#         original_title = str(row['Title'])
#         original_img = str(row['Image URL'])
        
#         # Applying Cleaning Functions
#         final_title = clean_title(original_title)
#         final_img = optimize_google_url(original_img)
        
#         novel = {
#             "title": final_title,
#             "link": str(row['Post URL']).strip(),
#             "img": final_img
#         }
#         novels_list.append(novel)
#     except KeyError:
#         continue

# # JSON Data Generation
# json_data = json.dumps(novels_list, ensure_ascii=False)

# # --- 7. OPTIMIZED HTML TEMPLATE ---
# html_template = r"""<style>
# /* --- CONTAINER --- */
# .novels-box { 
#     margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px; 
#     contain: content; 
# }
# .novels-head { font-size: 18px; font-weight: bold; color: #333; margin-bottom: 15px; border-left: 4px solid #e74c3c; padding-left: 10px; text-transform: uppercase; }

# /* --- GRID --- */
# .novels-grid {
#     display: grid; 
#     grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); 
#     gap: 10px;
#     min-height: 300px;
#     content-visibility: auto; 
# }

# /* --- CARD --- */
# .novel-card { 
#     background: #fff; border: 1px solid #ddd; border-radius: 5px; overflow: hidden; 
#     text-decoration: none; display: flex; flex-direction: column; 
#     position: relative; 
#     contain-intrinsic-size: 100px 180px; 
#     transition: transform 0.2s ease;
# }
# .novel-card:hover { transform: translateY(-3px); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }

# /* --- IMAGE (CLS FIX) --- */
# .novel-card img {
#     width: 100%; 
#     height: auto;
#     aspect-ratio: 2 / 3; 
#     object-fit: cover; 
#     display: block; 
#     background: #f0f0f0;
# }

# /* --- TITLE --- */
# .novel-title { 
#     padding: 6px 4px; font-size: 11px; font-weight: 700; color: #333; 
#     text-align: center; line-height: 1.3;
#     display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
#     height: 30px; 
# }

# /* --- BUTTONS --- */
# .load-more-area { text-align: center; margin-top: 20px; width: 100%; display: none; }
# .load-btn {
#     background: #e74c3c; color: white; border: none; padding: 12px 40px;
#     font-size: 14px; font-weight: bold; cursor: pointer; border-radius: 50px;
# }
# .end-msg {
#     text-align: center; margin-top: 20px; padding: 10px; font-weight: bold; 
#     font-size: 13px; color: #e74c3c; display: none;
# }
# </style>

# <div class="novels-box">
#   <div class="novels-head">Writers Novels Library</div>
  
#   <div class="novels-grid" id="libGrid">
#     </div>

#   <div class="load-more-area" id="libBtnArea">
#     <button class="load-btn" onclick="renderNextBatch()">Load More Novels</button>
#   </div>
#   <div class="end-msg" id="libEndMsg">All novels loaded. Keep in touch!</div>
# </div>

# <script>
# // --- STATIC DATA ---
# var staticNovels = __DATA_HERE__;

# var renderedCount = 0;
# var batchSize = 30; 
# var grid = document.getElementById("libGrid");

# // Initialize Immediately
# (function initLibrary() {
#     // Sort A-Z
#     staticNovels.sort(function(a, b) {
#         return a.title.localeCompare(b.title);
#     });
#     renderNextBatch();
# })();

# function renderNextBatch() {
#     var fragment = document.createDocumentFragment(); 
    
#     var limit = renderedCount + batchSize;
#     if (limit > staticNovels.length) limit = staticNovels.length;

#     for (var i = renderedCount; i < limit; i++) {
#         var post = staticNovels[i];
        
#         // --- LCP OPTIMIZATION ---
#         // Pehli 4 images ko jaldi load kro (Eager), baqi ko Lazy
#         var isLCP = (i < 4);
#         var loadAttr = isLCP ? 'loading="eager" fetchpriority="high"' : 'loading="lazy" decoding="async"';
        
#         var safeTitle = post.title.replace(/"/g, '&quot;');

#         var linkEl = document.createElement('a');
#         linkEl.className = 'novel-card';
#         linkEl.href = post.link;
#         linkEl.title = safeTitle;

#         linkEl.innerHTML = `
#             <img src="${post.img}" ${loadAttr} alt="${safeTitle}" width="300" height="450">
#             <div class="novel-title">${post.title}</div>
#         `;
        
#         fragment.appendChild(linkEl);
#     }

#     grid.appendChild(fragment);
#     renderedCount = limit;
    
#     // UI Update
#     var btn = document.getElementById("libBtnArea");
#     var msg = document.getElementById("libEndMsg");
    
#     if (renderedCount >= staticNovels.length) {
#         if(btn) btn.style.display = 'none';
#         if(msg) msg.style.display = 'block';
#     } else {
#         if(btn) btn.style.display = 'block';
#         if(msg) msg.style.display = 'none';
#     }
# }
# </script>
# """

# # --- 8. MERGE & SAVE ---
# final_html = html_template.replace('__DATA_HERE__', json_data)

# with open(output_file_path, 'w', encoding='utf-8') as f:
#     f.write(final_html)

# print("--------------------------------------------------")
# print("SUCCESS! Titles Cleaned & Optimized.")
# print(f"File Location: {output_file_path}")
# print("Example Change: 'Name - Read Online...' -> 'Name'")
# print("--------------------------------------------------")