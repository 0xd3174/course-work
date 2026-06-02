import os
import subprocess
import glob

def ocr_images():
    os.makedirs("scratch/ocr_results", exist_ok=True)
    images = glob.glob("data/*.JPG")
    
    for img_path in sorted(images):
        base_name = os.path.basename(img_path)
        name, _ = os.path.splitext(base_name)
        out_txt_path = f"scratch/ocr_results/{name}"
        
        print(f"Running OCR on {img_path} -> {out_txt_path}.txt ...")
        # Run tesseract
        try:
            # We specify both Russian and English languages
            subprocess.run([
                "tesseract",
                img_path,
                out_txt_path,
                "-l", "rus+eng",
                "--psm", "6" # Assume a single uniform block of text
            ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"Error OCR-ing {img_path}: {e.stderr.decode('utf-8', errors='replace')}")

if __name__ == '__main__':
    ocr_images()
