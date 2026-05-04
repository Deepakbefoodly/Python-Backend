from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

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

@app.get("/api/wallets/{wallet_id}")
def get_wallet(wallet_id: int):
    for wallet in wallets:
        if wallet["id"] == wallet_id:
            return wallet
    raise HTTPException(status_code=404, detail="Wallet not found")

# we can write custom api error validations using this code block
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if request.url.path.startswith("/api"):
        return None
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


# jinja2 html template integration
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
@app.get("/jinja2", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"wallets": wallets, "title": "Jinja2"})