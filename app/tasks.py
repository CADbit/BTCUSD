from celery.task import task
from .controllesrs import ExchangeController
from exceptions import Exception
#
@task()
def getBTCUSD():
    ec = ExchangeController()
    try:
        print ec.getData()
    except Exception:
        print Exception.message