# Backend container for Azure Container Apps.
# Build from the REPO ROOT:  docker build -f backend/Dockerfile -t cdfd-backend .
FROM python:3.11-slim

# ODBC Driver 18 for SQL Server (needed for mssql+pyodbc against Azure SQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl gnupg ca-certificates unixodbc-dev gcc g++ \
    && curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt backend/requirements.txt ai/requirements.txt ./reqs/
RUN pip install --no-cache-dir -r reqs/requirements.txt pyodbc azure-storage-blob azure-identity

COPY backend/ ./backend/
COPY database/ ./database/
COPY ai/ ./ai/
COPY cloud/ ./cloud/
COPY alembic.ini ./

EXPOSE 8000
# init_db() also runs on startup; for Azure SQL run `alembic upgrade head` as a one-off first (see cloud/DEPLOY.md).
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
