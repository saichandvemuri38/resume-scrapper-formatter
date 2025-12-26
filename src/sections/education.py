import re



# =====================================================
# EDUCATION
# =====================================================
EDU_BLOCKLIST = [
    "university",
    "college",
    "bachelor",
    "master",
    "institute"
]

def looks_like_education(line):
    return any(k in line.lower() for k in EDU_BLOCKLIST)

def parse_education(lines):
    education = []
    current = {}

    for line in lines:
        clean = line.lstrip("•").strip()

        if looks_like_education(clean):
            if current:
                education.append(current)
            current = {
                "degree": clean,
                "school": "",
                "location": ""
            }
        elif "University" in clean or "College" in clean or "Institute" in clean:
            current["school"] = clean
        elif "," in clean and len(clean.split(",")) <= 3:
            current["location"] = clean

    if current:
        education.append(current)

    return education
