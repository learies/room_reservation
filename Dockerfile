FROM python:3.11-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code
RUN apk update \
    && apk add --no-cache gcc musl-dev libffi-dev
RUN pip install --upgrade pip \
    && pip install poetry
COPY . /code
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-cache --no-ansi --without develop
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]