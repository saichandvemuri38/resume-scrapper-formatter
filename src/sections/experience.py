import re

from src.util.bullet_scoring import reorder_bullets
from src.util.helpers_variables import EXPERIENCE_HEADER_REGEX, KNOWN_SKILLS

# =====================================================
# EXPERIENCE (FIXED FOR YOUR RESUME)
# =====================================================

def parse_experience(lines):
    experiences = []
    current = None

    for line in lines:
        header = EXPERIENCE_HEADER_REGEX.match(line)

        if header:
            if current:
                current["summary"] = current["summary"]
                current["skills"] = sorted(current["skills"])
                experiences.append(current)

            current = {
                "title": header.group("title"),
                "company_name": header.group("company"),
                "location": header.group("location").strip() if header.group("location") else "",
                "duration": header.group("duration"),
                "summary": [],
                "skills": set()
            }

        elif current and line.startswith("•"):
            bullet = line.lstrip("•").strip()
            split_bullets = split_long_bullets([bullet])
            current["summary"].extend(reorder_bullets(split_bullets, current["skills"]))
            # print("Extracting skills from bullet:", current["title"], "->", bullet)
            extract_skills(bullet, current["skills"])

        elif current and EXPERIENCE_HEADER_REGEX.search(line):
            current["summary"] = " ".join(current["summary"])
            current["skills"] = sorted(current["skills"])
            experiences.append(current)
            current = None

    if current:
        current["summary"] = " ".join(current["summary"])
        current["skills"] = sorted(current["skills"])
        experiences.append(current)

    return experiences

def extract_skills(text, skill_set):
    for skill in KNOWN_SKILLS:
        if skill.lower() in text.lower():
            skill_set.add(skill)

def split_long_bullets(bullets):
    new_bullets = []

    for b in bullets:
        parts = [p.strip() for p in b.split(". ") if len(p.strip()) > 20]
        for p in parts:
            if not p.endswith("."):
                p += "."
            new_bullets.append(p)

    return new_bullets