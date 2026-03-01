import pandas as pd
import re
import os

def convert_to_direct_link(url):
    # Agar cell khali ho toh error na aaye
    if pd.isna(url) or not isinstance(url, str):
        return url
        
    # Google Drive File ID nikalne ke liye regex
    file_id_pattern = r'/d/([a-zA-Z0-9-_]+)'
    match = re.search(file_id_pattern, url)
    
    if match:
        file_id = match.group(1)
        return f'https://drive.google.com/uc?export=download&id={file_id}'
    
    return url

# 1. File Path
input_path = r"C:\Users\PCS\Desktop\Book1.xlsx"
output_path = r"C:\Users\PCS\Desktop\Book2.xlsx"

# Check karein ke file desktop par mojud hai ya nahi
if not os.path.exists(input_path):
    print(f"Error: File nahi mili! Path check karein: {input_path}")
else:
    # 2. Excel file load karein
    df = pd.read_excel(input_path)

    # 3. Column Identify karein
    # Agar 'DriveLinks' column nahi milta, toh ye pehla column (index 0) utha lega
    if 'DriveLinks' in df.columns:
        target_column = 'DriveLinks'
    else:
        target_column = df.columns[0]
        print(f"Note: 'DriveLinks' nahi mila, hum '{target_column}' column use kar rahe hain.")

    # 4. Conversion apply karein
    df['DirectDownloadLinks'] = df[target_column].apply(convert_to_direct_link)

    # 5. Save karein
    df.to_excel(output_path, index=False)
    print(f"Mubarak ho! File convert ho kar yahan save ho gayi hai: {output_path}")