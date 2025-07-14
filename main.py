# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import shutil

# Import functions from your other files
from resume_parser import extract_text_from_pdf, extract_text_from_docx, parse_resume_text
from database import create_resumes_table, insert_resume_data, get_db_connection

app = FastAPI(
    title="AI Resume Analyzer API",
    description="API for extracting and parsing information from resumes (PDF/DOCX) and storing it.",
    version="1.0.0"
)

# --- Pydantic Models for API Response ---
class ExtractedResumeData(BaseModel):
    file_name: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = []
    full_text_preview: str # A preview of the full text

# --- API Endpoints ---

@app.on_event("startup")
async def startup_event():
    """Ensures the database table exists when the FastAPI app starts."""
    print("Starting up: Ensuring 'resumes' table exists...")
    create_resumes_table()
    print("Startup complete.")

@app.post("/analyze-resume/", response_model=ExtractedResumeData, summary="Analyze and Extract Data from a Resume")
async def analyze_resume(file: UploadFile = File(...)):
    """
    Uploads a resume file (PDF or DOCX), extracts its text,
    parses key information, and stores the data in a PostgreSQL database.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in [".pdf", ".docx"]:
        raise HTTPException(status_code=400, detail="Unsupported file type. Only PDF and DOCX are supported.")

    # Create a temporary file to save the uploaded content
    temp_file_path = f"temp_{file.filename}"
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        full_text = None
        if file_extension == ".pdf":
            full_text = extract_text_from_pdf(temp_file_path)
        elif file_extension == ".docx":
            full_text = extract_text_from_docx(temp_file_path)

        if not full_text:
            raise HTTPException(status_code=500, detail="Failed to extract text from the resume file.")

        # Parse the extracted text
        parsed_data = parse_resume_text(full_text)

        # Convert skills list to a comma-separated string for database storage
        skills_str = ", ".join(parsed_data["skills"]) if parsed_data["skills"] else None

        # Store in database
        insert_resume_data(
            file.filename,
            parsed_data["name"],
            parsed_data["email"],
            parsed_data["phone"],
            skills_str,
            full_text
        )

        # Return a preview (first 500 chars) of the full text
        full_text_preview = full_text[:500] + "..." if len(full_text) > 500 else full_text

        return ExtractedResumeData(
            file_name=file.filename,
            name=parsed_data["name"],
            email=parsed_data["email"],
            phone=parsed_data["phone"],
            skills=parsed_data["skills"],
            full_text_preview=full_text_preview
        )

    except Exception as e:
        print(f"An error occurred during resume analysis: {e}")
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.get("/health", summary="Health Check")
async def health_check():
    """Checks the health of the API and database connection."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.close()
        conn.close()
        return {"status": "ok", "database_connection": "successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")