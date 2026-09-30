# ---- Backend image: Python + FastAPI ----------------------------------
# A small official Python base image.
FROM python:3.12-slim

# Keep .pyc files out of the image and make logs appear immediately.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements FIRST and install them. Docker caches this layer, so
# changing your Python code later does not reinstall all the dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the actual application code.
COPY app ./app

# Documentation for humans: this container listens on 8000.
EXPOSE 8000

# --host 0.0.0.0 is required. 127.0.0.1 would only be reachable from
# INSIDE the container and the port mapping would appear to do nothing.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
