import pdfplumber
import re


def normalize_lines(lines):
    normalized = []
    buffer = ""

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # If line ends abruptly, likely broken sentence
        if (
            buffer
            and not buffer.endswith((".", "•"))
            and not line.startswith("•")
            and line[0].islower()
        ):
            buffer += " " + line
        else:
            if buffer:
                normalized.append(buffer)
            buffer = line

    if buffer:
        normalized.append(buffer)

    return normalized
    
def extract_text_from_pdf(pdf_path):
    lines = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text(
                x_tolerance=2,
                y_tolerance=3,
                layout=True
            )
            if page_text:
                lines.extend(page_text.split("\n"))

    return normalize_lines(lines)



def clean_bullets(lines):
    cleaned = []
    for line in lines:
        line = re.sub(r"^[•\-–]+", "•", line)
        cleaned.append(line)
    return cleaned
