import os
from PyPDF2 import PdfReader, PdfWriter

def remove_page_from_pdfs(input_folder, output_folder, page_to_remove):
    # Output folder agar exist nahi karta to banaye
    os.makedirs(output_folder, exist_ok=True)

    # Sabhi files par loop
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".pdf"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            reader = PdfReader(input_path)
            writer = PdfWriter()

            # Pages add karo except the one to remove
            for i in range(len(reader.pages)):
                if i != (page_to_remove - 1):  # page_to_remove 1-based hai
                    writer.add_page(reader.pages[i])

            # Nayi file save karo
            with open(output_path, "wb") as f:
                writer.write(f)

            print(f"Processed: {filename}")

# Example usage
if __name__ == "__main__":
    input_folder = r"C:\Users\PCS\Downloads\input"  # yahan apna input folder ka path dein
    output_folder = r"C:\Users\PCS\Downloads\outputtt" # yahan apna output folder ka path dein
    page_to_remove = 2            # jis page ko remove karna hai (1-based index)

    remove_page_from_pdfs(input_folder, output_folder, page_to_remove)
