"""
Functional tests: full request/response flows through the Flask test client.

Covers:
  - Full registration -> login -> view jobs -> submit referral flow
  - Admin (superadmin) access to admin dashboard
  - Non-admin denied access to admin-only pages
"""
import io
import json
import pytest
from app import db as _db
from app.models import User, JobListing, Referral


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SUPERADMIN_EMAIL = 'tobi196183@gmail.com'
SUPERADMIN_PWD = 'AdminPass1'


def _register_and_login(client, email='flow@example.com', password='FlowPass1',
                         first_name='Flow', last_name='User'):
    """Register a new user and immediately log in."""
    client.post('/auth/register', data={
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
    }, follow_redirects=True)
    return client.post('/auth/login', data={'email': email, 'password': password},
                       follow_redirects=True)


def _create_job(app, db, creator_email, title='Aviation Tech', location='Frankfurt'):
    with app.app_context():
        admin = User.query.filter_by(email=creator_email).first()
        job = JobListing(
            title=title,
            description='Technical aviation role',
            requirements='EASA Part-66',
            location=location,
            creator_id=admin.user_id,
            is_active=True,
        )
        db.session.add(job)
        db.session.commit()
        db.session.refresh(job)
        return job.job_id


# ---------------------------------------------------------------------------
# Full registration -> login -> view jobs -> submit referral flow
# ---------------------------------------------------------------------------

