FROM python:3.12-slim

# 1. System dependencies (Only runs once ever)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && rm -rf /var/lib/apt/lists/*

# 2. Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /project

# 3. CACHE LAYER: Copy ONLY requirements first
# If requirements.txt hasn't changed, Docker SKIPS this entire step!
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

# 4. CODE LAYER: Copy your app last
# Since your code changes often, only THIS step runs on most builds
COPY . .

CMD ["python", "-u", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

