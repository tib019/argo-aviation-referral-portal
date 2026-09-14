# app/__init__.py - KORRIGIERTE VERSION
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import logging
from logging.handlers import RotatingFileHandler
import os
from config import Config

# Globale Instanzen
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

# KORREKTUR 1: Login Manager Konfiguration
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Bitte melden Sie sich an, um auf diese Seite zuzugreifen.'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # KORREKTUR 2: Entfernung der Debug-Print-Statements
    # Stattdessen: Proper Logging
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/referral_portal.log',
                                         maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Referral Portal startup')

    # KORREKTUR 3: Initialisierung der Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # KORREKTUR 4: User Loader Funktion
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        try:
            return User.query.get(user_id)
        except Exception as e:
            app.logger.error(f'Error loading user {user_id}: {e}')
            return None

    # KORREKTUR 5: Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    # Import Models (nach db.init_app)
    from app.models import User, JobListing, Referral

    # Blueprint Registration
    from app.auth import auth_bp
    from app.main import main_bp
    from app.api import api_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    # CORS: nur explizit freigegebene Origins statt '*'.
    # Wildcard erlaubte jeder fremden Seite, die API-Antworten dieser App
    # im Browser auszulesen. Erlaubte Origins kommagetrennt in CORS_ORIGINS.
    allowed_origins = {
        o.strip() for o in os.environ.get('CORS_ORIGINS', '').split(',') if o.strip()
    }

    @app.after_request
    def after_request(response):
        origin = request.headers.get('Origin')
        if origin and origin in allowed_origins:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
            response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
        response.headers.add('Vary', 'Origin')
        return response

    return app
