# CozyWrites — FastAPI Backend

Simple FastAPI backend for blog posts with users, auth, and voting.

## Features
- User registration & login (JWT)
- Posts CRUD
- Voting on posts
- SQLAlchemy + Alembic migrations
- Docker Compose for local dev
- Ready for Render (or similar) deployment

## Requirements
- Python 3.13
- Docker & docker-compose (for containerized dev)
- PostgreSQL (local or hosted)
- Git

## Quick start (local, without Docker)
1. Create venv and install:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Create `.env` (see section below).
3. Run migrations:
   ```bash
   alembic upgrade head
   ```
4. Start app:
   ```bash
   uvicorn CozyWrites.main:app --reload --host 0.0.0.0 --port 8000
   ```
5. Open docs: `http://localhost:8000/docs`

## Quick start (Docker Compose)
1. Ensure `Dockerfile` and `docker-compose.yml` are present.
2. Build and run:
   ```bash
   docker-compose down -v
   docker-compose up --build
   ```
3. API available at `http://localhost:8000`
4. To run migrations inside container:
   ```bash
   docker-compose exec api alembic upgrade head
   ```

## Env variables (.env or platform)
Required envs (Render will provide `DATABASE_URL` if linked):
- DATABASE_URL (or:)
  - DATABASE_HOSTNAME
  - DATABASE_PORT
  - DATABASE_USERNAME
  - DATABASE_PASSWORD
  - DATABASE_NAME
- SECRET_KEY
- ALGORITHM (e.g. HS256)
- ACCESS_TOKEN_EXPIRE_MINS

Example `.env` (local):
```
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=sw4pneel
DATABASE_NAME=fastapi
SECRET_KEY=your_secret_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINS=30
```

## Migrations
- Generate: `alembic revision --autogenerate -m "msg"`
- Apply: `alembic upgrade head`

## Deployment (Render)
- Repo connected to Render.
- Set env vars (SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINS, ALGORITHM). Link a Managed Postgres to populate DATABASE_URL.
- Start command: `uvicorn CozyWrites.main:app --host 0.0.0.0 --port $PORT`
- Optional build step to run migrations: `alembic upgrade head`

## Troubleshooting / Common fixes
- Database host inside Docker must be the compose service name (`postgres`), not `localhost`.
- If using platform-provided `DATABASE_URL` and it starts with `postgres://`, replace the scheme to `postgresql+psycopg://` for SQLAlchemy.
- Avoid unguarded print statements during startup — they can crash or block containers in some environments (was the root cause of your crash).
- Use `passlib[bcrypt]` for password hashing (secure) instead of `hashlib`.
- Handle unique constraint errors for user email: check for existing user before insert and return 409.
- If you see UniqueViolation during dev, remove the test row:
  ```sql
  DELETE FROM users WHERE email = 'Swappyz@gmail.com';
  ```
- For container DB readiness, use service healthchecks or a small wait loop before starting the app.

## API docs & tags
- Docs: `/docs` (OpenAPI UI)
- Recommended tag groups: Root, Health, Authentication, Users, Posts, Votes

## Useful commands
```bash
# check ports
lsof -i :8000

# view logs
docker-compose logs -f api

# interactive container debug
docker-compose run --rm api /bin/bash
```

## Contributing
- Follow the repo style, add migrations, run tests (if added), keep secrets out of Git.



- Small debugging outputs (print) during startup can crash or block containers — be careful printing variables before they are defined.
- In Docker Compose, "localhost" inside a container is the container itself; use service names for inter-service connections.
- Deployment platforms often supply `DATABASE_URL` in a `postgres://` form; convert to SQLAlchemy-friendly scheme.
- Always validate unique constraints at the application level and catch IntegrityError to return meaningful HTTP errors.
- Use proper password hashing libraries (passlib + bcrypt), not raw hashing (hashlib), for security.
- Add health endpoints and use container healthchecks / wait logic so the app only starts when DB is ready.
- Keep secrets out of the repo and set them in the deployment environment.



Next steps: 

Add automated tests and CI, refine logging/metrics, and harden config for multiple environments.


Skills developed working on this project

Backend development

FastAPI for building REST APIs, route organization, request/response models (Pydantic)
Designing CRUD endpoints, OpenAPI/docs, router/tag structure
Databases & ORMs

PostgreSQL schema design and constraints (unique keys, foreign keys)
SQLAlchemy ORM usage and engine/session management
Alembic migrations (create/apply migration files)
Authentication & Security

JWT-based auth (token creation/verification), OAuth2 patterns
Secure password hashing (passlib + bcrypt)
Secret management and env-driven configuration
DevOps / Containerization

Dockerfile authoring and multi-service apps with docker-compose
Container networking (use service names vs localhost), healthchecks and wait-for-db patterns
Deploying to cloud platforms (Render/Railway/Heroku): handling DATABASE_URL, PORT, env vars
Reliability & Observability

Graceful DB connection handling (pool_pre_ping, retries), health endpoints
Proper logging vs unguarded print statements, handling IntegrityError and returning HTTP errors
Tooling & Ecosystem

psycopg, uvicorn, alembic, pydantic-settings, python-jose, passlib
requirements management and building lightweight production images
Debugging & Troubleshooting

Diagnosing container crash loops, reading docker logs, interactive container debugging
Fixing runtime errors caused by scope/print/log statements and env/config mismatches
Code quality & project practices

Organizing routers, schemas, models; separating concerns (database, utils, oauth)
Writing clear README, documenting envs and deployment steps
Error handling, input validation, API grouping with tags
Soft skills & workflow

Incremental debugging, hypothesis-driven fixes, test/deploy loop
Translating local dev to production constraints (ports, secrets, health)
Preparing code for CI/CD and platform-driven deployments
