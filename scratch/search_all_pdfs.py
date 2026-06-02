import sys
try:
    import pypdf
except ImportError:
    print("pypdf not installed")
    sys.exit(1)

def extract_and_search(filename, keywords):
    print(f"\nReading {filename}...")
    reader = pypdf.PdfReader(filename)
    print(f"Total pages: {len(reader.pages)}")
    
    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text:
            continue
        
        for kw in keywords:
            if kw.lower() in text.lower():
                print(f"--- Match on page {page_num + 1} for '{kw}': ---")
                lines = text.split("\n")
                for line in lines:
                    if kw.lower() in line.lower():
                        print(f"  {line.strip()}")

if __name__ == '__main__':
    keywords = ["0.1248", "0,1248", "0.1531", "0,1531", "0.1600", "0,1600", "0.2004", "0,2004", "0.0445", "0,0445", "0.1009", "0,1009"]
    extract_and_search("анионы, методичка.pdf", keywords)
    extract_and_search("Практическое_руководство_по_использованию_систем_капиллярного_электрофореза.pdf", keywords)
