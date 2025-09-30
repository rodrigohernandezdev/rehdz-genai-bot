FROM ghcr.io/astral-sh/uv:0.8.22-python3.12-bookworm-slim

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_TOOL_BIN_DIR=/usr/local/bin \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_NO_SYNC=1

RUN groupadd --system --gid 999 nonroot \
 && useradd  --system --gid 999 --uid 999 --create-home nonroot \
 && mkdir -p /opt/venv /app \
 && chown -R nonroot:nonroot /opt/venv /app

WORKDIR /app

RUN --mount=type=cache,id=uv-cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=/app/pyproject.toml,ro \
    --mount=type=bind,source=uv.lock,target=/app/uv.lock,ro \
    uv sync --locked --no-install-project --no-dev

COPY --chown=nonroot:nonroot . /app

RUN --mount=type=cache,id=uv-cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

USER nonroot

ENV PATH="/opt/venv/bin:${PATH}"

CMD ["uv", "run", "--no-sync", "main.py"]