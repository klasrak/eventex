ARG PYTHON_VERSION=3.8
ARG ALPINE_VERSION=3.10

# Build dependencies in separate container
FROM tiangolo/uvicorn-gunicorn:python${PYTHON_VERSION}-alpine${ALPINE_VERSION} AS builder

ENV WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=true

RUN apk update \
    && apk add --virtual build-dependencies \
    build-base \
    gcc \
    python3-dev \
    openssl-dev \
    musl-dev \
    libffi-dev \
    && pip install --no-cache-dir cryptography==2.1.4

COPY pyproject.toml ${WORKDIR}/
COPY poetry.lock ${WORKDIR}/

RUN cd ${WORKDIR} \
    && pip install --upgrade pip setuptools \
    && pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create true \
    && poetry install --no-dev

# Create the final container with the app
FROM tiangolo/uvicorn-gunicorn:python${PYTHON_VERSION}-alpine${ALPINE_VERSION}

ENV USER=docker \
    GROUP=docker \
    UID=12345 \
    GID=23456 \
    HOME=/app \
    PYTHONUNBUFFERED=1

WORKDIR ${HOME}

# Create user/group
RUN addgroup --gid "${GID}" "${GROUP}" \
    && adduser \
    --disabled-password \
    --gecos "" \
    --home "$(pwd)" \
    --ingroup "${GROUP}" \
    --no-create-home \
    --uid "${UID}" \
    "${USER}"

# Run as docker user
USER ${USER}
# Copy installed packages
# COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=builder /app/.venv/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
# Copy the application
COPY --chown=docker:docker . .
# Collect the static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000
