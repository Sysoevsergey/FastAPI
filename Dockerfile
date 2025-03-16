FROM python:3.12-alpine3.21
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt
COPY ./app /app
WORKDIR /app

ENTRYPOINT ["uvicorn", "server:app","--host", "0.0.0.0", "--port", "8080"]