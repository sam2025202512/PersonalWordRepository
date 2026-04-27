FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY client/requirements.txt /app/client-requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt -r /app/client-requirements.txt

COPY . /app

EXPOSE 5050

CMD ["python", "-m", "client.app"]
