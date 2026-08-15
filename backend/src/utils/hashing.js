const bcrypt = require('bcryptjs');

async function hashPassword(password) {
  return bcrypt.hash(password, 10);
}

async function verifyPassword(plain, hashed) {
  return bcrypt.compare(plain, hashed);
}

module.exports = { hashPassword, verifyPassword };
