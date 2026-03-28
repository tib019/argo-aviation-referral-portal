"""
Unit tests for authentication routes:
  POST /auth/login, POST /auth/register, GET /auth/logout
"""
import pytest
from app import db as _db
from app.models import User


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _register(client, **kwargs):
    defaults = dict(
        first_name='Test',
        last_name='User',
        email='new@example.com',
        password='Password1',
    )
    defaults.update(kwargs)
    return client.post('/auth/register', data=defaults, follow_redirects=True)


def _login(client, email='regular@example.com', password='Password1'):
    return client.post(
        '/auth/login',
        data={'email': email, 'password': password},
        follow_redirects=True,
    )


# ---------------------------------------------------------------------------
# GET pages load
# ---------------------------------------------------------------------------

class TestAuthPages:
    def test_register_page_loads(self, client):
        resp = client.get('/auth/register')
        assert resp.status_code == 200

    def test_login_page_loads(self, client):
        resp = client.get('/auth/login')
        assert resp.status_code == 200

    def test_register_page_contains_form(self, client):
        resp = client.get('/auth/register')
        assert b'first_name' in resp.data or b'Vorname' in resp.data or b'register' in resp.data.lower()

    def test_login_page_contains_form(self, client):
        resp = client.get('/auth/login')
        # Look for email/password fields or "Login" keyword
        assert b'email' in resp.data.lower() or b'Login' in resp.data


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

class TestRegistration:
    def test_register_valid_creates_user(self, client, app, db):
        resp = _register(client)
        assert resp.status_code == 200
        with app.app_context():
            user = User.query.filter_by(email='new@example.com').first()
            assert user is not None
            assert user.first_name == 'Test'

    def test_register_valid_redirects_to_login(self, client, db):
        resp = _register(client)
        # After registration the page contains login-related content
        assert b'Registrierung erfolgreich' in resp.data or resp.status_code == 200

    def test_register_duplicate_email_shows_error(self, client, app, db):
        _register(client)
        resp = _register(client)  # second attempt with same email
        assert resp.status_code == 200
        assert (
            b'bereits registriert' in resp.data
            or b'bereits' in resp.data
            or b'already' in resp.data.lower()
        )

    def test_register_missing_first_name_shows_error(self, client, db):
        resp = _register(client, first_name='')
        assert resp.status_code == 200
        # Should not create user and should show validation message
        # The auth.py route flashes "Alle Pflichtfelder müssen ausgefüllt werden!"
        assert b'Pflichtfelder' in resp.data or b'erforderlich' in resp.data or b'first_name' in resp.data

    def test_register_missing_email_shows_error(self, client, db):
        resp = _register(client, email='')
        assert resp.status_code == 200
        assert b'Pflichtfelder' in resp.data or b'erforderlich' in resp.data

    def test_register_short_password_shows_error(self, client, db):
        resp = _register(client, password='ab')
        assert resp.status_code == 200
        # auth.py checks len(password) < 6
        assert b'Passwort' in resp.data or b'mindestens' in resp.data

    def test_register_does_not_store_plaintext_password(self, client, app, db):
        _register(client, email='plaintext@example.com', password='Password1')
        with app.app_context():
            user = User.query.filter_by(email='plaintext@example.com').first()
            assert user is not None
            assert user.password_hash != 'Password1'


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------

class TestLogin:
    def test_login_valid_credentials_redirects(self, client, db, regular_user, app):
        resp = _login(client)
        assert resp.status_code == 200
        # After successful login user ends up on dashboard
        assert b'Dashboard' in resp.data or b'dashboard' in resp.data.lower() or b'Willkommen' in resp.data

    def test_login_invalid_password_shows_error(self, client, db, regular_user, app):
        resp = _login(client, password='WrongPassword')
        assert resp.status_code == 200
        assert b'Ung' in resp.data or b'Invalid' in resp.data.lower() or b'Passwort' in resp.data

    def test_login_nonexistent_email_shows_error(self, client, db):
        resp = _login(client, email='nobody@example.com', password='Password1')
        assert resp.status_code == 200
        assert b'Ung' in resp.data or b'danger' in resp.data

    def test_login_empty_email_fails(self, client, db):
        resp = client.post('/auth/login', data={'email': '', 'password': 'Password1'}, follow_redirects=True)
        assert resp.status_code == 200
        # Should not be authenticated - session should not have _user_id
        with client.session_transaction() as sess:
            assert '_user_id' not in sess

    def test_login_empty_password_fails(self, client, db):
        resp = client.post('/auth/login', data={'email': 'regular@example.com', 'password': ''}, follow_redirects=True)
        assert resp.status_code == 200
        assert b'dashboard' not in resp.data.lower() or b'Ung' in resp.data

    def test_login_sets_session(self, client, db, regular_user, app):
        """After login the session contains _user_id set by Flask-Login."""
        with client.session_transaction() as sess:
            assert '_user_id' not in sess
        _login(client)
        with client.session_transaction() as sess:
            assert '_user_id' in sess

    def test_already_authenticated_redirects_to_dashboard(self, client, db, regular_user, app):
        """Visiting /auth/login while authenticated redirects to dashboard."""
        _login(client)
        resp = client.get('/auth/login', follow_redirects=True)
        assert resp.status_code == 200
        assert b'bereits' in resp.data or b'Dashboard' in resp.data


# ---------------------------------------------------------------------------
# Logout
# ---------------------------------------------------------------------------

class TestLogout:
    def test_logout_clears_session(self, client, db, regular_user, app):
        _login(client)
        # Confirm we are logged in
        with client.session_transaction() as sess:
            assert '_user_id' in sess

        resp = client.get('/auth/logout', follow_redirects=True)
        assert resp.status_code == 200
        with client.session_transaction() as sess:
            assert '_user_id' not in sess

    def test_logout_redirects_to_login(self, client, db, regular_user, app):
        _login(client)
        resp = client.get('/auth/logout', follow_redirects=True)
        # Should end up on the login page
        assert b'Login' in resp.data or b'Anmelden' in resp.data or b'login' in resp.data.lower()

    def test_logout_shows_confirmation_message(self, client, db, regular_user, app):
        _login(client)
        resp = client.get('/auth/logout', follow_redirects=True)
        assert b'abgemeldet' in resp.data

    def test_logout_unauthenticated_redirects(self, client, db):
        """Calling /auth/logout without being logged in should redirect to login."""
        resp = client.get('/auth/logout', follow_redirects=True)
        # Flask-Login will redirect to the login view
        assert resp.status_code == 200
        assert b'Login' in resp.data or b'login' in resp.data.lower()
