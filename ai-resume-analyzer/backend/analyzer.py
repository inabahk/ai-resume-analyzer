import re
from typing import Dict, Any, List

SKILL_KEYWORDS = {
    "Languages": ["python", "javascript", "typescript", "java", "c++", "c#", "go", "rust", "ruby", "php", "swift", "kotlin", "scala", "r", "matlab"],
    "AI/ML": ["machine learning", "deep learning", "neural network", "nlp", "computer vision", "pytorch", "tensorflow", "keras", "scikit-learn", "hugging face", "llm", "transformer", "bert", "gpt", "reinforcement learning", "xgboost", "pandas", "numpy"],
    "Web": ["react", "angular", "vue", "node.js", "django", "flask", "fastapi", "express", "spring", "rest api", "graphql", "html", "css"],
    "Cloud & DevOps": ["aws", "gcp", "azure", "docker", "kubernetes", "terraform", "ci/cd", "jenkins", "github actions", "linux", "bash"],
    "Databases": ["sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "sqlite", "dynamodb", "cassandra"],
    "Data": ["spark", "hadoop", "airflow", "dbt", "tableau", "power bi", "excel", "data pipeline", "etl"],
}

SECTION_PATTERNS = {
    "contact": r"(email|phone|linkedin|github|portfolio|contact)",
    "education": r"(education|degree|university|college|bachelor|master|phd|b\.s\.|m\.s\.)",
    "experience": r"(experience|work|employment|job|position|role|intern)",
    "skills": r"(skills|technologies|tools|stack|competencies)",
    "projects": r"(projects|portfolio|work samples|built|developed)",
    "achievements": r"(achievements|awards|certifications|honors|publications)",
}

ACTION_VERBS = ["built", "developed", "designed", "led", "managed", "created", "implemented", "optimized",
                "deployed", "analyzed", "improved", "reduced", "increased", "automated", "architected",
                "collaborated", "delivered", "launched", "scaled", "migrated", "integrated"]

def extract_skills(text: str) -> Dict[str, List[str]]:
    text_lower = text.lower()
    found = {}
    for category, skills in SKILL_KEYWORDS.items():
        matched = [s for s in skills if s in text_lower]
        if matched:
            found[category] = matched
    return found

def detect_sections(text: str) -> List[str]:
    text_lower = text.lower()
    found = []
    for section, pattern in SECTION_PATTERNS.items():
        if re.search(pattern, text_lower):
            found.append(section)
    return found

def score_resume(text: str, skills: dict, sections: list) -> Dict[str, Any]:
    scores = {}
    text_lower = text.lower()

    # Skills score (0-25)
    total_skills = sum(len(v) for v in skills.values())
    scores["skills"] = min(25, total_skills * 2)

    # Sections score (0-20)
    scores["sections"] = min(20, len(sections) * 4)

    # Action verbs (0-20)
    verb_count = sum(1 for v in ACTION_VERBS if v in text_lower)
    scores["impact_language"] = min(20, verb_count * 3)

    # Length & detail (0-15)
    word_count = len(text.split())
    if word_count < 100:
        scores["length"] = 5
    elif word_count < 300:
        scores["length"] = 10
    else:
        scores["length"] = 15

    # Quantification (0-20)
    numbers = re.findall(r'\b\d+[%+]?\b', text)
    scores["quantification"] = min(20, len(numbers) * 3)

    total = sum(scores.values())
    return {"breakdown": scores, "total": total}

def generate_suggestions(text: str, skills: dict, sections: list, scores: dict) -> List[str]:
    suggestions = []
    text_lower = text.lower()

    if "experience" not in sections:
        suggestions.append("Add a clear Work Experience section with job titles, companies, and dates.")
    if "education" not in sections:
        suggestions.append("Add your Education section with degree, institution, and graduation year.")
    if "skills" not in sections:
        suggestions.append("Add a dedicated Skills section to make it easy for ATS systems to find your tech stack.")
    if "projects" not in sections:
        suggestions.append("Add a Projects section — especially important for AI/ML roles to show practical work.")

    verb_count = sum(1 for v in ACTION_VERBS if v in text_lower)
    if verb_count < 3:
        suggestions.append("Use strong action verbs like 'Built', 'Optimized', 'Deployed' to describe your work.")

    numbers = re.findall(r'\b\d+[%+]?\b', text)
    if len(numbers) < 3:
        suggestions.append("Quantify your impact: e.g. 'Reduced latency by 40%' or 'Trained model on 1M+ samples'.")

    if not skills.get("AI/ML"):
        suggestions.append("Highlight AI/ML tools you've used (PyTorch, TensorFlow, Hugging Face, etc.) for AI/ML roles.")
    if not skills.get("Cloud & DevOps"):
        suggestions.append("Mention cloud/deployment experience (AWS, GCP, Docker) — critical for production AI roles.")

    if len(text.split()) < 300:
        suggestions.append("Your resume seems short. Expand on your projects and responsibilities with more detail.")

    return suggestions[:6]

def analyze_resume(text: str) -> Dict[str, Any]:
    skills = extract_skills(text)
    sections = detect_sections(text)
    score_data = score_resume(text, skills, sections)
    suggestions = generate_suggestions(text, skills, sections, score_data)

    word_count = len(text.split())
    total_skills = sum(len(v) for v in skills.values())

    grade = "A" if score_data["total"] >= 80 else "B" if score_data["total"] >= 65 else "C" if score_data["total"] >= 50 else "D"

    return {
        "overall_score": score_data["total"],
        "grade": grade,
        "score_breakdown": score_data["breakdown"],
        "detected_skills": skills,
        "detected_sections": sections,
        "suggestions": suggestions,
        "stats": {
            "word_count": word_count,
            "total_skills_found": total_skills,
            "sections_found": len(sections),
            "action_verbs_found": sum(1 for v in ACTION_VERBS if v in text.lower()),
        }
    }
