import json

from typer.testing import CliRunner

from localdocs.cli import app

runner = CliRunner()

def test_parse_command_outputs_json(tmp_path):
    file_path = tmp_path / "sample.py"
    file_path.write_text(
        """import os

class A:
    pass
""",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["parse", str(file_path)])
    assert result.exit_code == 0, result.stdout
    data = json.loads(result.stdout)
    assert data["file"] == str(file_path)
    assert data["imports"][0]["name"] == "os"
    assert data["classes"][0]["name"] == "A"

def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0, result.stdout
    assert "Usage" in result.stdout

def test_version_command():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0, result.stdout
    assert "LocalDocs AI v1.0.0" in result.stdout

def test_markdown_command(tmp_path):
    file_path = tmp_path / "sample.py"
    file_path.write_text(
        """import os

class A:
    pass
""",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["markdown", str(file_path)])
    assert result.exit_code == 0, result.stdout
    assert "# " in result.stdout
    assert "## Preview" in result.stdout
    assert "import os" in result.stdout



