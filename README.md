# API Sentinel

> A backend system for monitoring APIs, tracking their health, and alerting users when things go wrong.

API Sentinel lets you register any HTTP endpoint you care about, checks it automatically at regular intervals, and sends you an email the moment it goes down — and another one when it recovers.

---

## What it does

- **Register endpoints** under projects and monitor them on a schedule
- **Detect failures** by tracking consecutive failed checks against a configurable threshold
- **Alert automatically** via email when an endpoint crosses the failure threshold
- **Resolve automatically** when the endpoint comes back healthy — no manual intervention needed
- **Store history** of every check result so you can see uptime trends and incident timelines
- **Secure everything** behind JWT authentication so only you can see your endpoints

---

## Tech stack

| Layer | Technology | Why |
|---|---|---|
| Web framework | FastAPI | Async-first, auto Swagger docs, native Pydantic support |
| Database | PostgreSQL | Relational data, strong consistency, JSONB support |
| ORM | SQLAlchemy | Pythonic queries, connection pooling, DB-agnostic |
| Validation | Pydantic | Validates request bodies, serializes responses, separates API shape from DB shape |
| Authentication | JWT (JSON Web Tokens) | Stateless auth, no DB lookup per request |
| Password hashing | bcrypt (via passlib) | Industry-standard one-way hashing, brute-force resistant |
| Scheduler | APScheduler | In-process background jobs, configurable intervals per endpoint |
| Email | SMTP | Standard email delivery for alerts and recovery notifications |
| API docs | Swagger / OpenAPI | Auto-generated from route and schema definitions |
| Frontend | JavaScript | Dashboard for managing projects and viewing endpoint status |

---

## Project structure

```
Api-Sentinel/
├── backend/
│   ├── main.py                  # App entry point — creates FastAPI instance, registers routers and middleware
│   ├── config.py                # Loads environment variables (DB URL, JWT secret, SMTP config)
│   ├── requirements.txt         # Python dependencies
│   │
│   ├── database/
│   │   └── connection.py        # SQLAlchemy engine, session factory, get_db() dependency
│   │
│   ├── models/                  # SQLAlchemy ORM models — define database tables
│   │   ├── user.py              # Users table
│   │   ├── project.py           # Projects table
│   │   ├── endpoint.py          # Monitored endpoints table
│   │   ├── monitor_log.py       # One row per check result (status code, latency, is_up)
│   │   └── alert.py             # Active and resolved alerts
│   │
│   ├── schemas/                 # Pydantic schemas — define what the API accepts and returns
│   │   ├── user_schema.py
│   │   ├── project_schema.py
│   │   ├── endpoint_schema.py
│   │   └── alert_schema.py
│   │
│   ├── routes/                  # URL definitions — maps endpoints to controller functions
│   │   ├── auth_routes.py       # POST /auth/register, POST /auth/login, POST /auth/logout
│   │   ├── user_routes.py       # GET /users/me, PUT /users/me
│   │   ├── project_routes.py    # CRUD for /projects
│   │   └── endpoint_routes.py   # CRUD for /projects/{id}/endpoints
│   │
│   ├── controllers/             # Request handlers — receive validated data, call services, return responses
│   │   ├── auth_controller.py
│   │   ├── user_controller.py
│   │   ├── project_controller.py
│   │   └── endpoint_controller.py
│   │
│   ├── services/                # Business logic — no HTTP awareness, fully testable in isolation
│   │   ├── auth_service.py      # Register, login, token creation/verification
│   │   ├── user_service.py      # User CRUD
│   │   ├── project_service.py   # Project CRUD
│   │   ├── endpoint_service.py  # Endpoint CRUD
│   │   ├── checker_service.py   # Sends the actual HTTP request to a monitored endpoint, records result
│   │   └── alert_service.py     # Evaluates consecutive failures, creates/resolves alerts
│   │
│   ├── middleware/
│   │   └── auth_middleware.py   # JWT validation on protected routes; logs request timing
│   │
│   ├── scheduler/
│   │   └── scheduler.py         # APScheduler setup; runs check jobs at configured intervals
│   │
│   ├── email/
│   │   └── email_service.py     # SMTP client; sends alert and recovery emails
│   │
│   └── utils/
│       └── hashing.py           # bcrypt password hash and verify helpers
│
└── frontend/                    # JavaScript dashboard
    ├── index.html
    ├── dashboard.js
    └── styles.css
```

---

## How a monitoring check works

When the scheduler wakes up for a registered endpoint, this is the sequence:

```
Scheduler triggers check
        ↓
checker_service sends HTTP GET (or configured method) to the endpoint URL
        ↓
Records: status code, response time in ms, timestamp
        ↓
is_up = True if status 200–299, False otherwise (includes timeouts, connection errors)
        ↓
Writes one row to monitor_logs
        ↓
alert_service evaluates:
    if is_up:
        reset consecutive_failures to 0
        if active alert exists → mark RESOLVED, send recovery email
    if not is_up:
        increment consecutive_failures
        if consecutive_failures >= threshold → create alert, send alert email
```

