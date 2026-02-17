"""PDF document processor using Dockling"""
from typing import Dict, Any, List
import os
from ..models.document import DocumentContent, DocumentType
from .base import BaseProcessor


class PDFProcessor(BaseProcessor):
    """Processor for PDF documents using Dockling"""
    
    @property
    def supported_type(self) -> DocumentType:
        return DocumentType.PDF
    
    async def validate(self, file_path: str) -> bool:
        """Validate PDF file"""
        if not os.path.exists(file_path):
            return False
        return file_path.lower().endswith('.pdf')
    
    async def process(self, file_path: str) -> DocumentContent:
        """
        Process PDF document using Dockling
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            DocumentContent with extracted information
        """
        try:
            # Import Dockling for PDF processing
            from docling.document_converter import DocumentConverter
            
            # Initialize converter
            converter = DocumentConverter()
            
            # Convert document
            result = converter.convert(file_path)
            
            # Extract text content
            text_content = result.document.export_to_markdown()
            
            # Extract metadata
            metadata: Dict[str, Any] = {
                "num_pages": len(result.document.pages) if hasattr(result.document, 'pages') else 0,
                "source": file_path,
                "processor": "dockling",
            }
            
            # Extract images if available
            images: List[str] = []
            if hasattr(result.document, 'pictures'):
                images = [pic.uri for pic in result.document.pictures if hasattr(pic, 'uri')]
            
            # Extract tables if available
            tables: List[Dict[str, Any]] = []
            if hasattr(result.document, 'tables'):
                for table in result.document.tables:
                    tables.append({
                        "data": table.export_to_dataframe().to_dict() if hasattr(table, 'export_to_dataframe') else {},
                        "position": getattr(table, 'position', None)
                    })
            
            return DocumentContent(
                text=text_content,
                metadata=metadata,
                images=images,
                tables=tables,
            )
            
        except Exception as e:
            # Fallback to basic PDF text extraction
            return await self._fallback_process(file_path, str(e))
    
    async def _fallback_process(self, file_path: str, error: str) -> DocumentContent:
        """Fallback processing using PyPDF2"""
        try:
            from PyPDF2 import PdfReader
            
            reader = PdfReader(file_path)
            text_parts = []
            
            for page in reader.pages:
                text_parts.append(page.extract_text())
            
            return DocumentContent(
                text="\n\n".join(text_parts),
                metadata={
                    "num_pages": len(reader.pages),
                    "source": file_path,
                    "processor": "pypdf2",
                    "dockling_error": error,
                },
            )
        except Exception as fallback_error:
            raise Exception(f"PDF processing failed: {error}. Fallback also failed: {fallback_error}")
