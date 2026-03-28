"""
Unit tests for SQLAlchemy models: User, JobListing, Referral.
"""
import uuid
import pytest
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash

from app import db as _db
from app.models import User, JobListing, Referral, SUPERADMIN_EMAIL


# ---------------------------------------------------------------------------
# User model
# ---------------------------------------------------------------------------

class TestUserModel:
    def test_user_creation(self, db, app):
        """A User record can be created with all required fields."""
        with app.app_context():
            user = User(
                email='alice@example.com',
                first_name='Alice',
                last_name='Smith',
            )
            user.set_password('Secret1')
            db.session.add(user)
            db.session.commit()

            fetched = User.query.filter_by(email='alice@example.com').first()
            assert fetched is not None
            assert fetched.first_name == 'Alice'
            assert fetched.last_name == 'Smith'
            assert fetched.is_active is True
            assert fetched.is_admin is False

    def test_user_primary_key_is_uuid(self, db, app):
        """User primary key is a UUID string."""
        with app.app_context():
            user = User(email='bob@example.com', first_name='Bob', last_name='Jones')
            user.set_password('Secret1')
            db.session.add(user)
            db.session.commit()

            fetched = User.query.filter_by(email='bob@example.com').first()
            # Should be parseable as UUID
            uuid.UUID(fetched.user_id)

    def test_email_uniqueness(self, db, app):
        """Two users cannot share the same email address."""
        with app.app_context():
            u1 = User(email='dup@example.com', first_name='A', last_name='B')
            u1.set_password('Secret1')
            u2 = User(email='dup@example.com', first_name='C', last_name='D')
            u2.set_password('Secret1')
            db.session.add(u1)
            db.session.commit()
            db.session.add(u2)
            with pytest.raises(Exception):
                db.session.commit()
            db.session.rollback()

    def test_password_hashing(self, db, app):
        """Password is stored as a hash, not plaintext."""
        with app.app_context():
            user = User(email='hash@example.com', first_name='H', last_name='U')
            user.set_password('MyPassword1')
            db.session.add(user)
            db.session.commit()

            fetched = User.query.filter_by(email='hash@example.com').first()
            assert fetched.password_hash != 'MyPassword1'
            assert fetched.check_password('MyPassword1') is True
            assert fetched.check_password('wrongpassword') is False

    def test_check_password_correct(self, db, app):
        """check_password returns True for the correct password."""
        with app.app_context():
            user = User(email='pw@example.com', first_name='P', last_name='W')
            user.set_password('Correct1')
            db.session.add(user)
            db.session.commit()
            fetched = User.query.filter_by(email='pw@example.com').first()
            assert fetched.check_password('Correct1') is True

    def test_check_password_wrong(self, db, app):
        """check_password returns False for a wrong password."""
        with app.app_context():
            user = User(email='wpw@example.com', first_name='W', last_name='P')
            user.set_password('Correct1')
            db.session.add(user)
            db.session.commit()
            fetched = User.query.filter_by(email='wpw@example.com').first()
            assert fetched.check_password('WrongPass') is False

    def test_is_superadmin_property(self, db, app):
        """is_superadmin returns True only for the configured superadmin email."""
        with app.app_context():
            superadmin = User(
                email=SUPERADMIN_EMAIL,
                first_name='Super',
                last_name='Admin',
            )
            superadmin.set_password('AdminPass1')
            regular = User(email='regular@example.com', first_name='R', last_name='U')
            regular.set_password('RegPass1')
            db.session.add_all([superadmin, regular])
            db.session.commit()

            sa = User.query.filter_by(email=SUPERADMIN_EMAIL).first()
            ru = User.query.filter_by(email='regular@example.com').first()
            assert sa.is_superadmin is True
            assert ru.is_superadmin is False

    def test_has_permission_regular_user(self, db, app):
        """Regular users only have create_referral and view_jobs permissions."""
        with app.app_context():
            user = User(email='reg2@example.com', first_name='R', last_name='U')
            user.set_password('RegPass1')
            db.session.add(user)
            db.session.commit()
            fetched = User.query.filter_by(email='reg2@example.com').first()
            assert fetched.has_permission('create_referral') is True
            assert fetched.has_permission('view_jobs') is True
            assert fetched.has_permission('view_users') is False

    def test_has_permission_admin_user(self, db, app):
        """Admin users have admin-level permissions."""
        with app.app_context():
            user = User(email='adm@example.com', first_name='A', last_name='D')
            user.set_password('AdminPass1')
            user.is_admin = True
            db.session.add(user)
            db.session.commit()
            fetched = User.query.filter_by(email='adm@example.com').first()
            assert fetched.has_permission('view_users') is True
            assert fetched.has_permission('edit_jobs') is True

    def test_registration_date_defaults_to_now(self, db, app):
        """registration_date is set automatically on creation."""
        with app.app_context():
            before = datetime.utcnow()
            user = User(email='ts@example.com', first_name='T', last_name='S')
            user.set_password('Time1Pass')
            db.session.add(user)
            db.session.commit()
            after = datetime.utcnow()
            fetched = User.query.filter_by(email='ts@example.com').first()
            assert before <= fetched.registration_date <= after

    def test_get_id_returns_string(self, db, app):
        """get_id() returns user_id as a string (Flask-Login requirement)."""
        with app.app_context():
            user = User(email='gid@example.com', first_name='G', last_name='I')
            user.set_password('GidPass1')
            db.session.add(user)
            db.session.commit()
            fetched = User.query.filter_by(email='gid@example.com').first()
            assert isinstance(fetched.get_id(), str)


