import pypdf

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from each page of a PDF and returns as a single string.
    """
    text = ""
    with open(pdf_path, 'rb') as f:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text
