from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.background import BackgroundTasks

import uuid
from datetime import datetime

from .calander import generateCalander
from .database import readFile, saveFile
from .types import CreateTaskRequest, DeleteTaskRequest, EditTaskRequest, EventTask, TodoTask

app = FastAPI()

templates = Jinja2Templates(directory = 'src/templates')
app.mount('/static', StaticFiles(directory = 'src/static'), name = 'static')




# Pages
@app.get('/', response_class = HTMLResponse)
def render_homepage(request: Request):
  return templates.TemplateResponse(
    'index.html',
    context = { 'request': request, 'tasks': readFile()['tasks'] }
  )


@app.get('/create', response_class = HTMLResponse)
def render_createpage(request: Request):
  return templates.TemplateResponse(
    'create.html',
    context = { 'request': request }
  )


@app.get('/edit', response_class = HTMLResponse)
def render_editpage(request: Request, uid: str):
  currentData = readFile()
  toEdit = currentData['tasks'].get(uid)

  if not toEdit:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Task does not exist')
  
  return templates.TemplateResponse(
    'edit.html',
    context = { 'request': request, 'task': toEdit }
  )


@app.get('/export')
def download_calander_ics(bg_tasks: BackgroundTasks):
  tmpPath, cleanup = generateCalander(readFile()['tasks'], [])

  bg_tasks.add_task(cleanup)
  return FileResponse(
    path = tmpPath,
    filename = f'mytasks-{datetime.utcnow().isoformat()}.ics',
    media_type = 'application/octet-stream',
    background = bg_tasks
  )




# API
@app.post('/create-task', status_code = status.HTTP_201_CREATED)
def handle_create_task(body: CreateTaskRequest):
  now = datetime.utcnow()

  if body.type == 'Event':
    created_event = EventTask(
      id          = uuid.uuid4().hex,
      type        = 'Event',
      title       = body.title,
      description = body.description,
      tags        = body.tags,
      location    = body.location,
      start_date  = body.start_date or now,
      end_date    = body.end_date,
      created_at  = now
    )

    currentData = readFile()
    currentData['tasks'][created_event.id] = created_event
    saveFile(currentData)
    return { 'id': created_event.id }
  
  else:
    created_todo = TodoTask(
      id          = uuid.uuid4().hex,
      type        = 'Todo',
      title       = body.title,
      description = body.description,
      tags        = body.tags,
      end_date    = body.end_date,
      created_at  = now
    )

    currentData = readFile()
    currentData['tasks'][created_todo.id] = created_todo
    saveFile(currentData)
    return { 'id': created_todo.id }


@app.post('/edit-task', status_code = status.HTTP_200_OK)
def handle_edit_task(body: EditTaskRequest):
  currentData = readFile()
  taskData = currentData['tasks'].get(body.id)

  if not taskData:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Task not found')
  
  changed = False
  if body.title       and taskData.title                 : changed = True; taskData.title = body.title
  if body.description and taskData.description           : changed = True; taskData.description = body.description
  if body.tags        and taskData.tags                  : changed = True; taskData.tags = body.tags
  if body.location    and isinstance(taskData, EventTask): changed = True; taskData.location = taskData.location
  if body.start_date  and isinstance(taskData, EventTask): changed = True; taskData.start_date = body.start_date
  if body.end_date    and taskData.end_date              : changed = True; taskData.end_date = body.end_date

  if not changed:
    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'Nothing to edit')

  currentData['tasks'][body.id] = taskData
  saveFile(currentData)


@app.post('/delete-task', status_code = status.HTTP_200_OK)
def handle_delete_task(body: DeleteTaskRequest):
  currentData = readFile()
  excluded = { uid: task for uid, task in currentData['tasks'].items() if uid != body.id }

  if currentData['tasks'] == excluded:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'Task not found')
  
  currentData['tasks'] = excluded
  saveFile(currentData)




# Errors
@app.exception_handler(status.HTTP_404_NOT_FOUND)
async def handle_404(request: Request, exc: HTTPException):
  if request.url.path.endswith('-task'):
    return JSONResponse(
      status_code = status.HTTP_404_NOT_FOUND,
      content = { 'detail': exc.detail }
    )
  
  return templates.TemplateResponse(
    '404.html',
    context = { 'request': request },
    status_code = status.HTTP_404_NOT_FOUND
  )