class TestFullUserFlow:
    def test_registration_creates_user(self, client, app, db):
        resp = client.post('/auth/register', data={
            'first_name': 'Alice',
            'last_name': 'Pilot',
            'email': 'alice@aviationtest.com',
            'password': 'AirPlane1',
        }, follow_redirects=True)
        assert resp.status_code == 200
        with app.app_context():
            user = User.query.filter_by(email='alice@aviationtest.com').first()
            assert user is not None

    def test_login_after_registration_succeeds(self, client, app, db):
        client.post('/auth/register', data={
            'first_name': 'Bob',
            'last_name': 'Mech',
            'email': 'bob@aviationtest.com',
            'password': 'Mechanic1',
        }, follow_redirects=True)
        resp = client.post('/auth/login', data={
            'email': 'bob@aviationtest.com',
            'password': 'Mechanic1',
        }, follow_redirects=True)
        assert resp.status_code == 200
        assert b'Dashboard' in resp.data or b'Willkommen' in resp.data

    def test_dashboard_accessible_after_login(self, client, app, db):
        _register_and_login(client, email='dash@test.com', password='DashPass1')
        resp = client.get('/dashboard')
        assert resp.status_code == 200

    def test_jobs_page_accessible_after_login(self, client, app, db):
        _register_and_login(client, email='jobs@test.com', password='JobsPass1')
        resp = client.get('/jobs')
        assert resp.status_code == 200

    def test_view_jobs_shows_active_jobs(self, client, app, db, admin_user):
        _create_job(app, db, SUPERADMIN_EMAIL, title='Loadmaster')
        _register_and_login(client, email='viewer@test.com', password='ViewPass1')
        resp = client.get('/jobs')
        assert resp.status_code == 200
        assert b'Loadmaster' in resp.data

    def test_submit_referral_via_form(self, client, app, db, admin_user):
        job_id = _create_job(app, db, SUPERADMIN_EMAIL, title='Dispatcher')
        _register_and_login(client, email='referrer@test.com', password='ReferPass1')

        resp = client.post(
            f'/jobs/{job_id}/submit-referral',
            data={
                'applicant_name': 'Referral Person',
                'applicant_email': 'referred@test.com',
                'applicant_phone': '+491234567',
                'notes': 'Excellent candidate',
                'resume': (io.BytesIO(b'%PDF-1.4 mock'), 'resume.pdf'),
            },
            content_type='multipart/form-data',
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert b'Referral erfolgreich eingereicht' in resp.data

    def test_my_referrals_shows_submitted_referral(self, client, app, db, admin_user):
        job_id = _create_job(app, db, SUPERADMIN_EMAIL, title='Navigator')
        _register_and_login(client, email='nav@test.com', password='NavPass1')

        client.post(
            f'/jobs/{job_id}/submit-referral',
            data={
                'applicant_name': 'Nav Candidate',
                'applicant_email': 'navcand@test.com',
                'resume': (io.BytesIO(b'%PDF'), 'resume.pdf'),
            },
            content_type='multipart/form-data',
            follow_redirects=True,
        )
        resp = client.get('/my-referrals')
        assert resp.status_code == 200
        assert b'Nav Candidate' in resp.data

    def test_logout_ends_session(self, client, app, db):
        _register_and_login(client, email='logoutflow@test.com', password='LogOut12')
        resp = client.get('/auth/logout', follow_redirects=True)
        assert resp.status_code == 200
        # After logout, dashboard should not be accessible without redirect
        resp2 = client.get('/dashboard', follow_redirects=False)
        assert resp2.status_code in (302, 401, 403)

    def test_full_flow_end_to_end(self, client, app, db, admin_user):
        """Complete end-to-end flow: register -> login -> view jobs -> refer -> my referrals."""
        job_id = _create_job(app, db, SUPERADMIN_EMAIL, title='Cabin Crew')

        # Register
        r = client.post('/auth/register', data={
            'first_name': 'End',
            'last_name': 'ToEnd',
            'email': 'e2e@test.com',
            'password': 'End2End1',
        }, follow_redirects=True)
        assert b'Registrierung erfolgreich' in r.data

        # Login
        r = client.post('/auth/login', data={
            'email': 'e2e@test.com', 'password': 'End2End1'
        }, follow_redirects=True)
        assert b'Dashboard' in r.data or b'Willkommen' in r.data

        # View jobs
        r = client.get('/jobs')
        assert b'Cabin Crew' in r.data

        # Submit referral
        r = client.post(
            f'/jobs/{job_id}/submit-referral',
            data={
                'applicant_name': 'E2E Candidate',
                'applicant_email': 'e2ecand@test.com',
                'resume': (io.BytesIO(b'%PDF'), 'cv.pdf'),
            },
            content_type='multipart/form-data',
            follow_redirects=True,
        )
        assert b'Referral erfolgreich eingereicht' in r.data

        # Check referrals list
        r = client.get('/my-referrals')
        assert b'E2E Candidate' in r.data

        # Logout
        r = client.get('/auth/logout', follow_redirects=True)
        assert b'abgemeldet' in r.data


# ---------------------------------------------------------------------------
# Admin access
# ---------------------------------------------------------------------------

class TestAdminAccess:
    def test_superadmin_can_access_admin_dashboard(self, client, app, db, admin_user):
        client.post('/auth/login', data={
            'email': SUPERADMIN_EMAIL, 'password': SUPERADMIN_PWD
        }, follow_redirects=True)
        resp = client.get('/admin')
        assert resp.status_code == 200

    def test_superadmin_can_access_admin_users(self, client, app, db, admin_user):
        client.post('/auth/login', data={
            'email': SUPERADMIN_EMAIL, 'password': SUPERADMIN_PWD
        }, follow_redirects=True)
        resp = client.get('/admin/users')
        assert resp.status_code == 200

    def test_superadmin_can_access_admin_jobs(self, client, app, db, admin_user):
        client.post('/auth/login', data={
            'email': SUPERADMIN_EMAIL, 'password': SUPERADMIN_PWD
        }, follow_redirects=True)
        resp = client.get('/admin/jobs')
        assert resp.status_code == 200

    def test_regular_user_cannot_access_admin_dashboard(self, client, app, db, regular_user):
        client.post('/auth/login', data={
            'email': 'regular@example.com', 'password': 'Password1'
        }, follow_redirects=True)
        # Without follow_redirects the app returns a 302 redirect away from admin
        resp = client.get('/admin', follow_redirects=False)
        # Must be redirected (302) and NOT allowed in (200 would mean access granted)
        assert resp.status_code == 302
        assert '/admin' not in (resp.headers.get('Location') or '')

    def test_regular_user_cannot_access_admin_users(self, client, app, db, regular_user):
        client.post('/auth/login', data={
            'email': 'regular@example.com', 'password': 'Password1'
        }, follow_redirects=True)
        resp = client.get('/admin/users', follow_redirects=False)
        assert resp.status_code == 302
        assert '/admin' not in (resp.headers.get('Location') or '')

    def test_unauthenticated_user_cannot_access_admin(self, client, db):
        resp = client.get('/admin', follow_redirects=False)
        assert resp.status_code in (302, 401, 403)

    def test_superadmin_stats_api(self, client, app, db, admin_user):
        client.post('/auth/login', data={
            'email': SUPERADMIN_EMAIL, 'password': SUPERADMIN_PWD
        }, follow_redirects=True)
        resp = client.get('/api/stats')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert 'total_users' in data

    def test_regular_user_stats_api_denied(self, client, app, db, regular_user):
        client.post('/auth/login', data={
            'email': 'regular@example.com', 'password': 'Password1'
        }, follow_redirects=True)
        resp = client.get('/api/stats')
        assert resp.status_code == 403
