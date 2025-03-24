FROM python:3.13-slim

WORKDIR /app
COPY . /app/
RUN pip install --no-cache-dir -e .

ENTRYPOINT ["python", "-m", "zyte_test_websites.main"]
