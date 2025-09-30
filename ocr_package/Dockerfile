FROM python:3.13-slim 
#нужная версия python

WORKDIR /app

# установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# копируем и запускаем код
COPY . .
CMD ["python", "app/main.py"]