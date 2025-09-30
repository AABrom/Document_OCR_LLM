import json
import base64
import numpy as np
import cv2
from app.ocr import main_ocr_pipeline_from_image
from app.llm_client import structure_with_llm
from app.logger import logger


async def ocr_handler(websocket):
    async for message in websocket:
        logger.info("Received message, starting processing")
        await websocket.send("Received message, starting processing")        
        try:
            data = json.loads(message)

            image_b64 = data.get('image_data')
            schema = data.get('schema')

            if not image_b64 or not schema:
                err = "Missing image_data or schema in request"
                await websocket.send(json.dumps({'type': 'error', 'data': err}))
                logger.warning(err)
                continue

            # Декодируем изображение
            image_bytes = base64.b64decode(image_b64)
            image_array = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            if image is None:
                err = "Failed to decode image"
                await websocket.send(json.dumps({'type': 'error', 'data': err}))
                logger.warning(err)
                continue
            
            await websocket.send("Starting OCR extraction")
            logger.info("Starting OCR extraction")

            # OCR пайплайн (предобработка + извлечение текста)
            extracted_text = main_ocr_pipeline_from_image(image)
            if not extracted_text:
                err = "OCR extraction failed"
                await websocket.send(json.dumps({'type': 'error', 'data': err}))
                continue
            
            await websocket.send("Sending text to LLM")
            logger.info("Sending text to LLM")
            # Формируем промпт для LLM с названием и данными из схемы
            title = schema.get('title', 'data')
            properties = ', '.join(schema.get('properties', {}).keys())

            prompt_text = f"""
Извлеки результаты {title} из этого текста в виде JSON:
{extracted_text}

Ключи: {properties}.
Верни ТОЛЬКО JSON без примечаний. 
"""

            llm_response = await structure_with_llm(prompt_text)
            await websocket.send(json.dumps({'type': 'result', 'data': llm_response}))
            logger.info("LLM responded success")

        except Exception as e:
            err_msg = f"Processing error: {str(e)}"
            logger.error(err_msg, exc_info=True)
            await websocket.send(json.dumps({'type': 'error', 'data': err_msg}))