FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY . ./
RUN pip install --upgrade pip && \
    pip install .

CMD ["python", "main.py"]
