FROM python:3.9.15-slim

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.2.2

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential

ENV PATH="/root/.local/bin:$PATH"

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python

WORKDIR /app
COPY ./poetry.lock ./pyproject.toml /app/
RUN poetry config virtualenvs.create false \
  && poetry install --only main --no-interaction --no-ansi

COPY ./gistapi ./gistapi

EXPOSE "9876"

CMD ["gunicorn", "-w 4", "-b 0.0.0.0:9876", "gistapi:create_app()"]

