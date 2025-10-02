#!/usr/bin/env python3
"""
Simple PDF extraction script
"""
import os
import sys
import subprocess

def try_pdftotext(pdf_path):
    """Try using pdftotext if available"""
    try:
        result = subprocess.run(['pdftotext', pdf_path, '-'], 
                              capture_output=True, text=True, check=True)
        return result.stdout
    except:
        return None

def try_python_pdf_extract(pdf_path):
    """Try using Python libraries"""
    try:
        # Try to install and import PyPDF2
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'PyPDF2'], 
                      capture_output=True, check=True)
        
        import PyPDF2
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(min(5, len(reader.pages))):  # First 5 pages
                page = reader.pages[page_num]
                text += f"=== Page {page_num + 1} ===\n"
                text += page.extract_text() + "\n\n"
            return text
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """Extract text from PDFs"""
    base_path = "/Users/alex/Documents/Personal projects/KIOSK/KIOSK/docs"
    
    files = [
        ("P_Full_Domain_Model.pdf", "Domain Model"),
        ("P_initial requirements.pdf", "Requirements"),
        ("P_Tech stack overview.pdf", "Tech Stack")
    ]
    
    for filename, description in files:
        pdf_path = os.path.join(base_path, filename)
        if os.path.exists(pdf_path):
            print(f"\n{'='*60}")
            print(f"EXTRACTING: {description}")
            print(f"{'='*60}")
            
            # Try pdftotext first
            text = try_pdftotext(pdf_path)
            if text and len(text.strip()) > 10:
                print("Method: pdftotext")
                print(text[:2000])
                print("\n[Content truncated]\n")
                continue
            
            # Try Python extraction
            text = try_python_pdf_extract(pdf_path)
            if text and len(text.strip()) > 10:
                print("Method: PyPDF2")
                print(text[:2000])
                print("\n[Content truncated]\n")
            else:
                print("Failed to extract text")
                
        else:
            print(f"File not found: {pdf_path}")

if __name__ == "__main__":
    main()