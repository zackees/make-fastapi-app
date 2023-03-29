"""
Unit test file.
"""
import os
import shutil
import subprocess
import unittest

from createfastapiapp.createapp import do_create_fastapi_app

HERE = os.path.abspath(os.path.dirname(__file__))


def read_utf8(path: str) -> str:
    """Read a file as UTF-8."""
    with open(path, encoding="utf-8", mode="r") as file:
        return file.read()


class CreateAppTester(unittest.TestCase):
    """Main tester class."""

    def test_imports(self) -> None:
        """Test command line interface (CLI)."""

        outdir = os.path.normpath(os.path.join(HERE, "..", ".MyAppTest"))
        if os.path.exists(outdir):
            shutil.rmtree(outdir)
        do_create_fastapi_app(
            app_description="MyAppTest description",
            app_author="Firstname Lastname",
            app_keywords="myapp test",
            version="1.2.3",
            github_url="https://github.com/author/myapp",
            cwd=outdir,
        )
        self.assertTrue(os.path.exists(outdir))
        self.assertTrue(os.path.exists(os.path.join(outdir, "pyproject.toml")))
        self.assertTrue(os.path.exists(os.path.join(outdir, "setup.py")))
        setup_py_lines: list[str] = read_utf8(
            os.path.join(outdir, "setup.py")
        ).splitlines()
        self.assertIn('KEYWORDS = "myapp test"', setup_py_lines)
        self.assertTrue(os.path.exists(os.path.join(outdir, "src", "myapp")))
        # self.assertTrue(os.path.exists(os.path.join(outdir, "src", "myapp", "cli.py")))
        self.assertTrue(
            os.path.exists(os.path.join(outdir, "src", "myapp", "__init__.py"))
        )
        self.assertTrue(os.path.exists(os.path.join(outdir, "tests")))
        # self.assertTrue(os.path.exists(os.path.join(outdir, "tests", "test_cli.py")))
        self.assertTrue(os.path.exists(os.path.join(outdir, "tox.ini")))
        self.assertTrue(os.path.exists(os.path.join(outdir, "run_dev.py")))
        # Check that each *.py file does not have template_fastapi_project in it.
        for root, _, files in os.walk(outdir):
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
        os.chdir(outdir)
        subprocess.check_call("pip install -e .", shell=True)
        subprocess.check_call("pip install -r requirements.testing.txt", shell=True)
        # subprocess.check_call("python tests/test_cli.py", shell=True)
        subprocess.check_call("pylint src tests", shell=True)
        subprocess.check_call("flake8 src tests", shell=True)
        subprocess.check_call("mypy src tests", shell=True)


if __name__ == "__main__":
    unittest.main()
