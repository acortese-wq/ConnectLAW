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

## Ohne eigene Domain (Tunnel) – empfohlen zum Loslegen

Kein Server, keine Domain nötig. Backend + HTTPS-Tunnel mit einem Skript:

```bash
pip install -r requirements-server.txt
cp .env.example .env          # ANTHROPIC_API_KEY eintragen
./tunnel.sh
```

`cloudflared` muss installiert sein
(https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/).
Das Skript startet das Backend und gibt eine `https://….trycloudflare.com`-URL
aus – diese in der Chat-Seite unter **⚙ Backend** eintragen (ohne `/` am Ende).

### Windows (PowerShell)

```powershell
# einmalig: Python + cloudflared installieren
winget install --id Python.Python.3.12
winget install --id Cloudflare.cloudflared

# im Projektordner:
pip install -r requirements-server.txt
copy .env.example .env        # .env oeffnen, ANTHROPIC_API_KEY eintragen
powershell -ExecutionPolicy Bypass -File .\tunnel.ps1
```

Die ausgegebene `https://….trycloudflare.com`-URL in ⚙ Backend eintragen.

Manuell (zwei Terminals) geht es auch:
```bash
# Terminal 1
export ANTHROPIC_API_KEY=sk-ant-...
export CONNECTLAW_CORS_ORIGINS="https://acortese-wq.github.io"
uvicorn server:app --host 127.0.0.1 --port 8000
# Terminal 2
cloudflared tunnel --url http://localhost:8000
```

Hinweis: Die Quick-Tunnel-URL ändert sich bei jedem Neustart – einfach die
neue URL in ⚙ Backend eintragen. (Mixed-Content: eine HTTPS-Seite kann kein
`http://`-Backend aufrufen, deshalb der Tunnel.)
