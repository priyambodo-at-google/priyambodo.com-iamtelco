# Base image with Python and Poetry pre-installed
FROM python:3.11 AS base

# Install Poetry
RUN pip install poetry

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy application code
COPY . .

# Expose port for Streamlit
EXPOSE 8080

# Set entrypoint to start Streamlit
ENTRYPOINT ["streamlit", "run", "0_💰_IamRich_Financial_Advisor_v3.py", "--server.port=8080", "--server.address=0.0.0.0"]