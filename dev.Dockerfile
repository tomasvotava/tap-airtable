ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}

ENV PATH=/root/.local/bin:$PATH
ENV POETRY_VIRTUALENVS_CREATE=false

RUN python -m pip install pipx && python -m pipx ensurepath

ARG POETRY_VERSION=1.8.3

RUN pipx install poetry==${POETRY_VERSION}

ADD pyproject.toml .
ADD poetry.lock .

RUN poetry install --no-root

ADD . .

ENTRYPOINT /bin/bash
