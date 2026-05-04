from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

wallets: list[dict] = [
    {
        "id": 1,
        "name": "Deepak",
        "amount": 200.0,
    },
    {
        "id": 2,
        "name": "Kapil",
        "amount": 0.0,
    }
]

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/api/wallets", response_class=JSONResponse)
def get_wallets():
    return wallets

# jinja2 html template integration
# app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
@app.get("/jinja2", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"wallets": wallets, "title": "Jinja2"})