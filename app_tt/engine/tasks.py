from celery import Celery

celery = Celery('tasks', backend='amqp', broker='amqp://celery:celery@localhost:5672/celery')


@celery.task
def check_app_done(short_name):
    return short_name
