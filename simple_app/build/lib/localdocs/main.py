import json
import os
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from localdocs.parsers.core import parse_file_content

app = FastAPI(title="LocalDocs AI", version="1.0.0")

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "cases.json")


class Case(BaseModel):
    id: int
    title: str
    status: str = "open"


def load_cases_from_file() -> List[Case]:
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Case(**item) for item in data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_cases_to_file(cases: List[Case]) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([case.model_dump() for case in cases], f, indent=2)


cases: List[Case] = load_cases_from_file()


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.get("/parse")
def parse_source(file_path: str, language: str = "python"):
    path = file_path

    try:
        return {"success": True, "result": parse_file_content(path, language=language)}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/cases")
def get_cases():
    return cases
