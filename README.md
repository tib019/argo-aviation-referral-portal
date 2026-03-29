# Argo Aviation Referral Portal

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Azure](https://img.shields.io/badge/Azure-Deployed-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

Mitarbeiter-Referral-Portal für die Argo Aviation GmbH, entwickelt als IHK-Abschlussarbeit 2025. Ermöglicht Mitarbeitern, Kandidaten für offene Stellen zu empfehlen, und gibt HR-Teams ein vollständiges Dashboard zur Verwaltung aller Empfehlungen.

---

## Projektüberblick

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
- HR-Dashboard für vollständige Verwaltung aller Empfehlungen
- E-Mail-Benachrichtigungen bei Statusänderungen
- Responsive Design im Argo Aviation Corporate Design
- Docker-Support für einfaches Deployment
- Azure-Integration (Azure SQL, App Service, DevOps)

---

## Quick Start

### Lokal (ohne Docker)

```bash
git clone https://github.com/tib019/argo-aviation-referral-portal.git
cd argo-aviation-referral-portal
pip install -r requirements.txt
python app.py
```

Die Anwendung ist dann unter `http://localhost:5000` erreichbar.

### Docker

```bash
docker-compose up --build
```

---

## Sicherheitsfeatures

| Feature | Implementierung |
|---|---|
| Passwort-Hashing | werkzeug.security |
| CSRF-Schutz | Flask-WTF |
| Session-Management | Flask-Login |
| SQL-Injection-Schutz | SQLAlchemy ORM |

---

## Tests

```bash
pytest tests/ -v
```

58 Tests (Unit, Funktions-, Regressionstests) mit SQLite in-memory Datenbank.

---

## Dokumentation

| Dokument | Beschreibung |
|---|---|
| FINAL_PROJECT_REPORT.md | Vollständiger Projektbericht (DE) |
| FINAL_PROJECT_REPORT_EN.md | Full Project Report (EN) |
| DEVELOPMENT.md | Entwicklungsrichtlinien |
| DOCKER_DEPLOYMENT.md | Docker-Deployment-Anleitung |
| WINDOWS_SETUP.md | Windows-Setup-Anleitung |

---

## Autor

**Tobias Buss** — [@tib019](https://github.com/tib019)

Entwickelt als IHK-Abschlussarbeit 2025 für die Argo Aviation GmbH.

---

## Lizenz

MIT License — siehe [LICENSE](LICENSE) für Details.
