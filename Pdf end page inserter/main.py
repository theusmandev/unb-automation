import os
import fitz  # PyMuPDF

def add_endpage_with_links(folder_path):
    folder = os.path.abspath(folder_path)

    # Check folder
    if not os.path.isdir(folder):
        print("Error: Folder exist nahi karta.")
        return

    # Check endpage.pdf
    endpage_path = os.path.join(folder, "endpage.pdf")
    if not os.path.isfile(endpage_path):
        print("Error: endpage.pdf folder mein nahi mila.")
        return

    print("Endpage found:", endpage_path)

    # Open endpage PDF
    end_doc = fitz.open(endpage_path)
    end_src_page = end_doc[0]  # first page

    for file in os.listdir(folder):

        if file.lower().endswith(".pdf") and file != "endpage.pdf":
            pdf_path = os.path.join(folder, file)
            print(f"\nProcessing: {file}")

            try:
                novel = fitz.open(pdf_path)

                # Get last page size of novel
                last_page = novel[-1]
                target_rect = last_page.rect
                tw, th = target_rect.width, target_rect.height

                # Get source page size
                src_rect = end_src_page.rect
                sw, sh = src_rect.width, src_rect.height

                # Scaling factors
                scale_x = tw / sw
                scale_y = th / sh

                # Create new blank page with novel size
                new_page = novel.new_page(width=tw, height=th)

                # Insert the endpage PDF page (KEEPING LINKS)
                new_page.show_pdf_page(
                    target_rect,
                    end_doc,
                    0,
                    clip=None,
                    keep_proportion=False,
                    overlay=False
                )

                # Save temporary
                temp_path = pdf_path + ".tmp"
                novel.save(temp_path, incremental=False)
                novel.close()

                # Replace original
                os.remove(pdf_path)
                os.rename(temp_path, pdf_path)

                print("✔ Added end page with original clickable links preserved!")

            except Exception as e:
                print("❌ Error:", e)

    print("\nAll PDFs Updated Successfully!")


# Run
add_endpage_with_links(r"C:\Users\PCS\Downloads\ok")