# ---------------------------------------------------------------------------
# JobListing model
# ---------------------------------------------------------------------------

class TestJobListingModel:
    def test_job_creation(self, db, app, admin_user):
        """A JobListing record can be created with required fields."""
        with app.app_context():
            admin = User.query.filter_by(email='tobi196183@gmail.com').first()
            job = JobListing(
                title='Flight Attendant',
                description='Serve passengers',
                requirements='Service experience',
                location='Munich',
                creator_id=admin.user_id,
            )
            db.session.add(job)
            db.session.commit()

            fetched = JobListing.query.filter_by(title='Flight Attendant').first()
            assert fetched is not None
            assert fetched.location == 'Munich'

    def test_job_defaults(self, db, app, admin_user):
        """JobListing is active by default and has a UUID primary key."""
        with app.app_context():
            admin = User.query.filter_by(email='tobi196183@gmail.com').first()
            job = JobListing(
                title='Ground Staff',
                location='Berlin',
                creator_id=admin.user_id,
            )
            db.session.add(job)
            db.session.commit()

            fetched = JobListing.query.filter_by(title='Ground Staff').first()
            assert fetched.is_active is True
            assert fetched.priority == 'normal'
            uuid.UUID(fetched.job_id)

    def test_job_posting_date_defaults(self, db, app, admin_user):
        """posting_date is set automatically."""
        with app.app_context():
            admin = User.query.filter_by(email='tobi196183@gmail.com').first()
            before = datetime.utcnow()
            job = JobListing(title='Mechanic', location='Hamburg', creator_id=admin.user_id)
            db.session.add(job)
            db.session.commit()
            after = datetime.utcnow()
            fetched = JobListing.query.filter_by(title='Mechanic').first()
            assert before <= fetched.posting_date <= after

    def test_job_is_expired_false_when_no_expiry(self, db, app, admin_user):
        """is_expired is False when expiry_date is None."""
        with app.app_context():
            admin = User.query.filter_by(email='tobi196183@gmail.com').first()
            job = JobListing(title='No Expiry', location='Cologne', creator_id=admin.user_id)
            db.session.add(job)
            db.session.commit()
            fetched = JobListing.query.filter_by(title='No Expiry').first()
            assert fetched.is_expired is False

    def test_job_is_expired_true_when_past_expiry(self, db, app, admin_user):
        """is_expired is True when expiry_date is in the past."""
        with app.app_context():
            admin = User.query.filter_by(email='tobi196183@gmail.com').first()
            job = JobListing(
                title='Expired Job',
                location='Dusseldorf',
                creator_id=admin.user_id,
                expiry_date=datetime.utcnow() - timedelta(days=1),
            )
            db.session.add(job)
            db.session.commit()
            fetched = JobListing.query.filter_by(title='Expired Job').first()
            assert fetched.is_expired is True

    def test_job_creator_relationship(self, db, app, admin_user):
        """JobListing.creator back-references the User who created it."""
        with app.app_context():
            admin = User.query.filter_by(email='tobi196183@gmail.com').first()
            job = JobListing(title='Captain', location='Stuttgart', creator_id=admin.user_id)
            db.session.add(job)
            db.session.commit()
            fetched = JobListing.query.filter_by(title='Captain').first()
            assert fetched.creator is not None
            assert fetched.creator.email == 'tobi196183@gmail.com'


# ---------------------------------------------------------------------------
# Referral model
# ---------------------------------------------------------------------------

