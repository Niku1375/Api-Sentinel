const cron = require('node-cron');
const { runMonitoring } = require('./monitor.worker');

function startScheduler() {
  // Runs every 60 seconds
  cron.schedule('* * * * *', async () => {
    console.log('[Scheduler] Running monitoring sweep...');
    try {
      await runMonitoring();
    } catch (err) {
      console.error('[Scheduler] Error:', err.message);
    }
  });
  console.log('[Scheduler] Started');
}

module.exports = { startScheduler };
