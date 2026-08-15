const router = require('express').Router();
const { requireAuth } = require('../middleware/auth.middleware');
const { createEndpoint, getEndpoints, getEndpoint, deleteEndpoint } = require('../services/endpoint.service');

router.post('/', requireAuth, async (req, res) => {
  const endpoint = await createEndpoint(req.body, req.user.id);
  if (!endpoint) return res.status(404).json({ detail: 'Project not found' });
  res.json(endpoint);
});

router.get('/', requireAuth, async (req, res) => {
  res.json(await getEndpoints(req.user.id));
});

router.get('/:id', requireAuth, async (req, res) => {
  const endpoint = await getEndpoint(req.params.id, req.user.id);
  if (!endpoint) return res.status(404).json({ detail: 'Endpoint not found' });
  res.json(endpoint);
});

router.delete('/:id', requireAuth, async (req, res) => {
  const endpoint = await deleteEndpoint(req.params.id, req.user.id);
  if (!endpoint) return res.status(404).json({ detail: 'Endpoint not found' });
  res.json({ message: 'Endpoint deleted' });
});

module.exports = router;
