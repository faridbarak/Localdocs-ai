from pathlib import Path

def parse_file_content(file_path: str, language: str = "python") -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    return {
        "file": file_path,
        "language": language,
        "length": len(code),
        "preview": code[:200],
    }
