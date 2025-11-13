FROM python:3.11-slim

WORKDIR /app

RUN pip install feedparser schedule request

COPY newsletter.py .

CMD ["python", "-u", "newsletter.py"]