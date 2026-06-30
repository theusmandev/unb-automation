"""
inp_hex_dump.py

Yeh script aapki InPage (.inp) file ko binary mode mein parhta hai aur
uska hex dump (saath mein readable ASCII preview) ek .txt file mein
save kar deta hai. Iska maqsad sirf yeh dekhna hai ke .inp file ke
andar text kis tarah store hota hai (taake aage chal kar search/
page-finder script bana sakein).

Usage:
    1) Neeche INP_PATH apni .inp file ka path daal dein
    2) python inp_hex_dump.py
    3) Output OUTPUT_TXT file mein milega
"""

INP_PATH = r"E:\unb-workstation\InPage DNA\DNA\NEW VERSION\urdu words finder.INP"    # apni .inp file ka path
OUTPUT_TXT = r"C:\Users\PCS\Desktop\inp_hexdump.txt"    # hex dump kahan save karna hai

# Kitne bytes dump karne hain (None = poori file, ya koi number jaise 2000)
MAX_BYTES = 2000

BYTES_PER_LINE = 16


def make_ascii_preview(chunk):
    """Har byte ko printable ASCII character ya '.' mein convert karta hai."""
    preview = ""
    for b in chunk:
        if 32 <= b <= 126:
            preview += chr(b)
        else:
            preview += "."
    return preview


def dump_hex(input_path, output_path, max_bytes=None):
    with open(input_path, "rb") as f:
        data = f.read(max_bytes) if max_bytes else f.read()

    total_size = len(data)
    lines = []
    lines.append(f"File: {input_path}")
    lines.append(f"Dumped bytes: {total_size} (file ka size in mein zyada bhi ho sakta hai agar MAX_BYTES limit lagayi gayi ho)")
    lines.append("-" * 70)

    for offset in range(0, total_size, BYTES_PER_LINE):
        chunk = data[offset:offset + BYTES_PER_LINE]
        hex_part = " ".join(f"{b:02X}" for b in chunk)
        hex_part_padded = hex_part.ljust(BYTES_PER_LINE * 3 - 1)
        ascii_part = make_ascii_preview(chunk)
        lines.append(f"{offset:08X}  {hex_part_padded}  |{ascii_part}|")

    with open(output_path, "w", encoding="utf-8") as out:
        out.write("\n".join(lines))

    print(f"Hex dump ban gaya: {output_path}")
    print(f"Total {total_size} bytes dump hue.")


if __name__ == "__main__":
    dump_hex(INP_PATH, OUTPUT_TXT, MAX_BYTES)