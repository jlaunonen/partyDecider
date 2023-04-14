# Party game decider (WIP)

## Requirements

- Python 3.11
  - Python 3.10 might work, but using `build.py` requires `pip install tomlkit` to be run first.
    (3.11 uses built in `tomllib`)
- pip


## Installing development

Note: On Windows, commands like `venv/bin/pip` may need to be written like `venv\bin\pip`

1. Create virtual environment: `python -m venv venv`
2. Install dependencies: `venv/bin/pip install -r requirements-dev.txt`


## Running on development

Optionally, in project root, create and edit file `env` and into it write following:

    DEBUG=1
    HOST=127.0.0.1
    NO_BROWSER=1

Available options can be found from `backend/__init__.py`, on class `Settings`.

In project root, run `venv/bin/python -m backend`

Then open browser to `http://127.0.0.1:8192`, or `http://127.0.0.1:8192/docs` to see generated API access UI.


## Building zipapp

In project root, running `venv/bin/python build.py` should create executable `partyDecider.pyz`
