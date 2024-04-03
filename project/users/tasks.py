import random
import requests

from project import db

from celery import shared_task
from celery.utils.log import get_task_logger
from celery.signals import task_postrun

from project.celery_utils import custom_celery_task

logger = get_task_logger(__name__)


@shared_task
def divide(x, y):
    # from celery.contrib import rdb
    # rdb.set_trace()

    import time
    time.sleep(5)
    return x / y


@shared_task()
def sample_task(email):
    from project.users.views import api_call

    api_call(email)



# @shared_task(bind=True)
# def task_process_notification(self):
#     try:
#         # if not random.choice([0, 1]):
#         #     raise Exception()

#         # this would block the I/O
#         requests.post('https://httpbin.org/delay/5')
#     except Exception as e:
#         logger.error('exception raised, it would be retry after 5 seconds')
#         raise self.retry(exc=e, countdown=5)
    
@custom_celery_task(max_retries=3)
def task_process_notification():
    if not random.choice([0, 1]):
        # mimic random error
        raise Exception()

    requests.post('https://httpbin.org/delay/5')
    

@shared_task(name='task_schedule_work')
def task_schedule_work():
    logger.info('task_schedule_work run')


@shared_task(name='default:dynamic_example_one')
def dynamic_example_one():
    logger.info('Example One')


@shared_task(name='low_priority:dynamic_example_two')
def dynamic_example_two():
    logger.info('Example Two')


@shared_task(name='high_priority:dynamic_example_three')
def dynamic_example_three():
    logger.info('Example Three')


@shared_task()
def task_send_welcome_email(user_pk):
    from project.users.models import User
    user = User.query.get(user_pk)
    logger.info(f'send email to {user.email} {user.id}')


@task_postrun.connect
def task_postrun_handler(task_id, **kwargs):
    from project.users.events import update_celery_task_status
    update_celery_task_status(task_id)


@shared_task()
def task_test_logger():
    logger.info('test')



@shared_task(bind=True)
def task_add_subscribe(self, user_pk):
    try:
        from project.users.models import User
        user = db.session.get(User, user_pk)
        requests.post(
            'https://httpbin.org/delay/5',
            data={'email': user.email},
        )
    except Exception as exc:
        raise self.retry(exc=exc)