import pandas as pd

def generate_blogger_post(excel_file, output_file):
    # Excel فائل پڑھیں
    df = pd.read_excel(excel_file)

    # Blogger Post HTML شروع (CSS سمیت)
    html = """
<div id="blogger-novel-requests">
    <style type="text/css">
        #blogger-novel-requests {
            max-width: 960px;
            margin: 32px auto;
            background: #ffffff;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        #blogger-novel-requests h3 {
            font-size: 1.75rem;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 20px;
            text-align: center;
        }
        #blogger-novel-requests .request-item {
            padding: 16px;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            background: #f9fafb;
            margin-bottom: 12px;
        }
        #blogger-novel-requests .request-item p {
            margin: 4px 0;
            font-size: 0.95rem;
        }
        #blogger-novel-requests .status-pending {
            color: #f59e0b;
            font-weight: 600;
        }
        #blogger-novel-requests .status-fulfilled {
            color: #10b981;
            font-weight: 600;
        }
        #blogger-novel-requests .status-system-error-not-found {
            color: #ef4444;
            font-weight: 600;
        }
        #blogger-novel-requests .download-button {
            display: inline-block;
            padding: 8px 16px;
            background-color: #10b981;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            font-weight: 500;
            transition: background-color 0.3s;
        }
        #blogger-novel-requests .download-button:hover {
            background-color: #0e8f6a;
        }
    </style>
    <h3>Novel Requests Status</h3>
    <div class="requestsList">
    """

    # ہر row کو HTML میں شامل کریں
    for _, row in df.iterrows():
        novel_name = str(row.get("Novel Name", "")).strip()
        author_name = str(row.get("Author Name", "")).strip()
        status = str(row.get("Status", "Pending")).strip()
        download_link = str(row.get("downloadLink", "")).strip()  # Case-sensitive match with column name

        # Determine the status class based on the status value
        if status == "System Error- Not Found":
            status_class = "system-error-not-found"
        elif status.lower() == "pending":
            status_class = "pending"
        elif status.lower() == "fulfilled":
            status_class = "fulfilled"
        else:
            status_class = "pending"  # Default to pending if status is unrecognized

        html += f"""
        <div class="request-item">
            <p><strong>Novel Name:</strong> {novel_name}</p>
            <p><strong>Author Name:</strong> {author_name}</p>
            <p><strong>Status:</strong> <span class="status-{status_class}">{status}</span></p>
        """

        if status.lower() == "fulfilled" and download_link:
            html += f"""<p><strong>Download Link:</strong> <a href="{download_link}" target="_blank" class="download-button">Download</a></p>"""

        html += "</div>\n"

    # HTML بند کریں
    html += """
    </div>
</div>
    """

    # Output HTML فائل میں لکھیں
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Blogger post HTML generated successfully → {output_file}")


# 👇 یہاں اپنے input (Excel) اور output (HTML) فائل کے path دیں
excel_input_path = r"C:\Users\PCS\Downloads\Novel Requests.xlsx"
html_output_path = r"D:\-UNB\Segments\Novel Request\Novel Requests.txt"

generate_blogger_post(excel_input_path, html_output_path)