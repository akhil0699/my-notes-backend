ARG BUILDER_FROM=python:3.11.9-alpine3.19
ARG RUNTIME_FROM=python:3.11.9-alpine3.19

FROM $BUILDER_FROM as builder

ARG CODEARTIFACT_AUTH_TOKEN
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN python -m pip install --upgrade pip && \
    python -m pip install poetry==1.6.1 && \
    touch README.md && \
    poetry install --no-root && \
    rm -rf $POETRY_CACHE_DIR && \
    pip uninstall poetry -y

# Final stage
FROM $RUNTIME_FROM as runtime

WORKDIR /app
EXPOSE 8000

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY notes_service ./notes_service
COPY gunicorn.conf.py .

# Create certs directory
RUN mkdir -p ./notes_service/certs

# Simple startup script that works as root
RUN echo '#!/bin/sh' > /start.sh && \
    echo 'echo "🔐 Setting up SSL certificates..."' >> /start.sh && \
    echo 'if [ -f "/etc/secrets/secret.pem" ]; then' >> /start.sh && \
    echo '  cp /etc/secrets/secret.pem ./notes_service/certs/secret.pem' >> /start.sh && \
    echo '  chmod 644 ./notes_service/certs/secret.pem' >> /start.sh && \
    echo '  echo "✅ SSL certificate ready"' >> /start.sh && \
    echo 'else' >> /start.sh && \
    echo '  echo "❌ No SSL certificate found"' >> /start.sh && \
    echo 'fi' >> /start.sh && \
    echo 'exec gunicorn notes_service.main:app -c gunicorn.conf.py' >> /start.sh && \
    chmod +x /start.sh

# NO USER CREATION - RUN AS ROOT
CMD ["/start.sh"]
