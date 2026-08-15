# API Sentinel

> A backend system for monitoring APIs, tracking their health, and alerting users when things go wrong.

API Sentinel lets you register any HTTP endpoint, checks it automatically at regular intervals, and sends you an email the moment it goes down — and another when it recovers.

---

## Live Demo

Deployed on Railway. Base URL:
```
https://your-url.up.railway.app
```

Interactive API docs:
```
https://your-url.up.railway.app/docs
```

---

## What it does

- **Register endpoints** under projects and monitor them on a schedule
- **Detect failures** by tracking consecutive failed checks against a configurable threshold
- **Alert automatically** via email when an endpoint crosses the failure threshold
- **Resolve automatically** when the endpoint recovers — no manual intervention needed
- **Store history** of every check result so you can see uptime trends and incident timelines
- **Secure everything** behind JWT authentication so only you can see your endpoints
- **API key support** for external services to authenticate programmatically
- **WebSocket feed** for real-time monitoring updates on the dashboard

---

## Tech Stack

| Layer            | Technology       | Why                                                              |
|------------------|------------------|------------------------------------------------------------------|
| Web framework    | Express.js       | Minimal, fast, widely supported on Railway                       |
| Database         | PostgreSQL        | Relational data, strong consistency                              |
| ORM              | Prisma           | Type-safe queries, automatic migrations, Railway-friendly        |
| Validation       | Zod              | Runtime schema validation on all request bodies                  |
| Authentication   | JWT              | Stateless auth, no DB lookup per request                         |
| Password hashing | bcryptjs         | Industry-standard one-way hashing                                |
| Scheduler        | node-cron        | Runs monitoring sweeps every 60 seconds                          |
| Email            | Nodemailer       | SMTP email delivery for alerts and recovery notifications        |
| WebSocket        | ws               | Real-time check results pushed to connected clients              |
| Deployment       | Railway          | Auto-deploy from GitHub, managed PostgreSQL, env var injection   |

---

## Project Structure

```
Api-Sentinel/
├── backend/
│   ├── prisma/
│   │   └── schema.prisma        # All database models — single source of truth
│   ├── src/
│   │   ├── config.js            # Loads and validates all environment variables
│   │   ├── app.js               # Express app setup, middleware, routes, WebSocket
│   │   ├── server.js            # Starts the HTTP server
│   │   ├── database/
│   │   │   └── client.js        # Prisma client singleton
│   │   ├── middleware/
│   │   │   └── auth.middleware.js  # JWT validation, createAccessToken
│   │   ├── routers/             # URL definitions — one file per domain
│   │   │   ├── auth.router.js
│   │   │   ├── projects.router.js
│   │   │   ├── endpoints.router.js
│   │   │   ├── monitoring.router.js
│   │   │   ├── alerts.router.js
│   │   │   ├── api_keys.router.js
│   │   │   ├── health.router.js
│   │   │   └── ws_monitor.router.js
│   │   ├── services/            # Business logic — no HTTP awareness
│   │   │   ├── auth.service.js
│   │   │   ├── project.service.js
│   │   │   ├── endpoint.service.js
│   │   │   ├── monitoring.service.js
│   │   │   ├── alert.service.js
│   │   │   ├── notification.service.js
│   │   │   └── api_key.service.js
│   │   ├── schemas/             # Zod schemas — request validation
│   │   ├── websocket/
│   │   │   └── connection_manager.js  # Manages active WebSocket connections
│   │   ├── workers/
│   │   │   ├── monitor.worker.js      # Sends HTTP checks, records results, triggers alerts
│   │   │   └── scheduler.js           # Runs monitor sweep every 60 seconds
│   │   └── utils/
│   │       └── hashing.js             # bcrypt password hash and verify
│   ├── Dockerfile
│   └── package.json
├── frontend/                    # Dashboard (JS)
├── railway.json                 # Railway deployment config
└── README.md
```

---

## How a monitoring check works

```
Scheduler triggers every 60s
        ↓
monitor.worker fetches all active endpoints
        ↓
Each endpoint checked concurrently (Promise.all)
        ↓
HTTP request sent — records status code, response time, success
        ↓
Result written to monitor_results table
        ↓
Result broadcast over WebSocket to connected dashboard clients
        ↓
alert.service checks last 3 results:
    if all failed AND alert not active → create alert, send email, set alert_active = true
    if success AND alert was active   → send recovery email, set alert_active = false
```

---

## How a request flows

```
Client sends HTTP request
        ↓
CORS middleware
        ↓
express.json() — parses body
        ↓
Rate limiter — 100 req/min per IP
        ↓
Router — matches URL to handler
        ↓
requireAuth middleware — validates JWT, attaches req.user
        ↓
Zod schema — validates request body
        ↓
Service — business logic via Prisma
        ↓
JSON response
```

---

## API Reference

### Authentication
| Method | Route            | Auth | Description                        |
|--------|------------------|------|------------------------------------|
| POST   | `/auth/register` | No   | Create a new user account          |
| POST   | `/auth/login`    | No   | Login, receive JWT access token    |

