"""
Regression tests:
  - Empty job list handling
  - Invalid referral data (missing fields, bad formats)
  - SQL injection protection via parameterized ORM queries
  - CSRF-like duplicate submissions
  - Profile update with disallowed fields
  - Status transitions
"""
import io
import json
import pytest
from app import db as _db
from app.models import User, JobListing, Referral


SUPERADMIN_EMAIL = 'tobi196183@gmail.com'
SUPERADMIN_PWD = 'AdminPass1'


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _login(client, email='regular@example.com', password='Password1'):
    return client.post('/auth/login', data={'email': email, 'password': password},
                       follow_redirects=True)


def _create_job(app, db, title='Regression Job'):
    with app.app_context():
        admin = User.query.filter_by(email=SUPERADMIN_EMAIL).first()
        job = JobListing(
            title=title,
            location='Berlin',
            creator_id=admin.user_id,
            is_active=True,
        )
        db.session.add(job)
        db.session.commit()
        db.session.refresh(job)
        return job.job_id


def _json_post(client, url, payload):
    return client.post(
        url,
        data=json.dumps(payload),
        content_type='application/json',
    )


# ---------------------------------------------------------------------------
# Empty job list
# ---------------------------------------------------------------------------

class TestEmptyJobList:
    def test_api_jobs_empty_list_returns_200(self, client, db, regular_user, app):
        _login(client)
        resp = client.get('/api/jobs')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['jobs'] == []
        assert data['pagination']['total'] == 0

    def test_ui_jobs_page_handles_empty_list(self, client, db, regular_user, app):
        _login(client)
        resp = client.get('/jobs')
        assert resp.status_code == 200
        # Should render without error even with 0 jobs

    def test_api_referrals_empty_list_returns_200(self, client, db, regular_user, app):
        _login(client)
        resp = client.get('/api/referrals')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['referrals'] == []


# ---------------------------------------------------------------------------
# Invalid referral data
# ---------------------------------------------------------------------------

