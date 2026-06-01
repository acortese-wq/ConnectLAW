# Deployment: Backend mit automatischem HTTPS (Caddy)

Die GitHub-Pages-Seite (`https://acortese-wq.github.io/ConnectLAW/`) ist nur
das Frontend. Zum Chatten muss das **Backend über HTTPS** erreichbar sein.
Diese Compose-Konfiguration startet Backend + Caddy; Caddy holt das
TLS-Zertifikat automatisch.

## Voraussetzungen

1. Ein Server (VM) mit Docker + Docker Compose.
2. Eine **Domain**, deren DNS-Eintrag (A/AAAA) auf die Server-IP zeigt,
   z. B. `connectlaw.example.com`.
3. Ports **80** und **443** am Server offen (Let's-Encrypt-Challenge + HTTPS).

## Einrichtung

```bash
cp .env.example .env
# in .env setzen:
#   ANTHROPIC_API_KEY=sk-ant-...
#   DOMAIN=connectlaw.example.com
#   CONNECTLAW_CORS_ORIGINS=https://acortese-wq.github.io

# (optional) Wissensdokumente lokal ablegen – bleiben auf dem Host:
#   knowledge/vertrag.pdf, knowledge/richtlinie.md

./deploy.sh up        # bauen & starten (oder: docker compose up -d --build)
```

Danach in der Chat-Seite **⚙ Backend** öffnen und eintragen:
```
https://connectlaw.example.com
```
Der Status muss „verbunden" zeigen.

## Betrieb

```bash
./deploy.sh logs      # Logs verfolgen
./deploy.sh reload    # knowledge/ neu einlesen (nach neuen Dokumenten)
./deploy.sh restart   # Dienste neu starten
./deploy.sh down      # stoppen
```

## Daten & Sicherheit

- `knowledge/` wird **schreibgeschützt** als Volume gemountet – die Daten
  bleiben lokal auf dem Server, nicht im Image und nicht im Repo.
- Der API-Schlüssel liegt nur im Backend-Container (`.env`), nie im Frontend.
- `.env` ist in `.gitignore` – nicht committen.

## Ohne eigene Domain (nur Test)

Wenn (noch) keine Domain verfügbar ist, das Backend lokal starten und einen
HTTPS-Tunnel verwenden:

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
cloudflared tunnel --url http://localhost:8000   # liefert eine https-URL
```
Die ausgegebene `https://…`-URL in ⚙ Backend eintragen. (Mixed-Content:
eine HTTPS-Seite kann kein `http://`-Backend aufrufen.)
