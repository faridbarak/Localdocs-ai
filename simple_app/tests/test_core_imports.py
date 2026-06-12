from localdocs.parsers.core import parse_file_content

def test_parse_file_content_extracts_imports(tmp_path):
    file_path = tmp_path / "sample.py"
    file_path.write_text(
        """import os
import sys as system
from pathlib import Path
from collections import defaultdict as dd
""",
        encoding="utf-8",
    )

    result = parse_file_content(file_path, language="python")

    assert len(result["imports"]) == 4
    assert result["imports"][0]["type"] == "import"
    assert result["imports"][0]["name"] == "os"

    assert result["imports"][1]["type"] == "import"
    assert result["imports"][1]["name"] == "sys"
    assert result["imports"][1]["alias"] == "system"

    assert result["imports"][2]["type"] == "from"
    assert result["imports"][2]["module"] == "pathlib"
    assert result["imports"][2]["name"] == "Path"

    assert result["imports"][3]["type"] == "from"
    assert result["imports"][3]["module"] == "collections"
    assert result["imports"][3]["name"] == "defaultdict"
    assert result["imports"][3]["alias"] == "dd"
