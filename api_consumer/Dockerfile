FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

#COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

#CMD ["python", "consumer:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["python", "consumer.py"]