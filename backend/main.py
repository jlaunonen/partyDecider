import contextlib

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from . import config, settings
from .admin import router as admin_router
from .db import finish_request
from .db import lifecycle as db_lifecycle
from .platforms import Platform
from .frontend_integration import ZipStaticFiles, lifecycle as hmr_lifecycle


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

    async with db_lifecycle(), hmr_lifecycle():
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


@app.middleware("http")
async def database_middleware(request: Request, call_next) -> Response:
    response = await call_next(request)
    await finish_request(request)
    return response


if config.IS_ZIP_APP:
    app.mount("/", ZipStaticFiles())
else:
    print("Root path is expecting frontend server to be found at", f"{config.VITE_DEV_URL}?port={settings.PORT}")

    @app.get("/", status_code=307)
    async def root() -> RedirectResponse:
        url = config.VITE_DEV_URL + f"?port={settings.PORT}"
        return RedirectResponse(url)
