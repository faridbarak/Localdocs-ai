"""Configuration settings for LocalDocs AI"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "LocalDocs AI"
    app_version: str = "1.0.0"
    debug: bool = False
    
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_default_model: str = "qwen2:0.5b"  # Perfectly aligned with your local model targets
    
    # Fallback aliases to protect parallel modules
    default_model: str = "qwen2:0.5b"
    storage_dir: str = "./data"
    
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "INFO"
    data_dir: str = "./data"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
