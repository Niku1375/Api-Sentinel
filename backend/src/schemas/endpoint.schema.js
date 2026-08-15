const { z } = require('zod');

const EndpointCreate = z.object({
  project_id: z.string().uuid(),
  name: z.string(),
  url: z.string().url(),
  method: z.string().default('GET'),
  interval_seconds: z.number().int().default(60),
  timeout_seconds: z.number().int().default(5),
});

const EndpointResponse = z.object({
  id: z.string().uuid(),
  name: z.string(),
  url: z.string(),
  method: z.string(),
  interval_seconds: z.number(),
  timeout_seconds: z.number(),
});

module.exports = { EndpointCreate, EndpointResponse };
