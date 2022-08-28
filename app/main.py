from fastapi import Depends, FastAPI, Request
from fastapi import __version__ as fastapi_version
from fastapi import responses
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import Base, User, engine, get_db

j2templates = Jinja2Templates(directory="templates")
render = j2templates.TemplateResponse

app = FastAPI(
    title="Gruppuppgift-Linux 2",
    version="DEMO",
    description="A simple demonstration of a LAMF stack",
)


@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
    app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=responses.HTMLResponse)
async def get_all_users(request: Request, db: Session = Depends(get_db)):
    all_users = db.query(User).all()
    return render("users.html", {"request": request, "users": all_users})


@app.get("/status", response_class=responses.HTMLResponse)
async def status(request: Request, db: Session = Depends(get_db)):
    return render("status.html", {"request": request, "fa": fastapi_version})
