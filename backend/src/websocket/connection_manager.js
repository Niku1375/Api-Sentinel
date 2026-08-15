const WebSocket = require('ws');

class ConnectionManager {
  constructor() {
    this.active_connections = [];
  }

  connect(ws) {
    this.active_connections.push(ws);
  }

  disconnect(ws) {
    this.active_connections = this.active_connections.filter(c => c !== ws);
  }

  broadcast(message) {
    const data = JSON.stringify(message);
    for (const ws of this.active_connections) {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(data);
      }
    }
  }
}

const manager = new ConnectionManager();
module.exports = { manager };
