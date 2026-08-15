const express = require('express');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const http = require('http');

const { registerWebSocket } = require('./routers/ws_monitor.router');
const { startScheduler } = require('./workers/scheduler');

const healthRouter = require('./routers/health.router');
const authRouter = require('./routers/auth.router');
const projectsRouter = require('./routers/projects.router');
const endpointsRouter = require('./routers/endpoints.router');
const monitoringRouter = require('./routers/monitoring.router');
const alertsRouter = require('./routers/alerts.router');
const apiKeysRouter = require('./routers/api_keys.router');

const app = express();

// CORS
app.use(cors({
  origin: [
    'http://localhost:3000',
    'http://localhost:5173',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:5173',
  ],
  credentials: true,
}));

// Body parsing
app.use(express.json());

// Rate limiting
app.use(rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 100,
}));

// Routes
app.use('/health', healthRouter);
app.use('/auth', authRouter);
app.use('/projects', projectsRouter);
app.use('/endpoints', endpointsRouter);
app.use('/monitoring', monitoringRouter);
app.use('/alerts', alertsRouter);
app.use('/api-keys', apiKeysRouter);

app.get('/', (req, res) => {
  res.json({ message: 'API Sentinel Running' });
});

// HTTP server (needed to attach WebSocket to same port)
const server = http.createServer(app);
registerWebSocket(server);

// Start scheduler
startScheduler();

module.exports = { server };
