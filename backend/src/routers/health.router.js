const router = require('express').Router();
const { requireAuth } = require('../middleware/auth.middleware');

router.get('/', (req, res) => {
  res.json({ status: 'healthy' });
});

router.get('/protected', requireAuth, (req, res) => {
  res.json({ message: 'You are authenticated', user: req.user.email });
});

module.exports = router;
