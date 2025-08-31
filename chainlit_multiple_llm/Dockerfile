# Base image.
FROM python:3.12-slim-trixie

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

Add . /app

# Working directory set karein.
WORKDIR /app


# Dependencies install karein uv.lock file se.
# --locked flag se ye ensure hota hai ke sirf wohi versions install hon jo lock file mein hain.
RUN uv sync --locked

# Ab baki ka application code copy karein.
# Ye step tab hi chalega jab code mein tabdeeli ho.
COPY . .

# Default port expose karein.
EXPOSE 8000

# Application run karein.
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port","8000"]
