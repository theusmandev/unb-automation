import os
from PyPDF2 import PdfReader, PdfWriter

def remove_pages_from_pdfs(input_folder, output_folder, pages_to_remove):
    # Output folder agar exist nahi karta to banaye
    os.makedirs(output_folder, exist_ok=True)

    # 0-based index me convert karna
    pages_to_remove = [p - 1 for p in pages_to_remove]

    # Sabhi files par loop
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".pdf"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            reader = PdfReader(input_path)
            writer = PdfWriter()

            # Pages add karo except the ones to remove
            for i in range(len(reader.pages)):
                if i not in pages_to_remove:
                    writer.add_page(reader.pages[i])

            # Nayi file save karo
            with open(output_path, "wb") as f:
                writer.write(f)

            print(f"Processed: {filename}")

# Example usage
if __name__ == "__main__":
    input_folder = "input_pdfs"      # apna input folder path
    output_folder = "output_pdfs"    # apna output folder path
    pages_to_remove = [2, 5, 7]      # multiple pages (1-based index)

    remove_pages_from_pdfs(input_folder, output_folder, pages_to_remove)
