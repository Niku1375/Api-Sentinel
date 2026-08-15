const router = require('express').Router();
const { requireAuth } = require('../middleware/auth.middleware');
const { createApiKey, listApiKeys, revokeApiKey, verifyApiKey } = require('../services/api_key.service');

router.post('/', requireAuth, async (req, res) => {
  const { dbKey, rawKey } = await createApiKey(req.user.id, req.body);
  res.json({
    id: dbKey.id,
    name: dbKey.name,
    key_hint: dbKey.key_hint,
    is_active: dbKey.is_active,
    created_at: dbKey.created_at,
    last_used_at: dbKey.last_used_at,
    raw_key: rawKey,
  });
});

router.get('/', requireAuth, async (req, res) => {
  res.json(await listApiKeys(req.user.id));
});

router.delete('/:id', requireAuth, async (req, res) => {
  try {
    res.json(await revokeApiKey(req.params.id, req.user.id));
  } catch (err) {
    res.status(err.status || 500).json({ detail: err.message });
  }
});

// No requireAuth — this is FOR external services authenticating themselves
router.post('/verify', async (req, res) => {
  const key = await verifyApiKey(req.body.key);
  if (!key) return res.json({ valid: false });
  res.json({ valid: true, user_id: key.user_id });
});

module.exports = router;
