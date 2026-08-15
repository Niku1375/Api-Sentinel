const axios = require('axios');
const prisma = require('../database/client');
const { manager } = require('../websocket/connection_manager');
const { checkFailureThreshold, createAlert } = require('../services/alert.service');
const { sendEmailAlert } = require('../services/notification.service');

async function checkEndpoint(endpointId) {
  const endpoint = await prisma.endpoint.findUnique({ where: { id: endpointId } });
  if (!endpoint || !endpoint.is_active) return;

  const start = Date.now();
  let success = false;
  let status_code = null;

  try {
    const response = await axios({
      method: endpoint.method,
      url: endpoint.url,
      timeout: endpoint.timeout_seconds * 1000, // axios takes ms, not seconds
    });
    status_code = response.status;
    success = status_code < 500;
  } catch (err) {
    status_code = err.response?.status || null;
    success = false;
  }

  const response_time = Date.now() - start;

  await prisma.monitorResult.create({
    data: { endpoint_id: endpoint.id, status_code, response_time, success },
  });

  manager.broadcast({
    endpoint_id: endpoint.id,
    endpoint_name: endpoint.name,
    status_code,
    response_time,
    success,
  });

  // Fetch project → user for email
  const project = await prisma.project.findUnique({ where: { id: endpoint.project_id } });
  const user = project
    ? await prisma.user.findUnique({ where: { id: project.user_id } })
    : null;

  if (!success) {
    const threshold_reached = await checkFailureThreshold(endpoint.id);
    if (threshold_reached && !endpoint.alert_active) {
      const alert = await createAlert(
        endpoint.id,
        `Endpoint ${endpoint.name} failed 3 consecutive checks`
      );
      if (user) {
        try { await sendEmailAlert(user.email, 'API Sentinel Alert', alert.message); }
        catch (e) { console.error('Email failed:', e.message); }
      }
      await prisma.endpoint.update({
        where: { id: endpoint.id },
        data: { alert_active: true },
      });
    }
  } else {
    if (endpoint.alert_active) {
      if (user) {
        try {
          await sendEmailAlert(
            user.email,
            'API Sentinel Recovery',
            `Endpoint ${endpoint.name} is back UP`
          );
        } catch (e) { console.error('Recovery email failed:', e.message); }
      }
      await prisma.endpoint.update({
        where: { id: endpoint.id },
        data: { alert_active: false },
      });
    }
  }
}

async function runMonitoring() {
  const endpoints = await prisma.endpoint.findMany({ where: { is_active: true } });
  await Promise.all(endpoints.map(e => checkEndpoint(e.id)));
}

module.exports = { runMonitoring };
