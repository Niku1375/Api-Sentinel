const router = require('express').Router();
const { requireAuth } = require('../middleware/auth.middleware');
const { getMonitoringHistory, getMonitoringStats, getIncidents } = require('../services/monitoring.service');

router.get('/history/:endpointId', requireAuth, async (req, res) => {
  res.json(await getMonitoringHistory(req.params.endpointId, req.user.id));
});

router.get('/stats/:endpointId', requireAuth, async (req, res) => {
  res.json(await getMonitoringStats(req.params.endpointId, req.user.id));
});

router.get('/incidents/:endpointId', requireAuth, async (req, res) => {
  res.json(await getIncidents(req.params.endpointId, req.user.id));
});

module.exports = router;
