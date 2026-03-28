"""
Unit tests for the JSON API routes (Blueprint: api, prefix: /api).

Routes under test:
  GET  /api/jobs                - list active jobs (login required)
  GET  /api/jobs/<id>           - get single job (login required)
  GET  /api/referrals           - list own referrals (login required)
  POST /api/referrals           - create referral (login required)
  GET  /api/users/profile       - get own profile (login required)
  PUT  /api/users/profile       - update own profile (login required)
"""
import json
import pytest
from app import db as _db
from app.models import User, JobListing, Referral


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _login(client, email='regular@example.com', password='Password1'):
    client.post(
        '/auth/login',
        data={'email': email, 'password': password},
        follow_redirects=True,
    )


def _json_post(client, url, payload):
    return client.post(
        url,
        data=json.dumps(payload),
        content_type='application/json',
    )


def _json_put(client, url, payload):
    return client.put(
        url,
        data=json.dumps(payload),
        content_type='application/json',
    )


# ---------------------------------------------------------------------------
# Unauthenticated access
# ---------------------------------------------------------------------------

class TestUnauthenticatedAccess:
    def test_get_jobs_unauthenticated(self, client, db):
        resp = client.get('/api/jobs')
        # Flask-Login redirects to login; 302 or 401 are both acceptable
        assert resp.status_code in (302, 401, 403)

    def test_get_job_detail_unauthenticated(self, client, db):
        resp = client.get('/api/jobs/nonexistent-id')
        assert resp.status_code in (302, 401, 403)

    def test_get_referrals_unauthenticated(self, client, db):
        resp = client.get('/api/referrals')
        assert resp.status_code in (302, 401, 403)

    def test_post_referral_unauthenticated(self, client, db):
        resp = _json_post(client, '/api/referrals', {
            'job_id': 'fake',
            'applicant_email': 'x@y.com',
            'applicant_name': 'X Y',
        })
        assert resp.status_code in (302, 401, 403)

    def test_get_profile_unauthenticated(self, client, db):
        resp = client.get('/api/users/profile')
        assert resp.status_code in (302, 401, 403)


# ---------------------------------------------------------------------------
# GET /api/jobs
# ---------------------------------------------------------------------------

class TestGetJobs:
    def test_get_jobs_returns_json(self, client, db, regular_user, app):
        _login(client)
        resp = client.get('/api/jobs')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert 'jobs' in data
        assert 'pagination' in data

    def test_get_jobs_empty_list(self, client, db, regular_user, app):
        _login(client)
        resp = client.get('/api/jobs')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert isinstance(data['jobs'], list)
        assert len(data['jobs']) == 0

    def test_get_jobs_returns_active_jobs(self, client, db, regular_user, sample_job, app):
        _login(client)
        resp = client.get('/api/jobs')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        titles = [j['title'] for j in data['jobs']]
        assert 'Test Pilot' in titles

    def test_get_jobs_inactive_not_listed(self, client, db, regular_user, admin_user, app):
        with app.app_context():
            admin = User.query.filter_by(email='tobi196183@gmail.com').first()
            job = JobListing(
                title='Inactive Job',
                location='Berlin',
                creator_id=admin.user_id,
                is_active=False,
            )
            db.session.add(job)
            db.session.commit()
        _login(client)
        resp = client.get('/api/jobs')
        data = json.loads(resp.data)
        titles = [j['title'] for j in data['jobs']]
        assert 'Inactive Job' not in titles

    def test_get_jobs_search_filter(self, client, db, regular_user, sample_job, app):
        _login(client)
        resp = client.get('/api/jobs?search=Test+Pilot')
        data = json.loads(resp.data)
        assert any(j['title'] == 'Test Pilot' for j in data['jobs'])

    def test_get_jobs_location_filter(self, client, db, regular_user, sample_job, app):
        _login(client)
        resp = client.get('/api/jobs?location=Frankfurt')
        data = json.loads(resp.data)
        assert any(j['location'] == 'Frankfurt' for j in data['jobs'])

    def test_get_jobs_pagination_keys(self, client, db, regular_user, app):
        _login(client)
        resp = client.get('/api/jobs')
        data = json.loads(resp.data)
        pg = data['pagination']
        assert 'page' in pg and 'per_page' in pg and 'total' in pg and 'pages' in pg


# ---------------------------------------------------------------------------
# GET /api/jobs/<id>
# ---------------------------------------------------------------------------

