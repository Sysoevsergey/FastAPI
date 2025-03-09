FROM python:3.12-alpine3.21
COPY ./app /app/app
WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r ./requirements.txt
ENTRYPOINT ["uvicorn", "app.server:app","--host", "0.0.0.0", "--port", "8000"]