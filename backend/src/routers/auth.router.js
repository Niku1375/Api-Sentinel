const router = require('express').Router();
const { createUser, authenticateUser } = require('../services/auth.service');
const { createAccessToken } = require('../middleware/auth.middleware');

router.post('/register', async (req, res) => {
  try {
    const user = await createUser(req.body);
    res.json({ id: user.id, name: user.name, email: user.email });
  } catch (err) {
    res.status(err.status || 500).json({ detail: err.message });
  }
});

router.post('/login', async (req, res) => {
  const { email, password } = req.body;
  const user = await authenticateUser(email, password);
  if (!user) return res.status(401).json({ detail: 'Invalid credentials' });
  const token = createAccessToken(user.id);
  res.json({ access_token: token, token_type: 'bearer' });
});

module.exports = router;
