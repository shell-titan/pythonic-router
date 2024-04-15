
FROM python:3.8-slim

WORKDIR /app

COPY . /app
RUN pip install --no-cache-dir scapy matplotlib
CMD ["python", "router.py"]
