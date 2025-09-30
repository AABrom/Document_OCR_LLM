import easyocr
from app.logger import logger

logger.info("Initializing EasyOCR reader...")
reader = easyocr.Reader(['ru', 'en'])
logger.info("EasyOCR reader initialized.")

