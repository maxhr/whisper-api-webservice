FROM python:3.11-slim

ENV POETRY_VENV=/app/.venv

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -qq update \
    && apt-get -qq install --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools tensorflow torch torchvision \
    && $POETRY_VENV/bin/pip install poetry==1.6.1

ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

COPY . /app

RUN poetry config virtualenvs.in-project true
RUN poetry install

EXPOSE 8081

CMD ["uvicorn", "app.webservice:app", "--host", "0.0.0.0", "--port", "8081"]
