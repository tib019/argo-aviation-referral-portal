# ADR-002: Multi-Deployment-Strategie (Railway, Docker, Azure, Vercel)

**Status:** Accepted  
**Datum:** 2025

## Kontext
Das Portal muss in verschiedenen Umgebungen deploybar sein (lokal, Cloud, CI/CD).

## Entscheidung
Mehrere Deployment-Optionen wurden implementiert und getestet: Railway, Docker/Docker-Compose, Azure und Vercel.

## Abgewogene Alternativen
- **Nur Railway:** Einfachste Option, aber weniger Kontrolle
- **Nur Docker:** Maximale Portabilität, aber Betrieb erfordert Server

## Konsequenzen
**Positiv:**
- Flexibilität bei der Wahl der Hosting-Umgebung
- Lokale Entwicklung mit Docker identisch zur Produktion

**Negativ:**
- Mehrere Deployment-Konfigurationen müssen gepflegt werden
- Inkonsistenz zwischen verschiedenen Deployment-Artefakten
