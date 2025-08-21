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

# final stage
FROM $RUNTIME_FROM as runtime

WORKDIR /app

EXPOSE 8000

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY notes_service ./notes_service

COPY gunicorn.conf.py .

RUN mkdir -p ./notes_service/certs

COPY /etc/secrets/secret.pem ./notes_service/certs

# Run Unprivileged
RUN addgroup -S app && adduser -S app -G app

USER app

CMD ["gunicorn", "notes_service.main:app"]
