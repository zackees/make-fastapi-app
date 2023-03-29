"""Create a Python application."""


# pylint: disable=all
# flake8: noqa


import os
import shutil
import tempfile
from typing import Optional

TEMPLATE_PROJECT_URL = "https://github.com/zackees/template-fastapi-project"
DIR_MATCH = "fastapi_template_project"


def check_name(app_name: str) -> None:
    """Check the name of the application."""
    if not app_name.isidentifier():
        raise ValueError(
            "The name of the application is not a valid Python identifier."
        )


def check_semantic_version(version: str) -> None:
    """Check the version of the application."""
    version_list = version.split(".")
    for v in version_list:
        if not v.isnumeric():
            raise ValueError(
                "The version of the application is not a valid semantic version."
            )


def remove_double_blank_lines(lines: list) -> list:
    """Remove double blank lines."""
    new_lines = []
    last_line_blank = False
    for i, line in enumerate(lines):
        if line == "":
            if last_line_blank:
                continue
            new_lines.append(line)
            last_line_blank = True
        else:
            new_lines.append(line)
            last_line_blank = False
    return new_lines


def read_lines(path: str) -> list[str]:
    with open(path, encoding="utf-8", mode="r") as file:
        out = file.read().splitlines()
    return out


def write_lines(path: str, lines: list[str]) -> None:
    out = "\n".join(lines)
    # Add trailing newline if it is missing
    out = out.strip()
    if out != "":
        out += "\n"
    with open(path, encoding="utf-8", mode="w") as file:
        file.write(out)


def replace_in_file(path: str, old: str, new: str) -> None:
    lines = read_lines(path)
    for i, line in enumerate(lines):
        if old in line:
            lines[i] = line.replace(old, new)
    write_lines(path, lines)


