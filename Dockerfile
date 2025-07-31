FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2 \
    pango1.0-tools \
    libpango1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libxml2 \
    libxslt1.1 \
    libjpeg-dev \
    libpng-dev \
    libglib2.0-dev \
    netcat-openbsd \
    tzdata \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY .env .env
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "crm_project.wsgi:application", "--bind", "0.0.0.0:8000"]
