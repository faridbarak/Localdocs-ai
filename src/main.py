from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="LocalDocs AI", version="1.0.0")

# Add CORS immediately after creating app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root(): 
    return {"message": "LocalDocs AI is running!", "docs": "/docs"}

@app.get("/health")
def health(): 
    return {"status": "healthy"}
