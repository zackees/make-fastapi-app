"""
Unit test file.
"""

import atexit
import os
import shutil
import subprocess
import unittest

from createfastapiapp.createapp import do_create_fastapi_app

HERE = os.path.abspath(os.path.dirname(__file__))

OUTDIR = os.path.normpath(os.path.join(HERE, "..", ".MyAppTest"))
OUTDIR2 = os.path.normpath(os.path.join(HERE, "..", ".MyAppTest2"))

atexit.register(lambda: shutil.rmtree(OUTDIR, ignore_errors=True))
atexit.register(lambda: shutil.rmtree(OUTDIR2, ignore_errors=True))


def read_utf8(path: str) -> str:
    """Read a file as UTF-8."""
    with open(path, encoding="utf-8", mode="r") as file:
        return file.read()


class CreateAppTester(unittest.TestCase):
    """Main tester class."""

    def test_create(self) -> None:
        """Test command line interface (CLI)."""

        if os.path.exists(OUTDIR):
            shutil.rmtree(OUTDIR)
        do_create_fastapi_app(
            app_name="myapp",
            app_description="MyAppTest description",
            app_author="Firstname Lastname",
            app_keywords="myapp test",
            version="1.2.3",
            github_url="https://github.com/author/myapp",
            cwd=OUTDIR,
        )
        self.assertTrue(os.path.exists(OUTDIR))
        self.assertTrue(os.path.exists(os.path.join(OUTDIR, "pyproject.toml")))
        setup_py_lines: list[str] = read_utf8(
            os.path.join(OUTDIR, "pyproject.toml")
        ).splitlines()
        self.assertIn('keywords = ["myapp test"]', setup_py_lines)
        self.assertTrue(os.path.exists(os.path.join(OUTDIR, "src", "myapp")))
        # self.assertTrue(os.path.exists(os.path.join(OUTDIR, "src", "myapp", "cli.py")))
        self.assertTrue(
            os.path.exists(os.path.join(OUTDIR, "src", "myapp", "__init__.py"))
        )
        self.assertTrue(os.path.exists(os.path.join(OUTDIR, "tests")))
        # self.assertTrue(os.path.exists(os.path.join(OUTDIR, "tests", "test_cli.py")))
        self.assertTrue(os.path.exists(os.path.join(OUTDIR, "tox.ini")))
        self.assertTrue(os.path.exists(os.path.join(OUTDIR, "run_dev.py")))
        # Check that each *.py file does not have template_fastapi_project in it.
        for root, _, files in os.walk(OUTDIR):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    file_content = read_utf8(file_path)
                    lines = file_content.splitlines()
                    for line in lines:
                        if "template_fastapi_project" in line:
                            self.assertTrue(  # pylint: disable=redundant-unittest-assert
                                False,
                                f"Found template_fastapi_project in {file_path}: {line}",
                            )
        os.chdir(OUTDIR)
        subprocess.check_call("pip install -e .", shell=True)
        subprocess.check_call("pip install -r requirements.testing.txt", shell=True)
        # subprocess.check_call("python tests/test_cli.py", shell=True)
        subprocess.check_call("pylint src tests", shell=True)
        subprocess.check_call("flake8 src tests", shell=True)
        subprocess.check_call("mypy src tests", shell=True)

    def test_create_no_github(self) -> None:
        """Test command line interface (CLI)."""

        if os.path.exists(OUTDIR2):
            shutil.rmtree(OUTDIR2)
        do_create_fastapi_app(
            app_name="myapp",
            app_description="MyAppTest description",
            app_author="Firstname Lastname",
            app_keywords="myapp test",
            version="1.2.3",
            github_url="",
            cwd=OUTDIR2,
        )
        self.assertTrue(os.path.exists(OUTDIR2))
        self.assertTrue(os.path.exists(os.path.join(OUTDIR2, "pyproject.toml")))
        setup_py_lines: list[str] = read_utf8(
            os.path.join(OUTDIR2, "pyproject.toml")
        ).splitlines()
        self.assertIn('keywords = ["myapp test"]', setup_py_lines)
        self.assertTrue(os.path.exists(os.path.join(OUTDIR2, "src", "myapp")))
        # self.assertTrue(os.path.exists(os.path.join(OUTDIR2, "src", "myapp", "cli.py")))
        self.assertTrue(
            os.path.exists(os.path.join(OUTDIR2, "src", "myapp", "__init__.py"))
        )
        self.assertTrue(os.path.exists(os.path.join(OUTDIR2, "tests")))
        # self.assertTrue(os.path.exists(os.path.join(OUTDIR2, "tests", "test_cli.py")))
        self.assertTrue(os.path.exists(os.path.join(OUTDIR2, "tox.ini")))
        self.assertTrue(os.path.exists(os.path.join(OUTDIR2, "run_dev.py")))
        # Check that each *.py file does not have template_fastapi_project in it.
        for root, _, files in os.walk(OUTDIR2):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    file_content = read_utf8(file_path)
                    lines = file_content.splitlines()
                    for line in lines:
                        if "template_fastapi_project" in line:
                            self.assertTrue(  # pylint: disable=redundant-unittest-assert
                                False,
                                f"Found template_fastapi_project in {file_path}: {line}",
                            )
        os.chdir(OUTDIR2)
        subprocess.check_call("pip install -e .", shell=True)
        subprocess.check_call("pip install -r requirements.testing.txt", shell=True)
        # subprocess.check_call("python tests/test_cli.py", shell=True)
        subprocess.check_call("pylint src tests", shell=True)
        subprocess.check_call("flake8 src tests", shell=True)
        subprocess.check_call("mypy src tests", shell=True)


if __name__ == "__main__":
    unittest.main()
