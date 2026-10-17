
import json

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pymupdf

from database import SessionLocal
from database_models import ResumeAnalysis
from matcher import compare_skills

app = FastAPI(title="AI Resume Analyzer")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "AI Resume Analyzer API is running!"}


@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    if not resume.filename or not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF resume."
        )

    try:
        pdf_bytes = await resume.read()

        with pymupdf.open(stream=pdf_bytes, filetype="pdf") as pdf:
            resume_text = "\n".join(
                page.get_text() for page in pdf
            ).strip()

        if not resume_text:
            raise HTTPException(
                status_code=400,
                detail="No text found in the PDF. The file may be scanned."
            )

        try:
            result = compare_skills(resume_text, job_description)
        except ValueError as error:
            raise HTTPException(
                status_code=422,
                detail=str(error),
            ) from error

        db = None
        try:
            db = SessionLocal()
            analysis = ResumeAnalysis(
                filename=resume.filename,
                job_description=job_description,
                match_percentage=result["match_percentage"],
                matched_skills=json.dumps(result["matched_skills"]),
                missing_skills=json.dumps(result["missing_skills"]),
            )
            db.add(analysis)
            db.commit()
        except Exception as error:
            if db is not None:
                try:
                    db.rollback()
                except Exception:
                    pass
            raise HTTPException(
                status_code=500,
                detail="Could not save resume analysis."
            ) from error
        finally:
            if db is not None:
                db.close()

        return {
            "filename": resume.filename,
            "match_percentage": result["match_percentage"],
            "matched_skills": result["matched_skills"],
            "missing_skills": result["missing_skills"],
            "resume_skills": result["resume_skills"],
            "required_skills": result["required_skills"]
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Could not read this PDF. Please check that it is valid."
        )
