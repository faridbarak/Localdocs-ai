from localdocs.parsers.core import parse_file_content

def test_parse_file_content_extracts_functions_and_classes(tmp_path):
    file_path = tmp_path / "sample.py"
    file_path.write_text(
        '''"""Module docstring."""

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

    result = parse_file_content(file_path, language="python")

    assert result["module_docstring"] == "Module docstring."
    assert len(result["functions"]) == 1
    assert result["functions"][0]["name"] == "hello"
    assert result["functions"][0]["docstring"] == "Say hello."
    assert len(result["classes"]) == 1
    assert result["classes"][0]["name"] == "Greeter"
    assert result["classes"][0]["docstring"] == "Greeter class."
    assert len(result["classes"][0]["methods"]) == 1
    assert result["classes"][0]["methods"][0]["name"] == "greet"
    assert result["classes"][0]["methods"][0]["docstring"] == "Greet someone."
