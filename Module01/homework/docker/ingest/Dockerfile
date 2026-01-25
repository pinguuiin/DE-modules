FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app

# force in-project venv
ENV UV_PROJECT_ENVIRONMENT=.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY "pyproject.toml" "uv.lock" ".python-version" ./

RUN uv sync --locked

COPY ingest_data.py .

CMD ["python", "ingest_data.py"]