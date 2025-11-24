import os

def save_image_names(folder_path):
    # Valid image extensions
    valid_exts = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".jfif")

    # Get all image files
    images = [f for f in os.listdir(folder_path) if f.lower().endswith(valid_exts)]
    images.sort()

    # TXT file path inside same folder
    output_txt = os.path.join(folder_path, "image_names.txt")

    # Write to TXT
    with open(output_txt, "w", encoding="utf-8") as file:
        for img in images:
            file.write(img + "\n")

    print(f"✅ TXT file saved here: {output_txt}")
    print(f"✅ Total {len(images)} names added.")

# ---------------------------
# Run
folder_path = r"C:\Users\PCS\Downloads\your_folder"   # <-- apna folder path
save_image_names(folder_path)
