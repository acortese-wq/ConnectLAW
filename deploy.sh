#!/usr/bin/env bash
# ConnectLAW – Deployment-Helfer für Backend + Caddy (automatisches HTTPS).
#
# Nutzung:
#   cp .env.example .env   # ANTHROPIC_API_KEY, DOMAIN, CONNECTLAW_CORS_ORIGINS setzen
#   ./deploy.sh up         # bauen & starten
#   ./deploy.sh logs       # Logs ansehen
#   ./deploy.sh reload     # knowledge/ ohne Neustart neu einlesen
#   ./deploy.sh down       # stoppen
set -euo pipefail

cd "$(dirname "$0")"

# docker compose (v2) oder docker-compose (v1) erkennen
if docker compose version >/dev/null 2>&1; then
  DC="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
  DC="docker-compose"
else
  echo "Fehler: Docker Compose nicht gefunden. Bitte Docker installieren." >&2
  exit 1
fi

if [[ ! -f .env ]]; then
  echo "Fehler: .env fehlt. Bitte 'cp .env.example .env' und Werte setzen" >&2
  echo "       (ANTHROPIC_API_KEY, DOMAIN, CONNECTLAW_CORS_ORIGINS)." >&2
  exit 1
fi

cmd="${1:-up}"
case "$cmd" in
  up)
    $DC up -d --build
    echo
    echo "Gestartet. Caddy beschafft das TLS-Zertifikat für deine DOMAIN."
    echo "Trage in der Chat-Seite unter ⚙ Backend ein:  https://<DOMAIN>"
    ;;
  down)    $DC down ;;
  logs)    $DC logs -f --tail=100 ;;
  restart) $DC restart ;;
  reload)
    # knowledge/ im laufenden Backend neu einlesen
    $DC exec backend python -c "import urllib.request,urllib.error; \
      req=urllib.request.Request('http://localhost:8000/reload',method='POST'); \
      print(urllib.request.urlopen(req).read().decode())"
    ;;
  *)
    echo "Unbekannter Befehl: $cmd  (up|down|logs|restart|reload)" >&2
    exit 1
    ;;
esac
