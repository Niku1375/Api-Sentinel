const { z } = require('zod');

const APIKeyCreate = z.object({
  name: z.string(),
});

const APIKeyResponse = z.object({
  id: z.string().uuid(),
  name: z.string(),
  key_hint: z.string(),
  is_active: z.boolean(),
  created_at: z.date(),
  last_used_at: z.date().nullable().optional(),
});

const APIKeyCreatedResponse = APIKeyResponse.extend({
  raw_key: z.string(),
});

const APIKeyVerifyRequest = z.object({
  key: z.string(),
});

const APIKeyVerifyResponse = z.object({
  valid: z.boolean(),
  user_id: z.string().uuid().nullable().optional(),
});

module.exports = {
  APIKeyCreate,
  APIKeyResponse,
  APIKeyCreatedResponse,
  APIKeyVerifyRequest,
  APIKeyVerifyResponse,
};
