# Builder stage
FROM python:3.13-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

# Install dependencies using system Python
RUN uv sync --frozen --python $(which python)

# Copy application code
COPY . .

# Runtime stage
FROM python:3.13-slim AS runtime

WORKDIR /app

# Copy the virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy only the application code from builder stage
COPY --from=builder /app/app /app/app
# # Copy application code
# COPY . .

# Set PATH to include the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Expose port
EXPOSE 8000

# Environment variable
ENV DATABASE_URL=""

# Run the application using the virtual environment's Python
CMD ["python", "-m", "app.main"]