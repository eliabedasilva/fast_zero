FROM python:3.10-slim

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY . .

RUN pip install poetry
RUN pip install pydantic[email]

RUN poetry install --no-interaction --no-ansi

EXPOSE 8000

CMD poetry run uvicorn --host 0.0.0.0 --port 8000 fast_zero.app:app