def do_create_fastapi_app(
    app_description: str,
    app_author: str,
    app_keywords: str,  # Example "keyword1, keyword2, keyword3"
    version: str,
    github_url: str,
    cwd: Optional[str] = None,
) -> None:
    # Create the app directory
    # get app name from the github url
    cwd = cwd or os.getcwd()
    os.makedirs(cwd, exist_ok=True)
    app_name = github_url.split("/")[-1]
    app_name_underscore = app_name.replace("-", "_")
    with tempfile.TemporaryDirectory() as tmpdir:
        # download https://github.com/zackees/template-python-cmd
        # extract to tmpdir
        # copy files from tmpdir to app_name
        os.system(f"git clone {TEMPLATE_PROJECT_URL} {tmpdir}")
        # change every directory name of from template-python-cmd to app_name
        found = False
        for root, dirs, files in os.walk(tmpdir):
            for d in dirs:
                if d == DIR_MATCH:
                    src = os.path.join(root, d)
                    dst = os.path.join(root, app_name_underscore)
                    shutil.move(src, dst)
                    found = True
        assert found, f"Directory {DIR_MATCH} not found."
        pyproject = os.path.join(tmpdir, "pyproject.toml")
        with open(pyproject, encoding="utf-8", mode="r") as pyproject_file:
            pyproject_lines = pyproject_file.read().splitlines()
        for i, line in enumerate(pyproject_lines):
            if line.startswith("name ="):
                pyproject_lines[i] = f'name = "{app_name}"'
            if line.startswith("description ="):
                pyproject_lines[i] = f'description = "{app_description}"'
            if line.startswith("version ="):
                pyproject_lines[i] = f'version = "{version}"'
            if line.startswith("authors ="):
                pyproject_lines[i] = f'authors = ["{app_author}"]'
        ########
        # Transform pyproject file with the new information
        pyproject_lines = remove_double_blank_lines(pyproject_lines)
        with open(pyproject, encoding="utf-8", mode="w") as pyproject_file:
            pyproject_file.write("\n".join(pyproject_lines))
        ########
        # Transform setup.py with the new information
        setup = os.path.join(tmpdir, "setup.py")
        with open(setup, encoding="utf-8", mode="r") as setup_file:
            setup_lines = setup_file.read().splitlines()
        for i, line in enumerate(setup_lines):
            if line.startswith("URL ="):
                setup_lines[i] = f'URL = "{github_url}"'
            # maintainer
            if line.startswith("maintainer="):
                setup_lines[i] = f'maintainer="{app_author}"'
            if line.startswith("KEYWORDS ="):
                setup_lines[i] = f'KEYWORDS = "{app_keywords}"'
        with open(setup, encoding="utf-8", mode="w") as setup_file:
            setup_file.write("\n".join(setup_lines))
        ########
        # Transform src python files with new imports
        app_dir = os.path.join(tmpdir, "src", app_name_underscore)
        pyfiles = [f for f in os.listdir(app_dir) if f.endswith(".py")]
        for filename in pyfiles:
            file = os.path.join(app_dir, filename)
            assert os.path.exists(file), f"File {file} not found."
            replace_in_file(file, "fastapi_template_project", app_name_underscore)
        # TODO: template_fastapi_project -> fastapi_template_project
        replace_in_file(
            os.path.join(app_dir, "app.py"),
            "template_fastapi_project",
            app_name_underscore,
        )
        replace_in_file(
            os.path.join(app_dir, "app.py"),
            "FastAPI Template Project",
            app_name_underscore,
        )
        ########
        # Transform run_dev.py with new imports
        replace_in_file(
            os.path.join(tmpdir, "run_dev.py"),
            "fastapi_template_project",
            app_name_underscore,
        )
        ########
        # Transform run_dev.py with new imports
        replace_in_file(
            os.path.join(tmpdir, "entry_point.sh"),
            "fastapi_template_project",
            app_name_underscore,
        )
        replace_in_file(
            os.path.join(tmpdir, "README.md"),
            "fastapi_template_project",
            app_name_underscore,
        )
        replace_in_file(
            os.path.join(tmpdir, "README.md"),
            "Example FastAPI Project with Docker, ready for Render.com / DigitalOcean",
            f"{app_name_underscore} with Docker, ready for Render.com / DigitalOcean",
        )
        ########
        # Transform src python test files with new imports
        test_dir = os.path.join(tmpdir, "tests")
        pyfiles = [f for f in os.listdir(test_dir) if f.endswith(".py")]
        for filename in pyfiles:
            file = os.path.join(test_dir, filename)
            assert os.path.exists(file), f"File {file} not found."
            replace_in_file(file, "fastapi_template_project", app_name_underscore)
        ########
        # Copy template files from this temporary directory to the app directory
        files = os.listdir(tmpdir)
        files = [os.path.join(tmpdir, f) for f in files if f != ".git"]
        for f in files:
            if os.path.isdir(f):
                shutil.copytree(f, os.path.join(cwd, os.path.basename(f)))
            else:
                shutil.copy(f, cwd)
        # Add +x to all *.sh files
        for root, _, files in os.walk(tmpdir):
            for f in files:
                if f.endswith(".sh"):
                    path = os.path.join(root, f)
                    # git +x permission
                    os.system(f'git update-index --chmod=+x "{path}"')


def create_python_app() -> None:
    """Create a Python application."""
    # check if git exists
    if not shutil.which("git"):
        raise RuntimeError("Git is not installed.")
    app_name = input("Python app name: ")
    check_name(app_name)
    app_description = input("Python app description: ")
    app_keywords = input("Python app keywords: ")
    app_author = input("Python app author: ")
    github_url = input("GitHub URL: ")
    if github_url.endswith("/"):
        github_url = github_url[:-1]
    if github_url.endswith(".git"):
        github_url = github_url[:-4]
    version = input("Version [1.0.0]: ")
    if not version:
        version = "1.0.0"
    check_semantic_version(version)
    do_create_fastapi_app(
        app_description=app_description,
        app_author=app_author,
        app_keywords=app_keywords,
        version=version,
        github_url=github_url,
    )


if __name__ == "__main__":
    create_python_app()
