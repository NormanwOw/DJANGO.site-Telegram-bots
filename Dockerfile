FROM python:3.10-slim

WORKDIR /app

COPY /pyproject.toml /app

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .

LABEL project='site_telegram_bots' version=1.0