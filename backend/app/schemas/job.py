from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class JobBase(BaseModel):
    job_type: str
    input_file: Optional[str] = Field(None, description="Filename or input reference")  # Now optional

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int
    user_id: int
    status: str
    result: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True
