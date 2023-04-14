import contextlib

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse

from . import config, crud, settings
from .admin import router as admin_router
from .db import finish_request
from .db import lifecycle as db_lifecycle
from .dependencies import Database
from .platforms import Platform

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

    async with db_lifecycle():
        yield


app = FastAPI(
    debug=settings.DEBUG,
    lifespan=lifecycle,
    openapi_tags=tags_metadata,
)

app.include_router(admin_router, prefix="/api/admin")


@app.middleware("http")
async def database_middleware(request: Request, call_next) -> Response:
    response = await call_next(request)
    await finish_request(request)
    return response


@app.get("/")
async def root(db: Database):
    tpl = """<!DOCTYPE html><html lang="en">
<head><meta charset="UTF-8"><title>Party Decider</title></head>
<body><script>
    function do_shutdown() {
        fetch("/api/admin/shutdown").then(function (result) {
            console.log(result)
        })
    }
</script><button onclick="do_shutdown()">Shutdown</button>
<ul>
%s
</ul></body></html>"""
    return HTMLResponse(
        tpl % "\n".join(f"<li>{a.name} [{a.steam_id}]</li>" for a in crud.get_apps(db))
    )
