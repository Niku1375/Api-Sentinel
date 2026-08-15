const { z } = require('zod');

const MonitoringResultResponse = z.object({
  status_code: z.number().int().nullable(),
  response_time: z.number(),
  success: z.boolean(),
  checked_at: z.date(),
});

const MonitoringStats = z.object({
  total_checks: z.number().int(),
  successes: z.number().int(),
  failures: z.number().int(),
  uptime_percentage: z.number(),
  avg_response_time: z.number(),
});

module.exports = { MonitoringResultResponse, MonitoringStats };
