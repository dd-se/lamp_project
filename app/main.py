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


@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(router)


@app.exception_handler(500)
async def internal_server_error_handler(
    request: Request, exception: Union[Exception, Any]
):
    return responses.JSONResponse(
        content={
            "Type": "Internal Server Error",
            "Action": "Staff has been notified, please try again later.",
        }
    )
