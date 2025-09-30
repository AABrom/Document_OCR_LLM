import asyncio
import websockets
from app.handlers import ocr_handler
from app.logger import logger


async def main():
    start_server = await websockets.serve(ocr_handler, "0.0.0.0", 8080)
    logger.info("OCR WebSocket server running at ws://0.0.0.0:8080")
    await start_server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
