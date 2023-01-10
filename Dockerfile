# The base image we want to inherit from
FROM python:3


# System deps:
RUN pip install poetry && poetry --version

WORKDIR /django
# set work directory
COPY pyproject.toml poetry.lock /django/

# Install dependencies:
RUN poetry install
# copy project
COPY . .


