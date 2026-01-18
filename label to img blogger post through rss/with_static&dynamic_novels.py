import requests
import json
import os
import re
import xml.etree.ElementTree as ET

# ==========================================
# CONFIGURATION
# ==========================================
# Apna Label URL yahan paste karein
LABEL_URL = "https://www.urdunovelbanks.com/search/label/Romantic%20Urdu%20Novels"
# ==========================================

downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
output_file_path = os.path.join(downloads_path, "hybrid_tooltip_final.txt")

def get_clean_label(url):
    if "/search/label/" in url:
        label = url.split("/search/label/")[-1].split('?')[0]
        return label
    return "Post"

def clean_title(title):
    if not title: return ""
    title = title.replace('–', '-').replace('—', '-').replace('|', '-')
    # Display ke liye title clean karein
    clean_text = re.sub(r'\s*[-]\s*(Read Online|Download|PDF|Free PDF|Urdu Novel).*', '', title, flags=re.IGNORECASE)
    clean_text = re.sub(r'[\(\[\{].*?[\)\]\}]', '', clean_text)
    return clean_text.strip()

def optimize_img(url):
    if not url: return "https://via.placeholder.com/300x450?text=No+Image"
    if 'blogger.googleusercontent.com' in url or 'bp.blogspot.com' in url:
        if '/s72-c/' in url: return url.replace('/s72-c/', '/w300-h450-c-rw/')
        url = re.sub(r'\/s\d+.*?\/', '/w300-h450-c-rw/', url)
        url = re.sub(r'=s\d+.*', '=w300-h450-c-rw', url)
    return url

print(f"Processing Feed for: {LABEL_URL}")
label_name = get_clean_label(LABEL_URL)
rss_feed_url = f"https://www.urdunovelbanks.com/feeds/posts/default/-/{label_name}?alt=rss&max-results=500"

