# ConnectLAW – Web-Frontend (GitHub Pages)

Statische Chat-Oberfläche für den juristischen Fach-Chatbot v4.0. Wird von
GitHub Pages aus diesem `docs/`-Ordner ausgeliefert.

## Wichtig: Sicherheit

GitHub Pages ist **reines Static-Hosting**. Der Anthropic-API-Schlüssel darf
**niemals** in diese Seite. Das Frontend ruft ausschliesslich ein separates
**Backend** (`server.py`) auf, das den Schlüssel hält.

## Inbetriebnahme

1. **Backend starten** (auf einem Server, in einer VM oder lokal):
   ```bash
   pip install -r requirements-server.txt
   export ANTHROPIC_API_KEY=sk-ant-...
   # nur die Pages-Domain als Ursprung zulassen (CORS):
   export CONNECTLAW_CORS_ORIGINS="https://<user>.github.io"
   uvicorn server:app --host 0.0.0.0 --port 8000
   ```
2. **Pages-Quelle setzen:** Repo → Settings → Pages → Source = Branch,
   Ordner `/docs`.
3. Seite öffnen, oben rechts **⚙ Backend** anklicken und die Backend-URL
   eintragen (z.B. `https://dein-host:8000`). Status muss „verbunden" zeigen.

## Lokaler Test

```bash
# Backend
uvicorn server:app --port 8000
# Frontend (eigenes Terminal)
cd docs && python -m http.server 8080
# Browser: http://localhost:8080  → Backend-URL http://localhost:8000
```

## Dateien

- `index.html` – Seitengerüst
- `assets/css/chat.css` – Styling
- `assets/js/chat.js` – Chat-Logik (Streaming, Sitzung, Backend-Status)
- `.nojekyll` – schaltet die Jekyll-Verarbeitung ab (reine Static-Auslieferung)
