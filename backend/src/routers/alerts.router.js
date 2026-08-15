const router = require('express').Router();
const { requireAuth } = require('../middleware/auth.middleware');
const prisma = require('../database/client');

router.get('/', requireAuth, async (req, res) => {
  const alerts = await prisma.alert.findMany({
    where: { endpoint: { project: { user_id: req.user.id } } },
  });
  res.json(alerts);
});

module.exports = router;
