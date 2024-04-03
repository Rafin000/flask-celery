import json
import os
from kombu import Queue
from pathlib import Path



def route_task(name, args, kwargs, options, task=None, **kw):
    if ':' in name:
        queue, _ = name.split(':')
        return {'queue': queue}
    return {'queue': 'default'}


class BaseConfig:
    """Base Configuration"""
    BASE_DIR = Path(__file__).parent.parent

    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATION = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR}/db.sqlite3")

    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0")  

    SOCKETIO_MESSAGE_QUEUE = os.environ.get(
        'SOCKETIO_MESSAGE_QUEUE',
        'redis://127.0.0.1:6379/0'
    )

    CELERY_BEAT_SCHEDULE = {
        # 'task-schedule-work': {
        #     'task': 'task_schedule_work',
        #     "schedule": 5.0, 
        # },

    #     'add-every-30-seconds': {
    #     'task': 'tasks.add',
    #     'schedule': 30.0,
    #     'args': (16, 16)
    # },
    }


    CELERY_TASK_DEFAULT_QUEUE = 'default'
    CELERY_TASK_CREATE_MISSING_QUEUES = False

    CELERY_TASK_QUEUES = (
        Queue('default'),
        Queue('high_priority'),
        Queue('low_priority'),
    )


    # CELERY_TASK_ROUTES = {
    #     'project.users.tasks.*': {
    #         'queue': 'high_priority',
    #     },
    # }
    
    CELERY_TASK_ROUTES = (route_task,)

    # CELERY_TASK_ALWAYS_EAGER=True
    # CELERY_TASK_STORE_EAGER_RESULT = True

    CELERY_WORKER_PREFETCH_MULTIPLIER = 1
    # CELERY_TASK_SERIALIZER = json
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOADS_DEFAULT_DEST = str(BASE_DIR / 'upload')



class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SOCKETIO_MESSAGE_QUEUE = None
    SECRET_KEY = 'my secret'
    WTF_CSRF_ENABLED = False



config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    'testing': TestingConfig
}