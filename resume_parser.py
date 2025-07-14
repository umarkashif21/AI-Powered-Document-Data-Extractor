# resume_parser.py
import PyPDF2
from docx import Document
import re

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error extracting text from PDF {pdf_path}: {e}")
        return None
    return text

def extract_text_from_docx(docx_path):
    """Extracts text from a DOCX file."""
    text = ""
    try:
        doc = Document(docx_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        print(f"Error extracting text from DOCX {docx_path}: {e}")
        return None
    return text

def parse_resume_text(text):
    """
    Performs basic parsing of resume text to extract key information.
    This is a simplified example using regex and string matching.
    A real-world solution would use advanced NLP libraries (e.g., spaCy, NLTK).
    """
    extracted_data = {
        "name": None,
        "email": None,
        "phone": None,
        "skills": []
    }

    # Extract Email
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    if email_match:
        extracted_data["email"] = email_match.group(0)

    # Extract Phone Number (simplified, may need refinement for international formats)
    phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    if phone_match:
        extracted_data["phone"] = phone_match.group(0)

    # Extract Name (very basic, assumes name is at the top and before email/phone)
    # This is highly heuristic and might fail for many resumes.
    lines = text.split('\n')
    if lines:
        # Try to get the first non-empty line as name, if it doesn't look like an email/phone
        for line in lines:
            line = line.strip()
            if line and len(line) < 50 and not re.search(r'\d', line) and not '@' in line and not 'http' in line:
                extracted_data["name"] = line
                break
    
    # Extract Skills (very basic, looks for common skill keywords)
    # This would typically involve a predefined list of skills and more sophisticated matching.
    skill_keywords = [
        "Python", "JavaScript", "Java", "C++", "SQL", "PostgreSQL", "FastAPI", "Flask",
        "React", "Docker", "Git", "NLP", "Machine Learning", "Data Analysis", "API",
        "Web Scraping", "Automation", "AWS", "Azure", "GCP", "Agile", "Jira", "Trello", "Postman"
    ]
    
    found_skills = []
    text_lower = text.lower()
    for skill in skill_keywords:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    extracted_data["skills"] = list(set(found_skills)) # Remove duplicates

    return extracted_data