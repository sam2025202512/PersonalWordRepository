FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/instance

EXPOSE 5000

CMD ["sh", "-c", "python init_db.py && python -m flask --app wordrepo.api:create_app run --host=0.0.0.0 --port=5000"]
