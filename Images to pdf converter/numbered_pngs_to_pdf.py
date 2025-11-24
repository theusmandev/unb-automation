import os
from PIL import Image

def images_to_pdf(folder_path):
    # Supported image extensions
    valid_exts = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".tif", ".jfif")

    # Check if folder exists
    if not os.path.isdir(folder_path):
        print(f"Error: Folder not found!\n   Path: {folder_path}")
        return

    # Collect only numeric-named images (like 1.png, 2.jpg, 50.webp etc.)
    numeric_files = {}
    non_numeric_files = []

    print("Scanning folder for numbered images...")
    for f in os.listdir(folder_path):
        file_path = os.path.join(folder_path, f)
        if os.path.isfile(file_path) and f.lower().endswith(valid_exts):
            name_no_ext = os.path.splitext(f)[0]
            try:
                num = int(name_no_ext)
                numeric_files[num] = file_path
            except ValueError:
                non_numeric_files.append(f)

    if not numeric_files:
        print("No images with numeric names found (e.g., 1.png, 2.jpg, etc.)")
        if non_numeric_files:
            print("   Found non-numeric images (ignored):")
            for f in sorted(non_numeric_files)[:15]:
                print(f"      - {f}")
            if len(non_numeric_files) > 15:
                print(f"      ... and {len(non_numeric_files) - 15} more.")
        return

    # Sort by number
    sorted_numbers = sorted(numeric_files.keys())
    start_num = sorted_numbers[0]
    end_num = sorted_numbers[-1]
    total_expected = end_num - start_num + 1
    missing = [n for n in range(start_num, end_num + 1) if n not in numeric_files]

    # Load images
    image_list = []
    failed_images = []

    print(f"Loading {len(sorted_numbers)} images...")
    for num in sorted_numbers:
        img_path = numeric_files[num]
        try:
            img = Image.open(img_path).convert("RGB")
            image_list.append(img)
        except Exception as e:
            failed_images.append((num, os.path.basename(img_path), str(e)))

    if failed_images:
        print("Warning: Some images failed to load:")
        for num, name, err in failed_images:
            print(f"   {num} → {name} : {err}")

    if not image_list:
        print("No valid images to create PDF!")
        return

    # Output PDF
    output_pdf = os.path.join(folder_path, "combined.pdf")

    # Save PDF with high quality
    try:
        print("Creating PDF... (please wait)")
        image_list[0].save(
            output_pdf,
            save_all=True,
            append_images=image_list[1:],
            quality=95,
            optimize=True,
            dpi=(300, 300)  # Good for reading novels
        )
        print(f"PDF Successfully Created!")
        print(f"   File: {output_pdf}")
    except Exception as e:
        print(f"Failed to save PDF: {e}")
        return

    # Final Beautiful Report
    print("\n" + "=" * 55)
    print("                PDF CREATION REPORT")
    print("=" * 55)
    print(f"   Folder       : {os.path.basename(folder_path)}")
    print(f"   Output File  : combined.pdf")
    print(f"   Page Range   : {start_num} → {end_num}")
    print(f"   Added Pages  : {len(image_list)}")
    print(f"   Expected     : {total_expected}")
    print(f"   Missing      : {len(missing)}")
    if missing:
        print(f"   Missing Nos  : {', '.join(map(str, missing))}")
    else:
        print("   Status       : Perfect sequence! No missing pages.")
    print("=" * 55)
    print("              All Done! Enjoy Reading!\n")

# —————————————— Run Directly ——————————————
if __name__ == "__main__":
    # ←←←←← Yahan apna folder path daalo ←←←←←
    folder_path = r"E:\unb-workstation\Writers All Novels\workstation\Farzana Kharal Novels\AJNABI KON ho tum - Copy"
    
    # Agar chaaho to yahan multiple folders bhi daal sakte ho:
    # folders = [r"path1", r"path2", r"path3"]
    # for folder in folders:
    #     print(f"\nProcessing: {folder}")
    #     images_to_pdf(folder)

    images_to_pdf(folder_path)