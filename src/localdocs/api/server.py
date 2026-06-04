"""LocalDocs Dynamic Technical Web Template Server Engine with Multi-File Workspace Support"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import markdown

app = FastAPI(title="LocalDocs AI Studio")

# 📂 ROBUST TEMPLATE LOOKUP FRAMEWORK
# This checks both relative and deep module paths automatically to eliminate 500 errors
CURRENT_DIR = Path(__file__).resolve().parent
if (CURRENT_DIR.parent / "templates").exists():
    TEMPLATE_DIR = CURRENT_DIR.parent / "templates"
else:
    TEMPLATE_DIR = Path(".") / "src" / "localdocs" / "templates"

templates = Jinja2Templates(directory=str(TEMPLATE_DIR.resolve()))

TARGET_FILE = "parser_docs.md"
MODEL_USED = "qwen2:0.5b"

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard(request: Request, file: str = None):
    """Scan root directory for Markdown documents, build dynamic sidebar menus, and stream selected views"""
    # 1. Look for all markdown files available in the root workspace directory
    workspace_path = Path(".")
    md_files = [f.name for f in workspace_path.glob("*.md")]
    
    # If no markdown files are found in root, look in workspace tracking targets
    if not md_files:
        md_files = ["parser_docs.md", "secure_report.md"]
    else:
        md_files.sort()
    
    # 2. Determine which file the user requested to view (fallback to default flag)
    active_file = file or TARGET_FILE
    
    # 3. Read and parse the selected document target safely
    doc_path = workspace_path / active_file
    if doc_path.exists():
        markdown_text = doc_path.read_text(encoding="utf-8")
    else:
        markdown_text = f"# File Not Found\n\nThe documentation target content file `{active_file}` cannot be resolved on local disk storage arrays."

    # Render raw text stream tokens securely into structured HTML frames
    html_content = markdown.markdown(markdown_text, extensions=['fenced_code', 'codehilite'])

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "Project Documentation Studio",
            "model": MODEL_USED,
            "html_content": html_content,
            "workspace_files": md_files,
            "active_file": active_file
        }
    )
