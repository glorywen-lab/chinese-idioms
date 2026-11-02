import re

def analyze_ocr(filepath):
    lines = []
    with open(filepath, "r", encoding="utf-8") as f:
        for l in f:
            match = re.match(r"\[\[.*?\]\]: (.*?) \((.*?)\)", l.strip())
            if match:
                text = match.group(1).strip()
                lines.append(text)
    return lines

p3 = analyze_ocr("debug_logs/ocr_page_3.txt")
p4 = analyze_ocr("debug_logs/ocr_page_4.txt")

with open("debug_logs/parsed_p3_p4.txt", "w", encoding="utf-8") as f:
    f.write("=== PAGE 3 (Printed P.8 & P.9) ===\n")
    f.write("\n".join(p3))
    f.write("\n\n=== PAGE 4 (Printed P.10 & P.11) ===\n")
    f.write("\n".join(p4))

print("Saved parsed_p3_p4.txt, P3 count:", len(p3), "P4 count:", len(p4))
