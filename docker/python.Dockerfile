# One image recipe for all three Python services. The SERVICE build arg picks
# which workspace member's dependencies get installed.
#
# Ubuntu 24.04 to match Tread's stated runtime; its system Python is 3.12.
FROM ubuntu:24.04

COPY --from=ghcr.io/astral-sh/uv:0.11 /uv /bin/uv

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 ca-certificates \
    && rm -rf /var/lib/apt/lists/*

ENV UV_PYTHON=python3 \
    UV_PYTHON_DOWNLOADS=never \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH=/opt/venv/bin:$PATH \
    PYTHONUNBUFFERED=1

WORKDIR /app
ARG SERVICE

# Layer caching: copy only the files that describe dependencies, install them,
# THEN copy the source. Editing code reuses the cached dependency layer, so
# rebuilds take seconds instead of re-downloading every package.
COPY pyproject.toml uv.lock ./
COPY packages/common/pyproject.toml packages/common/
COPY services/backend/pyproject.toml services/backend/
COPY services/market_adapter/pyproject.toml services/market_adapter/
COPY services/twap_executor/pyproject.toml services/twap_executor/
RUN uv sync --frozen --no-dev --package ${SERVICE} --no-install-workspace

COPY packages ./packages
COPY services ./services
RUN uv sync --frozen --no-dev --package ${SERVICE}

# Don't run as root inside the container.
RUN useradd --create-home --uid 10001 app
USER app
