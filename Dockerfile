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

# Install shadow package for usermod (Alpine doesn't have it by default)
RUN apk add shadow

# Create user and add to group 1000 (required for Render secret file access)
RUN addgroup -g 1000 secrets && \
    addgroup -S app && \
    adduser -S app -G app && \
    usermod -a -G 1000 app

# Create startup script to handle SSL certificate
RUN echo '#!/bin/sh' > /start.sh && \
    echo 'echo "🔐 Setting up SSL certificates..."' >> /start.sh && \
    echo 'if [ -f "/etc/secrets/secret.pem" ]; then' >> /start.sh && \
    echo '  cp /etc/secrets/secret.pem ./notes_service/certs/secret.pem' >> /start.sh && \
    echo '  chmod 644 ./notes_service/certs/secret.pem' >> /start.sh && \
    echo '  echo "✅ SSL certificate copied successfully"' >> /start.sh && \
    echo 'else' >> /start.sh && \
    echo '  echo "⚠️ No SSL certificate found in secrets"' >> /start.sh && \
    echo 'fi' >> /start.sh && \
    echo 'exec gunicorn notes_service.main:app -c gunicorn.conf.py' >> /start.sh && \
    chmod +x /start.sh

# Set ownership
RUN chown -R app:app /app

USER app

CMD ["/start.sh"]
