FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


WORKDIR /code

COPY ./pyproject.toml ./uv.lock /code/
RUN uv sync --frozen --no-cache


COPY ./requirements.txt /code/requirements.txt


#RUN uv pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./app /code/app


CMD ["fastapi", "run", "app/main.py", "--port", "80"]