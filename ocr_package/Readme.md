# OCR Microservice with Ollama LLM Integration

This project provides an OCR microservice combining EasyOCR for image-to-text recognition and Ollama for interacting with large language models (LLMs) to process and structure extracted text. The service operates a WebSocket server for real-time OCR requests and uses Ollama to enhance text structuring capabilities.

---

Or run manually:

## 1. Install and Run Ollama Server

- **Official repository**: [https://github.com/ollama/ollama](https://github.com/ollama/ollama)  
- **Official website**: [https://ollama.com/](https://ollama.com/)

Check your installed Ollama version:

```bash
ollama -v
```
Example output:

```bash
ollama version is 0.12.3
```
If the Ollama server does not start automatically, start it manually with:

```bash
ollama serve
```
The Ollama server will listen locally at http://127.0.0.1:11434

## 2. Pull Ollama LLM Model for Text Structuring
Download llama3.1 for text structuring:

```bash
ollama pull llama3.1
```

## 3. Run the OCR Microservice
Start the OCR microservice from the project root:

```bash
python -m ocr_package.app.main
```

Wait for successful initialization logs like:

[2025-09-29 20:10:07,942] INFO app.logger: EasyOCR reader initialized.
[2025-09-29 20:10:08,051] INFO app.logger: OCR WebSocket server running at ws://0.0.0.0:8080

# Project Structure

ocr_package/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── handlers.py
│   ├── ocr.py
│   ├── models.py
│   └── llm_client.py