import PyPDF2

def merge_and_insert_pdf_pages():
    # --- Hardcoded Paths ---
    main_pdf_path = r"C:\Users\PCS\Desktop\test.pdf"         # Aap ki asal 500+ pages wali PDF
    pdf_1_path = r"E:\unb-workstation\InPage DNA\DNA\InPage DNA\extracted_pages\1.pdf" 
    pdf_2_path = r"E:\unb-workstation\InPage DNA\DNA\InPage DNA\extracted_pages\2.pdf" 
    pdf_3_path = r"E:\unb-workstation\InPage DNA\DNA\InPage DNA\extracted_pages\3.pdf" # Jo Original ke exact 7th page ke baad aayegi
    pdf_4_path = r"E:\unb-workstation\InPage DNA\DNA\InPage DNA\extracted_pages\4.pdf" # Jo sab se aakhir mein aaye gi
    
    output_pdf_path = r"C:\Users\PCS\Desktop\test_Final.pdf"  # Nayi banni wali PDF ka naam

    writer = PyPDF2.PdfWriter()

    try:
        # Saari files ko open karein
        main_file = open(main_pdf_path, 'rb')
        file1 = open(pdf_1_path, 'rb')
        file2 = open(pdf_2_path, 'rb')
        file3 = open(pdf_3_path, 'rb')
        file4 = open(pdf_4_path, 'rb')

        # PDF Readers set up karein
        main_reader = PyPDF2.PdfReader(main_file)
        reader1 = PyPDF2.PdfReader(file1)
        reader2 = PyPDF2.PdfReader(file2)
        reader3 = PyPDF2.PdfReader(file3)
        reader4 = PyPDF2.PdfReader(file4)

        total_main_pages = len(main_reader.pages)
        print(f"Original PDF total pages: {total_main_pages}")

        # STEP 1: 1.pdf ko sab se pehle add karein
        print("Adding 1.pdf...")
        for page in reader1.pages:
            writer.add_page(page)

        # STEP 2: 2.pdf ko add karein
        print("Adding 2.pdf...")
        for page in reader2.pages:
            writer.add_page(page)

        # STEP 3: Original PDF ke sirf pehle 7 pages copy karein (1.pdf aur 2.pdf isme count NAHI ho rahe)
        print("Copying original pages 1 to 7...")
        pages_to_copy_first_part = min(7, total_main_pages)
        for i in range(pages_to_copy_first_part):
            writer.add_page(main_reader.pages[i]) # Yeh sirf original PDF se pages utha raha hai

        # STEP 4: Ab exact 7 original pages ke baad 3.pdf ko insert karein
        print("Inserting 3.pdf after original page 7...")
        for page in reader3.pages:
            writer.add_page(page)

        # STEP 5: Original PDF ke baqi bache hue pages add karein (Page 8 se lekar aakhir tak)
        if total_main_pages > 7:
            print("Copying remaining original pages...")
            for i in range(7, total_main_pages):
                writer.add_page(main_reader.pages[i])

        # STEP 6: 4.pdf ko sab se aakhir mein add karein
        print("Adding 4.pdf at the very end...")
        for page in reader4.pages:
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
        file4.close()

    except FileNotFoundError as e:
        print(f"\nError: Koi file nahi mili. Kripya paths check karein.\nDetail: {e}")
    except Exception as e:
        print(f"\nKoi error aagaya: {e}")

if __name__ == "__main__":
    merge_and_insert_pdf_pages()