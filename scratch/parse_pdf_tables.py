import sys
import re
try:
    import pypdf
except ImportError:
    print("pypdf not installed")
    sys.exit(1)

def search_pdf_details(filename):
    print(f"\n=========================================")
    print(f"Reading PDF: {filename}")
    print(f"=========================================")
    reader = pypdf.PdfReader(filename)
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text:
            continue
        # Search for words like "градуир" or "регресс"
        if "градуир" in text.lower() or "регресс" in text.lower() or "мнк" in text.lower():
            lines = text.split("\n")
            for line in lines:
                if any(w in line.lower() for w in ["хлорид", "сульфат", "нитрат", "нитрит", "фторид", "фосфат"]) and any(w in line.lower() for w in ["0.", "0,", "1.", "1,", "2.", "2,", "5.", "5,", "уравн"]):
                    print(f"Page {i+1}: {line.strip()}")

if __name__ == '__main__':
    search_pdf_details("анионы, методичка.pdf")
    search_pdf_details("Практическое_руководство_по_использованию_систем_капиллярного_электрофореза.pdf")
