"""Markdown document processor"""
import os
from typing import Dict, Any
from ..models.document import DocumentContent, DocumentType
from .base import BaseProcessor


class MarkdownProcessor(BaseProcessor):
    """Processor for Markdown documents"""
    
    @property
    def supported_type(self) -> DocumentType:
        return DocumentType.MARKDOWN
    
    async def validate(self, file_path: str) -> bool:
        """Validate Markdown file"""
        if not os.path.exists(file_path):
            return False
        return file_path.lower().endswith(('.md', '.markdown'))
    
    async def process(self, file_path: str) -> DocumentContent:
        """
        Process Markdown document
        
        Args:
            file_path: Path to Markdown file
            
        Returns:
            DocumentContent with extracted information
        """
        try:
            # Read the markdown content
            with open(file_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            metadata: Dict[str, Any] = {
                "source": file_path,
                "processor": "markdown",
                "format": "markdown",
                "char_count": len(md_content),
            }
            
            # Try to convert to HTML if markdown module is available
            html = None
            try:
                import markdown
                html = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
            except ImportError:
                pass  # HTML conversion is optional
            
            structure = {"html": html} if html else None
            
            return DocumentContent(
                text=md_content,
                metadata=metadata,
                structure=structure,
            )
            
        except Exception as e:
            raise Exception(f"Markdown processing failed: {str(e)}")
