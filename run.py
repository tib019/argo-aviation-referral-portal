#!/usr/bin/env python3
"""
Argo Aviation Referral Portal - Flask App Entry Point
Optimiert für lokale Entwicklung und Azure App Service
"""

import os
import logging
from app import create_app, db

# Erstelle die Flask-App
app = create_app()

# Azure App Service Optimierungen
if not app.debug and os.environ.get('WEBSITE_SITE_NAME'):
    # Wir laufen in Azure App Service
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)
 app.logger.info(' Argo Aviation Referral Portal starting in Azure...')
    
    # Datenbank-Initialisierung für Azure
    with app.app_context():
        try:
            # Erstelle notwendige Verzeichnisse
            os.makedirs('instance', exist_ok=True)
            os.makedirs('logs', exist_ok=True)
            
            # Erstelle Tabellen falls sie nicht existieren
            db.create_all()
 app.logger.info(' Database initialized successfully')
            
        except Exception as e:
 app.logger.error(f' Database error: {e}')

if __name__ == '__main__':
    # Lokale Entwicklung
    app.run(debug=True, port=5001)
else:
    # Azure App Service
    if os.environ.get('WEBSITE_SITE_NAME'):
 app.logger.info(' Argo Aviation Referral Portal ready for production')
