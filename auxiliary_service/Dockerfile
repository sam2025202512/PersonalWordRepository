FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY auxiliary_service/requirements.txt /app/auxiliary-requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt -r /app/auxiliary-requirements.txt

COPY . /app

EXPOSE 5001

CMD ["python", "-m", "auxiliary_service.app"]