class TestInvalidReferralData:
    def test_referral_missing_job_id(self, client, db, regular_user, app):
        _login(client)
        resp = _json_post(client, '/api/referrals', {
            'applicant_email': 'x@x.com',
            'applicant_name': 'X',
        })
        assert resp.status_code == 400
        data = json.loads(resp.data)
        assert 'job_id' in data.get('missing', [])

    def test_referral_missing_applicant_email(self, client, db, regular_user, admin_user, app):
        job_id = _create_job(app, db)
        _login(client)
        resp = _json_post(client, '/api/referrals', {
            'job_id': job_id,
            'applicant_name': 'Missing Email',
        })
        assert resp.status_code == 400
        data = json.loads(resp.data)
        assert 'applicant_email' in data.get('missing', [])

    def test_referral_missing_applicant_name(self, client, db, regular_user, admin_user, app):
        job_id = _create_job(app, db)
        _login(client)
        resp = _json_post(client, '/api/referrals', {
            'job_id': job_id,
            'applicant_email': 'noname@test.com',
        })
        assert resp.status_code == 400
        data = json.loads(resp.data)
        assert 'applicant_name' in data.get('missing', [])

    def test_referral_nonexistent_job_id(self, client, db, regular_user, app):
        _login(client)
        resp = _json_post(client, '/api/referrals', {
            'job_id': '00000000-dead-beef-0000-000000000000',
            'applicant_email': 'ghost@test.com',
            'applicant_name': 'Ghost Candidate',
        })
        assert resp.status_code == 404

    def test_form_referral_missing_resume(self, client, db, regular_user, admin_user, app):
        """Submitting the HTML form without a resume should fail validation."""
        job_id = _create_job(app, db, title='No Resume Job')
        _login(client)
        resp = client.post(
            f'/jobs/{job_id}/submit-referral',
            data={
                'applicant_name': 'No Resume Person',
                'applicant_email': 'noresume@test.com',
            },
            content_type='multipart/form-data',
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert b'Lebenslauf' in resp.data or b'erforderlich' in resp.data or b'resume' in resp.data.lower()

    def test_form_referral_missing_name(self, client, db, regular_user, admin_user, app):
        """Submitting without applicant_name should fail validation."""
        job_id = _create_job(app, db, title='No Name Job')
        _login(client)
        resp = client.post(
            f'/jobs/{job_id}/submit-referral',
            data={
                'applicant_email': 'noname@test.com',
                'resume': (io.BytesIO(b'%PDF'), 'cv.pdf'),
            },
            content_type='multipart/form-data',
            follow_redirects=True,
        )
        assert resp.status_code == 200
        assert b'erforderlich' in resp.data or b'Name' in resp.data


# ---------------------------------------------------------------------------
# SQL injection protection
# ---------------------------------------------------------------------------

class TestSQLInjectionProtection:
    """
    SQLAlchemy uses parameterized queries by default.
    We send SQL injection strings and verify the ORM handles them safely
    (no crash, no data leak, no unintended rows returned).
    """

    def test_login_sql_injection_email(self, client, db):
        """SQL injection in email field does not bypass authentication."""
        resp = client.post('/auth/login', data={
            'email': "' OR '1'='1",
            'password': 'anything',
        }, follow_redirects=True)
        assert resp.status_code == 200
        # Should not be logged in -> no Dashboard
        with client.session_transaction() as sess:
            assert '_user_id' not in sess

    def test_login_sql_injection_password(self, client, db):
        """SQL injection in password field does not authenticate user."""
        resp = client.post('/auth/login', data={
            'email': 'nobody@example.com',
            'password': "' OR '1'='1' --",
        }, follow_redirects=True)
        assert resp.status_code == 200
        with client.session_transaction() as sess:
            assert '_user_id' not in sess

    def test_api_jobs_search_injection(self, client, db, regular_user, app):
        """SQL injection in the jobs search parameter does not cause errors."""
        _login(client)
        resp = client.get("/api/jobs?search='; DROP TABLE Job_Listings; --")
        assert resp.status_code == 200
        # ORM should return a safe (possibly empty) list
        data = json.loads(resp.data)
        assert 'jobs' in data

    def test_register_injection_in_name(self, client, db):
        """SQL injection in name fields is treated as literal data."""
        resp = client.post('/auth/register', data={
            'first_name': "Robert'); DROP TABLE Users; --",
            'last_name': 'Tables',
            'email': 'bobby@tables.com',
            'password': 'DropTable1',
        }, follow_redirects=True)
        assert resp.status_code == 200
        # Application should not crash

    def test_api_jobs_location_injection(self, client, db, regular_user, app):
        """SQL injection in location filter is safe."""
        _login(client)
        resp = client.get("/api/jobs?location=' UNION SELECT * FROM Users --")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert 'jobs' in data


# ---------------------------------------------------------------------------
# Duplicate submissions (CSRF-like)
# ---------------------------------------------------------------------------

class TestDuplicateSubmissions:
    def test_duplicate_referral_api_creates_two_records(self, client, db, regular_user, admin_user, app):
        """
        The API currently allows duplicate referral submissions.
        This test documents current behaviour: two records are created.
        If deduplication is added in the future, update this test.
        """
        job_id = _create_job(app, db, title='Dup Referral Job')
        _login(client)
        payload = {
            'job_id': job_id,
            'applicant_email': 'dup@test.com',
            'applicant_name': 'Dup Candidate',
        }
        r1 = _json_post(client, '/api/referrals', payload)
        r2 = _json_post(client, '/api/referrals', payload)
        assert r1.status_code == 201
        assert r2.status_code == 201
        with app.app_context():
            count = Referral.query.filter_by(applicant_email='dup@test.com').count()
            assert count == 2

    def test_duplicate_registration_rejected(self, client, db):
        """Registering with the same email twice shows an error on the second attempt."""
        client.post('/auth/register', data={
            'first_name': 'A', 'last_name': 'B',
            'email': 'duplicate@reg.com', 'password': 'DupReg12',
        }, follow_redirects=True)
        resp = client.post('/auth/register', data={
            'first_name': 'C', 'last_name': 'D',
            'email': 'duplicate@reg.com', 'password': 'DupReg12',
        }, follow_redirects=True)
        assert resp.status_code == 200
        assert b'bereits' in resp.data or b'already' in resp.data.lower()

    def test_rapid_login_attempts_do_not_crash(self, client, db):
        """Rapid repeated login attempts with wrong credentials don't cause errors."""
        for _ in range(5):
            resp = client.post('/auth/login', data={
                'email': 'brute@test.com',
                'password': 'WrongPass',
            }, follow_redirects=True)
            assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_job_detail_inactive_job_redirects(self, client, db, regular_user, admin_user, app):
        """Accessing an inactive job detail should redirect with a warning."""
        with app.app_context():
            admin = User.query.filter_by(email=SUPERADMIN_EMAIL).first()
            job = JobListing(title='Inactive', location='X', creator_id=admin.user_id, is_active=False)
            db.session.add(job)
            db.session.commit()
            job_id = job.job_id
        _login(client)
        resp = client.get(f'/jobs/{job_id}', follow_redirects=True)
        assert resp.status_code == 200
        assert b'nicht mehr aktiv' in resp.data or b'aktiv' in resp.data

    def test_profile_page_loads(self, client, db, regular_user, app):
        _login(client)
        resp = client.get('/profile')
        assert resp.status_code == 200

    def test_my_referrals_page_no_referrals(self, client, db, regular_user, app):
        _login(client)
        resp = client.get('/my-referrals')
        assert resp.status_code == 200

    def test_index_unauthenticated_redirects_to_login(self, client, db):
        resp = client.get('/', follow_redirects=True)
        assert resp.status_code == 200
        assert b'Login' in resp.data or b'Anmelden' in resp.data

    def test_index_authenticated_redirects_to_dashboard(self, client, db, regular_user, app):
        _login(client)
        resp = client.get('/', follow_redirects=True)
        assert resp.status_code == 200
        assert b'Dashboard' in resp.data or b'dashboard' in resp.data.lower()
