import logging
import os

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from .currency import get_usd_to_uah

logger = logging.getLogger(__name__)


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def start():
    if os.environ.get("RUN_MAIN") != "true":
        return
    scheduler = BackgroundScheduler(timezone="Europe/Kyiv")
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(
        get_usd_to_uah,
        CronTrigger(hour=22, minute=37),
        id="get_usd_to_uah",
        replace_existing=True,
    )

    logger.info("Job 'get_usd_to_uah' added!")

    scheduler.add_job(
        delete_old_job_executions,
        CronTrigger(day_of_week="mon", hour=0, minute=0),
        id="delete_old_job_executions",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("APScheduler started!")
