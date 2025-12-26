import re

from src.util.helpers_variables import EMAIL_REGEX, PHONE_REGEX

# =====================================================
# PROFILE
# =====================================================

def parse_profile(lines):
    text = " ".join(lines)
    profile = {}
    if m := EMAIL_REGEX.search(text):
        profile["email"] = m.group()
    if m := PHONE_REGEX.search(text):
        profile["phone"] = m.group()
    return profile