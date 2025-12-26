import re
# =====================================================
# REGEX DEFINITIONS
# =====================================================

DATE_ONLY_REGEX = re.compile(
    r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|\w+)\s+\d{4}\s*[–-]\s*(Present|\w+\s+\d{4})$"
)

EXPERIENCE_HEADER_REGEX = re.compile(
    r"""
    ^(?P<title>[^,]+),\s*
    (?P<company>[^,]+),\s*
    (?P<location>[A-Za-z\s]+)\s+
    (?P<duration>(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|\w+)\s+\d{4}\s*[–-]\s*(Present|\w+\s+\d{4}))
    """,
    re.VERBOSE
)

EMAIL_REGEX = re.compile(r"[\w\.-]+@[\w\.-]+")
PHONE_REGEX = re.compile(r"\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b")

KNOWN_SKILLS = {
    "Java","Spring Boot","Kafka","React","Redux","Python","AWS","Docker",
    "Kubernetes","JPA","Hibernate","CI/CD","TypeScript","Next.js",
    "Redis","JUnit","Agile","Scrum","SQL","NoSQL"
}