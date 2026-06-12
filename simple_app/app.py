from fastapi import FastAPI
from localdocs.api.routes import router as api_router

app = FastAPI(
    title="LocalDocs AI",
    version="1.0.0",
    description="Privacy-first local documentation generator",
)

app.include_router(api_router)

@app.get("/")
def read_root():
    return {
        "message": "LocalDocs AI is running!",
        "docs": "/docs",
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
