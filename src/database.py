"""
Using local JSON file as database so as to make exporting and readinging easier :>
"""

import os
import json
from typing import Dict
from datetime import datetime

from .logger import logger
from .types import (
  Task,
  _RawTask,

  TodoTask,
  EventTask,

  JSONData,
  _RawJSONData,
)


# Setup, Change this as you like :D
_dirname : str = 'saves'
_filename: str = 'tasks.json'

defaultData: _RawJSONData = {
  'tags': ['Examination', 'Assignment'],
  'tasks': {}
}



# Core functions
def _convertToJSONSerializable(tasks: Dict[str, Task]) -> Dict[str, _RawTask]:
  """
  Convert a list of tasks to JSON serializable format
  """

  converted: Dict[str, _RawTask] = {}
  for uid, task in tasks.items():
    converted_event: _RawTask = {
      'type'       : task.type,
      'title'      : task.title,
      'description': task.description,
      'tags'       : task.tags,
      'location'   : isinstance(task, EventTask) and task.location or None,
      'start_date' : isinstance(task, EventTask) and task.start_date.timestamp() or None,
      'end_date'   : task.end_date.timestamp(),
      'created_at' : task.created_at.timestamp()
    }
    converted[uid] = converted_event

  return converted

def _convertFromJSONSerializable(raw_tasks: Dict[str, _RawTask]) -> Dict[str, Task]:
  """
  Convert a list of tasks from JSON serializable format
  """

  converted: Dict[str, Task] = {}
  for uid, rawtask in raw_tasks.items():
    if rawtask['type'] == 'Event':
      converted[uid] = EventTask(
        id          = uid,
        type        = 'Event',
        title       = rawtask['title'],
        description = rawtask['description'],
        tags        = rawtask['tags'],
        location    = rawtask['location'],
        start_date  = datetime.fromtimestamp(rawtask['start_date'] or rawtask['created_at']),
        end_date    = datetime.fromtimestamp(rawtask['end_date']),
        created_at  = datetime.fromtimestamp(rawtask['created_at'])
      )

    elif rawtask['type'] == 'Todo':
      converted[uid] = TodoTask(
        id          = uid,
        type        = 'Todo',
        title       = rawtask['title'],
        description = rawtask['description'],
        tags        = rawtask['tags'],
        end_date    = datetime.fromtimestamp(rawtask['end_date']),
        created_at  = datetime.fromtimestamp(rawtask['created_at'])
      )

  return converted



def getPath() -> str:
  global _dirname
  global _filename
  global defaultData

  directoryPath: str = os.path.join(os.getcwd(), _dirname)
  if not os.path.isdir(directoryPath):
    logger.warning('Could not locate data directory in: %s' % directoryPath)
    logger.info('Buidling data directory...')
    os.mkdir(directoryPath)
    logger.info('Built data directory')

  
  filePath: str = os.path.join(directoryPath, _filename)
  if not os.path.isfile(filePath):
    logger.warning('Could not locate save file in: %s' % filePath)
    logger.info('Building save file...')

    with open(filePath, 'x') as f:
      f.write(json.dumps(defaultData, indent = 2))

    logger.info('Built save file')

  return filePath



def readFile() -> JSONData:
  with open(getPath(), 'r') as f:
    data: _RawJSONData = json.load(f)

  return {
    'tags': data['tags'],
    'tasks': _convertFromJSONSerializable(data['tasks'])
  }
    
def saveFile(data: JSONData) -> None:
  serializedData: _RawJSONData = {
    'tags': data['tags'],
    'tasks': _convertToJSONSerializable(data['tasks'])
  }

  with open(getPath(), 'w') as f:
    f.write(json.dumps(serializedData, indent = 2))
  logger.warning('Saved file')
