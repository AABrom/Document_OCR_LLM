FROM python:3.13-slim 
#нужная версия python

WORKDIR /app

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-rus \
    tesseract-ocr-eng \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# копируем и запускаем код
COPY . .
CMD ["python", "-m", "app.main"]