from celery import Celery

from .tasks import celery_app

if __name__ == '__main__':
    celery_app.worker_main(argv=['worker', '--loglevel=info', '--pool=solo'])
