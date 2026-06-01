#!/usr/bin/env bash
# ConnectLAW – lokales Backend + HTTPS-Tunnel (cloudflared).
#
# Liefert eine öffentliche https-URL, die du in der Chat-Seite unter
# ⚙ Backend einträgst. Kein Server, keine Domain nötig.
#
# Voraussetzungen:
#   - pip install -r requirements-server.txt
#   - cloudflared installiert  (https://github.com/cloudflare/cloudflared)
#   - .env mit ANTHROPIC_API_KEY  (oder Variable bereits gesetzt)
#
# Nutzung:  ./tunnel.sh
set -euo pipefail
cd "$(dirname "$0")"

# .env laden, falls vorhanden
if [[ -f .env ]]; then
  set -a; # shellcheck disable=SC1091
  source .env; set +a
fi

if [[ -z "${ANTHROPIC_API_KEY:-}" ]]; then
  echo "Fehler: ANTHROPIC_API_KEY nicht gesetzt (in .env eintragen)." >&2
  exit 1
fi

if ! command -v cloudflared >/dev/null 2>&1; then
  echo "Fehler: 'cloudflared' nicht gefunden." >&2
  echo "Installieren: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/" >&2
  exit 1
fi

# CORS auf die GitHub-Pages-Domain (überschreibbar via .env)
export CONNECTLAW_CORS_ORIGINS="${CONNECTLAW_CORS_ORIGINS:-https://acortese-wq.github.io}"

PORT="${PORT:-8000}"

# Backend im Hintergrund starten, beim Beenden mit aufräumen
echo "Starte Backend auf http://localhost:${PORT} (CORS: ${CONNECTLAW_CORS_ORIGINS}) ..."
uvicorn server:app --host 127.0.0.1 --port "${PORT}" &
BACKEND_PID=$!
trap 'echo; echo "Beende Backend ..."; kill "${BACKEND_PID}" 2>/dev/null || true' EXIT

# Kurz warten, bis das Backend bereit ist
sleep 2

echo
echo "Starte HTTPS-Tunnel. Die ausgegebene https-URL unten in der Chat-Seite"
echo "unter  ⚙ Backend  eintragen (ohne / am Ende, ohne /chat)."
echo "---------------------------------------------------------------"
cloudflared tunnel --url "http://localhost:${PORT}"
