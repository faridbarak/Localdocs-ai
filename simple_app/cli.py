from pathlib import Path
import json
import typer

app = typer.Typer(help="LocalDocs AI command-line interface")

def parse_file_content(file_path: str, language: str):
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    return {
        "file": file_path,
        "language": language,
        "length": len(code),
        "preview": code[:200],
    }

@app.command()
def parse(
    file: Path = typer.Argument(..., exists=True),
    language: str = typer.Option("python", help="Language name"),
):
    result = parse_file_content(str(file), language)
    typer.echo(json.dumps(result, indent=2))

@app.command()
def markdown(
    file: Path = typer.Argument(..., exists=True),
    language: str = typer.Option("python", help="Language name"),
):
    result = parse_file_content(str(file), language)
    lines = []
    lines.append(f"# {result['file']}")
    lines.append("")
    lines.append(f"- Language: {result['language']}")
    lines.append(f"- Length: {result['length']}")
    lines.append("")
    lines.append("## Preview")
    lines.append("")
    lines.append("```text")
    lines.append(result["preview"])
    lines.append("```")
    typer.echo("
".join(lines))

@app.command()
def check():
    typer.echo("LocalDocs AI setup looks good.")

@app.command()
def version():
    typer.echo("LocalDocs AI v1.0.0")

if __name__ == "__main__":
    app()
