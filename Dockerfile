# ConnectLAW Backend – FastAPI/uvicorn
FROM python:3.12-slim

WORKDIR /app

# Abhängigkeiten zuerst (besseres Layer-Caching)
COPY requirements.txt requirements-server.txt ./
RUN pip install --no-cache-dir -r requirements-server.txt

# Anwendungscode + System-Prompt
COPY connectlaw/ ./connectlaw/
COPY prompts/ ./prompts/
COPY server.py ./

# knowledge/ wird zur Laufzeit als Volume gemountet (Daten bleiben lokal,
# nicht im Image, nicht im Repo). Leeres Verzeichnis als Mountpunkt anlegen.
RUN mkdir -p /app/knowledge

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
