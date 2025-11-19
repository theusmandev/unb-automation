import os
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
from tqdm import tqdm
import time

# ===================== CONFIGURATION =====================
BASE_URL = "https://urdunovelcollection.com/teray-ishq-nachaya-complete-novel-by-zainab-khan/"
START_PAGE = 1
END_PAGE = 927  # Poori novel ke liye itna kaafi hai, automatically ruk jayega

SAVE_FOLDER = "Teray_Ishq_Nachaya_Images"
PDF_NAME = "Teray_Ishq_Nachaya_Complete_Novel_by_Zainab_Khan.pdf"

# Sirf Flickr images hi novel pages hoti hain
ALLOWED_DOMAIN = "staticflickr.com"   # ✅ Correct line

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

os.makedirs(SAVE_FOLDER, exist_ok=True)
# =========================================================

def get_image_url(img_tag):
    return (
        img_tag.get("data-src") or
        img_tag.get("data-lazy-src") or
        img_tag.get("data-orig-file") or
        img_tag.get("src")
    )

def extract_url_from_srcset(srcset):
    if not srcset:
        return None
    return srcset.split()[0]

def download_image(img_url, filename):
    if os.path.exists(filename):
        return True

    for attempt in range(3):
        try:
            response = requests.get(img_url, headers=HEADERS, timeout=20)
            if response.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(response.content)
                return True
        except Exception as e:
            print(f"Retry {attempt + 1} failed: {e}")
            time.sleep(2)
    print(f"Failed to download: {img_url}")
    return False

def scrape_novel_images():
    downloaded_count = len([f for f in os.listdir(SAVE_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    seen_urls = set()
    
    print(f"Already downloaded: {downloaded_count} images\n")
    print(f"Scraping from page {START_PAGE} to {END_PAGE}...\n")

    for page in tqdm(range(START_PAGE, END_PAGE + 1), desc="Pages"):
        url = f"{BASE_URL}{page}/"
        
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            if r.status_code != 200:
                print(f"\nPage {page} not found (404) → Novel khatam ho gayi!")
                return downloaded_count  # Novel end ho gayi
        except:
            continue

        soup = BeautifulSoup(r.text, "html.parser")
        content = soup.find("div", class_="entry-content")
        if not content:
            continue

        for img in content.find_all("img"):
            img_url = get_image_url(img)
            
            if not img_url and img.get("srcset"):
                img_url = extract_url_from_srcset(img.get("srcset"))

            if not img_url or ALLOWED_DOMAIN not in img_url:
                continue

            if img_url.startswith("//"):
                img_url = "https:" + img_url

            if img_url in seen_urls:
                continue
            seen_urls.add(img_url)

            ext = img_url.split("/")[-1].split("?")[0].split(".")[-1]
            if ext not in ["jpg", "jpeg", "png", "gif"]:
                ext = "jpg"
            
            filename = os.path.join(SAVE_FOLDER, f"{downloaded_count + 1:04d}.{ext}")

            if download_image(img_url, filename):
                downloaded_count += 1

        time.sleep(0.5)  # Polite scraping

    return downloaded_count

def create_pdf():
    images = sorted(
        [f for f in os.listdir(SAVE_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))],
        key=lambda x: x.lower()
    )

    if not images:
        print("Koi image nahi mili!")
        return

    print(f"\n{len(images)} pages ki PDF bana raha hoon...")

    pdf = FPDF(unit="mm")
    pdf.set_auto_page_break(False)

    for img_file in tqdm(images, desc="PDF Pages"):
        path = os.path.join(SAVE_FOLDER, img_file)
        pdf.add_page()
        pdf.image(path, x=0, y=0, w=210, h=297)  # Full A4 size

    pdf.output(PDF_NAME)
    print(f"\n✅ PDF ban gayi: {PDF_NAME}")
    print(f"Total pages: {len(images)}")

# ===================== RUN =====================
if __name__ == "__main__":
    print("=== Teray Ishq Nachaya - Complete Novel by Zainab Khan ===\n")
    scrape_novel_images()
    create_pdf()
    print("\n🎉 Sab kuch ho gaya! Apka novel PDF ready hai.")