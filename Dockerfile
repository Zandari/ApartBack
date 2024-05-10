FROM python:3.11 as requirements-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11
WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./apart /code/apart
EXPOSE 8000/tcp
RUN export PYTHONDONTWRITEBYTECODE=1
CMD ["fastapi", "dev", "apart/main.py", "--host", "0.0.0.0", "--port", "8000"]
