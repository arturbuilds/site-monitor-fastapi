# Async Website Uptime Monitor

A robust, production-ready asynchronous website monitoring service built with **FastAPI**, **SQLAlchemy 2.0**, and **Celery**. The system automatically tracks website availability in the background and logs status changes.

## 🛠️ Tech Stack & Features
- **FastAPI** — high-performance asynchronous web framework.
- **SQLAlchemy 2.0 (Async)** + **aiosqlite** — clean database integration with async session management.
- **JWT & Bcrypt** — secure user registration, password hashing, and token-based protection for API routes.
- **Celery & Redis** — background worker and task scheduler (Celery Beat) running independently.
- **HTTPX** — fast, non-blocking HTTP requests for website pinging with exception handling.

## 📁 Project Structure
- `app/main.py` — application entry point and startup initialization.
- `app/config.py` — environment configuration managed via `pydantic-settings`.
- `app/database.py` — db dependency engine and async session makers.
- `app/models.py` — SQLAlchemy tables (`User` and `Site`) with cascade deletes.
- `app/schemas.py` — Pydantic data validation and filtering layers.
- `app/api/` — modular authentication and site management endpoints.
- `app/tasks/` — Celery worker instance and automated ping tasks.

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd async-uptime-monitor
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   Create a `.env` file in the root directory:
   ```text
   database_url=sqlite+aiosqlite:///./site_monitor.db
   redis_host=rediss://default:YOUR_PASSWORD@YOUR_UPSTASH_HOST:6379?ssl_cert_reqs=none
   secret_key=YOUR_SUPER_SECRET_KEY
   ```

4. **Run the FastAPI server:**
   ```bash
   python -m uvicorn app.main:app --reload
   ```
   Open `http://127.0.0` to access interactive Swagger API documentation.

5. **Start Celery Worker (Windows optimized):**
   ```bash
   python -m celery -A app.tasks.worker.celery_app worker --loglevel=info -P solo
   ```

6. **Start Celery Beat Scheduler:**
   ```bash
   python -m celery -A app.tasks.worker.celery_app beat --loglevel=info
   ```
