const prisma = require('../database/client');

async function createProject(data, userId) {
  return prisma.project.create({
    data: { name: data.name, description: data.description, user_id: userId },
  });
}

async function getProjects(userId) {
  return prisma.project.findMany({ where: { user_id: userId } });
}

async function getProject(projectId, userId) {
  return prisma.project.findFirst({
    where: { id: projectId, user_id: userId },
  });
}

async function deleteProject(projectId, userId) {
  const project = await getProject(projectId, userId);
  if (!project) return null;
  return prisma.project.delete({ where: { id: projectId } });
}

module.exports = { createProject, getProjects, getProject, deleteProject };
