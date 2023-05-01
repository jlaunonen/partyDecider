#!/usr/bin/env python

# Module entry point.
# Zip app entry point calls main() directly from generated code.

import os

import uvicorn

from backend import config, settings


def main():
    # Save main PID to environment for shutdown to use.
    # If uvicorn starts new processes we need to kill the main process
    # instead of "self". Sub processes will not run this function.
    # Expect: Environment variables are inherited to child processes.
    os.environ["X_SERV_PID"] = str(os.getpid())

    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG and not config.IS_ZIP_APP,
        reload_dirs="backend",
    )


if __name__ == "__main__":
    main()
