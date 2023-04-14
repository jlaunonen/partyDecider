from email.utils import format_datetime
import contextlib
import datetime
import os
import sys
import hashlib
import importlib.util
import subprocess
import threading
import typing
import zipfile

import anyio

from fastapi import HTTPException

from starlette.responses import FileResponse, Response
from starlette.types import Receive, Scope, Send

from backend import config, settings


@contextlib.asynccontextmanager
async def lifecycle():
    thread: threading.Thread | None = None
    interrupt: bool = False

    if not config.IS_ZIP_APP and settings.VITE_DEV_CMD:
        cmd = settings.VITE_DEV_CMD.replace("%h", settings.HOST).replace(
            "%p", str(settings.VITE_DEV_PORT)
        )

        def runner():
            with contextlib.chdir("frontend"):
                proc = subprocess.Popen(
                    cmd, stdout=sys.stdout, stderr=sys.stderr, shell=True
                )
                while not interrupt and proc.poll() is None:
                    try:
                        proc.communicate(timeout=1)
                    except subprocess.TimeoutExpired:
                        pass
                print("Stopping vite...")
                proc.terminate()
                try:
                    proc.wait(2)
                except subprocess.TimeoutExpired:
                    print("Killing vite...")
                    proc.kill()

        thread = threading.Thread(target=runner, name="Vite")
        thread.start()

    yield

    interrupt = True
    if thread is not None:
        thread.join()


class ZipStaticFiles:
    def __init__(self):
        # Assumption: backend and frontend are provided from same archive.
        # Assumption: We are in a zipapp.
        spec = importlib.util.find_spec("backend")

        available_files: dict[str, zipfile.ZipInfo] = {}
        self._zip: zipfile.ZipFile = zipfile.ZipFile(spec.loader.archive)
        for info in self._zip.infolist():
            name = info.filename
            if name.startswith("frontend/") and not name.endswith("/"):
                available_files[name] = info

        self._available_files = available_files

    def __del__(self):
        if self._zip is not None:
            self._zip.close()

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        path = os.path.normpath(os.path.join(*scope["path"].split("/")))
        response = await self.get_response(path, scope)
        await response(scope, receive, send)

    async def get_response(self, path: str, scope: Scope) -> Response:
        if scope["method"] not in ("GET", "HEAD"):
            raise HTTPException(status_code=405)

        p = os.path.normpath(os.path.join("frontend", path))
        pindex = os.path.join(p, "index.html")

        info = self._available_files.get(p) or self._available_files.get(pindex)
        if info is None:
            raise HTTPException(status_code=404)

        return ZipFileResponse(
            info=info,
            opener=lambda: self._zip.open(info.filename),
        )


class ZipFileResponse(FileResponse):
    def __init__(
        self,
        info: zipfile.ZipInfo,
        opener: callable,
        status_code: int = 200,
        headers: typing.Optional[typing.Mapping[str, str]] = None,
        media_type: typing.Optional[str] = None,
        filename: typing.Optional[str] = None,
        method: typing.Optional[str] = None,
    ) -> None:
        super().__init__(
            path=info.filename,  # used only for type guess
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            filename=filename,
            method=method,
        )
        self._opener = opener
        self.set_info_headers(info)

    def set_info_headers(self, info: zipfile.ZipInfo):
        dt = datetime.datetime(*info.date_time, tzinfo=datetime.timezone.utc)

        content_length = str(info.file_size)
        last_modified = format_datetime(dt, usegmt=True)
        etag_base = str(info.date_time) + "-" + str(info.file_size)
        etag = hashlib.md5(etag_base.encode(), usedforsecurity=False).hexdigest()

        self.headers.setdefault("content-length", content_length)
        self.headers.setdefault("last-modified", last_modified)
        self.headers.setdefault("etag", etag)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": self.raw_headers,
            }
        )
        if self.send_header_only:
            await send({"type": "http.response.body", "body": b"", "more_body": False})
        else:
            f = await anyio.to_thread.run_sync(self._opener)
            async with anyio.AsyncFile(f) as af:
                more = True
                while more:
                    chunk = await af.read(self.chunk_size)
                    more = len(chunk) == self.chunk_size
                    await send(
                        {
                            "type": "http.response.body",
                            "body": chunk,
                            "more_body": more,
                        }
                    )
