const { z } = require('zod');

const UserCreate = z.object({
  name: z.string(),
  email: z.string().email(),
  password: z.string(),
});

const UserLogin = z.object({
  email: z.string().email(),
  password: z.string(),
});

const UserResponse = z.object({
  id: z.string().uuid(),
  name: z.string(),
  email: z.string().email(),
});

module.exports = { UserCreate, UserLogin, UserResponse };