try:
    response = requests.get(rss_feed_url)
    if response.status_code != 200:
        print("Error: RSS feed fetch nahi ho saki.")
        exit()

    root = ET.fromstring(response.content)
    novels_list = []

    for item in root.findall('channel/item'):
        title_raw = item.find('title').text
        link = item.find('link').text
        img_url = ""
        
        media_thumb = item.find('{http://search.yahoo.com/mrss/}thumbnail')
        if media_thumb is not None:
            img_url = media_thumb.attrib['url']
        
        if not img_url:
            desc = item.find('description').text
            img_match = re.search(r'src="(https://[^"]+)"', desc) if desc else None
            img_url = img_match.group(1) if img_match else ""

        novels_list.append({
            "display_title": clean_title(title_raw),
            "tooltip_title": title_raw.strip(), # Raw title for Tooltip
            "link": link,
            "img": optimize_img(img_url)
        })

    # Static data is sorted A-Z initially
    novels_list.sort(key=lambda x: x['display_title'])
    json_data = json.dumps(novels_list, ensure_ascii=False)

    html_code = f"""
<style>
.novels-box {{ margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px; font-family: sans-serif; }}
.novels-head {{ font-size: 19px; font-weight: bold; color: #333; margin-bottom: 15px; border-left: 5px solid #e74c3c; padding-left: 12px; text-transform: uppercase; }}
.novels-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)); gap: 12px; }}
.novel-card {{ background: #fff; border: 1px solid #ddd; border-radius: 6px; overflow: hidden; text-decoration: none; display: flex; flex-direction: column; transition: 0.2s; position: relative; }}
.novel-card:hover {{ transform: translateY(-4px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
.novel-card img {{ width: 100%; aspect-ratio: 2/3; object-fit: cover; display: block; background: #f0f0f0; }}
.novel-title {{ padding: 8px 5px; font-size: 11px; font-weight: 700; color: #333; text-align: center; line-height: 1.3; height: 48px; display: flex; align-items: center; justify-content: center; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; }}
.load-more-area {{ text-align: center; margin-top: 30px; }}
.load-btn {{ background: #e74c3c; color: white; border: none; padding: 13px 40px; font-size: 14px; font-weight: bold; cursor: pointer; border-radius: 50px; transition: 0.3s; }}
.load-btn:hover {{ background: #c0392b; }}
.load-btn:disabled {{ background: #999; cursor: not-allowed; }}
.end-msg {{ text-align: center; margin-top: 20px; font-weight: bold; color: #e74c3c; display: none; }}
.skel-item {{ width: 100%; aspect-ratio: 2/3; background: #eee; position: relative; overflow: hidden; border-radius: 6px; }}
.skel-item::after {{ content: ""; position: absolute; inset: 0; transform: translateX(-100%); background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent); animation: shim 1.5s infinite; }}
@keyframes shim {{ 100% {{ transform: translateX(100%); }} }}
</style>

<div class="novels-box">
    <div class="novels-head" id="libStatusTitle">Romantic Novels Library</div>
    <div class="novels-grid" id="libGrid"></div>
    <div class="load-more-area" id="libBtnArea">
        <button class="load-btn" id="actionBtn" onclick="handleLogic()">Load More Novels</button>
    </div>
    <div class="end-msg" id="libEndMsg">Tamam novels load ho chuki hain.</div>
</div>

<script>
var staticNovels = {json_data};
var dynamicData = [];
var renderedStaticCount = 0;
var renderedDynamicCount = 0;
var batchSize = 30;
var currentMode = "STATIC_PHASE"; 
var grid = document.getElementById("libGrid");
var btn = document.getElementById("actionBtn");

(function init() {{ renderStatic(); }})();

function handleLogic() {{
    if (currentMode === "STATIC_PHASE") renderStatic();
    else if (currentMode === "SWITCH_PHASE") startDynamicFetch();
    else if (currentMode === "DYNAMIC_PHASE") renderDynamic();
}}

function renderStatic() {{
    var limit = renderedStaticCount + batchSize;
    if (limit > staticNovels.length) limit = staticNovels.length;
    for (var i = renderedStaticCount; i < limit; i++) {{
        var item = staticNovels[i];
        grid.appendChild(createCard(item.display_title, item.link, item.img, i, item.tooltip_title));
    }}
    renderedStaticCount = limit;
    if (renderedStaticCount >= staticNovels.length) {{
        currentMode = "SWITCH_PHASE";
        btn.innerHTML = "View Latest Library Online";
    }}
}}

function startDynamicFetch() {{
    btn.disabled = true; btn.innerHTML = "Connecting to Feed...";
    for(var i=0; i<6; i++) {{
        var d = document.createElement('div'); d.className = 'novel-card temp-skel';
        d.innerHTML = '<div class="skel-item"></div>'; grid.appendChild(d);
    }}
    var script = document.createElement('script');
    script.src = "https://www.urdunovelbanks.com/feeds/posts/default/-/{label_name}?alt=json-in-script&callback=feedCallback&max-results=250";
    document.body.appendChild(script);
}}

window.feedCallback = function(json) {{
    document.querySelectorAll('.temp-skel').forEach(el => el.remove());
    var entries = json.feed.entry || [];
    // SORTING: Newest First
    entries.sort((a, b) => new Date(b.published.$t) - new Date(a.published.$t));
    dynamicData = entries;
    currentMode = "DYNAMIC_PHASE"; btn.disabled = false;
    btn.innerHTML = "Load More Latest";
    document.getElementById("libStatusTitle").innerHTML = "Latest Romantic Updates";
    renderDynamic();
}};

function renderDynamic() {{
    var limit = renderedDynamicCount + batchSize;
    if (limit > dynamicData.length) limit = dynamicData.length;
    for (var i = renderedDynamicCount; i < limit; i++) {{
        var post = dynamicData[i];
        var rawTitle = post.title.$t;
        var cleanTitle = rawTitle.replace(/\\s*[-–—|]?\\s*(Read Online|Download|PDF|Free).*/i, "").trim();
        var link = post.link.find(l => l.rel === 'alternate').href;
        var img = post.media$thumbnail ? post.media$thumbnail.url.replace(/\\/s[0-9]+.*?\\//, "/w300-h450-c-rw/") : "https://via.placeholder.com/300x450";
        grid.appendChild(createCard(cleanTitle, link, img, 10, rawTitle)); 
    }}
    renderedDynamicCount = limit;
    if (renderedDynamicCount >= dynamicData.length) {{
        document.getElementById("libBtnArea").style.display = "none";
        document.getElementById("libEndMsg").style.display = "block";
    }}
}}

function createCard(displayTitle, link, img, idx, tooltipText) {{
    var a = document.createElement('a');
    a.className = 'novel-card';
    a.href = link;
    a.title = tooltipText.replace(/"/g, '&quot;'); // Raw Title in Tooltip
    
    var priority = (idx < 9) ? 'fetchpriority="high"' : '';
    var loading = (idx < 9) ? 'eager' : 'lazy';
    a.innerHTML = `<img src="${{img}}" loading="${{loading}}" ${{priority}} alt="${{displayTitle}}"><div class="novel-title">${{displayTitle}}</div>`;
    return a;
}}
</script>
    """

    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(html_code)

    print(f"Success! Final Hybrid Code saved to: {output_file_path}")

except Exception as e:
    print(f"Script Error: {e}")













# import requests
# import json
# import os
# import re
# import xml.etree.ElementTree as ET

