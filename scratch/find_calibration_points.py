import sys

def search_transcript():
    print("Searching transcript for calibration points...")
    with open("/home/delta/.gemini/antigravity-cli/brain/2a743378-8ae4-4567-ac42-8774ba839725/.system_generated/logs/transcript_full.jsonl", "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f):
            # We look for lines containing "хлорид" and calibration-like numbers or regression calculations
            if "хлорид" in line.lower() and any(w in line.lower() for w in ["площад", "концентраци", "град", "мнк"]):
                # Print line number and a snippet
                snippet = line[:300] + "..." if len(line) > 300 else line
                print(f"Line {line_num+1}: {snippet.strip()}")

if __name__ == '__main__':
    search_transcript()
