import os
import PyPDF2
from docx import Document
import pandas as pd

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_text_from_txt(txt_path):
    with open(txt_path, "r", encoding="utf-8") as file:
        return file.read()

def extract_text(file_path):
    try:
        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".pdf":
            return extract_text_from_pdf(file_path)
        elif ext == ".docx":
            return extract_text_from_docx(file_path)
        elif ext == ".txt":
            return extract_text_from_txt(file_path)
        elif ext=='.xlsx':
            df = pd.read_excel(file_path)
            return df
        elif ext=='.csv':
            df = pd.read_csv(file_path)
            return df
        else:
            return "Unsupported file format!"
    except Exception as e:
        print(e)
        return -1
    

    
# if __name__ == '__main__':
#     print(extract_text('data/raw/documents/Sample_Abstract.pdf'))
#     print(extract_text('data/raw/documents/Sample_Manuscript.docx'))
#     print(extract_text('data/raw/documents/Sample_text.txt'))
#     print(extract_text('data/raw/documents/Issues_DS.xlsx'))