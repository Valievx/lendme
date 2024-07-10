FROM python:3.10.5-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
CMD ["sh", "entrypoint.sh"]