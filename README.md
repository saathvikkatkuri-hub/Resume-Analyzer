# ResumeIQ — Resume Analyzer

ResumeIQ is a web application that analyzes resumes against job descriptions. It extracts skills from uploaded PDF resumes, identifies matching and missing skills, and calculates a keyword-based match percentage.

## Features

- Upload resumes in PDF format.
- Extract text from resumes.
- Identify skills in resumes and job descriptions.
- Display matched and missing skills.
- Calculate a resume match percentage.
- Store analysis results in a MySQL database.

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, FastAPI
- **PDF Processing:** PyMuPDF
- **Database:** MySQL
- **ORM:** SQLAlchemy

## How It Works

1. Upload a PDF resume.
2. Enter the target job description.
3. Extract text and identify recognized skills.
4. Compare resume skills with job requirements.
5. Display the match percentage, matched skills, and missing skills.
6. Save the analysis results in MySQL.

## Project Structure

- `frontend/` — User interface and browser-side logic
- `main.py` — FastAPI application and analysis endpoint
- `matcher.py` — Skill extraction and matching logic
- `resume_reader.py` — PDF text extraction utilities
- `database.py` — Database connection configuration
- `database_models.py` — SQLAlchemy database models
- `test_db.py` — Database table setup/testing

## Scoring

The match percentage is based on the proportion of detected required job skills that are also found in the resume. It is a keyword-based score, not an official ATS score.

## Future Improvements

- Expand the skill vocabulary and support more skill variations.
- Improve skill matching accuracy.
- Enhance resume analysis and reporting.
- Improve the user interface and analysis history.

