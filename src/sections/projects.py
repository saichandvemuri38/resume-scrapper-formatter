

from src.sections.education import looks_like_education


def parse_projects(lines):
    projects = []
    current = None

    for line in lines:
        clean = line.strip()

        # ⛔ Skip education leakage
        if looks_like_education(clean):
            continue

        if not clean.startswith("•"):
            current = {
                "name": clean,
                "description": []
            }
            projects.append(current)
        elif current:
            current["description"].append(clean.lstrip("•").strip())

    return projects