# # ==========================================
# # CONFIGURATION
# # ==========================================
# LABEL_URL = "https://www.urdunovelbanks.com/search/label/Romantic%20Urdu%20Novels"
# # ==========================================

# downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
# output_file_path = os.path.join(downloads_path, "hybrid_blogger_tooltip_code.txt")

# def get_clean_label(url):
#     if "/search/label/" in url:
#         label = url.split("/search/label/")[-1].split('?')[0]
#         return label
#     return "Post"

# def clean_title(title):
#     if not title: return ""
#     title = title.replace('–', '-').replace('—', '-').replace('|', '-')
#     clean_text = re.sub(r'\s*[-]\s*(Read Online|Download|PDF|Free PDF|Urdu Novel).*', '', title, flags=re.IGNORECASE)
#     clean_text = re.sub(r'[\(\[\{].*?[\)\]\}]', '', clean_text)
#     return clean_text.strip()

# def optimize_img(url):
#     if not url: return "https://via.placeholder.com/300x450?text=No+Image"
#     if 'blogger.googleusercontent.com' in url or 'bp.blogspot.com' in url:
#         if '/s72-c/' in url: return url.replace('/s72-c/', '/w300-h450-c-rw/')
#         url = re.sub(r'\/s\d+.*?\/', '/w300-h450-c-rw/', url)
#         url = re.sub(r'=s\d+.*', '=w300-h450-c-rw', url)
#     return url

# print(f"Generating Code for: {LABEL_URL}")
# label_name = get_clean_label(LABEL_URL)
# rss_feed_url = f"https://www.urdunovelbanks.com/feeds/posts/default/-/{label_name}?alt=rss&max-results=500"

# try:
#     response = requests.get(rss_feed_url)
#     if response.status_code != 200:
#         print("Error: RSS feed fetch nahi ho saki.")
#         exit()

#     root = ET.fromstring(response.content)
#     novels_list = []

#     for item in root.findall('channel/item'):
#         title_raw = item.find('title').text
#         link = item.find('link').text
#         img_url = ""
        
#         media_thumb = item.find('{http://search.yahoo.com/mrss/}thumbnail')
#         if media_thumb is not None:
#             img_url = media_thumb.attrib['url']
        
#         if not img_url:
#             desc = item.find('description').text
#             img_match = re.search(r'src="(https://[^"]+)"', desc) if desc else None
#             img_url = img_match.group(1) if img_match else ""

#         novels_list.append({
#             "title": clean_title(title_raw),
#             "link": link,
#             "img": optimize_img(img_url)
#         })

#     novels_list.sort(key=lambda x: x['title'])
#     json_data = json.dumps(novels_list, ensure_ascii=False)

#     html_code = f"""
# <style>
# .novels-box {{ margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px; font-family: sans-serif; }}
# .novels-head {{ font-size: 19px; font-weight: bold; color: #333; margin-bottom: 15px; border-left: 5px solid #e74c3c; padding-left: 12px; text-transform: uppercase; }}
# .novels-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)); gap: 12px; }}
# .novel-card {{ background: #fff; border: 1px solid #ddd; border-radius: 6px; overflow: hidden; text-decoration: none; display: flex; flex-direction: column; transition: 0.2s; position: relative; cursor: pointer; }}
# .novel-card:hover {{ transform: translateY(-4px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
# .novel-card img {{ width: 100%; aspect-ratio: 2/3; object-fit: cover; display: block; background: #f0f0f0; }}
# .novel-title {{ padding: 8px 5px; font-size: 11px; font-weight: 700; color: #333; text-align: center; line-height: 1.3; height: 48px; display: flex; align-items: center; justify-content: center; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; }}
# .load-more-area {{ text-align: center; margin-top: 30px; }}
# .load-btn {{ background: #e74c3c; color: white; border: none; padding: 13px 40px; font-size: 14px; font-weight: bold; cursor: pointer; border-radius: 50px; }}
# .error-msg {{ grid-column: 1/-1; text-align: center; padding: 20px; background: #fff3cd; color: #856404; border-radius: 6px; display: none; }}
# .end-msg {{ text-align: center; margin-top: 20px; font-weight: bold; color: #e74c3c; display: none; }}
# .skel-item {{ width: 100%; aspect-ratio: 2/3; background: #eee; position: relative; overflow: hidden; border-radius: 6px; }}
# .skel-item::after {{ content: ""; position: absolute; inset: 0; transform: translateX(-100%); background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent); animation: shim 1.5s infinite; }}
# @keyframes shim {{ 100% {{ transform: translateX(100%); }} }}
# </style>

