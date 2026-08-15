const jwt = require('jsonwebtoken');
const config = require('../config');
const { manager } = require('../websocket/connection_manager');

// This is not an Express router — WebSocket is handled differently
// Called from app.js during server setup
function registerWebSocket(server) {
  const { WebSocketServer } = require('ws');
  const wss = new WebSocketServer({ server, path: '/ws/monitor' });

  wss.on('connection', (ws, req) => {
    const url = new URL(req.url, 'http://localhost');
    const token = url.searchParams.get('token');

    if (token) {
      try {
        const payload = jwt.verify(token, config.SECRET_KEY);
        if (!payload.sub) { ws.close(1008); return; }
      } catch {
        ws.close(1008);
        return;
      }
    }

    manager.connect(ws);
    ws.on('message', () => {}); // keep-alive, messages ignored
    ws.on('close', () => manager.disconnect(ws));
  });
}

module.exports = { registerWebSocket };
