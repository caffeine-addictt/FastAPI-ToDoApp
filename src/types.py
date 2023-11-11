"""
Types of all objects used
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Tuple, Callable, Literal
from typing_extensions import TypedDict

from pydantic import BaseModel


TaskType = Literal['Event', 'Todo']

# Request bodys
class CreateTaskRequest(BaseModel):
  type       : TaskType
  title      : str
  description: str
  tags       : List[str]
  location   : Optional[str]
  start_date : Optional[datetime]
  end_date   : datetime

class EditTaskRequest(BaseModel):
  id         : str
  title      : Optional[str]
  description: Optional[str]
  tags       : Optional[List[str]]
  location   : Optional[str]
  start_date : Optional[datetime]
  end_date   : Optional[datetime]

class DeleteTaskRequest(BaseModel):
  id: str



# DB
class _RawTask(TypedDict):
  """JSON Serialized"""
  type       : TaskType
  title      : str
  description: str
  tags       : List[str]
  location   : Optional[str]
  start_date : Optional[float] # UNIX Timestamp
  end_date   : float           # UNIX Timestamp
  created_at : float           # UNIX Timestamp



@dataclass
class TaskBase:
  """Base Class"""
  id         : str
  type       : TaskType
  title      : str
  description: str
  tags       : List[str]
  end_date   : datetime
  created_at : datetime

@dataclass
class EventTask(TaskBase):
  """For use in application"""
  type = 'Event'
  location: Optional[str]
  start_date: datetime

@dataclass
class TodoTask(TaskBase):
  """For use in application"""
  type = 'Todo'

Task = TodoTask | EventTask



class _RawJSONData(TypedDict):
  """
  What is returned from JSON file
  """
  tags : List[str]
  tasks: Dict[str, _RawTask]

class JSONData(TypedDict):
  """
  Interpretated JSON data for use in application
  """
  tags : List[str]
  tasks: Dict[str, Task]



# Calendar
CalendarFilePath = str
CalendarCleanupFunc = Callable[[], None]
GeneratedCalendarResponse = Tuple[CalendarFilePath, CalendarCleanupFunc]
