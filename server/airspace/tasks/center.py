from celery import shared_task
from celery.utils.log import get_task_logger
from airspace.tasks import helpers

logger = get_task_logger(__name__)

@shared_task
def update_centers():
    logger.info(helpers.get_latest_date())
