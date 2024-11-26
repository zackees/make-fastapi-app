# make-fastapi-app

```bash
pip install make-fastapi-app
```

Running
```bash
make-fastapi-app
```


FastAPI app creation template

[![Linting](../../actions/workflows/lint.yml/badge.svg)](../../actions/workflows/lint.yml)

[![MacOS_Tests](../../actions/workflows/push_macos.yml/badge.svg)](../../actions/workflows/push_macos.yml)
[![Ubuntu_Tests](../../actions/workflows/push_ubuntu.yml/badge.svg)](../../actions/workflows/push_ubuntu.yml)
[![Win_Tests](../../actions/workflows/push_win.yml/badge.svg)](../../actions/workflows/push_win.yml)


# Instructions

First off, make sure you have python installed and this package `pip install make-fastapi-app`, this will create a new global command `make-fastapi-app` that you will use in the steps below.

  * Create a new python github repo, let's call it "myapp"
  * Clone that "myapp" repo to your local computer
  * `cd` into "myapp`
  * Run `make-fastapi-app` at the project root.
    * Follow the instructions
  * Now `git commit` the files into the repo.
  
Now you should have a fully formed app that is ready to be used at Render.com or DigitalOcean, which will use the Dockerfile install. Everything should be automatic with this option.

## Running locally

You can either run the app locally. See the run scripts at the project root. You'll need to install the project globally with `pip install -e .` or else use a virtual environment with `python make_venv.py` and then using `. ./activate.sh` and then `pip install -e .` and then running the `run_dev.py` which should launch everything. Also there is a VSCode build tool that will do this automatically. It will be something like `Terminal` -> `Run Build Tools` -> `Run Local`

# Windows

This environment requires you to use `git-bash`.

# Linting

Run `./lint.sh` to find linting errors using `pylint`, `flake8` and `mypy`.

# Versions
 
  * 1.0.7: Upgrade setup.py -> pyproject.toml
  * 1.0.6: Command broke due to new python. I fixed it.
  * 1.0.5: Fixes adding +x to sh files
  * 1.0.4: Allows empty github url
  * 1.0.3: Adds post install instructions to the command line.
  * 1.0.2: Remove trailing `.git` and `/` for githurl repo input
  * 1.0.1: Adds +x to all shell scripts
  * 1.0.0: Initial commit
