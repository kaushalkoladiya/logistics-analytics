# Use official Python image
FROM python:3.11

# Install PostgreSQL development headers
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Copy and install dependencies inside virtual environment
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Create necessary directories
RUN mkdir -p /app/data /app/src

# Copy application source code and data folders
COPY src/ /app/src/
COPY data/ /app/data/

# Set Python path to include src directory
ENV PYTHONPATH=/app/src

# Run the application
CMD ["python", "src/main.py"]
