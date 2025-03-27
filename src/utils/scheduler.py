from apscheduler.schedulers.asyncio import AsyncIOScheduler

def schedule_func(func):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(func=func, trigger="cron", hour=12, minuts=5)
    scheduler.start()