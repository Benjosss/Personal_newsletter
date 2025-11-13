FROM python:3.11-slim

WORKDIR /app

RUN pip install feedparser schedule requests

COPY newsletter.py .

CMD ["python", "-u", "newsletter.py"]