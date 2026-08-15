const jwt = require('jsonwebtoken');
const prisma = require('../database/client');
const config = require('../config');

function createAccessToken(userId) {
  return jwt.sign(
    { sub: userId },
    config.SECRET_KEY,
    { expiresIn: config.ACCESS_TOKEN_EXPIRE_MINUTES * 60 }
  );
}

async function requireAuth(req, res, next) {
  const header = req.headers.authorization;
  if (!header || !header.startsWith('Bearer ')) {
    return res.status(401).json({ detail: 'Could not validate credentials' });
  }

  const token = header.split(' ')[1];

  try {
    const payload = jwt.verify(token, config.SECRET_KEY);
    const user = await prisma.user.findUnique({ where: { id: payload.sub } });
    if (!user) return res.status(401).json({ detail: 'Could not validate credentials' });
    req.user = user; // attached here, available in every route handler after this
    next();
  } catch {
    return res.status(401).json({ detail: 'Could not validate credentials' });
  }
}

module.exports = { createAccessToken, requireAuth };
