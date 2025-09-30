import cv2
from typing import Optional
from app.logger import logger
from app.models import reader

def preprocess_image_cv2(image: cv2.Mat) -> cv2.Mat:
    logger.info("Starting image preprocessing")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def extract_text_with_easyocr_from_image(image: cv2.Mat) -> Optional[str]:
    logger.info("Starting OCR extraction")
    try:
        results = reader.readtext(image)
        all_text = ""
        logger.info(f"Extracted {len(results)} text pieces")
        for (_, text, confidence) in results:
            if confidence > 0.4:
                logger.debug(f"   {text} (confidence: {confidence:.2f})")
                all_text += text + "\n"
        return all_text.strip()
    except Exception as e:
        logger.error(f"OCR error: {e}")
        return None

def main_ocr_pipeline_from_image(image: cv2.Mat) -> Optional[str]:
    processed = preprocess_image_cv2(image)
    extracted_text = extract_text_with_easyocr_from_image(processed)
    return extracted_text
