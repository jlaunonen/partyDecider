import contextlib
import csv
import os
import typing

import fastapi

from . import settings
from .models import AppItem
from .utils import ChangeTrackedDict


class _Database:
    def __init__(self):
        apps = [
            AppItem(1, 550, "Left 4 Dead 2"),  # TODO: Remove test entries
            AppItem(2, 620, "Portal 2"),
        ]
        self.apps: ChangeTrackedDict[int, AppItem] = ChangeTrackedDict({
            app.id: app
            for app in apps
        })  # fmt: skip

    def any_changed(self):
        return self.apps.is_changed


_db: _Database | None = None

_TERMINATOR = r"\NUL"


class AsyncSession:
    def __init__(self, db: _Database):
        self.db: _Database = db


def connect():
    global _db
    if _db is None:
        file = settings.DB_PATH
        if os.path.exists(file):
            _read_db(file)
        else:
            _db = _Database()


def disconnect():
    db = _db
    if db is not None:
        file = settings.DB_PATH
        _write_db(file, db)


@contextlib.asynccontextmanager
async def lifecycle():
    connect()
    yield
    disconnect()


SCOPE_REQUEST_DB_NAME = "app_database"


def request_database(request: fastapi.Request) -> AsyncSession:
    db = request.scope.get(SCOPE_REQUEST_DB_NAME)
    if db is None:
        db = _db
        session = AsyncSession(_db)
        request.scope[SCOPE_REQUEST_DB_NAME] = db, session
    else:
        _, session = db
    return session


async def finish_request(request):
    pass


def _read_db(file_name: str):
    with open(file_name, "rt", newline="") as f:
        reader = csv.reader(f)
        reader_iter: typing.Iterator[list[str]] = iter(reader)
        _read_version(reader_iter)

        new_db = _Database()

        def proxy():
            for line in reader_iter:
                if len(line) == 1 and line[0] == _TERMINATOR:
                    break
                yield line

        while True:
            try:
                tab_type = next(reader_iter)
            except StopIteration:
                break
            if len(tab_type) != 1:
                raise ValueError()
            t_reader = _TYPES[tab_type[0]]
            t_reader.read(proxy(), new_db)

        global _db
        _db = new_db


def _read_version(it: iter):
    ver_val = next(it)
    if len(ver_val) != 2 or ver_val[0] != "version" or ver_val[1] != "1":
        print("Unknown database")
        raise ValueError(ver_val)

    return ver_val[1]


class _Table:
    @classmethod
    def read(cls, it: typing.Iterator[list[str]], db: _Database):
        raise NotImplementedError

    @classmethod
    def write(cls, to: csv.writer, db: _Database):
        raise NotImplementedError


class _Apps(_Table):
    @classmethod
    def read(cls, it: typing.Iterator[list[str]], db: _Database):
        # ID, Steam_ID, Name
        for line in it:
            item = AppItem.from_csv(line)
            db.apps[item.id] = item
        db.apps.clear_changed()

    @classmethod
    def write(cls, to: csv.writer, db: _Database):
        for app in db.apps.values():
            to.writerow(app.to_csv())
        db.apps.clear_changed()


_TYPES: dict[str, typing.Type[_Table]] = {
    "apps": _Apps,
}


def _write_db(file_name: str, db: _Database):
    if not db.any_changed() and os.path.exists(file_name):
        return

    with open(file_name, "wt", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["version", 1])

        for _type, dao in _TYPES.items():
            writer.writerow([_type])
            dao.write(writer, db)
            writer.writerow([_TERMINATOR])
