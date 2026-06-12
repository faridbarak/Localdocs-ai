from localdocs.parsers.core import parse_file_content

def test_parse_file_content(tmp_path):
    file_path = tmp_path / "sample.py"
    content = "print('hello world')"
    file_path.write_text(content, encoding="utf-8")

    result = parse_file_content(file_path, language="python")

    assert result["file"] == str(file_path)
    assert result["language"] == "python"
    assert result["length"] == len(content)
    assert result["preview"] == content[:200]
