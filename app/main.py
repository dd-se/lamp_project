from typing import Any, Union

from fastapi import FastAPI, Request, responses
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from api import router
from database import Base, engine

app = FastAPI(
    title="Gruppuppgift-Linux 2",
    version="DEMO",
    description="A simple demonstration of a LAMP stack",
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
        },
        status_code=500,
    )


@app.exception_handler(IntegrityError)
@app.exception_handler(ValidationError)
@app.exception_handler(RequestValidationError)
async def rick_rolled(
    request: Request,
    exception: Union[IntegrityError, Union[ValidationError, RequestValidationError]],
):
    return responses.RedirectResponse(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ", status_code=307
    )
