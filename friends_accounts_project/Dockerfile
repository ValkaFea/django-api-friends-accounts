FROM python:3.11

WORKDIR /code

COPY pyproject.toml poetry.lock* /code/

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

COPY . /code/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]