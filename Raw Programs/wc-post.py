import re

# ============ Yahan apne file paths set karein ============
INPUT_PATH = r"C:\Users\PCS\Desktop\New Text Document.txt"
OUTPUT_PATH = r"C:\Users\PCS\Desktop\output.txt"
# ============================================================


def remove_all_classes(html: str) -> str:
    """Har tag se class="..." ya class='...' attribute hata deta hai."""
    return re.sub(r'\s*class=(["\']).*?\1', "", html)


def fix_outer_div(html: str) -> str:
    """
    Post ke pehle <div ...> tag ko
    <div class="wc-post" dir="rtl"> se replace karta hai.
    """
    return re.sub(r"<div\b[^>]*>", '<div class="wc-post" dir="rtl">', html, count=1)


def add_class_to_tags(html: str, tags, class_name: str) -> str:
    """
    Diye gaye tags (jaise h1,h2,h3,h4 ya ul,ol) ke opening tag mein
    class="class_name" add karta hai, chahe tag mein pehle se dusre
    attributes hon ya na hon.
    """
    pattern = re.compile(r"<(" + "|".join(tags) + r")((?:\s[^>]*)?)>")

    def repl(match):
        tag = match.group(1)
        rest = match.group(2) or ""
        return f'<{tag} class="{class_name}"{rest}>'

    return pattern.sub(repl, html)


def process_html(html: str) -> str:
    # Step 1: sari purani classes remove karo
    html = remove_all_classes(html)

    # Step 2: pehla div (post wrapper) fix karo
    html = fix_outer_div(html)

    # Step 3: h1,h2,h3,h4 mein wc-heading class add karo
    html = add_class_to_tags(html, ["h1", "h2", "h3", "h4"], "wc-heading")

    # Step 4: ul, ol mein wc-list class add karo
    html = add_class_to_tags(html, ["ul", "ol"], "wc-list")

    # Step 5: blockquote mein wc-quote class add karo
    html = add_class_to_tags(html, ["blockquote"], "wc-quote")

    return html


def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = process_html(content)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Ho gaya! Output file yahan save hui hai: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()