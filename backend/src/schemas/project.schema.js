const { z } = require('zod');

const ProjectCreate = z.object({
  name: z.string(),
  description: z.string().optional(),
});

const ProjectResponse = z.object({
  id: z.string().uuid(),
  name: z.string(),
  description: z.string().nullable(),
});

module.exports = { ProjectCreate, ProjectResponse };
