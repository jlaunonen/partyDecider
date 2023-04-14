# Party game decider (WIP)

## Requirements

- Python 3.11
  - Python 3.10 might work, but using `build.py` requires `pip install tomlkit` to be run first.
    (3.11 uses built in `tomllib`)
- pip
- NodeJS 18 (or something)


## Installing development

Note: On Windows, commands like `venv/bin/pip` may need to be written like `venv\bin\pip`

1. Create virtual environment: `python -m venv venv`
2. Install backend dependencies: `venv/bin/pip install -r requirements-dev.txt`
3. Install frontend dependencies: `cd frontend` and `npm install`

## Running on development

Optionally, in project root, create and edit file `env` and into it write following:

    DEBUG=1
    HOST=127.0.0.1
    NO_BROWSER=1

Available options can be found from `backend/__init__.py`, on class `Settings`.

In project root, run `venv/bin/python -m backend`

Then open browser to `http://127.0.0.1:8192`, or `http://127.0.0.1:8192/docs` to see generated API access UI.

### Technical

Outside zipapp, backend also automatically starts vite dev server which runs on a separate port.
Because that, the root of backend redirects to the dev server port and adds `port`-parameter containing
the backend server port so that the frontend app can communicate with backend.
As vite is started by backend it is also stopped by it, slowing development restarts a bit.

When the app is run from a zipapp the frontend is compiled and bundled in the zip and so that extra parameter is not needed.

If you want to launch vite dev server by yourself, add `VITE_DEV_CMD=` to `env` file (setting the cmd to an empty string).
Do note, though, that the default Vite port is not same, and you might need to also change `VITE_DEV_PORT` setting to reflect that.


## Building zipapp

In project root, running `venv/bin/python build.py` should create executable `partyDecider.pyz`
