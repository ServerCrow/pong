FROM python:3.12-slim
ARG VERSION=unknown

# Create a non-root user
RUN useradd appuser

WORKDIR /app
COPY . .

# Python setup
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VERSION=${VERSION}

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV ENV=DEV

# Switch to non-root user
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Install curl
USER root
RUN apt-get update && apt-get install --no-install-recommends -y curl && apt-get clean

# Switch back to non-root user for healthcheck
USER appuser
HEALTHCHECK --interval=30s --timeout=10s --retries=5 \
  CMD curl --fail http://localhost:8000/openapi.json || exit 1
