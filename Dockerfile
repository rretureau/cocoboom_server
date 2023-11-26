# Creating python base 
FROM python:3.12-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Builder base, build dependencies (long)
FROM python-base as builder-base
RUN apt-get update && apt-get install -y libpq-dev gcc

# Install poetry
ENV POETRY_VERSION=1.7.1
RUN pip install poetry==$POETRY_VERSION

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
RUN poetry install --only main

# Production stage
FROM python-base as production

RUN apt-get update && apt-get install -y postgresql-client

COPY --from=builder-base $VENV_PATH $VENV_PATH
COPY . /app
WORKDIR /app

RUN sed -i 's/\r$//g' /app/docker_entrypoint.sh
RUN chmod +x /app/docker_entrypoint.sh

ENTRYPOINT [ "./docker_entrypoint.sh" ]