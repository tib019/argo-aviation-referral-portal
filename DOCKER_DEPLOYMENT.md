# Argo Aviation Referral Portal - Docker Deployment

## Schnellstart

### Option 1: Docker Compose (Empfohlen)
```bash
# Repository klonen
git clone https://github.com/tibo47-161/argo-aviation-referral-portal.git
cd argo-aviation-referral-portal

# Mit einem Befehl starten
docker-compose up -d

# App öffnen
open http://localhost:8000
```

### Option 2: Docker Build & Run
```bash
# Image bauen
docker build -t argo-aviation-referral-portal .

# Container starten
docker run -d -p 8000:8000 --name argo-app argo-aviation-referral-portal

# App öffnen
open http://localhost:8000
```

### Option 3: Windows (Automatisch)
```cmd
# Einfach doppelklicken:
docker-deploy.bat
```

## Zugriff

**URL:** http://localhost:8000

**Admin-Login:**
- Email: `admin@argo-aviation.com`
- Passwort: `admin123`

## Features

 **Vollständige Flask-App** mit allen Features
 **Argo Aviation Corporate Design**
 **Benutzer-Registrierung & Login**
 **Job-Portal** mit Luftfahrt-Stellen
 **Referral-System** mit Bonus-Tracking
 **Admin-Dashboard** mit Statistiken
 **Responsive Design** für alle Geräte

## ️ Verwaltung

```bash
# Status prüfen
docker-compose ps

# Logs anzeigen
docker-compose logs -f

# App stoppen
docker-compose down

# App neu starten
docker-compose restart

# Datenbank zurücksetzen
docker-compose down -v
docker-compose up -d
```

## Konfiguration

### Environment-Variablen
```bash
# .env Datei erstellen
FLASK_ENV=production
DATABASE_URL=sqlite:///instance/app.db
SECRET_KEY=your-secret-key-here
```

### Ports ändern
```yaml
# docker-compose.yml
ports:
  - "3000:8000"  # Ändere 3000 zu gewünschtem Port
```

## Produktions-Deployment

### Mit Nginx Reverse Proxy
```bash
# Mit Nginx starten
docker-compose --profile production up -d
```

### Auf Cloud-Servern
```bash
# Für Cloud-Deployment
export FLASK_ENV=production
docker-compose up -d
```

## Troubleshooting

### App startet nicht
```bash
# Logs prüfen
docker-compose logs argo-referral-portal

# Container neu starten
docker-compose restart
```

### Port bereits belegt
```bash
# Anderen Port verwenden
docker run -p 3000:8000 argo-aviation-referral-portal
```

### Datenbank-Probleme
```bash
# Datenbank zurücksetzen
docker-compose down -v
docker-compose up -d
```

## Systemanforderungen

- **Docker:** Version 20.10+
- **Docker Compose:** Version 2.0+
- **RAM:** Mindestens 512MB
- **Speicher:** 1GB freier Speicherplatz

## Öffentliches Deployment

### Railway
```bash
# Automatisches Deployment
git push origin main
```

### Heroku
```bash
# Heroku Container Registry
heroku container:push web
heroku container:release web
```

### DigitalOcean
```bash
# Docker Droplet
doctl apps create --spec .do/app.yaml
```

## Support

Bei Problemen:
1. Logs prüfen: `docker-compose logs -f`
2. Container neu starten: `docker-compose restart`
3. Issue auf GitHub erstellen

---

** Viel Erfolg mit dem Argo Aviation Referral Portal!**
