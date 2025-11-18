import os
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF

BASE_URL = "https://urdunovelcollection.com/teray-ishq-nachaya-complete-novel-by-zainab-khan/"
START_PAGE = 1
END_PAGE = 40

SAVE_FOLDER = "novel_images"
os.makedirs(SAVE_FOLDER, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_image_url(img):
    """Return correct image URL from lazy-load images."""
    return (
        img.get("data-src")
        or img.get("data-lazy-src")
        or img.get("data-large_image")
        or img.get("src")
    )

def download_image(url, index):
    ext = url.split("?")[0].split(".")[-1]
    filename = f"{SAVE_FOLDER}/{index:03d}.{ext}"

    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            with open(filename, "wb") as f:
                f.write(r.content)
            print("Downloaded:", filename)
        else:
            print("Failed:", url)
    except:
        print("Error:", url)

def scrape_pages():
    img_count = 1

    for page in range(START_PAGE, END_PAGE + 1):
        url = BASE_URL + str(page) + "/"
        print("\nScraping:", url)

        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, "html.parser")

        # Correct selector for this website
        content = soup.find("div", class_="entry-content")
        if not content:
            print("No content found on this page!")
            continue

        images = content.find_all("img")

        for img in images:
            img_url = get_image_url(img)
            if not img_url:
                continue

            # Filter only novel images (hosted on Flickr)
            if "staticflickr.com" not in img_url:
                continue

            download_image(img_url, img_count)
            img_count += 1

    print("\nAll images downloaded!")

def images_to_pdf(pdf_name="novel.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(0)

    files = sorted(os.listdir(SAVE_FOLDER))

    for img in files:
        path = f"{SAVE_FOLDER}/{img}"
        pdf.add_page()
        pdf.image(path, x=0, y=0, w=210)

    pdf.output(pdf_name)
    print("\nPDF Created:", pdf_name)


# Run
scrape_pages()
images_to_pdf("Teray_Ishq_Nachaya.pdf")