class TestReferralModel:
    def test_referral_creation(self, db, app, regular_user, sample_job):
        """A Referral record can be created with required fields."""
        with app.app_context():
            user = User.query.filter_by(email='regular@example.com').first()
            job = JobListing.query.filter_by(title='Test Pilot').first()
            referral = Referral(
                referrer_id=user.user_id,
                job_id=job.job_id,
                applicant_email='candidate@test.com',
                applicant_name='Jane Candidate',
            )
            db.session.add(referral)
            db.session.commit()

            fetched = Referral.query.filter_by(applicant_email='candidate@test.com').first()
            assert fetched is not None
            assert fetched.applicant_name == 'Jane Candidate'

    def test_referral_default_status(self, db, app, regular_user, sample_job):
        """Referral status defaults to 'submitted'."""
        with app.app_context():
            user = User.query.filter_by(email='regular@example.com').first()
            job = JobListing.query.filter_by(title='Test Pilot').first()
            referral = Referral(
                referrer_id=user.user_id,
                job_id=job.job_id,
                applicant_email='defaultstatus@test.com',
                applicant_name='Default Status',
            )
            db.session.add(referral)
            db.session.commit()
            fetched = Referral.query.filter_by(applicant_email='defaultstatus@test.com').first()
            assert fetched.status == 'submitted'

    def test_referral_uuid_primary_key(self, db, app, regular_user, sample_job):
        """Referral primary key is a UUID string."""
        with app.app_context():
            user = User.query.filter_by(email='regular@example.com').first()
            job = JobListing.query.filter_by(title='Test Pilot').first()
            referral = Referral(
                referrer_id=user.user_id,
                job_id=job.job_id,
                applicant_email='uuid@test.com',
                applicant_name='UUID Test',
            )
            db.session.add(referral)
            db.session.commit()
            fetched = Referral.query.filter_by(applicant_email='uuid@test.com').first()
            uuid.UUID(fetched.referral_id)

    def test_referral_referrer_relationship(self, db, app, regular_user, sample_job):
        """Referral.referrer_user back-references the User who submitted it."""
        with app.app_context():
            user = User.query.filter_by(email='regular@example.com').first()
            job = JobListing.query.filter_by(title='Test Pilot').first()
            referral = Referral(
                referrer_id=user.user_id,
                job_id=job.job_id,
                applicant_email='rel@test.com',
                applicant_name='Rel Test',
            )
            db.session.add(referral)
            db.session.commit()
            fetched = Referral.query.filter_by(applicant_email='rel@test.com').first()
            assert fetched.referrer_user is not None
            assert fetched.referrer_user.email == 'regular@example.com'

    def test_referral_job_relationship(self, db, app, regular_user, sample_job):
        """Referral.job_listing back-references the JobListing."""
        with app.app_context():
            user = User.query.filter_by(email='regular@example.com').first()
            job = JobListing.query.filter_by(title='Test Pilot').first()
            referral = Referral(
                referrer_id=user.user_id,
                job_id=job.job_id,
                applicant_email='jobrel@test.com',
                applicant_name='Job Rel',
            )
            db.session.add(referral)
            db.session.commit()
            fetched = Referral.query.filter_by(applicant_email='jobrel@test.com').first()
            assert fetched.job_listing is not None
            assert fetched.job_listing.title == 'Test Pilot'

    def test_referral_update_status_valid(self, db, app, regular_user, sample_job):
        """update_status accepts valid status transitions."""
        with app.app_context():
            user = User.query.filter_by(email='regular@example.com').first()
            job = JobListing.query.filter_by(title='Test Pilot').first()
            referral = Referral(
                referrer_id=user.user_id,
                job_id=job.job_id,
                applicant_email='statusupdate@test.com',
                applicant_name='Status Update',
            )
            db.session.add(referral)
            db.session.commit()
            fetched = Referral.query.filter_by(applicant_email='statusupdate@test.com').first()
            result = fetched.update_status('hired', notes='Great fit')
            assert result is True
            assert fetched.status == 'hired'
            assert fetched.hired_date is not None

    def test_referral_update_status_invalid(self, db, app, regular_user, sample_job):
        """update_status rejects invalid status values."""
        with app.app_context():
            user = User.query.filter_by(email='regular@example.com').first()
            job = JobListing.query.filter_by(title='Test Pilot').first()
            referral = Referral(
                referrer_id=user.user_id,
                job_id=job.job_id,
                applicant_email='badinvalid@test.com',
                applicant_name='Bad Status',
            )
            db.session.add(referral)
            db.session.commit()
            fetched = Referral.query.filter_by(applicant_email='badinvalid@test.com').first()
            result = fetched.update_status('not_a_real_status')
            assert result is False
            assert fetched.status == 'submitted'

    def test_referral_referral_date_defaults(self, db, app, regular_user, sample_job):
        """referral_date is set automatically on creation."""
        with app.app_context():
            user = User.query.filter_by(email='regular@example.com').first()
            job = JobListing.query.filter_by(title='Test Pilot').first()
            before = datetime.utcnow()
            referral = Referral(
                referrer_id=user.user_id,
                job_id=job.job_id,
                applicant_email='datetest@test.com',
                applicant_name='Date Test',
            )
            db.session.add(referral)
            db.session.commit()
            after = datetime.utcnow()
            fetched = Referral.query.filter_by(applicant_email='datetest@test.com').first()
            assert before <= fetched.referral_date <= after
