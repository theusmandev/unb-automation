#  Umera Ahmed Urdu Novel Blogger Post Generator

This Python script automatically generates **SEO-optimized Blogger HTML posts** for **Umera Ahmed’s Urdu novels**, complete with:

- 📖 *Read Online* (Google Drive embedded preview)  
- 📥 *PDF Download Link*  
- 🏷️ *SEO Labels & Description*  
- 🧠 *Auto-formatted HTML ready for Blogger posts*

It’s designed for bloggers who publish Urdu novels (especially Umera Ahmed’s works) and want to quickly create professional, formatted posts with just a **Google Drive link** and **novel title**.

---

## 🚀 Features

✅ Automatically extracts **Google Drive file ID**  
✅ Generates **preview** and **download** links  
✅ Embeds a **responsive iframe** for online reading  
✅ Creates **SEO-friendly labels**, **meta description**, and **tags**  
✅ Produces **copy-ready HTML** for Blogger  
✅ Simple interface using **IPython / Jupyter Notebook**

---

## 🧩 Example Output

**Input:**
```python
drive_link = "https://drive.google.com/file/d/1KuWwZVzzQk93sHLJEPZRWqCK3nLTxkbC/view?usp=drive_link"
novel_title = "Alif novel by Umera Ahmed"
generate_novel_post_for_blogger_umera_ahmed(drive_link, novel_title)
```

**Output:**
- 📄 Blogger embed HTML (ready to paste into your Blogger post)
- 🏷️ Labels for SEO
- 📝 Short SEO description

It automatically creates a beautiful blog post with headings, book details, iframe preview, and a download button.

---

## 🛠️ Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/<yourusername>/umera-ahmed-blogger-generator.git
   cd umera-ahmed-blogger-generator
   ```

2. **Install dependencies**
   ```bash
   pip install ipython
   ```

   *(Optional: use a Jupyter Notebook environment for best output formatting.)*

---

## 📘 Usage

Open a **Jupyter Notebook** or **Google Colab**, and run:

```python
from umera_ahmed_blogger import generate_novel_post_for_blogger_umera_ahmed

drive_link = "https://drive.google.com/file/d/1KuWwZVzzQk93sHLJEPZRWqCK3nLTxkbC/view"
novel_title = "Alif novel by Umera Ahmed"

generate_novel_post_for_blogger_umera_ahmed(drive_link, novel_title)
```

You’ll see three sections in output:

1. **📄 Blogger Embed Code** – Full HTML ready to paste into Blogger  
2. **🏷️ Blogger Labels** – Copy into Blogger’s Labels section  
3. **📝 SEO Description** – Copy into post meta description

---

## 🧠 How It Works

1. Extracts the **file ID** from your Google Drive link.  
2. Builds:
   - a **preview URL** → for the embedded viewer  
   - a **download URL** → for PDF download  
3. Generates structured HTML with:
   - Intro paragraphs about the novel  
   - Book details (title, author, format, etc.)  
   - Embedded `<iframe>` for preview  
   - SEO tags and labels  

---

## 🪶 Example Blogger Preview

```html
<h1>Alif novel by Umera Ahmed | Download PDF</h1>

<div class="novel-post">
  <p><b>Alif novel by Umera Ahmed</b> is one of the finest works by <b>Umera Ahmed</b> — ...</p>
  ...
  <iframe src="https://drive.google.com/file/d/1KuWwZVzzQk93sHLJEPZRWqCK3nLTxkbC/preview"></iframe>
  <a href="https://drive.google.com/uc?export=download&id=1KuWwZVzzQk93sHLJEPZRWqCK3nLTxkbC">📥 Download PDF</a>
</div>
```

---

## 💡 Customization

You can easily adapt this script for:
- Other Urdu authors (e.g., Nimra Ahmed, Hashim Nadeem)  
- Different themes or layouts (change the HTML structure)  
- Multilingual SEO (add English/Urdu descriptions)

---

## 📂 Project Structure

```
📁 umera-ahmed-blogger-generator/
├── umera_ahmed_blogger.py        # main script
├── example.ipynb                 # example notebook usage
└── README.md                     # project documentation
```

---

## 📜 License

This project is licensed under the **MIT License** — you’re free to modify, distribute, or use it for personal and commercial Blogger projects.

---

## ❤️ Credits

Developed by Usman
Inspired by Urdu literature & the works of **Umera Ahmed**

> "Her words touch hearts — now your blog can, too."
