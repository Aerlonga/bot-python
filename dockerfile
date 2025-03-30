# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install -y build-essential python3-dev libgl1 libglib2.0-0 && \
    python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install pandas botcity-framework-core opencv-python pillow openpyxl pytest pytest-html coverage

# Ativa o ambiente virtual no entrypoint
ENV PATH="/venv/bin:$PATH"

CMD ["tail", "-f", "/dev/null"]
