import asyncio
import websockets
import requests
import time
from app.handlers import ocr_handler
from app.logger import logger


def wait_for_ollama():
    while True:
        try:
            r = requests.get("http://ollama:11434") #localhost, если запуск вручную 
            if r.status_code == 200:
                logger.info("Ollama is ready")
                break
        except Exception:
            logger.info("Waiting for Ollama to be ready...")
        time.sleep(5)

async def main():
    wait_for_ollama()  # Ждем, пока Ollama готов
    start_server = await websockets.serve(ocr_handler, "0.0.0.0", 8080)
    logger.info("OCR WebSocket server running at ws://0.0.0.0:8080")
    await start_server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
