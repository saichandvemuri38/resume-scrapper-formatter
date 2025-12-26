import re
from pathlib import Path
from src.pdf_extractor.plumber import extract_text_from_pdf
from src.pdf_extractor.plumber import clean_bullets
from src.sections.certifications import parse_certifications
from src.sections.education import parse_education
from src.sections.experience import parse_experience
from src.sections.profile import parse_profile
from src.sections.projects import parse_projects
from src.sections.skills import parse_skills
from src.util.helpers_variables import DATE_ONLY_REGEX, EXPERIENCE_HEADER_REGEX

# =====================================================
# MAIN ENTRY
# =====================================================

def parse_resume(file_path: str) -> dict:
    # raw_text = extract_text(file_path)
    lines = clean_bullets(extract_text_from_pdf(file_path))

    sections = detect_sections(lines)

    experience_lines = normalize_experience_lines(sections.get("experience", []))
    experience_lines = merge_broken_bullets(experience_lines)
    skill_sources = (
        sections.get("skills", [])
        + sections.get("experience", [])
        + sections.get("projects", [])
    )
    return {
        "raw_text": lines,
        "sections": {
            "profile": parse_profile(lines),
            "skills": parse_skills(skill_sources),
            "experience": parse_experience(experience_lines),
            "education": parse_education(sections.get("education", [])),
            "projects": parse_projects(sections.get("projects", [])),
            "certifications": parse_certifications(sections.get("certifications", []))
        }
    }

# =====================================================
# TEXT NORMALIZATION
# =====================================================

def normalize_experience_lines(lines):
    """
    Attach date-only lines to the following role/company line
    """
    normalized = []
    pending_date = None

    for line in lines:
        if DATE_ONLY_REGEX.match(line):
            pending_date = line
            continue

        if pending_date and "," in line:
            normalized.append(f"{line} {pending_date}")
            pending_date = None
        else:
            normalized.append(line)

    return normalized

def merge_broken_bullets(lines):
    merged = []
    buffer = ""

    for line in lines:
        # experience header → flush buffer
        if EXPERIENCE_HEADER_REGEX.match(line):
            if buffer:
                merged.append(buffer.strip())
                buffer = ""
            merged.append(line)
            continue

        if line.startswith("•"):
            if buffer:
                merged.append(buffer.strip())
            buffer = line
        else:
            buffer += " " + line

    if buffer:
        merged.append(buffer.strip())

    return merged

# =====================================================
# SECTION DETECTION
# =====================================================

SECTION_HEADERS = {
    "summary": ["summary"],
    "skills": ["skills"],
    "experience": ["professional experience","work experience","experience"],
    "education": ["education"],
    "projects": ["projects"],
    "certifications": ["certifications"]
}

def detect_sections(lines):
    sections = {}
    current = "other"
    sections[current] = []

    for line in lines:
        header = detect_header(line)
        if header:
            current = header
            sections[current] = []
        else:
            sections[current].append(line)

    return sections

def detect_header(line):
    l = line.lower()
    if len(l) > 40:
        return None
    for section, keywords in SECTION_HEADERS.items():
        if any(k in l for k in keywords):
            return section
    return None










