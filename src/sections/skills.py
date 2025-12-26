
import re

from src.util.helpers_variables import KNOWN_SKILLS

# =====================================================
# SKILLS
# =====================================================

def parse_skills(lines):
    skills = set()

    for line in lines:
        # Explicit SKILLS section
        if ":" in line:
            _, rest = line.split(":", 1)
            tokens = re.split(r"[,\|/]", rest)
            for t in tokens:
                t = t.strip()
                for skill in KNOWN_SKILLS:
                    if skill.lower() == t.lower():
                        skills.add(skill)

        # Experience / project inference
        for skill in KNOWN_SKILLS:
            if skill.lower() in line.lower():
                skills.add(skill)

    return sorted(skills)


