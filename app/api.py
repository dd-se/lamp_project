from fastapi import Depends, APIRouter, Request
from fastapi import __version__ as fastapi_version
from fastapi import responses
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import User, get_db
from settings import secrets

j2templates = Jinja2Templates(directory="templates")
render = j2templates.TemplateResponse

router = APIRouter(tags=["api"])


@router.get("/", response_class=responses.HTMLResponse)
async def get_all_users(request: Request, db: Session = Depends(get_db)):
    all_users = db.query(User).all()
    return render("users.html", {"request": request, "users": all_users})


@router.get("/status", response_class=responses.HTMLResponse)
async def status(request: Request, db: Session = Depends(get_db)):
    return render("status.html", {"request": request, "fa": fastapi_version})
