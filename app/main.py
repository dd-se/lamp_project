from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from typing import Any, Union

from fastapi import FastAPI, Request, responses
from fastapi.staticfiles import StaticFiles

from api import router
from database import Base, engine
from settings import secrets

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
    app.include_router(router)


@app.exception_handler(500)
async def internal_server_error_handler(
    request: Request, exception: Union[Exception, Any]
):
    if secrets.PRODUCTION:
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
