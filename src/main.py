from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from api.routers import main_router
from core import configs
from api.error_handler import request_validation_exception_handler, unrecognized_exception_handler
from dependencies.db import db_manager
from middlewares.camel_case import CamelCaseMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        if db_manager._engine is not None:
            await db_manager.close()


def init_app():
    app = FastAPI(
        title="Coffee Shop Backend",
        version="1.0",
        lifespan=lifespan,
        # TODO remove
        debug=True,
    )

    app.add_middleware(
        CORSMiddleware,
        **configs.CORS_SETTINGS
    )
    app.add_middleware(CamelCaseMiddleware)

    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(Exception, unrecognized_exception_handler)

    app.include_router(main_router)

    return app


app = init_app()
