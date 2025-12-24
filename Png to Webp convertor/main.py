import os
from PIL import Image

def convert_smart_webp(source_folder, output_folder, quality=65):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    extensions = ('.jpg', '.jpeg', '.png')

    for filename in os.listdir(source_folder):
        if filename.lower().endswith(extensions):
            file_path = os.path.join(source_folder, filename)
            
            try:
                with Image.open(file_path) as img:
                    file_name_without_ext = os.path.splitext(filename)[0]
                    new_filename = f"{file_name_without_ext}.webp"
                    output_path = os.path.join(output_folder, new_filename)

                    # METHOD 6 = Best Compression (Takes slightly longer but worth it)
                    img.save(output_path, 'webp', quality=quality, optimize=True, method=6)
                    
                    # --- SIZE CHECK LOGIC ---
                    original_size = os.path.getsize(file_path)
                    webp_size = os.path.getsize(output_path)
                    
                    if webp_size >= original_size:
                        print(f"⚠️ Skipped: {filename} (WebP was larger by {(webp_size - original_size)/1024:.2f} KB)")
                        os.remove(output_path) # WebP delete kar do kyunki faida nahi hua
                    else:
                        saved = (original_size - webp_size) / 1024
                        print(f"✅ Success: {filename} saved {saved:.2f} KB")
                    
            except Exception as e:
                print(f"Error converting {filename}: {e}")

# Usage
source_dir = r"C:\Users\PCS\Downloads\New folder"
output_dir = r"C:\Users\PCS\Downloads\New folder (2)"

# Quality ko 65 par rakha hai jo JPG to WebP ke liye best balance hai
convert_smart_webp(source_dir, output_dir, quality=65)