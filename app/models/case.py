from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.models.database import Base

class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    summary = Column(String)
    amount = Column(String)
    date = Column(String)
    issue_type = Column(String)
    risk_level = Column(String)
    risk_score = Column(Float)
    confidence_score = Column(Float)
    decision = Column(String)

    # ✅ ADD THIS
    user_id = Column(Integer, ForeignKey("users.id"))