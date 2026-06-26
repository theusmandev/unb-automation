import PyPDF2

def merge_and_insert_pdf_pages():
    # --- Hardcoded Paths ---
    # Apni files ke sahi paths yahan likhein
    main_pdf_path = r"C:\Users\PCS\Downloads\InPage DNA\DNA Inpage.pdf" # Aap ki asal 500+ pages wali PDF
    pdf_1_path = r"C:\Users\PCS\Downloads\InPage DNA\extracted_pages\1.pdf"                          # Jo sab se pehle (Cover Page) banegi
    pdf_2_path = r"C:\Users\PCS\Downloads\InPage DNA\extracted_pages\2.pdf"                         # Jo page 7 ke baad insert hogi
    pdf_3_path = r"C:\Users\PCS\Downloads\InPage DNA\extracted_pages\3.pdf"                          # Jo sab se aakhir (Last Page) banegi
    
    output_pdf_path = "final_combined_output.pdf"  # Nayi banni wali PDF ka naam

    writer = PyPDF2.PdfWriter()

    try:
        # Saari files ko open karein
        main_file = open(main_pdf_path, 'rb')
        file1 = open(pdf_1_path, 'rb')
        file2 = open(pdf_2_path, 'rb')
        file3 = open(pdf_3_path, 'rb')

        # PDF Readers set up karein
        main_reader = PyPDF2.PdfReader(main_file)
        reader1 = PyPDF2.PdfReader(file1)
        reader2 = PyPDF2.PdfReader(file2)
        reader3 = PyPDF2.PdfReader(file3)

        total_main_pages = len(main_reader.pages)
        print(f"Original PDF total pages: {total_main_pages}")

        # STEP 1: 1.pdf ko sab se pehle add karein (Cover Page)
        print("Adding 1.pdf at the beginning...")
        for page in reader1.pages:
            writer.add_page(page)

        # STEP 2: Original PDF ke pehle 7 pages add karein (Index 0 se 6 tak)
        print("Copying original pages 1 to 7...")
        pages_to_copy_first_part = min(7, total_main_pages)
        for i in range(pages_to_copy_first_part):
            writer.add_page(main_reader.pages[i])

        # STEP 3: 2.pdf ko page 7 ke aage (yani 8th position par) insert karein
        print("Inserting 2.pdf after page 7...")
        for page in reader2.pages:
            writer.add_page(page)

        # STEP 4: Original PDF ke baki bache hue pages add karein (Page 8 se lekar aakhir tak)
        if total_main_pages > 7:
            print("Copying remaining original pages...")
            for i in range(7, total_main_pages):
                writer.add_page(main_reader.pages[i])

        # STEP 5: 3.pdf ko sab se aakhir mein add karein
        print("Adding 3.pdf at the very end...")
        for page in reader3.pages:
            writer.add_page(page)

        # final output file write karein
        with open(output_pdf_path, 'wb') as output_file:
            writer.write(output_file)
            
        print(f"\nSuccess! Nayi PDF file tayar ho chuki hai: '{output_pdf_path}'")

        # Saari opened files ko close karein
        main_file.close()
        file1.close()
        file2.close()
        file3.close()

    except FileNotFoundError as e:
        print(f"\nError: Koi file nahi mili. Kripya paths check karein.\nDetail: {e}")
    except Exception as e:
        print(f"\nKoi error aagaya: {e}")

if __name__ == "__main__":
    merge_and_insert_pdf_pages()