const prisma = require('../database/client');

async function createEndpoint(data, userId) {
  const project = await prisma.project.findFirst({
    where: { id: data.project_id, user_id: userId },
  });
  if (!project) return null;
  return prisma.endpoint.create({ data });
}

async function getEndpoints(userId) {
  return prisma.endpoint.findMany({
    where: { project: { user_id: userId } },
  });
}

async function getEndpoint(endpointId, userId) {
  return prisma.endpoint.findFirst({
    where: { id: endpointId, project: { user_id: userId } },
  });
}

async function deleteEndpoint(endpointId, userId) {
  const endpoint = await getEndpoint(endpointId, userId);
  if (!endpoint) return null;
  return prisma.endpoint.delete({ where: { id: endpointId } });
}

module.exports = { createEndpoint, getEndpoints, getEndpoint, deleteEndpoint };
