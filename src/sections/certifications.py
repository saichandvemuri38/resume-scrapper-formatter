

# =====================================================
# CERTIFICATIONS
# =====================================================

def parse_certifications(lines):
    return [l.lstrip("•").strip() for l in lines if l.startswith("•")]