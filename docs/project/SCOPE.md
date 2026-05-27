# Projektscope — Argo Aviation Referral Portal

## Problem
Argo Aviation (Luftfahrt-Branche) benötigt ein strukturiertes System für Mitarbeiter-Empfehlungen und Referral-Tracking. Manuelle Prozesse sind fehleranfällig.

## Lösung
Ein webbasiertes Referral-Portal für Argo Aviation: Nutzer können Kandidaten empfehlen, Referrals tracken und werden über Status-Änderungen per E-Mail benachrichtigt.

## In Scope
- Nutzerregistrierung und -login
- Referral-Einreichung mit Kandidaten-Profil
- Referral-Status-Tracking (Eingereicht, In Review, Akzeptiert, Abgelehnt)
- E-Mail-Benachrichtigungen bei Status-Änderungen
- Admin-Dashboard für HR-Verwaltung
- Docker-Deployment
- Azure Pipelines CI/CD

## Out of Scope
- Bewerbungs-Management (ATS)
- Video-Interviews
- Mobile App

## Technologie-Stack
| Schicht | Technologie |
|---------|-------------|
| Backend | Python, Flask |
| Datenbank | SQLite/PostgreSQL |
| E-Mail | SMTP / E-Mail-Utils |
| Containerisierung | Docker, Docker Compose |
| CI/CD | Azure Pipelines |
| Hosting | Railway / Azure / Vercel |
| Tests | pytest, Playwright |
