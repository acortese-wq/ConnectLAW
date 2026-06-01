#!/usr/bin/env python3
"""Webseite einmalig abrufen und als [DOK]-Wissensquelle in knowledge/ ablegen.

Der Inhalt wird als konfigurierte Wissensquelle [DOK] gespeichert (mit echter
Quell-URL und echtem Abrufdatum im Kopf) – nicht als simulierte Live-Recherche.
Danach im Backend einlesen: POST /reload  (oder Backend neu starten).

Nutzung:
    python ingest_url.py https://www.fedlex.admin.ch/eli/cc/....
    python ingest_url.py <URL> --title "OR Art. xy" -o or-werkleitungen.md

Hinweise:
- Lädt nur die EINE angegebene URL (kein Crawling).
- HTML wird zu Text extrahiert (benötigt beautifulsoup4); PDFs werden als
  .pdf gespeichert und vom Backend via pypdf gelesen.
- Nur Seiten einlesen, deren Nutzung zulässig ist. Für öffentliche
  CH-Rechtsquellen i.d.R. unproblematisch.
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
import urllib.parse
import urllib.request

from connectlaw.config import KNOWLEDGE_DIR

USER_AGENT = "ConnectLAW-Ingest/1.0 (intern; juristische Wissensquelle)"


def fetch(url: str) -> tuple[str, bytes, str]:
    """Ruft die URL ab. Rückgabe: (Content-Type, Rohdaten, Zeichensatz)."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310 (bewusst)
        ctype = resp.headers.get_content_type()
        charset = resp.headers.get_content_charset() or "utf-8"
        data = resp.read()
    return ctype, data, charset


def html_to_text(html: str) -> str:
    """Extrahiert Lesetext aus HTML (Navigation/Skripte etc. entfernt)."""
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        sys.exit(
            "beautifulsoup4 fehlt. Installieren: pip install -r requirements-server.txt"
        )
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside", "form"]):
        tag.decompose()
    main = soup.find("main") or soup.find("article") or soup.body or soup
    text = main.get_text("\n")

    # Mehrfache Leerzeilen zusammenfassen
    out: list[str] = []
    blank = False
    for raw in text.splitlines():
        line = raw.strip()
        if line:
            out.append(line)
            blank = False
        elif not blank:
            out.append("")
            blank = True
    return "\n".join(out).strip()


def slugify(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    base = (parsed.netloc + parsed.path).strip("/")
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", base).strip("-").lower()
    return (slug or "webseite")[:80]


def build_document(url: str, title: str, ctype: str, text: str) -> str:
    today = datetime.date.today().isoformat()
    header = [
        f"# [DOK] {title}",
        "",
        f"- Quelle (URL): {url}",
        f"- Abgerufen am: {today}",
        f"- Inhaltstyp: {ctype}",
        "",
        "> Eingelesene Webseite als konfigurierte Wissensquelle [DOK]. Beim",
        "> Zitieren Quelle als [DOK] mit obiger URL und Abrufdatum angeben.",
        "",
        "---",
        "",
    ]
    return "\n".join(header) + text + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Webseite als [DOK]-Wissensquelle einlesen")
    ap.add_argument("url", help="abzurufende URL (öffentliche CH-Rechtsquelle)")
    ap.add_argument("-o", "--output", help="Zieldateiname in knowledge/ (z.B. quelle.md)")
    ap.add_argument("--title", help="Bezeichnung der Quelle (Standard: aus URL)")
    args = ap.parse_args()

    url = args.url
    if not url.lower().startswith(("http://", "https://")):
        ap.error("URL muss mit http:// oder https:// beginnen.")

    try:
        ctype, data, charset = fetch(url)
    except Exception as exc:  # Netzfehler/HTTP-Fehler verständlich melden
        print(f"Fehler beim Abruf: {exc}", file=sys.stderr)
        return 1

    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
    title = args.title or slugify(url)

    # PDFs roh ablegen – das Backend extrahiert den Text via pypdf.
    if "pdf" in ctype:
        name = args.output or (slugify(url) + ".pdf")
        target = KNOWLEDGE_DIR / name
        target.write_bytes(data)
        print(f"PDF gespeichert: {target}")
    else:
        html = data.decode(charset, errors="replace")
        text = html_to_text(html) if "html" in ctype else html.strip()
        if not text:
            print("Warnung: kein Text extrahierbar – nichts gespeichert.", file=sys.stderr)
            return 1
        name = args.output or (slugify(url) + ".md")
        if not name.lower().endswith((".md", ".txt")):
            name += ".md"
        target = KNOWLEDGE_DIR / name
        target.write_text(build_document(url, title, ctype, text), encoding="utf-8")
        print(f"Gespeichert: {target}  ({len(text)} Zeichen)")

    print("Im Backend übernehmen:  curl -X POST http://localhost:8000/reload")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
