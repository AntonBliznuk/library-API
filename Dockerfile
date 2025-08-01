# Dockerfile for Render deployment
FROM python:3.12-slim

LABEL maintainer="antonbliznuk71@gmail.com"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

ARG SERVICE=web
ENV SERVICE=${SERVICE}

CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py loaddata admin-user-fixture.json && python manage.py collectstatic --noinput && gunicorn core.wsgi:application --bind 0.0.0.0:8000"]