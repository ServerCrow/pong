FROM python:3.12-slim
ARG VERSION=unknown

WORKDIR /app
COPY . .

# Python setup
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VERSION=${VERSION}

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV ENV=DEV

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Install curl
RUN apt-get update && apt-get install --no-install-recommends -y curl && apt-get clean

HEALTHCHECK --interval=30s --timeout=10s --retries=5 \
  CMD curl --fail http://localhost:8000/openapi.json || exit 1