# <div class="novels-box">
#     <div class="novels-head" id="libStatusTitle">Romantic Novels Library</div>
#     <div class="novels-grid" id="libGrid">
#         <div class="error-msg" id="netError">Network Error. <span style="text-decoration:underline; cursor:pointer;" onclick="startDynamicFetch()">Retry</span></div>
#     </div>
#     <div class="load-more-area" id="libBtnArea">
#         <button class="load-btn" id="actionBtn" onclick="handleLogic()">Load More Novels</button>
#     </div>
#     <div class="end-msg" id="libEndMsg">Tamam Library Load Ho Chuki Hai.</div>
# </div>

# <script>
# var staticNovels = {json_data};
# var dynamicData = [];
# var renderedStaticCount = 0;
# var renderedDynamicCount = 0;
# var batchSize = 30;
# var currentMode = "STATIC_PHASE"; 
# var grid = document.getElementById("libGrid");
# var btn = document.getElementById("actionBtn");

# (function init() {{ renderStatic(); }})();

# function handleLogic() {{
#     if (currentMode === "STATIC_PHASE") renderStatic();
#     else if (currentMode === "SWITCH_PHASE") startDynamicFetch();
#     else if (currentMode === "DYNAMIC_PHASE") renderDynamic();
# }}

# function renderStatic() {{
#     var limit = renderedStaticCount + batchSize;
#     if (limit > staticNovels.length) limit = staticNovels.length;
#     for (var i = renderedStaticCount; i < limit; i++) {{
#         grid.appendChild(createCard(staticNovels[i].title, staticNovels[i].link, staticNovels[i].img, i));
#     }}
#     renderedStaticCount = limit;
#     if (renderedStaticCount >= staticNovels.length) {{
#         currentMode = "SWITCH_PHASE";
#         btn.innerHTML = "View Latest Updates (Online)";
#     }}
# }}

# function startDynamicFetch() {{
#     btn.disabled = true; btn.innerHTML = "Connecting Feed...";
#     for(var i=0; i<6; i++) {{
#         var d = document.createElement('div'); d.className = 'novel-card temp-skel';
#         d.innerHTML = '<div class="skel-item"></div>'; grid.appendChild(d);
#     }}
#     var script = document.createElement('script');
#     script.src = "https://www.urdunovelbanks.com/feeds/posts/default/-/{label_name}?alt=json-in-script&callback=feedCallback&max-results=200";
#     document.body.appendChild(script);
# }}

# window.feedCallback = function(json) {{
#     document.querySelectorAll('.temp-skel').forEach(el => el.remove());
#     var entries = json.feed.entry || [];
#     entries.sort((a, b) => new Date(b.published.$t) - new Date(a.published.$t));
#     dynamicData = entries;
#     currentMode = "DYNAMIC_PHASE"; btn.disabled = false;
#     btn.innerHTML = "Load More Latest";
#     document.getElementById("libStatusTitle").innerHTML = "Latest Romantic Library";
#     renderDynamic();
# }};

# function renderDynamic() {{
#     var limit = renderedDynamicCount + batchSize;
#     if (limit > dynamicData.length) limit = dynamicData.length;
#     for (var i = renderedDynamicCount; i < limit; i++) {{
#         var post = dynamicData[i];
#         var title = post.title.$t.replace(/\\s*[-–—|]?\\s*(Read Online|Download|PDF|Free).*/i, "").trim();
#         var link = post.link.find(l => l.rel === 'alternate').href;
#         var img = post.media$thumbnail ? post.media$thumbnail.url.replace(/\\/s[0-9]+.*?\\//, "/w300-h450-c-rw/") : "https://via.placeholder.com/300x450";
#         grid.appendChild(createCard(title, link, img, 10)); 
#     }}
#     renderedDynamicCount = limit;
#     if (renderedDynamicCount >= dynamicData.length) {{
#         document.getElementById("libBtnArea").style.display = "none";
#         document.getElementById("libEndMsg").style.display = "block";
#     }}
# }}

# function createCard(title, link, img, idx) {{
#     var a = document.createElement('a');
#     a.className = 'novel-card';
#     a.href = link;
#     // Tooltip logic: novel name safe for HTML
#     a.title = title.replace(/"/g, '&quot;'); 
    
#     var priority = (idx < 9) ? 'fetchpriority="high"' : '';
#     var loading = (idx < 9) ? 'eager' : 'lazy';
#     a.innerHTML = `<img src="${{img}}" loading="${{loading}}" ${{priority}} alt="${{title}}"><div class="novel-title">${{title}}</div>`;
#     return a;
# }}
# </script>
#     """

#     with open(output_file_path, 'w', encoding='utf-8') as f:
#         f.write(html_code)

#     print(f"Success! Hybrid Code with Hover Tooltip saved: {output_file_path}")

# except Exception as e:
#     print(f"Error logic: {e}")