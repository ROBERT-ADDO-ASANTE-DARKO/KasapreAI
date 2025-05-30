from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .base import Base

class ProcessingJob(Base):
    __tablename__ = "processing_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    job_type = Column(String(50))
    input_file = Column(String(255))
    status = Column(String(50), default="pending")
    result = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