The threshold approach (rather than alerting on a single failure) means transient network blips don't wake you up at 3am. Only sustained failures trigger an alert.

---

## How a request flows through the backend

```
Client sends HTTP request
        ↓
Middleware — validates JWT on protected routes, logs timing
        ↓
Router — matches URL to the right controller function
        ↓
Pydantic schema — validates and parses the request body (returns 422 if invalid)
        ↓
Controller — receives clean data, delegates to service
        ↓
Service — executes business logic, interacts with DB via SQLAlchemy
        ↓
Model — maps Python objects to database rows
        ↓
Response travels back up, filtered through the output schema
        ↓
Client receives JSON response
```

---

## Getting started

### Prerequisites

- Python 3.10+
- PostgreSQL running locally or a connection string to a hosted instance
- An SMTP account for email alerts (Gmail with app password works fine)

### 1. Clone the repo

```bash
git clone https://github.com/Niku1375/Api-Sentinel.git
cd Api-Sentinel/backend
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Create a `.env` file in the `backend/` directory:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/api_sentinel

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ALERT_FROM_EMAIL=your-email@gmail.com

# Monitoring
DEFAULT_CHECK_INTERVAL_MINUTES=5
FAILURE_THRESHOLD=3
```

> Never commit your `.env` file. It is listed in `.gitignore`.

### 4. Create the database tables

```bash
python -c "from database.connection import Base, engine; Base.metadata.create_all(bind=engine)"
```

### 5. Run the server

```bash
uvicorn main:app --reload
```

The API is now live at `http://localhost:8000`.

Interactive API docs are available at `http://localhost:8000/docs`.

---

## API overview

### Authentication

| Method | Route | Description |
|---|---|---|
| POST | `/auth/register` | Create a new user account |
| POST | `/auth/login` | Login and receive a JWT access token |
| POST | `/auth/logout` | Invalidate the current session |

### Projects

| Method | Route | Description |
|---|---|---|
| GET | `/projects` | List all projects for the authenticated user |
| POST | `/projects` | Create a new project |
| GET | `/projects/{id}` | Fetch a project by ID |
| PUT | `/projects/{id}` | Update a project |
| DELETE | `/projects/{id}` | Delete a project and all its endpoints |

### Endpoints

| Method | Route | Description |
|---|---|---|
| GET | `/projects/{id}/endpoints` | List all endpoints in a project |
| POST | `/projects/{id}/endpoints` | Register a new endpoint to monitor |
| GET | `/endpoints/{id}` | Fetch endpoint details and recent check history |
| PUT | `/endpoints/{id}` | Update URL, interval, or threshold |
| DELETE | `/endpoints/{id}` | Stop monitoring and remove endpoint |

### Alerts

| Method | Route | Description |
|---|---|---|
| GET | `/alerts` | List all alerts for the authenticated user |
| GET | `/alerts/{id}` | Fetch a specific alert and its incident timeline |

All protected routes require the header: `Authorization: Bearer <token>`

---

## Alert lifecycle

```
Endpoint is healthy
        │
        ▼
Consecutive failures reach threshold
        │
        ▼
Alert created (status: ACTIVE) → email sent to user
        │
        ▼
Endpoint recovers (check returns 2xx)
        │
        ▼
Alert updated (status: RESOLVED, resolved_at: timestamp) → recovery email sent
```

Alerts are never deleted — the full incident history is preserved so you can review when and how long an outage lasted.

---

## Design decisions

**Why FastAPI over Flask or Django?**
FastAPI is async-first, which allows the checker to make many outbound HTTP calls concurrently rather than blocking on each one. Django is a full-stack framework — its ORM, admin, and templating are more than we need for a pure API backend. Flask would work but requires more boilerplate for request validation and documentation.

**Why separate schemas from models?**
SQLAlchemy models represent database shape — they include `hashed_password`, internal foreign keys, and audit timestamps. Pydantic schemas represent API shape — inputs accept `password`, outputs never include it. Keeping them separate means API contracts can evolve independently of the database schema, and sensitive fields can never accidentally leak.

**Why consecutive failures rather than any failure?**
A single failed check is often a transient network blip. Alerting on every single failure produces noise that trains users to ignore alerts. Consecutive failures are a strong signal that the API is genuinely down.

**Why store resolved alerts instead of deleting them?**
Incident history is the most valuable output of a monitoring system. Deleted records give you no way to answer "how many times did this API go down last month?" or "how long was that outage on Tuesday?"

---

## Future improvements

- Celery + Redis for distributed, fault-tolerant check scheduling (current APScheduler is single-process)
- Table partitioning on `monitor_logs` by month (this table grows unboundedly in the current design)
- SSRF protection — validate that registered URLs don't point to private IP ranges
- Response body validation — alert when status is 200 but the response body indicates an error
- Uptime percentage calculation — computed from `monitor_logs` and surfaced on the dashboard
- Webhook alerts as an alternative to email

---

## License

MIT
