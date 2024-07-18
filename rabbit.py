from celery import Celery
from serial import SerialException
import logging
from infosys import display
import os

broker_url = os.environ['BROKER_URL']
display_tasks = Celery('tasks', broker=broker_url)

@display_tasks.task
def time_background():
    d = display()

    try:
      d.print_time()
    except SerialException as e:
      logging.warn('Time could not get lock')
      return
    
@display_tasks.task
def text_background(msg: str, effect: str, wipe: bool):
    d = display()

    try:
      d.write_text(msg, effect, wipe)
    except SerialException as e:
      logging.warn('Text could not get lock')
      return