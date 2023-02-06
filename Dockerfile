FROM python:3.10.5-slim-buster

WORKDIR /src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD python3 -m uvicorn app:app --host 0.0.0.0 --port 8080 --reload