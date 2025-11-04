# Use an official Python base image
FROM python:3.11-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Install uv (fast dependency installer)
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock* ./ 
COPY alembic.ini ./alembic.ini
COPY ./alembic ./alembic
COPY ./src ./src

# Create virtual environment and install dependencies
RUN uv venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
RUN uv pip install -e .

# Copy entrypoint script
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set environment variables (loaded at runtime)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000
# Run the app through entrypoint (will handle Alembic migration + start server)
ENTRYPOINT ["/entrypoint.sh"]
