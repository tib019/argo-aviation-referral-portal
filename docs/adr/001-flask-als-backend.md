# ADR-001: Flask als Backend-Framework

**Status:** Accepted  
**Datum:** 2025

## Kontext
Das Argo Aviation Referral Portal benötigt ein Python-Backend für Nutzerregistrierung, Referral-Tracking und E-Mail-Benachrichtigungen.

## Entscheidung
Flask mit SQLAlchemy für das Backend.

## Abgewogene Alternativen
- **FastAPI:** Modernere API, aber asynchron-Konventionen für dieses CRUD-Projekt überdimensioniert
- **Django:** Zu viel Boilerplate für einfaches Referral-Portal

## Konsequenzen
**Positiv:**
- Schnelle Entwicklung für CRUD-Operationen
- Flask-SQLAlchemy für einfache Datenbankzugriffe
- Gut dokumentiert und weit verbreitet

**Negativ:**
- Kein eingebautes async (relevant bei vielen gleichzeitigen E-Mails)
