const prisma = require('../database/client');

const FAILURE_THRESHOLD = 3;

async function checkFailureThreshold(endpointId) {
  const recent = await prisma.monitorResult.findMany({
    where: { endpoint_id: endpointId },
    orderBy: { checked_at: 'desc' },
    take: FAILURE_THRESHOLD,
  });
  if (recent.length < FAILURE_THRESHOLD) return false;
  return recent.every(r => !r.success);
}

async function createAlert(endpointId, message) {
  return prisma.alert.create({
    data: { endpoint_id: endpointId, message },
  });
}

module.exports = { checkFailureThreshold, createAlert };
