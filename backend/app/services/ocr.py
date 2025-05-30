import easyocr
import base64
import cv2
import numpy as np
from typing import Dict, Any
from ..schemas.ocr import OCRResult

class OCRService:
    def __init__(self, languages: list = ['en']):
        self.reader = easyocr.Reader(languages)

    def extract_text(self, image_path: str) -> OCRResult:
        """
        Process an image file and return OCR results in a structured format.
        
        Args:
            image_path: Path to the image file to process
            
        Returns:
            OCRResult: Structured results including text, confidence, bounding boxes,
                    and annotated image
        """
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not read image file")

        # Perform OCR
        results = self.reader.readtext(image)
        extracted_text = " ".join([result[1] for result in results])
        
        # Calculate average confidence
        avg_confidence = (sum(result[2] for result in results) / len(results)) if results else 0.0
        
        # Format bounding boxes
        formatted_boxes = []
        image_with_boxes = image.copy()
        base64_str = None
        
        for (bbox, text, confidence) in results:
            # Convert coordinates to serializable format
            coordinates = [{"x": int(point[0]), "y": int(point[1])} for point in bbox]
            
            formatted_boxes.append({
                "text": text,
                "confidence": float(confidence),
                "coordinates": coordinates
            })
            
            # Draw bounding boxes on image
            top_left = tuple(map(int, bbox[0]))
            bottom_right = tuple(map(int, bbox[2]))
            cv2.rectangle(image_with_boxes, top_left, bottom_right, (0, 0, 255), 2)
            cv2.putText(
                image_with_boxes, 
                f"{text} ({confidence:.2f})",
                (top_left[0], top_left[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )
        
        # Convert annotated image to base64
        if results:
            _, buffer = cv2.imencode('.png', image_with_boxes)
            base64_str = base64.b64encode(buffer).decode('utf-8')
        
        return OCRResult(
            text=extracted_text,
            confidence=float(avg_confidence),
            boxes=formatted_boxes,
            image_with_boxes=base64_str
        )
    '''
    def extract_text(self, image_path: str) -> Dict[str, Any]:
        """Extract text from image and return serializable results"""
        image = cv2.imread(image_path)
        results = self.reader.readtext(image)
        extracted_text = " ".join([result[1] for result in results])
        
        response = {
            "text": extracted_text,
            "confidence": sum([result[2] for result in results])/len(results) if results else 0,
            "boxes": []
        }

        if results:
            # Convert image with boxes to base64
            image_with_boxes = self._draw_boxes(image.copy(), results)
            _, buffer = cv2.imencode('.png', image_with_boxes)
            response["image_with_boxes"] = base64.b64encode(buffer).decode('utf-8')
            
            # Add box coordinates
            response["boxes"] = [
                {
                    "text": text,
                    "confidence": float(confidence),
                    "coordinates": [{"x": int(x), "y": int(y)} for x, y in bbox]
                }
                for (bbox, text, confidence) in results
            ]
            
        return response
        '''

    def _draw_boxes(self, image: np.ndarray, results: list) -> np.ndarray:
        """Draw bounding boxes around detected text"""
        for (bbox, text, prob) in results:
            top_left = tuple(map(int, bbox[0]))
            bottom_right = tuple(map(int, bbox[2]))
            cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 2)
            cv2.putText(
                image, f"{text} ({prob:.2f})", 
                (top_left[0], top_left[1] - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2
            )
        return image
