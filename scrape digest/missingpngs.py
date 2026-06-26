import os

# ✅ Apne folder ka path yahan likho (example: r"E:\myfolder")
folder_path = r"E:\SUNB\scrape digest\downloaded_pages"

# ✅ Total expected pages (1 to 216)
start_page = 1
end_page = 216

missing_files = []

for i in range(start_page, end_page + 1):
    # file ka naam pattern ke mutabiq
    filename = f"page_{i:03}.jpg"
    file_path = os.path.join(folder_path, filename)

    # agar file exist nahi karti to missing list me add karo
    if not os.path.exists(file_path):
        missing_files.append(filename)

# ✅ Result show karo
if missing_files:
    print("❌ Missing images:")
    for file in missing_files:
        print(file)
else:
    print("✅ All images are present!")
