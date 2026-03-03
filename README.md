# Argo Aviation Referral Portal

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Azure](https://img.shields.io/badge/Azure-Deployed-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

Ein professionelles **Mitarbeiter-Referral-Portal** fuer die Argo Aviation GmbH, entwickelt als IHK-Abschlussprojekt 2025.

---

## Projektueberblick

| Eigenschaft | Details |
|---|---|
| **Backend** | Python 3.11, Flask 2.3, SQLAlchemy |
| **Frontend** | HTML5, CSS3, JavaScript, Jinja2 |
| **Datenbank** | Azure SQL Database / SQLite (lokal) |
| **Deployment** | Azure App Service, Docker, Railway |
| **CI/CD** | Azure DevOps Pipelines |
| **Kontext** | IHK-Abschlussarbeit 2025 |

---

## Features

- Benutzerregistrierung und Authentifizierung mit sicherem Passwort-Hashing
- Rollenbasierte Zugriffskontrolle (Mitarbeiter, HR, Admin)
- Referral-Einreichung mit Lebenslauf-Upload
- Status-Tracking in Echtzeit
- HR-Dashboard fuer vollstaendige Verwaltung aller Empfehlungen
- E-Mail-Benachrichtigungen bei Statusaenderungen
- Responsive Design im Argo Aviation Corporate Design
- Docker-Support fuer einfaches Deployment
- Azure-Integration (Azure SQL, App Service, DevOps)

---

## Quick Start



Die Anwendung ist dann unter http://localhost:5000 erreichbar.

### Docker



---

## Sicherheitsfeatures

| Feature | Implementierung |
|---|---|
| Passwort-Hashing | werkzeug.security |
| CSRF-Schutz | Flask-WTF |
| Session-Management | Flask-Login |
| SQL-Injection-Schutz | SQLAlchemy ORM |

---

## Dokumentation

| Dokument | Beschreibung |
|---|---|
| FINAL_PROJECT_REPORT.md | Vollstaendiger Projektbericht (DE) |
| FINAL_PROJECT_REPORT_EN.md | Full Project Report (EN) |
| DEVELOPMENT.md | Entwicklungsrichtlinien |
| DOCKER_DEPLOYMENT.md | Docker-Deployment-Anleitung |
| WINDOWS_SETUP.md | Windows-Setup-Anleitung |

---

## Autor

**Tobias** - [@tib019](https://github.com/tib019)

Entwickelt als **IHK-Abschlussarbeit 2025** fuer die Argo Aviation GmbH.

---

## Lizenz

MIT License - siehe LICENSE fuer Details.
