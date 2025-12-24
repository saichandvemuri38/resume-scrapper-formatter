import PyPDF2
import spacy

# Load the NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    # Fallback if model isn't downloaded
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    """Reads a PDF and returns the full text string."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def get_keywords(text):
    """Extracts nouns and proper nouns as basic keywords."""
    doc = nlp(text)
    keywords = set([token.text.lower() for token in doc if token.pos_ in ["NOUN", "PROPN"]])
    return list(keywords)