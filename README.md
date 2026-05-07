# Django + Playwright Demo (Register/Login/User Management)

✅ How to setup Playwright framework
✅ Sample Unit, API and E2E tests
✅ CI pipeline integration (multi-stage)
✅ Coverage % badge
✅ PR coverage comments
✅ HTML reports
✅ Allure dashboard (best-in-class UI)

This is a minimal Django app with:
- UI screens: Register, Login, Manage Users (list/add/edit), Logout
- API endpoints (DRF): /api/users/ (list/create), /api/users/<id>/ (retrieve/update)
- Tests:
  - Unit tests (pytest + pytest-django)
  - API tests (pytest + DRF APIClient)
  - E2E tests (pytest-playwright) using Django's live_server

## Quickstart (local)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Browse:
- http://127.0.0.1:8000/register/
- http://127.0.0.1:8000/login/
- http://127.0.0.1:8000/users/

## Run tests

```bash
pytest
```

### Run E2E only

```bash
pytest -m e2e
```

## Postgres (optional)

A docker-compose file is provided.

```bash
docker compose up -d
export DATABASE_URL=postgres://demo:demo@127.0.0.1:5432/demo
python manage.py migrate
python manage.py runserver
```

# Playwright Django Automation

## ✅ CI Pipeline
![CI](https://github.com/ashanmugasundar/<repo>/actions/workflows/test-pipeline.yml/badge.svg)


## ✅ Test Coverage
![Coverage](https://ashanmugasundar.github.io/playwright-demo/badges/coverage.svg)


## ✅ Test Reports
- [Allure Dashboard](https://ashanmugasundar.github.io/playwright-demo/allure/)
- [Test Dashboard](https://ashanmugasundar.github.io/playwright-demo/)


### ✅ Test Types
- Unit Tests
- API Tests
- E2E Tests (Playwright)


## Sundar notes
1. How to run all tests in one go> pytest -vv
2. List of test cases> pytest -v
3. How to run only Unit test> Achieve using Marker (step 6)
4. How to run only API test> Achieve using Marker (step 6)
5. How to run only E2E test> pytest -m e2e OR pytest -m e2e --vv
   It runs only tests marked with @pytest.mark.e2e [pytestmark = pytest.mark.e2e]
6. Add markers for better control (Recommended for practical projects)
    @pytest.mark.unit
    def unit_test_something():
      ...
    @pytest.mark.api
    def test_api():
      ...
    @pytest.mark.e2e
    def test_flow():
      ...
    
    Command & What it does
    - pytest ✅ Runs all tests (unit + API + E2E)
    - pytest -vv ✅ Shows detailed output 
    - pytest -m unit -vv ✅ Runs only Unit tests (others skipped)
    - pytest -m api -vv ✅ Runs only API tests (others skipped)
    - pytest -m e2e -vv ✅ Runs only E2E tests (others skipped)
    - pytest -m "not e2e" ✅ Runs unit + API only
    - pytest -v --markers  [this is for all tests auto count in output]
    - pytest -v -rA ✅ Grouped implicitly via file names — add naming convention if needed
    - pytest --maxfail=1 --disable-warnings -v ✅ This stops early on failure and keeps logs clean
    - m = marker filter and Markers = labels applied to tests
    - vv = very verbose output - lists the testcases rather . and additional details. 

## Advanced(Production Grade reporting or dashboard)

pip install allure-pytest
pip install pytest-sugar pytest-testmon
pip install pytest-reportlog

👉 Then generate structured output (for dashboards/CI)

To run locally:

- pytest -m unit --html=reports/unit_report.html --self-contained-html
- pytest -m api --html=reports/api_report.html --self-contained-html
- pytest -m e2e --html=reports/e2e_report.html --self-contained-html
- pytest -m --html=reports/report.html --self-contained-html

### For Allure
- pytest -m unit --alluredir=allure-results/unit
- pytest --alluredir=allure-results
- choco install allure
- allure serve allure-results

## Common Pit Falls:
- Django blocks logout via GET for security (CSRF protection). Logout now requires POST only
   👉 So your Playwright test clicks "Logout", but logout never happens → page never changes → timeout. SO Logout should be button or inside form or POST action
- SynchronousOnlyOperation error - Playwright runs inside an async event loop; Django ORM is sync. 
   Django blocks unsafe sync calls in async contexts [bing.com]
  
    DJANGO_ALLOW_ASYNC_UNSAFE in conftest.py
    How to manage async to sync call in prod or test completely disabled so no need to worry it ? 