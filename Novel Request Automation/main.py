import pandas as pd

def generate_blogger_post(excel_file, output_file):
    # 1. Excel File Read karein
    # (fillna('') is liye use kia taake nan/empty cells string ban jayen)
    df = pd.read_excel(excel_file).fillna('')

    # 2. HTML Start (Header, Fonts, CSS)
    # Note: Python f-string mein CSS ke { } ko {{ }} likhna parta hai.
    html_part_1 = """
<link href="https://fonts.googleapis.com/css2?family=Gulzar&family=Poppins:wght@400;500;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">

<style>
    /* --- Main Container --- */
    #novel-requests-container {
        max-width: 1100px;
        margin: 40px auto;
        font-family: 'Poppins', sans-serif;
        box-sizing: border-box;
    }

    .requests-header {
        text-align: center;
        margin-bottom: 40px;
    }
    
    .requests-header h2 {
        font-size: 2.2rem;
        color: #1e293b;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 0;
    }

    /* --- Grid Layout --- */
    .requests-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 25px;
        padding: 10px;
    }

    /* --- Card Styling --- */
    .request-card {
        background: #ffffff;
        border-radius: 16px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        border: 1px solid #f1f5f9;
        border-top: 6px solid #10b981; /* Default Green */
    }

    .request-card:hover {
        transform: translateY(-7px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.1);
    }

    /* --- Top Status --- */
    .card-top {
        padding: 15px 20px 0;
        display: flex;
        justify-content: flex-end;
    }

    .status-badge {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        padding: 4px 12px;
        border-radius: 20px;
        letter-spacing: 0.5px;
    }
    .status-fulfilled { background: #d1fae5; color: #047857; }
    .status-pending { background: #fef3c7; color: #b45309; }
    .status-error { background: #fee2e2; color: #b91c1c; }

    /* --- Content --- */
    .card-content {
        padding: 10px 20px 25px;
        text-align: center;
    }

    .novel-title {
        font-size: 1.5rem;
        color: #111827;
        font-weight: 800;
        line-height: 1.3;
        margin-bottom: 8px;
        display: block;
    }

    .author-wrapper {
        display: inline-block;
        background-color: #f3f4f6;
        padding: 5px 15px;
        border-radius: 50px;
        margin-top: 5px;
    }

    .author-name {
        font-size: 0.95rem;
        color: #4b5563;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .author-icon { color: #10b981; font-size: 0.8rem; }

    /* --- Action Area --- */
    .card-action {
        padding: 20px;
        background-color: #f8fafc;
        border-top: 1px solid #e2e8f0;
        display: flex;
        justify-content: center; 
        align-items: center;
        flex-direction: column;
    }

    .download-btn {
        display: inline-block;
        min-width: 180px;
        max-width: 90%;
        background: #10b981;
        color: #ffffff !important;
        text-align: center;
        padding: 12px 24px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: 600;
        font-size: 1rem;
        transition: background 0.2s, transform 0.2s;
        box-shadow: 0 4px 6px rgba(16, 185, 129, 0.2);
    }
    
    .download-btn:hover {
        background: #059669;
        box-shadow: 0 6px 15px rgba(16, 185, 129, 0.4);
        transform: scale(1.02);
    }

    .message-text {
        font-size: 0.85rem;
        color: #b45309; /* Default brownish for pending */
        text-align: center;
        margin-bottom: 10px;
        font-weight: 500;
        line-height: 1.4;
    }

    /* --- Urdu Footer --- */
    .urdu-notice {
        margin-top: 50px;
        background: linear-gradient(to right, #f0fdf4, #ffffff);
        border: 1px solid #bbf7d0;
        padding: 25px;
        border-radius: 12px;
        text-align: right;
        direction: rtl;
    }
    .urdu-font {
        font-family: 'Gulzar', serif;
        font-size: 1.4rem;
        color: #1e293b;
        line-height: 1.8;
        margin: 0;
    }
    
    @media (max-width: 600px) {
        .requests-grid { grid-template-columns: 1fr; }
        .download-btn { width: 80%; }
    }
</style>

<div id="novel-requests-container">
    
    <div class="requests-header">
        <h2>Requested Novels</h2>
    </div>

    <div class="requests-grid">
"""

    cards_html = ""

    # 3. Loop through DataFrame to generate Cards
    for index, row in df.iterrows():
        # Data Cleaning
        novel_name = str(row.get("Novel Name", "Unknown Novel")).strip()
        author_name = str(row.get("Author Name", "Unknown Author")).strip()
        raw_status = str(row.get("Status", "Pending")).strip()
        download_link = str(row.get("downloadLink", "")).strip()
        
        # --- LOGIC FOR STYLING ---
        status_lower = raw_status.lower()
        
        # Default Variables
        border_color_hex = "#f59e0b" # Yellow (Pending)
        badge_class = "status-pending"
        badge_text = "Pending"
        action_html = "" # Will contain button or text

        # 1. Fulfilled Logic (Green)
        if "fulfilled" in status_lower:
            border_color_hex = "#10b981"
            badge_class = "status-fulfilled"
            badge_text = "Fulfilled"
            
            # Agar link hai to button dikhao
            if download_link and download_link.lower() != "nan":
                action_html = f'<a href="{download_link}" class="download-btn" target="_blank" rel="noopener noreferrer">Download PDF</a>'
            else:
                action_html = '<p class="message-text" style="color:#047857;">Uploaded (Link coming soon)</p>'

        # 2. Error / Not Found Logic (Red)
        elif "error" in status_lower or "not found" in status_lower or "not recommended" in status_lower:
            border_color_hex = "#ef4444"
            badge_class = "status-error"
            
            if "not recommended" in status_lower:
                badge_text = "Not Recommended"
            else:
                badge_text = "Not Found"
                
            action_html = f'<p class="message-text" style="color:#ef4444;">{raw_status}</p>'

        # 3. Pending / App Link / Other Message (Yellow/Orange)
        else:
            # Ye 'Else' wo cases handle karega jese "Available on Official App"
            border_color_hex = "#f59e0b"
            badge_class = "status-pending"
            
            if "app" in status_lower:
                badge_text = "App Only"
            else:
                badge_text = "Pending"
            
            # Show the raw status text as a message
            action_html = f'<p class="message-text">{raw_status}</p>'
            
            # Agar status pending hai lekin phir bhi koi link column me para hai (e.g. App Link)
            if download_link and download_link.lower() != "nan":
                btn_text = "Open Link"
                if "app" in status_lower:
                    btn_text = "Get App"
                action_html += f'<a href="{download_link}" class="download-btn" style="background:#f59e0b; margin-top:5px;" target="_blank" rel="nofollow">{btn_text}</a>'

        # --- BUILDING THE CARD HTML ---
        cards_html += f"""
        <article class="request-card" style="border-top-color: {border_color_hex};">
            <div class="card-top">
                <span class="status-badge {badge_class}">{badge_text}</span>
            </div>
            <div class="card-content">
                <h3 class="novel-title">{novel_name}</h3>
                <div class="author-wrapper">
                    <span class="author-name"><i class="fas fa-feather-alt author-icon"></i> {author_name}</span>
                </div>
            </div>
            <div class="card-action">
                {action_html}
            </div>
        </article>
        """

    # 4. Closing HTML
    html_part_end = """
    </div> <div class="urdu-notice">
        <p class="urdu-font">
            ⚠️ <strong>نوٹ:</strong> یاد رکھیں! یہاں صرف وہی ناولز دستیاب ہیں جو PDF فارمیٹ میں موجود ہیں۔ جن ناولز کو مصنف یا مصنفہ نے PDF میں شائع نہیں کیا، براہِ کرم اُن ناولز کو ہارڈ فارم میں خرید کر مصنفین کو سپورٹ کریں۔ شکریہ!
        </p>
    </div>

</div>
    """

    # Final Write
    final_html = html_part_1 + cards_html + html_part_end
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"🎉 New Design HTML Generated successfully at: {output_file}")


# 👇 APNA FILE PATH YAHAN CHECK KAREIN
excel_input_path = r"C:\Users\PCS\Downloads\Untitled spreadsheet.xlsx"
html_output_path = r"C:\Users\PCS\Downloads\Novel Requests.txt"

# Function Run karein
generate_blogger_post(excel_input_path, html_output_path)