FROM python:3

LABEL maintainer="mike.place@elastic.co"
WORKDIR /
RUN pip3 install poetry
COPY poetry.lock pyproject.toml /
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

COPY . /synthbean