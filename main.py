import time

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from schemas import WalletCreate, WalletResponse

app = FastAPI()

wallets: list[dict] = [
    {
        "id": 1,
        "name": "Deepak",
        "amount": 200.0,
        "created_at": "2023-01-01T00:00:00Z",
    },
    {
        "id": 2,
        "name": "Kapil",
        "amount": 0.0,
        "created_at": "2023-01-02T00:00:00Z",
    }
]

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/api/wallets", response_model=list[WalletResponse], response_model_exclude_none=True)
def get_wallets():
    return wallets

@app.get("/api/wallets/{wallet_id}", response_class=JSONResponse)
def get_wallet(wallet_id: int):
    for wallet in wallets:
        if wallet["id"] == wallet_id:
            return wallet
    raise HTTPException(status_code=404, detail="Wallet not found")

@app.post("/api/wallets", response_model=WalletResponse, status_code=201)
def create_wallet(wallet: WalletCreate):
    wallet_id = max(wallet["id"] for wallet in wallets) + 1
    new_wallet = {
        "id": wallet_id,
        "name": wallet.name,
        "amount": wallet.amount,
        "created_at": time.localtime(),
    }
    wallets.append(new_wallet)
    return new_wallet

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