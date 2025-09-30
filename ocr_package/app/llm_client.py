import httpx
from typing import Optional
import logging

logger = logging.getLogger(__name__)

async def structure_with_llm(prompt: str, model_name: str = "llama3.1") -> Optional[str]:
    url = 'http://localhost:11434/api/generate'
    payload = {
        'model': model_name,
        'prompt': prompt,
        'stream': False,
        'options': {'stream': False}
    }
    timeout_sec = 2*10**10

    logger.info("Sending LLM request")
    try:
        async with httpx.AsyncClient(timeout=timeout_sec) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            res_json = response.json()
            return res_json.get('response', '')
    except Exception as e:
        logger.error(f"LLM request error: {e}", exc_info=True)
        return None

