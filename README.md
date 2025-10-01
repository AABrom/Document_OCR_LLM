# OCR Microservice with Ollama LLM Integration

This project provides
- ocr_package: an OCR microservice combining EasyOCR for image-to-text recognition and Ollama for interacting with large language models (LLMs) to process and structure extracted text. The service operates a WebSocket server for real-time OCR requests and uses Ollama to enhance text structuring capabilities. To build and run package use docker or run manually.
- test_websocket: test dart\flutter client. Run manually.   

---

- Websocket-сервер на Python с функционалом обработки полученного сообщения со схемой документа и base64-конвертированным изображением: передача в модель OCR изображения, получение текста и передача текста со схемой Ollama-серверу 
- Тестовый клиент на flutter для демонстрации отправки изображения и схемы. Демонстрируется фрагмент Json-схемы. 
- В сборке docker: Ollama-сервер - open source ПО для локальной и удаленной работы с большими языковыми моделями, LLM-модель для структурирования текста согласно переданной схеме документа 


---

- Build and run by docker:
```bash
docker-compose up --build
```
When docker container created, detailed logs are available in Docker container. 
Build take a bunch of time due to docker creating base operating system layer, ollama server, environment, loading model to produce system image and host app without worrying about system differences and components installation.
Speed issue is common. Speed fluctuates and some parts stall during llm model download is normal behavior.

In most cases, the download will eventually complete successfully. Once the model is downloaded and cached in the Docker volume, subsequent usage won't redo this step unless the volume is deleted.

- Or compose and run manually:
!!! if running locally, replace in main "http://ollama:11434" -> "http://localhost:11434"

## 1. Install Python 3.13

## 2. Install and Run Ollama Server

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

## 3. Pull Ollama LLM Model for Text Structuring
Download llama3.1:

```bash
ollama pull llama3.1
```

## 4. Run the OCR Microservice
Start the OCR microservice from the project root (ocr_package folder):

```bash
python -m app.main
```

Wait for successful initialization logs like:

[2025-09-29 20:10:07,942] INFO app.logger: EasyOCR reader initialized.
[2025-09-29 20:10:08,051] INFO app.logger: OCR WebSocket server running at ws://0.0.0.0:8080


# OCR project Structure

ocr_package/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── handlers.py
│   ├── ocr.py
│   ├── models.py
│   └── llm_client.py
├──requirements.txt
└──readme.md

# Test dart\flutter client Structure

test_websocket/
…
├── assets/
│   	└── schemas/ 
│   		└── blood_test.json 	// json-schema example for document form	
├── lib/
 …  ├── main.dart		 // include simple interface
  	└── schema_repository/ 
  	│	└──schema_storage.dart    // schema loader	
  	└── services/
   		└──websocket_service.dart   // websocket connector
