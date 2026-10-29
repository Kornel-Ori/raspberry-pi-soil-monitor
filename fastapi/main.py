from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sample_readings import sample_readings

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="pages")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {
            "sensor_readings": sample_readings,
            "title": "My Plant Monitor"
        }
    )

@app.get("/demo")
def demo_dashboard(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {
            "sensor_readings": sample_readings,
            "title": "My Plant Monitor"
        }
    )
