# -*- coding: utf-8 -*-

import contextlib
import re
from urllib.parse import urlparse, urlunparse

from fastapi import FastAPI, Request, Response
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from starlette.exceptions import HTTPException as StarletteHTTPException

from . import config, settings
from .admin import router as admin_router
from .db import finish_request
from .db import lifecycle as db_lifecycle
from .platforms import Platform
from .public import router as public_router
from .resources import router as resources_router
from .state import dev_lifecycle as state_dev_lifecycle
from .frontend_integration import ZipStaticFiles, lifecycle as hmr_lifecycle
from .openapi import use_route_names_as_operation_ids


tags_metadata = [
    {
        "name": "admin",
        "description": "Operations that require access from 127.0.0.1",
    }
]


@contextlib.asynccontextmanager
async def lifecycle(_: FastAPI):
    config.CLIENT_URL = "http://{hostname}:{port}".format(
        hostname=Platform.get_hostname(), port=settings.PORT
    )
    config.ADMIN_URL = "http://127.0.0.1:{port}".format(port=settings.PORT)

    if not settings.NO_BROWSER:
        Platform.spawn_browser(settings.BROWSER_CMD, config.ADMIN_URL)

    async with db_lifecycle(), hmr_lifecycle(), state_dev_lifecycle():
        yield


app = FastAPI(
    debug=settings.DEBUG,
    lifespan=lifecycle,
    openapi_tags=tags_metadata,
)
if not config.IS_ZIP_APP:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[config.VITE_DEV_URL],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(admin_router, prefix="/api/admin")
app.include_router(public_router, prefix="/api")
app.include_router(resources_router, prefix="/res")


@app.middleware("http")
async def database_middleware(request: Request, call_next) -> Response:
    response = await call_next(request)
    await finish_request(request)
    return response


FRONTEND_PATHS = (
    re.compile(r"/$"),
    re.compile(r"/(admin|default)$"),
    re.compile(r"/poll/\w{8}-\w{4}-\w{4}-\w{12}$"),
)


def frontend_converter(path: str) -> str | None:
    for p in FRONTEND_PATHS:
        if p.match(path) is not None:
            break
    else:
        return

    if path == "/":
        path = ""

    if config.IS_ZIP_APP:
        # In zipapp, we probably don't have dev url at all, but the path is still valid.
        return path

    base_url = config.VITE_DEV_URL + f"?port={settings.PORT}"
    result_url = urlparse(base_url)._replace(path=path)
    return urlunparse(result_url)


if config.IS_ZIP_APP:
    app.mount("/", ZipStaticFiles(frontend_converter))
else:
    print(
        "Root path is expecting frontend server to be found at",
        f"{config.VITE_DEV_URL}?port={settings.PORT}",
    )

    @app.get(
        "/",
        response_class=RedirectResponse,
        include_in_schema=False,
    )
    async def root() -> RedirectResponse:
        """
        Development redirect to HMR frontend.
        In zipapp, root path is mounted to serve compiled frontend.
        """
        url = config.VITE_DEV_URL + f"?port={settings.PORT}"
        return RedirectResponse(url)

    @app.exception_handler(StarletteHTTPException)
    async def not_found_handler(request: Request, exc: StarletteHTTPException):
        # If the 404 path is a path handled by frontend routing, redirect to (dev) frontend instead.
        # In zipapp, this is handled in the ZipStaticFiles separately.
        path = request.url.path
        if (
            exc.status_code != 404
            or request.method != "GET"
            or path.startswith("/api/")
            or path.startswith("/res/")
        ):
            return await http_exception_handler(request, exc)

        converted_path = frontend_converter(path)
        if converted_path is None:
            return await http_exception_handler(request, exc)

        return RedirectResponse(converted_path)


# Provide sane names for api functions for client.
use_route_names_as_operation_ids(app)
