import asyncio
from app.workers.monitor_worker import run_monitoring

asyncio.run(run_monitoring())