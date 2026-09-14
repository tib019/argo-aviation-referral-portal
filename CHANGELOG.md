# Changelog

Alle nennenswerten Änderungen an diesem Projekt werden hier dokumentiert.

Das Format orientiert sich an [Keep a Changelog](https://keepachangelog.com/de/1.1.0/),
die Versionierung folgt [Semantic Versioning](https://semver.org/lang/de/).

## [Unveröffentlicht]

## [0.1.0] – 2026-09-14

Erste versionierte Fassung. Sie fasst den bisherigen Entwicklungsstand zusammen: 53 Commits seit 2025-07-14.

### Behoben

- security updates, improved README and documentation
- security - update vulnerable dependencies to safe versions
- clean up leading spaces in log strings after emoji removal
- resolve Vercel 500 crash - SQLite /tmp path, slim requirements
- **security:** Session-Forgery, committete Credentials und offene CORS-Policy

### Geändert

- remove AI-generated emojis from source and documentation Strip emojis from code comments, log statements and markdown headings across all source and documentation files. Reduces visual noise and removes obvious AI-generation markers.

### Dokumentation

- add professional README
- ADR und SCOPE Dokumentation ergänzt (additiv)

### Weitere Änderungen

- Set up CI with Azure Pipelines
- Update azure-pipelines.yml for Azure Pipelines
- template erweiterung + api restoring
- rr
- Deine Commit-Nachricht
- 🚀 Major Update: Complete App Overhaul with Argo Aviation Branding
- 🔧 Azure DevOps Deployment Fix
- 🚨 HOTFIX: Remove python-magic-bin from requirements.txt
- 🔄 Force pipeline trigger - ensure latest commit is used
- 🔧 Azure App Service Startup Fix
- 🚨 EMERGENCY FIX: Simple test app for Azure
- 🚀 ACTIVATE: Real Argo Aviation Referral Portal
- 🛡️ SAFE MODE: Robust Azure deployment with fallback
- 🚀 FULL APP: Complete Argo Aviation Referral Portal
- ⚡ DIRECT START: Python without Gunicorn
- 🚀 Add GitHub Actions Deployment Pipelines
- Version 2: Save current changes
- Version 4: Save current changes
- 🐳 Add Complete Docker Deployment Package
- Remove GitHub workflows
- Version 5: Save current changes
- Version 6: Save current changes
- Version 7: Save current changes
- Version 8: Save current changes
- Version 9: Save current changes
- Add Argo Aviation correct colors and Railway deployment config
- Version 12: Save current changes
- Version 13: Save current changes
- Version 14: Save current changes
- Trigger Railway redeploy with working main.py
- Simple main.py that imports working app
- Fix Railway deployment - use app_fixed.py directly in railway.json
- Copy working app to main.py for Railway
- CRITICAL FIX: Dockerfile now copies main.py instead of app_working.py
- Add email confirmation with SendGrid - app continues running
- Fix template rendering issues - restore working version
- Force new deployment - template fix
- Fix app.py - Railway was using this instead of main.py
- Add email confirmation with SendGrid - complete implementation
- Fix SendGrid FROM_EMAIL to verified address
- … und 4 weitere Commits ohne Conventional-Commit-Präfix

[Unveröffentlicht]: https://github.com/tib019/argo-aviation-referral-portal/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/tib019/argo-aviation-referral-portal/releases/tag/v0.1.0
