"""
Shared pytest fixtures for the Argo Aviation Referral Portal test suite.
"""
import io
import pytest
from app import create_app, db as _db
from app.models import User, JobListing, Referral
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret-key'
    SERVER_NAME = None


@pytest.fixture(scope='session')
def app():
    """Create application instance for the test session."""
    application = create_app(TestConfig)
    return application


@pytest.fixture(scope='function')
def db(app):
    """Provide a clean database for each test function."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope='function')
def client(app, db):
    """Provide a test client with a clean database."""
    with app.test_client() as c:
        yield c


@pytest.fixture(scope='function')
def regular_user(db, app):
    """Create and persist a regular (non-admin) user."""
    with app.app_context():
        user = User(
            email='regular@example.com',
            first_name='Regular',
            last_name='User',
            phone_number='+49123456789',
        )
        user.set_password('Password1')
        db.session.add(user)
        db.session.commit()
        # Refresh so the object is usable after commit
        db.session.refresh(user)
        return user


@pytest.fixture(scope='function')
def admin_user(db, app):
    """Create and persist a superadmin user."""
    with app.app_context():
        user = User(
            email='tobi196183@gmail.com',
            first_name='Super',
            last_name='Admin',
        )
        user.set_password('AdminPass1')
        user.is_admin = True
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user


@pytest.fixture(scope='function')
def sample_job(db, app, admin_user):
    """Create and persist a sample active job listing."""
    with app.app_context():
        # Re-query admin_user in this context
        admin = User.query.filter_by(email='tobi196183@gmail.com').first()
        job = JobListing(
            title='Test Pilot',
            description='Flying test aircraft',
            requirements='CPL/IR required',
            location='Frankfurt',
            employment_type='Vollzeit',
            salary_range='60000-80000',
            referral_bonus=1500.00,
            creator_id=admin.user_id,
            is_active=True,
        )
        db.session.add(job)
        db.session.commit()
        db.session.refresh(job)
        return job


def login_client(client, email, password):
    """Helper: log a client in via the auth route."""
    return client.post(
        '/auth/login',
        data={'email': email, 'password': password},
        follow_redirects=True,
    )
