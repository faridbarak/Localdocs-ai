from pathlib import Path
import json

import typer

from localdocs.parsers.core import parse_file_content

app = typer.Typer(help="LocalDocs AI command-line interface")


@app.command()
def parse(
    file: Path = typer.Argument(..., exists=True, readable=True),
    language: str = typer.Option("python", help="File language"),
):
    result = parse_file_content(file, language=language)
    typer.echo(json.dumps(result, indent=2, ensure_ascii=False))


@app.command()
def markdown(
    file: Path = typer.Argument(..., exists=True, readable=True),
    language: str = typer.Option("python", help="File language"),
):
    result = parse_file_content(file, language=language)
    lines = [f"# {result['file']}", ""]

    if result.get("module_docstring"):
        lines.extend(["## Module Docstring", result["module_docstring"], ""])

    if result.get("imports"):
        lines.append("## Imports")
        for item in result["imports"]:
            if item["type"] == "import":
                line = item["name"]
                if item["alias"]:
                    line += f" as {item['alias']}"
            else:
                line = f"from {item['module']} import {item['name']}"
                if item["alias"]:
                    line += f" as {item['alias']}"
            lines.append(f"- {line}")
        lines.append("")

    if result.get("functions"):
        lines.append("## Functions")
        for fn in result["functions"]:
            lines.append(f"- **{fn['name']}**")
            if fn["docstring"]:
                lines.append(f"  - {fn['docstring']}")
        lines.append("")

    if result.get("classes"):
        lines.append("## Classes")
        for cls in result["classes"]:
            lines.append(f"- **{cls['name']}**")
            if cls["docstring"]:
                lines.append(f"  - {cls['docstring']}")
            for method in cls["methods"]:
                lines.append(f"  - `{method['name']}`")
                if method["docstring"]:
                    lines.append(f"    - {method['docstring']}")
        lines.append("")

    output = ""
    for line in lines:
        output += line + chr(10)
    typer.echo(output)


if __name__ == "__main__":
    app()
