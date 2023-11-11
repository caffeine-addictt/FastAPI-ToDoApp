"""
Calendar stuff
"""

import os
import re
from datetime import datetime, timedelta
from icalendar import Calendar, Event, Todo, Alarm
from typing import Dict, List, Tuple

from .logger import logger
from .types import GeneratedCalendarResponse, CalendarCleanupFunc, CalendarFilePath, Task, TodoTask, EventTask


def _cleanUpFuncGenerator(path: str) -> CalendarCleanupFunc:
  def cleanup() -> None:
    """Cleans up tmp calendar ics file"""
    try:
      os.remove(path)
      logger.warning('Removed temp calendar file at: %s' % path)
    except Exception as e:
      logger.warning('Could not remove temp calendar file at: %s' % e.__str__())
  return cleanup

def generateCalander(data: Dict[str, Task], reminders: List[Tuple[str, float] | timedelta]) -> GeneratedCalendarResponse:
  calendar = Calendar()

  # Properties to be RFC5545 compliant
  calendar.add('prodid', '-//github.com/caffeine-addictt/FastAPI-ToDoApp - TODO App//')
  calendar.add('version', '2.0')

  # Add sub-components
  alarms = []
  for reminder in reminders:
    newAlarm = Alarm()
    newAlarm.add('action', 'DISPLAY')
    newAlarm.add('description', 'Reminder')
    newAlarm.add('trigger', (isinstance(reminder, tuple) and timedelta(**{ f'{reminder[0]}': reminder[1] })) or reminder)
    alarms.append(newAlarm)

  for uid, task in data.items():
    if isinstance(task, TodoTask):
      newTodo = Todo()
      newTodo.add('summary', task.title)
      newTodo.add('description', task.description)
      newTodo.add('due', task.end_date)
      newTodo.add('dtstamp', task.created_at)
      newTodo.add('priority', 0)
      newTodo.add('status', 'NEEDS-ACTION')

      cleaned_title = re.sub(r'\s+', '', task.title, flags =re.UNICODE)
      newTodo.add('uid', f'{cleaned_title}-{uid}')

      for alarm in alarms: newTodo.add_component(alarm)
      calendar.add_component(newTodo)

    elif isinstance(task, EventTask):
      event = Event()
      event.add('summary', task.title)
      event.add('location', task.location)
      event.add('description', task.description)
      event.add('dtstart', task.start_date)
      event.add('dtend', task.end_date)
      event.add('dtstamp', task.created_at)
      event.add('priority', 5)

      cleaned_title = re.sub(r'\s+', '', task.title, flags =re.UNICODE)
      event.add('uid', f'{cleaned_title}-{uid}')

      for alarm in alarms: event.add_component(alarm)
      calendar.add_component(event)

  filePath: CalendarFilePath = f'tmp-{datetime.utcnow().isoformat()}.ics'
  with open(filePath, 'wb') as f:
    f.write(calendar.to_ical())

  logger.warning('Generated temp calendar file at: %s' % filePath)
  return filePath, _cleanUpFuncGenerator(filePath)
