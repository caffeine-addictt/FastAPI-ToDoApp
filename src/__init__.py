from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory = 'src/templates')
app.mount('/static', StaticFiles(directory = 'src/static'), name = 'static')


@app.get('/')
def render_homepage():
  return templates.TemplateResponse(
    'index.html'
  )

