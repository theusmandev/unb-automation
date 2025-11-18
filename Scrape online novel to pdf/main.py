"""
Download images from paginated novel pages and combine into a single PDF.

Usage:
- change BASE_URL to your novel URL pattern (use {page} where page number goes)
  e.g. "https://urdunovelcollection.com/teray-ishq-nachaya-complete-novel-by-zainab-khan/{page}/"
- set START_PAGE and END_PAGE
- run: python download_novel_images_to_pdf.py
"""

import os
import time
import random
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

# --------- USER CONFIG ----------
BASE_URL = "https://urdunovelcollection.com/teray-ishq-nachaya-complete-novel-by-zainab-khan/{page}/"
START_PAGE = 1
END_PAGE = 10          # change to last page number you want to download
OUT_DIR = "teray_ishq_images"
OUT_PDF = "teray_ishq_novel.pdf"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
# --------------------------------

os.makedirs(OUT_DIR, exist_ok=True)

def get_image_urls_from_html(html, page_url):
    soup = BeautifulSoup(html, "html.parser")

    # first try typical article/content container(s)
    candidates = []
    # try common selectors used by WP themes
    for sel in ['.entry-content', '.post-content', '.post-body', 'article', '#content']:
        block = soup.select_one(sel)
        if block:
            candidates.append(block)

    # fallback: whole page
    if not candidates:
        candidates = [soup]

    img_urls = []
    for block in candidates:
        imgs = block.find_all("img")
        for img in imgs:
            # check multiple possible attributes (lazy-loading)
            src = img.get("src") or img.get("data-src") or img.get("data-lazy-src") or img.get("data-original") or img.get("data-echo")
            if not src:
                # sometimes in <noscript> there is an <img> tag string
                noscript = img.find_next("noscript")
                if noscript:
                    ns_soup = BeautifulSoup(noscript.text, "html.parser")
                    src = ns_soup.find("img").get("src") if ns_soup.find("img") else None
            if src:
                # normalize protocol-relative URLs
                if src.startswith("//"):
                    src = "https:" + src
                # skip tiny placeholders / tracking gifs
                if len(src) < 10 or src.endswith("lazy_placeholder.gif") or "data:image" in src:
                    continue
                # some pages use relative paths
                if src.startswith("/"):
                    from urllib.parse import urljoin
                    src = urljoin(page_url, src)
                if src not in img_urls:
                    img_urls.append(src)
    return img_urls

def download_image(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        return r.content
    except Exception as e:
        print(f"  ! failed to download {url}: {e}")
        return None

def main():
    downloaded_files = []
    for page in range(START_PAGE, END_PAGE+1):
        page_url = BASE_URL.format(page=page)
        print(f"[{page}] fetching {page_url}")
        try:
            r = requests.get(page_url, headers=HEADERS, timeout=20)
            r.raise_for_status()
            html = r.text
        except Exception as e:
            print(f"  ! failed to fetch page {page}: {e}")
            # continue to next page (partial progress ok)
            continue

        img_urls = get_image_urls_from_html(html, page_url)
        if not img_urls:
            print("  - no images found on this page.")
            # continue — maybe text-only page
            continue

        # Save images; name them with page index + index within page to keep order
        for idx, img_url in enumerate(img_urls, start=1):
            ext = os.path.splitext(img_url.split("?")[0])[1].lower()
            if ext not in [".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"]:
                # try to infer from content-type after download
                ext = ".jpg"
            filename = f"{page:04d}_{idx:02d}{ext}"
            out_path = os.path.join(OUT_DIR, filename)
            if os.path.exists(out_path):
                print(f"   - already have {filename}")
                downloaded_files.append(out_path)
                continue

            print(f"   - downloading image {idx} from page {page}")
            data = download_image(img_url)
            if not data:
                continue
            # Save raw file
            try:
                with open(out_path, "wb") as f:
                    f.write(data)
                downloaded_files.append(out_path)
            except Exception as e:
                print(f"    ! failed saving {out_path}: {e}")

        # polite pause
        time.sleep(random.uniform(1.0, 2.5))

    if not downloaded_files:
        print("No images downloaded — exiting.")
        return

    # Sort files by filename (so page order preserved)
    downloaded_files = sorted(downloaded_files)

    # Convert to PDF (use PIL). We will convert images to RGB pages.
    pil_images = []
    for fp in downloaded_files:
        try:
            img = Image.open(fp)
            # convert GIF/PNG/WEBP etc to RGB
            if img.mode in ("RGBA", "P", "LA"):
                img = img.convert("RGB")
            elif img.mode == "L":
                img = img.convert("RGB")
            pil_images.append(img)
        except Exception as e:
            print(f"  ! failed opening {fp}: {e}")

    if not pil_images:
        print("No valid images openable by PIL — cannot create PDF.")
        return

    # save first image and append rest
    try:
        first, rest = pil_images[0], pil_images[1:]
        first.save(OUT_PDF, "PDF", resolution=100.0, save_all=True, append_images=rest)
        print(f"PDF created: {OUT_PDF}  (contains {len(pil_images)} pages)")
    except Exception as e:
        print(f"Failed to create PDF: {e}")

if __name__ == "__main__":
    main()
