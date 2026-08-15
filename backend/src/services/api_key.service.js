const crypto = require('crypto');
const prisma = require('../database/client');

function generateRawKey() {
  return 'sk_' + crypto.randomBytes(32).toString('base64url');
}

function hashKey(rawKey) {
  return crypto.createHash('sha256').update(rawKey).digest('hex');
}

async function createApiKey(userId, data) {
  const rawKey = generateRawKey();
  const key_hash = hashKey(rawKey);
  const key_hint = rawKey.slice(-4);

  const dbKey = await prisma.aPIKey.create({
    data: { user_id: userId, name: data.name, key_hash, key_hint, is_active: true },
  });

  return { dbKey, rawKey }; // rawKey returned once, never stored
}

async function listApiKeys(userId) {
  return prisma.aPIKey.findMany({
    where: { user_id: userId, is_active: true },
    orderBy: { created_at: 'desc' },
  });
}

async function revokeApiKey(keyId, userId) {
  const key = await prisma.aPIKey.findFirst({
    where: { id: keyId, user_id: userId },
  });
  if (!key) {
    const err = new Error('API key not found');
    err.status = 404;
    throw err;
  }
  await prisma.aPIKey.delete({ where: { id: keyId } });
  return { message: 'API key revoked successfully' };
}

async function verifyApiKey(rawKey) {
  const key_hash = hashKey(rawKey);
  const key = await prisma.aPIKey.findFirst({
    where: { key_hash, is_active: true },
  });
  if (!key) return null;
  await prisma.aPIKey.update({
    where: { id: key.id },
    data: { last_used_at: new Date() },
  });
  return key;
}

module.exports = { createApiKey, listApiKeys, revokeApiKey, verifyApiKey };
