from celery import Celery
from celery.schedules import crontab
from datetime import timedelta

from app.config import settings

celery_app = Celery(
    'site_monitor',
    broker=settings.redis_host,
    backend=settings.redis_host
)

celery_app.conf.imports = ['app.tasks.monitor']

celery_app.conf.beat_schedule = {
    "check-sites-every-5-minutes": {
        "task": "app.tasks.monitor.check_all_sites",
        "schedule": timedelta(seconds=30),
    },
}

celery_app.autodiscover_tasks(['app.tasks'])