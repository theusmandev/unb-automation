import pandas as pd
import os
from rapidfuzz import fuzz

# Load the Excel file
excel_input_path = r"E:\unb-workstation\Writers All Novels\Uploadings\General thelibrarypk Workstation\Excel files\Asia mirza.xlsx" 
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
    current_title = str(current_row['Titles'])
    unique_rows.append(current_row)
    
    for j in range(i + 1, len(df)):
        if j in used_indexes:
            continue
        compare_title = str(df.iloc[j]['Titles'])
        similarity = fuzz.ratio(current_title, compare_title)
        
        if similarity >= 75:  # Similarity threshold
            used_indexes.add(j)

# 1. Create new DataFrame from unique rows
unique_df = pd.DataFrame(unique_rows)

# 2. UPDATION: Sort the DataFrame by 'Titles' column (A to Z)
# 'key=lambda col: col.str.lower()' is used to ignore case sensitivity while sorting
unique_df = unique_df.sort_values(by='Titles', ascending=True, key=lambda col: col.str.lower())

# Generate output file path
input_dir = os.path.dirname(excel_input_path)
input_filename = os.path.splitext(os.path.basename(excel_input_path))[0]
output_filename = f"{input_filename}_unique_sorted.xlsx"
output_path = os.path.join(input_dir, output_filename)

# Save the result to the new Excel file
unique_df.to_excel(output_path, index=False, engine='openpyxl')

print(f"✅ Unique and Sorted rows saved to: {output_path}")