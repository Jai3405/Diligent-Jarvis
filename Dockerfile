# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Set working directory
WORKDIR /app

# Install system dependencies (build-essential needed for some python packages like llama-cpp-python)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
# We need to install llama-cpp-python specifically with cmake args if we want GPU support, 
# but for a generic CPU build, standard pip install is fine.
# For Mac M1/M2 (Metal), we would need CMAKE_ARGS="-DLLAMA_METAL=on"
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create models directory
RUN mkdir -p models

# Expose port
EXPOSE 5000

# Run the application
# Using uvicorn directly for production-like execution
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "5000"]

