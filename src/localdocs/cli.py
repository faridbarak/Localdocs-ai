"""Command-line interface for LocalDocs AI Systems"""
import typer
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(name="localdocs")
console = Console()


@app.command()
def version():
    """Show version"""
    console.print(Panel("[bold green]LocalDocs AI v1.0.0[/bold green]"))


@app.command()
def init():
    """Initialize .env file"""
    env_file = Path(".env")
    if not env_file.exists():
        with open(".env.example", "r") as src:
            with open(".env", "w") as dst:
                dst.write(src.read())
        console.print(Panel("[green]✓ Created .env file[/green]"))
        console.print("Edit .env with your settings")
    else:
        console.print(Panel("[yellow]⚠ .env already exists[/yellow]"))


@app.command()
def check():
    """Check Ollama connection"""
    from localdocs.llm.ollama_client import OllamaClient
    
    client = OllamaClient()
    
    if client.check_connection():
        console.print(Panel("[bold green]✓ Ollama is running[/bold green]"))
        models = client.list_models()
        if models:
            console.print(f"\n[bold]Available models:[/bold]")
            for model in models:
                console.print(f"  • {model}")
    else:
        console.print(Panel("[bold red]✗ Ollama not running[/bold red]"))
        console.print("\nInstall Ollama:")
        console.print("  curl -fsSL https://ollama.com/install.sh | sh")


def get_parser_for_language(language: str, code: str):
    """Get appropriate parser for language"""
    from localdocs.parsers.python_parser import PythonParser
    from localdocs.parsers.javascript_parser import JavaScriptParser
    
    language = language.lower()
    
    if language in ["python", "py"]:
        return PythonParser(code)
    elif language in ["javascript", "js", "typescript", "ts"]:
        return JavaScriptParser(code)
    else:
        console.print(f"[yellow]⚠ Unknown language '{language}', using Python parser[/yellow]")
        return PythonParser(code)


def get_file_extensions(language: str) -> list:
    """Get file extensions for language"""
    language = language.lower()
    
    if language in ["python", "py"]:
        return ["*.py"]
    elif language in ["javascript", "js"]:
        return ["*.js"]
    elif language in ["typescript", "ts"]:
        return ["*.ts", "*.tsx"]
    elif language == "go":
        return ["*.go"]
    else:
        return ["*.py", "*.js", "*.ts"]


@app.command()
def generate(
    path: str = typer.Argument(..., help="Path to code folder"),
    output: str = typer.Option("docs.md", "--output", "-o", help="Output file"),
    model: str = typer.Option(None, "--model", "-m", help="LLM model"),
    language: str = typer.Option("auto", "--language", "-l", help="Language (auto/python/javascript/go)")
):
    """Generate documentation for code folder"""
    from localdocs.llm.ollama_client import OllamaClient
    from localdocs.generators.markdown_generator import MarkdownGenerator
    
    console.print(Panel(f"[bold]Scanning folder:[/bold] {path}"))
    
    client = OllamaClient()
    if not client.check_connection():
        console.print("[red]✗ Ollama not running[/red]")
        return
    
    if language.lower() == "auto":
        path_obj = Path(path)
        py_files = len(list(path_obj.rglob("*.py")))
        js_files = len(list(path_obj.rglob("*.js")))
        ts_files = len(list(path_obj.rglob("*.ts")))
        
        if py_files >= js_files and py_files >= ts_files:
            language = "python"
            console.print(f"[green]✓ Auto-detected: Python ({py_files} files)[/green]")
        elif js_files >= ts_files:
            language = "javascript"
            console.print(f"[green]✓ Auto-detected: JavaScript ({js_files} files)[/green]")
        else:
            language = "typescript"
            console.print(f"[green]✓ Auto-detected: TypeScript ({ts_files} files)[/green]")
    else:
        console.print(f"[blue]Using language:[/blue] {language}")
    
    code_content = ""
    file_count = 0
    file_extensions = get_file_extensions(language)
    
    for ext in file_extensions:
        for file in Path(path).rglob(ext):
            try:
                code_content += f"\n\n# File: {file}\n"
                code_content += file.read_text(encoding="utf-8")
                file_count += 1
            except Exception as e:
                console.print(f"[yellow]⚠ Could not read {file}: {e}[/yellow]")
    
    if file_count == 0:
        console.print(f"[red]✗ No files found with extensions: {file_extensions}[/red]")
        return
    
    console.print(f"[green]✓ Found and compiled {file_count} script units[/green]")
    
    parser = get_parser_for_language(language, code_content)
    elements = parser.parse()
    console.print(f"[green]✓ Successfully structured {len(elements)} structural multi-language parser elements[/green]")
    
    if len(elements) == 0:
        console.print("[yellow]⚠ No code elements found. Check your code syntax.[/yellow]")
    
    console.print("[bold]Passing data tokens to secure, localized AI model instance framework...[/bold]")
    code_limit = 15000 if "0.5b" in (model or "").lower() else 50000
    ai_docs = client.generate_docs(code_content[:code_limit], model, language)
    
    markdown = MarkdownGenerator.generate(elements, Path(path).name)
    markdown += "\n\n## AI Documentation Block Generation\n\n" + ai_docs
    
    Path(output).write_text(markdown, encoding="utf-8")
    console.print(Panel(f"[bold green]✓ Complete multi-language project manual safely built and stored at: {output}[/bold green]"))


@app.command()
def serve(
    file: str = typer.Option("docs.md", "--file", "-f", help="Target documentation file path to render"),
    port: int = typer.Option(8080, "--port", "-p", help="Port network socket target binding configuration")
):
    """Launch the LocalDocs Live Web Studio Engine dashboard server platform"""
    import uvicorn
    import os
    
    console.print(Panel("🚀 [bold green]Initializing LocalDocs Live Web Studio Engine...[/bold green]"))
    console.print(f"Reading documentation source map: [bold cyan]{file}[/bold cyan]")
    console.print(f"Local Host Address URL target: [bold link]http://127.0.0.1:{port}[/bold link]\n")
    
    os.environ["LOCALDOCS_FILE"] = file
    uvicorn.run("localdocs.api.server:app", host="127.0.0.1", port=port, log_level="info", reload=False)


if __name__ == "__main__":
    app()
