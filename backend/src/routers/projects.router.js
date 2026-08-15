const router = require('express').Router();
const { requireAuth } = require('../middleware/auth.middleware');
const { createProject, getProjects, getProject, deleteProject } = require('../services/project.service');

router.post('/', requireAuth, async (req, res) => {
  const project = await createProject(req.body, req.user.id);
  res.json(project);
});

router.get('/', requireAuth, async (req, res) => {
  res.json(await getProjects(req.user.id));
});

router.get('/:id', requireAuth, async (req, res) => {
  const project = await getProject(req.params.id, req.user.id);
  if (!project) return res.status(404).json({ detail: 'Project not found' });
  res.json(project);
});

router.delete('/:id', requireAuth, async (req, res) => {
  const project = await deleteProject(req.params.id, req.user.id);
  if (!project) return res.status(404).json({ detail: 'Project not found' });
  res.json({ message: 'Project deleted' });
});

module.exports = router;
