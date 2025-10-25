FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt /app/
RUN apt-get update && apt-get install -y --no-install-recommends gcc
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get remove --purge -y gcc && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . /app/

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]