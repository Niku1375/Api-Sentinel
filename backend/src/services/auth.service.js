const prisma = require('../database/client');
const { hashPassword, verifyPassword } = require('../utils/hashing');

async function createUser(data) {
  const existing = await prisma.user.findUnique({ where: { email: data.email } });
  if (existing) {
    const err = new Error('Email already registered');
    err.status = 400;
    throw err;
  }
  const password_hash = await hashPassword(data.password);
  return prisma.user.create({
    data: { name: data.name, email: data.email, password_hash },
  });
}

async function authenticateUser(email, password) {
  const user = await prisma.user.findUnique({ where: { email } });
  if (!user) return null;
  const valid = await verifyPassword(password, user.password_hash);
  if (!valid) return null;
  return user;
}

module.exports = { createUser, authenticateUser };
