import os
from PIL import Image

def images_to_pdf(folder_path):
    # ✅ Supported image extensions
    valid_exts = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".jfif")

    # ✅ Get all valid images
    images = [f for f in os.listdir(folder_path) if f.lower().endswith(valid_exts)]

    if not images:
        print("❌ No images found in this folder.")
        return

    # ✅ Sort numerically if filenames are numbers like 1, 2, 3
    try:
        images.sort(key=lambda x: int(os.path.splitext(x)[0]))
    except ValueError:
        # fallback to normal alphabetical sort
        images.sort()

    image_list = []
    for filename in images:
        img_path = os.path.join(folder_path, filename)
        img = Image.open(img_path).convert("RGB")
        image_list.append(img)

    # ✅ Save all images into one PDF
    output_pdf = os.path.join(folder_path, "combined.pdf")
    image_list[0].save(output_pdf, save_all=True, append_images=image_list[1:])
    print(f"✅ PDF created successfully: {output_pdf}")

# 🧩 Example usage
folder_path = r"E:\unb-workstation\Writers All Novels\workstation\Farzana Kharal Novels\AJNABI KON ho tum - Copy"# apna folder path likho
images_to_pdf(folder_path)
