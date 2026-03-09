import pandas as pd
import os

# Input JSON file path
json_file_path = r"E:\unb-workstation\Writers All Novels\Uploadings\readyready.json"
# Input search name
search_name = "Asia mirza"  # Case-insensitive search term

try:
    # Load JSON data
    df = pd.read_json(json_file_path)

    # Filter rows where any column contains the search_name (case-insensitive)
    filtered_df = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(search_name.lower(), na=False).any(), axis=1)]

    if filtered_df.empty:
        print(f"No rows found containing '{search_name}'.")
    else:
        # Output Excel file path (using search name)
        excel_output_path = fr"E:\unb-workstation\Writers All Novels\Uploadings\General thelibrarypk Workstation\Excel files\{search_name}.xlsx"

        # Check if output file already exists
        if os.path.exists(excel_output_path):
            print(f"Warning: Overwriting existing file at {excel_output_path}")

        # Save filtered rows to Excel
        filtered_df.to_excel(excel_output_path, index=False, engine='openpyxl')
        print(f"Filtered rows saved to: {excel_output_path}")

except FileNotFoundError:
    print(f"Error: The file {json_file_path} was not found.")
except ValueError as e:
    print(f"Error: Invalid JSON format in {json_file_path}. Details: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")