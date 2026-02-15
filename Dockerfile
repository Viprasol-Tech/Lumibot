FROM python:3.11-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt requirements_bot.txt ./
RUN pip install --no-cache-dir -r requirements_bot.txt

# Copy project
COPY lumibot/ lumibot/
COPY bot/ bot/
COPY api/ api/
COPY run_bot.py .
COPY setup.py setup.cfg pyproject.toml ./

# Install lumibot as local package
RUN pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["python", "run_bot.py"]
