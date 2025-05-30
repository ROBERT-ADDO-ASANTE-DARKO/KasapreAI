from pydantic import BaseModel
from typing import List, Optional, Dict

class BoxCoordinate(BaseModel):
    x: int
    y: int

class DetectedBox(BaseModel):
    text: str
    confidence: float
    coordinates: List[BoxCoordinate]

class OCRResult(BaseModel):
    text: str
    confidence: float
    boxes: List[DetectedBox]
    image_with_boxes: Optional[str] = None