### Projects
| Method | Route            | Auth | Description                        |
|--------|------------------|------|------------------------------------|
| GET    | `/projects`      | Yes  | List all projects                  |
| POST   | `/projects`      | Yes  | Create a new project               |
| GET    | `/projects/:id`  | Yes  | Get a project by ID                |
| DELETE | `/projects/:id`  | Yes  | Delete a project                   |

### Endpoints
| Method | Route             | Auth | Description                       |
|--------|-------------------|------|-----------------------------------|
| GET    | `/endpoints`      | Yes  | List all monitored endpoints      |
| POST   | `/endpoints`      | Yes  | Register a new endpoint           |
| GET    | `/endpoints/:id`  | Yes  | Get endpoint details              |
| DELETE | `/endpoints/:id`  | Yes  | Stop monitoring and remove        |

### Monitoring
| Method | Route                          | Auth | Description              |
|--------|--------------------------------|------|--------------------------|
| GET    | `/monitoring/history/:id`      | Yes  | Last 50 check results    |
| GET    | `/monitoring/stats/:id`        | Yes  | Uptime, avg response time|
| GET    | `/monitoring/incidents/:id`    | Yes  | Last 20 failures         |

### Alerts
| Method | Route       | Auth | Description                        |
|--------|-------------|------|------------------------------------|
| GET    | `/alerts`   | Yes  | All alerts for current user        |

### API Keys
| Method | Route              | Auth | Description                      |
|--------|--------------------|------|----------------------------------|
| POST   | `/api-keys`        | Yes  | Create key — raw key shown once  |
| GET    | `/api-keys`        | Yes  | List all active keys             |
| DELETE | `/api-keys/:id`    | Yes  | Revoke a key permanently         |
| POST   | `/api-keys/verify` | No   | Verify a raw key (for external services) |

### Health
| Method | Route               | Auth | Description          |
|--------|---------------------|------|----------------------|
| GET    | `/health`           | No   | Service health check |
| GET    | `/health/protected` | Yes  | Auth check           |

All protected routes require:
```
Authorization: Bearer <token>
```

### WebSocket
```
ws://your-url.up.railway.app/ws/monitor?token=<jwt>
```
Receives real-time JSON after every check:
```json
{
  "endpoint_id": "uuid",
  "endpoint_name": "My API",
  "status_code": 200,
  "response_time": 142,
  "success": true
}
```

---

## Deployment (Railway)

### Environment Variables

Set these in Railway → your service → Variables:

```
DATABASE_URL                  # Auto-set by Railway PostgreSQL plugin
SECRET_KEY                    # Any long random string
ALGORITHM                     # HS256
ACCESS_TOKEN_EXPIRE_MINUTES   # 30
SMTP_HOST                     # sandbox.smtp.mailtrap.io
SMTP_PORT                     # 587
SMTP_USER                     # From Mailtrap dashboard
SMTP_PASSWORD                 # From Mailtrap dashboard
EMAIL_FROM                    # Any email address
```

### Deploy steps

1. Push to GitHub
2. Railway → New Project → Deploy from GitHub
3. Railway → Add Plugin → PostgreSQL (sets `DATABASE_URL` automatically)
4. Add remaining env vars in Variables tab
5. Settings → Pre-deploy Command: `npx prisma migrate deploy`
6. Settings → Networking → Generate Domain

Railway auto-deploys on every push to `main`.

---

## Alert lifecycle

```
Endpoint healthy
      │
      ▼
3 consecutive failures reached
      │
      ▼
Alert created → email sent → alert_active = true
      │
      ▼
Endpoint recovers (2xx response)
      │
      ▼
Recovery email sent → alert_active = false
```

Alerts are never deleted — full incident history is preserved.

---

## Design decisions

**Why Express over Fastify or Hapi?** Maximum ecosystem compatibility, simplest Railway deployment, and the easiest mental model when learning Node.js from Python.

**Why Prisma over raw pg or Sequelize?** Prisma's schema-first approach means one file defines all tables, relations, and types. `prisma migrate deploy` on Railway creates everything in one command — no manual SQL.

**Why consecutive failures rather than any failure?** A single failed check is often a transient network blip. Three consecutive failures is a strong signal the API is genuinely down.

**Why store resolved alerts instead of deleting them?** Incident history is the most valuable output of a monitoring system — it answers "how many times did this go down last month?"

---

## Future improvements

- Celery/Redis equivalent (BullMQ) for distributed, fault-tolerant scheduling
- Table partitioning on `monitor_results` by month (grows unboundedly)
- SSRF protection — validate registered URLs don't point to private IP ranges
- Response body validation — alert when status 200 but body indicates error
- Uptime percentage on dashboard
- Webhook alerts as alternative to email

---

## Author

**Nikunj** — B.Tech CSE (Data Science), NSUT New Delhi  
GitHub: [github.com/Niku1375](https://github.com/Niku1375)

---

## License

MIT
