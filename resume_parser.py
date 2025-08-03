import docx2txt
import PyPDF2

ROLE_KEYWORDS = {
    "Data Analyst": ["excel", "sql", "power bi", "data visualization", "statistics", "python"],
    "AI Engineer": ["machine learning", "deep learning", "pytorch", "tensorflow", "nlp", "cv"],
    "Full Stack Developer": ["react", "node", "javascript", "django", "api", "sql", "html", "css"],
    "Software Engineer": ["c++", "java", "data structures", "algorithms", "oop", "system design"],
}

def extract_text_from_file(file_path):
    if file_path.endswith(".pdf"):
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            return " ".join(page.extract_text() for page in reader.pages if page.extract_text())
    elif file_path.endswith(".docx"):
        return docx2txt.process(file_path)
    return ""

def match_role(text, desired_role):
    text_lower = text.lower()
    keywords = ROLE_KEYWORDS.get(desired_role, [])
    matched = [kw for kw in keywords if kw in text_lower]
    match_percent = int((len(matched) / len(keywords)) * 100) if keywords else 0
    return match_percent, matched

def parse_resume(file_path, desired_role="Data Analyst"):
    text = extract_text_from_file(file_path)
    percent, matched_keywords = match_role(text, desired_role)
    recommendation = "Good match!" if percent >= 60 else "Partial match or consider another role."

    return {
        "desired_role": desired_role,
        "match_percent": percent,
        "matched_keywords": matched_keywords,
        "recommendation": recommendation
    }
