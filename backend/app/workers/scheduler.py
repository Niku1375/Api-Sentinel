from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.workers.monitor_worker import run_monitoring


scheduler = AsyncIOScheduler()


def start_scheduler():

    scheduler.add_job(
        run_monitoring,
        "interval",
        seconds=60
    )

    scheduler.start()