class TestGetJobDetail:
    def test_get_job_detail_valid_id(self, client, db, regular_user, sample_job, app):
        with app.app_context():
            job = JobListing.query.filter_by(title='Test Pilot').first()
            job_id = job.job_id
        _login(client)
        resp = client.get(f'/api/jobs/{job_id}')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['title'] == 'Test Pilot'

    def test_get_job_detail_invalid_id_returns_404(self, client, db, regular_user, app):
        _login(client)
        resp = client.get('/api/jobs/00000000-0000-0000-0000-000000000000')
        assert resp.status_code == 404

    def test_get_job_detail_fields_present(self, client, db, regular_user, sample_job, app):
        with app.app_context():
            job = JobListing.query.filter_by(title='Test Pilot').first()
            job_id = job.job_id
        _login(client)
        resp = client.get(f'/api/jobs/{job_id}')
        data = json.loads(resp.data)
        for field in ('job_id', 'title', 'location', 'is_active'):
            assert field in data


# ---------------------------------------------------------------------------
# POST /api/referrals
# ---------------------------------------------------------------------------

class TestCreateReferral:
    def test_create_referral_valid(self, client, db, regular_user, sample_job, app):
        with app.app_context():
            job = JobListing.query.filter_by(title='Test Pilot').first()
            job_id = job.job_id
        _login(client)
        resp = _json_post(client, '/api/referrals', {
            'job_id': job_id,
            'applicant_email': 'candidate@jobs.com',
            'applicant_name': 'Good Candidate',
        })
        assert resp.status_code == 201
        data = json.loads(resp.data)
        assert 'referral_id' in data
        assert data['status'] == 'submitted'

    def test_create_referral_persisted_in_db(self, client, db, regular_user, sample_job, app):
        with app.app_context():
            job = JobListing.query.filter_by(title='Test Pilot').first()
            job_id = job.job_id
        _login(client)
        _json_post(client, '/api/referrals', {
            'job_id': job_id,
            'applicant_email': 'persist@jobs.com',
            'applicant_name': 'Persistent Candidate',
        })
        with app.app_context():
            referral = Referral.query.filter_by(applicant_email='persist@jobs.com').first()
            assert referral is not None

    def test_create_referral_missing_field_returns_400(self, client, db, regular_user, sample_job, app):
        with app.app_context():
            job = JobListing.query.filter_by(title='Test Pilot').first()
            job_id = job.job_id
        _login(client)
        resp = _json_post(client, '/api/referrals', {
            'job_id': job_id,
            # missing applicant_email and applicant_name
        })
        assert resp.status_code == 400
        data = json.loads(resp.data)
        assert 'missing' in data

    def test_create_referral_invalid_job_returns_404(self, client, db, regular_user, app):
        _login(client)
        resp = _json_post(client, '/api/referrals', {
            'job_id': '00000000-0000-0000-0000-000000000000',
            'applicant_email': 'x@y.com',
            'applicant_name': 'No Job',
        })
        assert resp.status_code == 404

    def test_create_referral_optional_notes(self, client, db, regular_user, sample_job, app):
        with app.app_context():
            job = JobListing.query.filter_by(title='Test Pilot').first()
            job_id = job.job_id
        _login(client)
        resp = _json_post(client, '/api/referrals', {
            'job_id': job_id,
            'applicant_email': 'notes@jobs.com',
            'applicant_name': 'Notes Candidate',
            'notes': 'Great candidate!',
        })
        assert resp.status_code == 201


# ---------------------------------------------------------------------------
# GET /api/referrals
# ---------------------------------------------------------------------------

class TestListReferrals:
    def test_list_referrals_empty(self, client, db, regular_user, app):
        _login(client)
        resp = client.get('/api/referrals')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['referrals'] == []

    def test_list_referrals_returns_own_referrals(self, client, db, regular_user, sample_job, app):
        with app.app_context():
            job = JobListing.query.filter_by(title='Test Pilot').first()
            job_id = job.job_id
        _login(client)
        _json_post(client, '/api/referrals', {
            'job_id': job_id,
            'applicant_email': 'mine@jobs.com',
            'applicant_name': 'My Candidate',
        })
        resp = client.get('/api/referrals')
        data = json.loads(resp.data)
        emails = [r['applicant_email'] for r in data['referrals']]
        assert 'mine@jobs.com' in emails


# ---------------------------------------------------------------------------
# GET/PUT /api/users/profile
# ---------------------------------------------------------------------------

class TestUserProfile:
    def test_get_profile_returns_user_info(self, client, db, regular_user, app):
        _login(client)
        resp = client.get('/api/users/profile')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['email'] == 'regular@example.com'
        assert data['first_name'] == 'Regular'

    def test_update_profile_first_name(self, client, db, regular_user, app):
        _login(client)
        resp = _json_put(client, '/api/users/profile', {'first_name': 'Updated'})
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['updated'] is True

    def test_update_profile_disallowed_fields_ignored(self, client, db, regular_user, app):
        _login(client)
        _json_put(client, '/api/users/profile', {'is_admin': True})
        resp = client.get('/api/users/profile')
        data = json.loads(resp.data)
        # is_admin should not appear in profile and should not have changed
        assert 'is_admin' not in data
