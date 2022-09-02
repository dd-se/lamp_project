from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Union

from fastapi import Depends, FastAPI, Request
from fastapi import __version__ as fastapi_version
from fastapi import responses
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import Base, User, engine, get_db
from settings import secrets

j2templates = Jinja2Templates(directory="templates")
render = j2templates.TemplateResponse

app = FastAPI(
    title="Gruppuppgift-Linux 2",
    version="DEMO",
    description="A simple demonstration of a LAMF stack",
)


def send_email(status_code: int, mail_content: str):
    message = MIMEMultipart()
    message["From"] = secrets.EMAIL
    message["To"] = secrets.EMAIL
    message["Subject"] = f"{status_code} - Urgent"
    message.attach(MIMEText(mail_content, "plain"))
    session = SMTP("smtp.sendgrid.net", 587)
    session.starttls()
    session.login("apikey", secrets.EMAIL_PASSWORD)
    session.sendmail("apikey", secrets.EMAIL, message.as_string())
    session.quit()


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


@app.exception_handler(500)
async def internal_server_error_handler(
    request: Request, exception: Union[Exception, Any]
):
    if secrets.MYSQL_USER != "dbuser":
        send_email(
            500,
            mail_content=f"Intervention required.\nException:\n{exception.__dict__}",
        )
    return responses.JSONResponse(
        content={
            "Type": "Internal Server Error",
            "Action": "Staff has been notified, please try again later.",
        }
    )
