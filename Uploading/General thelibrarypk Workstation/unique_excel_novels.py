import pandas as pd
import os
from rapidfuzz import fuzz

# Load the Excel file
excel_input_path = r"D:\unb-workstation\writers\Tahir Javed Mughal_sorted.xlsx"     # Replace with your file path
df = pd.read_excel(excel_input_path)

# Ensure 'Titles' column exists
if 'Titles' not in df.columns:
    raise ValueError("Column 'Titles' not found in the Excel file")

# List to store unique rows
unique_rows = []
used_indexes = set()

# Loop to compare titles of each row with all others
for i in range(len(df)):
    if i in used_indexes:
        continue
    current_row = df.iloc[i]
    current_title = str(current_row['Titles'])  # Convert title to string
    unique_rows.append(current_row)
    
    for j in range(i + 1, len(df)):
        if j in used_indexes:
            continue
        compare_title = str(df.iloc[j]['Titles'])  # Convert title to string
        similarity = fuzz.ratio(current_title, compare_title)
        
        if similarity >= 75:  # Change threshold if needed
            used_indexes.add(j)

# Create new DataFrame from unique rows
unique_df = pd.DataFrame(unique_rows)

# Generate output file path with same directory and title, appending '_unique'
input_dir = os.path.dirname(excel_input_path)  # Get directory of input file
input_filename = os.path.splitext(os.path.basename(excel_input_path))[0]  # Get filename without extension
output_filename = f"{input_filename}_unique.xlsx"  # Append '_unique' to filename
output_path = os.path.join(input_dir, output_filename)  # Combine directory and new filename

# Save the result to the new Excel file
unique_df.to_excel(output_path, index=False, engine='openpyxl')

print(f"✅ Unique rows (based on title similarity) saved to: {output_path}")