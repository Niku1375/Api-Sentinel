# API Sentinel

> A backend system for monitoring APIs, tracking their health, and alerting users when things go wrong.

API Sentinel lets you register any HTTP endpoint, checks it automatically at regular intervals, and sends you an email the moment it goes down and another one when it recovers.

---

## What it does

- **Register endpoints** under projects and monitor them on a schedule
- **Detect failures** by tracking consecutive failed checks against a configurable threshold
- **Alert automatically** via email when an endpoint crosses the failure threshold
- **Resolve automatically** when the endpoint comes back healthy
- **Store history** of every check result for uptime trends and incident timelines
- **Secure everything** behind JWT authentication so only you can see your endpoints

---

## Tech Stack

| Layer     | Technology      | Why                                                        |
|-----------|-----------------|------------------------------------------------------------|
| Runtime   | Node.js         | Non-blocking I/O, ideal for concurrent HTTP checks         |
| Framework | Express.js      | Minimal, fast, unopinionated REST API framework            |
| Database  | PostgreSQL      | Relational data, strong consistency, incident history      |
| Auth      | JWT + bcrypt    | Stateless auth, no DB lookup per request                   |
| Scheduler | node-cron       | In-process background jobs, configurable intervals         |
| Email     | Nodemailer      | SMTP-based alerting and recovery notifications             |

---

## Project Structure

```
Api-Sentinel/
├── src/
│   ├── routes/
│   │   ├── auth.routes.js
│   │   ├── user.routes.js
│   │   ├── project.routes.js
│   │   └── endpoint.routes.js
│   ├── controllers/
│   │   ├── auth.controller.js
│   │   ├── user.controller.js
│   │   ├── project.controller.js
│   │   └── endpoint.controller.js
│   ├── services/
│   │   ├── auth.service.js
│   │   ├── checker.service.js
│   │   └── alert.service.js
│   ├── middleware/
│   │   └── auth.middleware.js
│   ├── models/
│   │   ├── user.model.js
│   │   ├── project.model.js
│   │   ├── endpoint.model.js
│   │   ├── monitor_log.model.js
│   │   └── alert.model.js
│   ├── scheduler/
│   │   └── scheduler.js
│   ├── email/
│   │   └── email.service.js
│   └── config/
│       └── db.js
├── .env
├── .gitignore
└── index.js
```

---

## How a monitoring check works

```
node-cron triggers check
        |
checker.service sends HTTP request to endpoint URL
        |
Records: status code, response time in ms, is_up
        |
is_up = true if status 200-299, false otherwise
        |
Writes one row to monitor_logs
        |
alert.service evaluates:
    if is_up:
        reset consecutive_failures to 0
        if active alert exists → mark RESOLVED → send recovery email
    if not is_up:
        increment consecutive_failures
        if consecutive_failures >= threshold → create alert → send alert email
```

The threshold approach means transient network blips do not trigger alerts. Only sustained failures do.

---

## How a request flows through the backend

```
Client sends HTTP request
        |
auth.middleware validates JWT on protected routes
        |
Router matches URL to controller function
        |
Controller receives clean data, delegates to service
        |
Service executes business logic, interacts with DB
        |
Model maps JavaScript objects to database rows
        |
Client receives JSON response
```

---

## API Overview

### Authentication

| Method | Route           | Description                        |
|--------|-----------------|------------------------------------|
| POST   | /auth/register  | Create a new user account          |
| POST   | /auth/login     | Login and receive a JWT token      |
| POST   | /auth/logout    | Invalidate the current session     |

### Users

| Method | Route     | Description                  |
|--------|-----------|------------------------------|
| GET    | /users/me | Get current user profile     |
| PUT    | /users/me | Update current user profile  |

### Projects

| Method | Route          | Description                              |
|--------|----------------|------------------------------------------|
| GET    | /projects      | List all projects for authenticated user |
| POST   | /projects      | Create a new project                     |
| GET    | /projects/:id  | Fetch a project by ID                    |
| PUT    | /projects/:id  | Update a project                         |
| DELETE | /projects/:id  | Delete a project and all its endpoints   |

### Endpoints

| Method | Route                     | Description                                    |
|--------|---------------------------|------------------------------------------------|
| GET    | /projects/:id/endpoints   | List all endpoints in a project                |
| POST   | /projects/:id/endpoints   | Register a new endpoint to monitor             |
| GET    | /endpoints/:id            | Fetch endpoint details and recent check history|
| PUT    | /endpoints/:id            | Update URL, interval, or threshold             |
| DELETE | /endpoints/:id            | Stop monitoring and remove endpoint            |

### Alerts

| Method | Route       | Description                                   |
|--------|-------------|-----------------------------------------------|
| GET    | /alerts     | List all alerts for the authenticated user    |
| GET    | /alerts/:id | Fetch a specific alert and its incident timeline |

All protected routes require the header: `Authorization: Bearer <token>`

---

## Getting Started

### Prerequisites

- Node.js 18+
- PostgreSQL running locally or a hosted instance
- An SMTP account for email alerts (Gmail with app password works fine)

### 1. Clone the repo

```bash
git clone https://github.com/Niku1375/Api-Sentinel.git
cd Api-Sentinel
```

### 2. Install dependencies

```bash
npm install
```

### 3. Configure environment

Create a `.env` file in the root directory:

```
PORT=3000
DATABASE_URL=postgresql://username:password@localhost:5432/api_sentinel
JWT_SECRET=your-secret-key
JWT_EXPIRES_IN=30m
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FAILURE_THRESHOLD=3
DEFAULT_CHECK_INTERVAL_MINUTES=5
```

Never commit your `.env` file. It is listed in `.gitignore`.

### 4. Run the server

```bash
node index.js
```

The API is now live at `http://localhost:3000`.

---

## Alert Lifecycle

```
Endpoint is healthy
        |
Consecutive failures reach threshold
        |
Alert created (status: ACTIVE) → email sent to user
        |
Endpoint recovers (check returns 2xx)
        |
Alert updated (status: RESOLVED) → recovery email sent
```

Alerts are never deleted. The full incident history is preserved so you can review when and how long an outage lasted.

---

## Design Decisions

**Why consecutive failures rather than any failure?**
A single failed check is often a transient network blip. Alerting on every failure produces noise. Consecutive failures are a strong signal the API is genuinely down.

**Why store resolved alerts instead of deleting them?**
Incident history is the most valuable output of a monitoring system. Deleted records give you no way to answer how many times an API went down or how long an outage lasted.

**Why JWT over session-based auth?**
JWT is stateless. No database lookup happens on every request. The token contains the user ID and is verified entirely in memory.

**Why separate routes, controllers and services?**
Routes define URLs. Controllers handle HTTP concerns only. Services contain all business logic with no HTTP awareness. This separation makes each layer independently testable and maintainable.

---

## Future Improvements

- Webhook alerts as an alternative to email
- Uptime percentage calculation surfaced per endpoint
- SSRF protection to validate registered URLs do not point to private IP ranges
- Response body validation to alert when status is 200 but body indicates an error
- Celery + Redis for distributed fault-tolerant scheduling

---

## License

MIT
