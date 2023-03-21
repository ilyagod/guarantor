import asyncio
import time

from asgiref.sync import async_to_sync
from celery import current_app
from celery.app import task, shared_task
from celery.schedules import crontab
from loguru import logger
from tortoise import Tortoise

from guarantor.db.config import TORTOISE_CONFIG
from guarantor.db.dao.deal_dao import DealDAO
from guarantor.settings import settings


def get_celery_app():
    celery = current_app
    celery.conf.broker_url = str(settings.redis_url)
    celery.conf.result_backend = str(settings.redis_url)
    celery.conf.update(task_acks_late=True)
    celery.conf.update(task_default_priority=5)
    celery.conf.update(task_queue_max_priority=10)
    celery.conf.beat_schedule = {
        'celery_beat_testing': {
            'task': 'guarantor.celery.worker.test_task',
            'schedule': crontab(minute='*/1')
        }
    }

    return celery

celery_app = get_celery_app()


async def test_task_async():
    await Tortoise.init(config=TORTOISE_CONFIG)
    data = [deal.title for deal in await DealDAO.get_all(100, 0)]
    logger.info(data)
    print(data)
    data = [deal.title for deal in await DealDAO.get_all(100, 0)]
    logger.info(data)
    print(data)


@shared_task(bind=True)
def test_task(*args, **kwargs):
    async_to_sync(test_task_async())



