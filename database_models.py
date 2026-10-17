
from sqlalchemy import Column, Integer, String, Text
from database import Base


class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    job_description = Column(Text, nullable=False)
    match_percentage = Column(Integer, nullable=False)
    matched_skills = Column(Text, nullable=False)
    missing_skills = Column(Text, nullable=False)
