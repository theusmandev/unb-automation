import os

# 🔹 فولڈر کا path یہاں دیں
folder_path = r"C:\Users\YourName\Desktop\MyFolder"

# 🔹 output txt فائل کا نام
output_file = "file_names.txt"

file_names = []

for file in os.listdir(folder_path):
    full_path = os.path.join(folder_path, file)
    
    if os.path.isfile(full_path):
        # 🔹 صرف نام، extension کے بغیر
        name_without_ext = os.path.splitext(file)[0]
        file_names.append(name_without_ext)

# 🔹 TXT فائل میں لکھنا
with open(output_file, "w", encoding="utf-8") as f:
    for name in file_names:
        f.write(name + "\n")

print("✅ File names successfully saved to", output_file)
