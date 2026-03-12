from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    hr_score = Column(Float)
    therapist_score_encrypted = Column(String)
    ai_score = Column(Float)

    combined_score = Column(Float)