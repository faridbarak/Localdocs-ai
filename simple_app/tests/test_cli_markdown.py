from typer.testing import CliRunner

from localdocs.cli import app

runner = CliRunner()

def test_markdown_command_outputs_sections(tmp_path):
    file_path = tmp_path / "sample.py"
    file_path.write_text(
        '''"""Module docstring."""

import os

def hello():
    """Say hello."""
    return "hi"

class Greeter:
    """Greeter class."""

    def greet(self):
        """Greet someone."""
        return "hello"
''',
        encoding="utf-8",
    )

    result = runner.invoke(app, ["markdown", str(file_path)], standalone_mode=False)

    assert result.exit_code == 0, result.stdout
    output = result.output
    assert "# " in output
    assert "Module Docstring" in output
    assert "Imports" in output
    assert "Functions" in output
    assert "Classes" in output
    assert "hello" in output
    assert "Greeter" in output
    assert "greet" in output
