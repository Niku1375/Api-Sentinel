const prisma = require('../database/client');

// Simple in-memory cache — same as your cache.py behaviour
const cache = new Map();

function cacheGet(key) {
  const entry = cache.get(key);
  if (!entry) return null;
  if (Date.now() > entry.expiresAt) { cache.delete(key); return null; }
  return entry.value;
}

function cacheSet(key, value, ttlSeconds) {
  cache.set(key, { value, expiresAt: Date.now() + ttlSeconds * 1000 });
}

async function getMonitoringHistory(endpointId, userId) {
  return prisma.monitorResult.findMany({
    where: { endpoint_id: endpointId, endpoint: { project: { user_id: userId } } },
    orderBy: { checked_at: 'desc' },
    take: 50,
  });
}

async function getMonitoringStats(endpointId, userId) {
  const cacheKey = `stats:${endpointId}`;
  const cached = cacheGet(cacheKey);
  if (cached) return cached;

  const results = await prisma.monitorResult.findMany({
    where: { endpoint_id: endpointId, endpoint: { project: { user_id: userId } } },
  });

  const total_checks = results.length;
  const successes = results.filter(r => r.success).length;
  const failures = total_checks - successes;
  const avg_response_time = total_checks > 0
    ? results.reduce((sum, r) => sum + (r.response_time || 0), 0) / total_checks
    : 0;
  const uptime_percentage = total_checks > 0
    ? Math.round((successes / total_checks) * 10000) / 100
    : 0;

  const stats = {
    total_checks,
    successes,
    failures,
    uptime_percentage,
    avg_response_time: Math.round(avg_response_time * 100) / 100,
  };

  cacheSet(cacheKey, stats, 30);
  return stats;
}

async function getIncidents(endpointId, userId) {
  return prisma.monitorResult.findMany({
    where: {
      endpoint_id: endpointId,
      success: false,
      endpoint: { project: { user_id: userId } },
    },
    orderBy: { checked_at: 'desc' },
    take: 20,
  });
}

module.exports = { getMonitoringHistory, getMonitoringStats, getIncidents };
