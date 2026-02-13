"""Configuration settings for Power Assist application"""
from pydantic import BaseModel
from typing import List


class Settings(BaseModel):
    """Application settings"""
    
    # Application
    app_name: str = "Power Assist"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api/v1"
    
    # File Upload
    max_upload_size: int = 100 * 1024 * 1024  # 100 MB
    allowed_extensions: List[str] = [
        ".pdf", ".pptx", ".ppt", ".docx", ".doc", 
        ".eml", ".msg", ".md", ".txt"
    ]
    upload_dir: str = "uploads"
    processed_dir: str = "processed"
    
    # Agno Framework
    agno_model: str = "gpt-4"
    agno_temperature: float = 0.7
    agno_max_tokens: int = 2000
    
    # Document Processing
    enable_ocr: bool = True
    extract_images: bool = True
    preserve_layout: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
