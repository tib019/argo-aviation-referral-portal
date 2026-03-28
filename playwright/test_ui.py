"""
Playwright UI tests for the Argo Aviation Referral Portal.

These tests require a running Flask server.  They are intentionally skipped
when no server is available (PORTAL_URL env var unset) so they don't break CI
pipelines that only run the pytest unit/functional suite.

To run manually:
  1. Start the app:   flask run --port 5000
  2. Set env var:     export PORTAL_URL=http://localhost:5000
  3. Run tests:       pytest playwright/ -v

The tests use pytest + playwright-python (sync API).
Install:  pip install pytest-playwright && playwright install chromium
"""
import os
import pytest

BASE_URL = os.environ.get('PORTAL_URL', '')

# Skip all playwright tests when no server URL is configured.
pytestmark = pytest.mark.skipif(
    not BASE_URL,
    reason='PORTAL_URL is not set; skipping Playwright UI tests.'
)

try:
    from playwright.sync_api import sync_playwright, expect
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope='module')
def browser_context():
    """Provide a Playwright browser context for the test module."""
    if not PLAYWRIGHT_AVAILABLE:
        pytest.skip('playwright is not installed')
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()


@pytest.fixture
def page(browser_context):
    """Provide a fresh page for each test."""
    pg = browser_context.new_page()
    yield pg
    pg.close()


# ---------------------------------------------------------------------------
# Homepage / login redirect
# ---------------------------------------------------------------------------

class TestHomepage:
    def test_homepage_loads(self, page):
        """Visiting / should return a 200-level response."""
        response = page.goto(BASE_URL + '/')
        assert response.status < 400

    def test_homepage_redirects_to_login(self, page):
        """Unauthenticated visit to / should end up on the login page."""
        page.goto(BASE_URL + '/')
        assert '/auth/login' in page.url or 'login' in page.url.lower()

    def test_page_title_contains_argo(self, page):
        """Page title should mention 'Argo'."""
        page.goto(BASE_URL + '/')
        assert 'Argo' in page.title() or 'argo' in page.title().lower()


# ---------------------------------------------------------------------------
# Login form
# ---------------------------------------------------------------------------

class TestLoginForm:
    def test_login_page_loads(self, page):
        page.goto(BASE_URL + '/auth/login')
        assert page.url.endswith('/auth/login') or 'login' in page.url

    def test_login_form_has_email_field(self, page):
        page.goto(BASE_URL + '/auth/login')
        assert page.locator('input[name="email"]').count() > 0

    def test_login_form_has_password_field(self, page):
        page.goto(BASE_URL + '/auth/login')
        assert page.locator('input[name="password"]').count() > 0

    def test_login_form_has_submit_button(self, page):
        page.goto(BASE_URL + '/auth/login')
        # Accept any button/submit element
        btn = page.locator('button[type="submit"], input[type="submit"]')
        assert btn.count() > 0

    def test_login_invalid_credentials_shows_error(self, page):
        page.goto(BASE_URL + '/auth/login')
        page.fill('input[name="email"]', 'nobody@example.com')
        page.fill('input[name="password"]', 'wrongpassword')
        page.click('button[type="submit"], input[type="submit"]')
        page.wait_for_load_state('networkidle')
        # Should stay on login page (or show flash message)
        assert 'login' in page.url.lower() or page.locator('.alert-danger, .flash-error').count() > 0


# ---------------------------------------------------------------------------
# Registration form
# ---------------------------------------------------------------------------

class TestRegistrationForm:
    def test_register_page_loads(self, page):
        page.goto(BASE_URL + '/auth/register')
        assert page.url.endswith('/auth/register') or 'register' in page.url

    def test_register_form_has_required_fields(self, page):
        page.goto(BASE_URL + '/auth/register')
        assert page.locator('input[name="first_name"]').count() > 0
        assert page.locator('input[name="last_name"]').count() > 0
        assert page.locator('input[name="email"]').count() > 0
        assert page.locator('input[name="password"]').count() > 0

    def test_register_with_valid_data_redirects_to_login(self, page):
        page.goto(BASE_URL + '/auth/register')
        page.fill('input[name="first_name"]', 'Playwright')
        page.fill('input[name="last_name"]', 'Tester')
        page.fill('input[name="email"]', 'playwright@uiTest.com')
        page.fill('input[name="password"]', 'UITest123')
        page.click('button[type="submit"], input[type="submit"]')
        page.wait_for_load_state('networkidle')
        # Should redirect to login after successful registration
        assert 'login' in page.url.lower() or 'Registrierung' in page.content()

    def test_register_duplicate_email_shows_warning(self, page):
        page.goto(BASE_URL + '/auth/register')
        page.fill('input[name="first_name"]', 'Duplicate')
        page.fill('input[name="last_name"]', 'User')
        page.fill('input[name="email"]', 'playwright@uiTest.com')
        page.fill('input[name="password"]', 'UITest123')
        page.click('button[type="submit"], input[type="submit"]')
        page.wait_for_load_state('networkidle')
        assert 'bereits' in page.content() or 'already' in page.content().lower()


# ---------------------------------------------------------------------------
# Job list page
# ---------------------------------------------------------------------------

class TestJobListPage:
    def _login(self, page, email='playwright@uiTest.com', password='UITest123'):
        page.goto(BASE_URL + '/auth/login')
        page.fill('input[name="email"]', email)
        page.fill('input[name="password"]', password)
        page.click('button[type="submit"], input[type="submit"]')
        page.wait_for_load_state('networkidle')

    def test_jobs_page_renders_after_login(self, page):
        self._login(page)
        page.goto(BASE_URL + '/jobs')
        assert page.url.endswith('/jobs') or 'jobs' in page.url
        assert page.locator('body').count() > 0

    def test_jobs_page_has_title(self, page):
        self._login(page)
        page.goto(BASE_URL + '/jobs')
        content = page.content()
        assert 'Stellen' in content or 'Jobs' in content or 'job' in content.lower()

    def test_dashboard_shows_user_name(self, page):
        self._login(page)
        page.goto(BASE_URL + '/dashboard')
        content = page.content()
        assert 'Playwright' in content or 'Dashboard' in content
