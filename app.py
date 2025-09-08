from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import docx2txt
import pdfplumber
import re

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Keywords dictionary
ROLE_KEYWORDS = {
    "Data Analyst": [
        "excel", "sql", "power bi", "tableau", "python", "data analysis", "statistics",
        "pivot table", "data visualization", "numpy", "pandas", "matplotlib", "seaborn", "jupyter", "postgresql", "mysql"
    ],
    
    "AI Engineer": [
        "machine learning", "deep learning", "tensorflow", "pytorch", "nlp", "cv", "bert",
        "neural network", "transformer", "scikit-learn", "keras", "matplotlib", "pandas",
        "flask", "huggingface", "distilbert", "nltk", "text classification",
        "multi-class classification", "tokenization", "fine-tuning", "python"
    ],

    "Full Stack Developer": [
        "react", "node", "express", "django", "api", "javascript", "html", "css", "typescript",
        "mongodb", "postgresql", "mysql", "flask", "vite", "next.js", "redux", "tailwind", "bootstrap"
    ],
    
    "Software Engineer": [
        "c++", "java", "python", "data structures", "algorithms", "oop", "system design", "linux",
        "multithreading", "rest api", "mysql", "postgresql", "docker", "git", "flask", "socket programming"
    ]
}

AIML_KEYWORDS = [
    "machine learning", "deep learning", "nlp", "bert", "transformer",
    "classification", "regression", "sentiment analysis", "clustering"
]

FULLSTACK_KEYWORDS = [
    "html", "css", "javascript", "react", "django", "flask", "api", "node", "express",
    "postgresql", "mysql", "mongodb"
]

# Normalize text
def normalize(text):
    return re.sub(r'[^a-z0-9\s]', ' ', text.lower())

def match_keywords(text, keywords):
    text_clean = normalize(text)
    return [kw for kw in keywords if re.search(r'\b' + re.escape(kw.lower()) + r'\b', text_clean)]

# Extract text from file
def extract_text_from_file(filepath):
    text = ""
    if filepath.endswith(".pdf"):
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    elif filepath.endswith(".docx"):
        text = docx2txt.process(filepath)
    elif filepath.endswith(".txt"):
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

    return text

# Root route (important for Render)
@app.route("/")
def home():
    return jsonify({"message": "✅ SkillBridge Backend is live 🚀"})

# Resume parsing route
@app.route('/parse_resume', methods=['POST'])
def parse_resume():
    if 'resume' not in request.files or 'desired_role' not in request.form:
        return jsonify({'error': 'Missing resume file or desired role'}), 400

    file = request.files['resume']
    desired_role = request.form['desired_role']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        text = extract_text_from_file(filepath)

        aiml_highlights = match_keywords(text, AIML_KEYWORDS)
        fullstack_highlights = match_keywords(text, FULLSTACK_KEYWORDS)
        role_keywords = ROLE_KEYWORDS.get(desired_role, [])

        # Role-based matching
        if desired_role == "Full Stack Developer":
            matched_role_keywords = match_keywords(text, ROLE_KEYWORDS["Full Stack Developer"])
        elif desired_role == "AI Engineer":
            matched_role_keywords = match_keywords(text, ROLE_KEYWORDS["AI Engineer"])
        else:
            matched_role_keywords = match_keywords(text, role_keywords)

        match_count = len(matched_role_keywords)

        # Recommendation logic
        if match_count >= 8:
            recommendation = f"✅ You are a strong match for the role of {desired_role}!"
        elif 5 <= match_count < 8:
            recommendation = f"👍 You are a good match for the role of {desired_role}."
        else:
            suggested_roles = []
            if len(fullstack_highlights) >= 4 and desired_role != "Full Stack Developer":
                suggested_roles.append("Full Stack Developer")
            if len(aiml_highlights) >= 3 and desired_role != "AI Engineer":
                suggested_roles.append("AI Engineer")
            alt = ", ".join(suggested_roles) if suggested_roles else "other roles"
            recommendation = f"⚠️ Partial match. You may also consider applying for: {alt}."

        return jsonify({
            "desired_role": desired_role,
            "matched_keywords": matched_role_keywords,
            "match_count": match_count,
            "recommendation": recommendation
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(filepath)

if __name__ == '__main__':
    app.run(debug=True)
