import os
import img2pdf
import re
from pathlib import Path

def convert_images_to_pdf_robust(folder_path, output_name):
    folder = Path(folder_path)
    output_pdf = Path(output_name)
    
    # 1. Image files filter karein
    valid_extensions = ('.jpg', '.jpeg', '.png')
    image_files = [f for f in folder.iterdir() if f.suffix.lower() in valid_extensions]
    
    if not image_files:
        print("Error: Is folder mein koi images nahi mili!")
        return

    # 2. Filenames se numbers extract karein (Dictionary: {number: full_path})
    image_map = {}
    for img in image_files:
        match = re.search(r'^\d+', img.name)
        if match:
            num = int(match.group())
            image_map[num] = str(img)
    
    if not image_map:
        print("Error: Files ke naam digit se shuru nahi ho rahe!")
        return

    # 3. Missing Pages Check Karein
    existing_nums = sorted(image_map.keys())
    start_num = existing_nums[0]
    end_num = existing_nums[-1]
    
    all_nums_range = set(range(start_num, end_num + 1))
    missing_nums = sorted(list(all_nums_range - set(existing_nums)))

    # 4. Images ko sahi sequence mein sort karein
    sorted_image_paths = [image_map[n] for n in existing_nums]

    # 5. PDF Conversion
    try:
        print(f"Conversion shuru ho rahi hai: {output_pdf}...")
        with open(output_pdf, "wb") as f:
            f.write(img2pdf.convert(sorted_image_paths))
        success = True
    except Exception as e:
        print(f"Conversion mein masla aaya: {e}")
        success = False

    # --- SUMMARY ---
    print("\n" + "="*30)
    print("      CONVERSION SUMMARY")
    print("="*30)
    print(f"Kul Images:        {len(existing_nums)}")
    print(f"Pehla Page No:     {start_num}")
    print(f"Aakhri Page No:    {end_num}")
    
    if missing_nums:
        print(f"Missing Pages:     {missing_nums} (Gaps found!)")
    else:
        print(f"Missing Pages:     Koi nahi (Perfect sequence!)")
    
    if success:
        print(f"Status:            Kamyab (Saved as {output_pdf})")
    else:
        print(f"Status:            Nakaam")
    print("="*30)

# Folder path aur file name yahan likhein
input_dir = r"E:\unb-workstation\Writers All Novels\aymal raza\aymal raza\bari bi"
output_file = "Novel_Final.pdf"

if __name__ == "__main__":
    convert_images_to_pdf_robust(input_dir, output_file)