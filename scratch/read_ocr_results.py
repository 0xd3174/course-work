import os
import glob

def print_ocr_results():
    txt_files = glob.glob("scratch/ocr_results/*.txt")
    for filepath in sorted(txt_files):
        print(f"\n=========================================")
        print(f"FILE: {filepath}")
        print(f"=========================================")
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[:30]: # print first 30 lines
                print(line.strip())

if __name__ == '__main__':
    print_ocr_results()
