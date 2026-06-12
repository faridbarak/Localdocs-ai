from pathlib import Path
import ast

def _extract_imports(tree):
    imports = []

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(
                    {
                        "type": "import",
                        "name": alias.name,
                        "alias": alias.asname,
                    }
                )
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imports.append(
                    {
                        "type": "from",
                        "module": node.module,
                        "name": alias.name,
                        "alias": alias.asname,
                        "level": node.level,
                    }
                )

    return imports

def parse_file_content(file_path: str | Path, language: str = "python"):
    path = Path(file_path)
    text = path.read_text(encoding="utf-8")

    result = {
        "file": str(path),
        "language": language,
        "length": len(text),
        "preview": text[:200],
    }

    if language.lower() != "python":
        return result

    tree = ast.parse(text, filename=str(path))

    functions = []
    classes = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            functions.append(
                {
                    "name": node.name,
                    "docstring": ast.get_docstring(node),
                }
            )
        elif isinstance(node, ast.ClassDef):
            methods = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    methods.append(
                        {
                            "name": item.name,
                            "docstring": ast.get_docstring(item),
                        }
                    )
            classes.append(
                {
                    "name": node.name,
                    "docstring": ast.get_docstring(node),
                    "methods": methods,
                }
            )

    result["module_docstring"] = ast.get_docstring(tree)
    result["imports"] = _extract_imports(tree)
    result["functions"] = functions
    result["classes"] = classes
    return result
