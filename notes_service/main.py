"""Main module"""

from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

# Import and include API routers
from notes_service.api.endpoints import notes
from starlette.exceptions import HTTPException as StarletteHTTPException
from notes_service.config.settings import app_config


def create_app() -> FastAPI:
    # Initialize FastAPI app
    application = FastAPI()

    # # Add Routers
    application.include_router(notes.router)
    # Add Middlewares
    # Allow these origins to access the API
    origins = (
        app_config.ALLOW_ORIGINS.split(",")
        if app_config.ALLOW_ORIGINS.strip()
        else ["*"]
    )

    # Allow these methods to be used
    methods = ["*"]

    # Allow these methods to be used
    headers = ["*"]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=app_config.ALLOW_CREDENTIALS,
        allow_methods=methods,
        allow_headers=headers,
    )
    # Mount files
    application.mount(
        "/notes_service/upload_files",
        StaticFiles(directory="notes_service/upload_files"),
        name="files",
    )
    return application


app = create_app()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_: Any, exc: StarletteHTTPException) -> JSONResponse:
    return JSONResponse(
        content={"status": False, "data": None, "message": exc.detail},
        status_code=exc.status_code,
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Any, exc: Exception) -> JSONResponse:
    response = JSONResponse(
        content={
            "status": False,
            "data": None,
            "message": f"Unhandled Exception :: {str(exc)}",
        },
        status_code=500,
    )
    response.headers.update(
        {
            "Access-Control-Allow-Origin": (
                app_config.ALLOW_ORIGINS if app_config.ALLOW_ORIGINS.strip() else "*"
            ),
            "Access-Control-Allow-Credentials": (
                "true" if app_config.ALLOW_CREDENTIALS else "false"
            ),
        }
    )
    return response
