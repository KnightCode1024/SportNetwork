FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements/prod.txt /app/requirements/prod.txt
RUN pip install --no-cache-dir -r /app/requirements/prod.txt

COPY src /app/src
ENV PYTHONPATH=/app/src

EXPOSE 8000
