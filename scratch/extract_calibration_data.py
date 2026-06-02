import os
import re

def parse_file(filepath):
    print(f"\nParsing {filepath}:")
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Let's find all numbers in the lines that look like table rows
    lines = content.split('\n')
    for line in lines:
        # If line contains numbers and looks like a table row (e.g. starting with № or number)
        if re.search(r'\d', line):
            print(f"  {line.strip()}")

if __name__ == '__main__':
    for anion in ['хлорид', 'нитрит', 'сульфат', 'нитрат', 'фторид', 'фосфат']:
        for i in [1, 2]:
            filepath = f"scratch/ocr_results/{anion}{i}.txt"
            if os.path.exists(filepath):
                parse_file(filepath)
