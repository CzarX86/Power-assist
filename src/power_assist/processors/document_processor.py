"""Main document processor coordinator"""
from typing import Dict, Type, Optional
import os
import uuid
from datetime import datetime

from ..models.document import (
    Document,
    DocumentMetadata,
    DocumentContent,
    DocumentType,
    ProcessingStatus,
)
from ..config import settings
from .base import BaseProcessor
from .pdf_processor import PDFProcessor
from .powerpoint_processor import PowerPointProcessor
from .word_processor import WordProcessor
from .markdown_processor import MarkdownProcessor
from .email_processor import EmailProcessor


class DocumentProcessor:
    """Main document processor that coordinates all document type processors"""
    
    def __init__(self):
        """Initialize the document processor with all supported processors"""
        self.processors: Dict[DocumentType, BaseProcessor] = {
            DocumentType.PDF: PDFProcessor(),
            DocumentType.POWERPOINT: PowerPointProcessor(),
            DocumentType.WORD: WordProcessor(),
            DocumentType.MARKDOWN: MarkdownProcessor(),
            DocumentType.EMAIL: EmailProcessor(),
        }
        
        # Ensure directories exist
        os.makedirs(settings.upload_dir, exist_ok=True)
        os.makedirs(settings.processed_dir, exist_ok=True)
    
    def _detect_document_type(self, filename: str) -> DocumentType:
        """Detect document type from filename extension"""
        ext = os.path.splitext(filename)[1].lower()
        
        type_mapping = {
            '.pdf': DocumentType.PDF,
            '.pptx': DocumentType.POWERPOINT,
            '.ppt': DocumentType.POWERPOINT,
            '.docx': DocumentType.WORD,
            '.doc': DocumentType.WORD,
            '.md': DocumentType.MARKDOWN,
            '.markdown': DocumentType.MARKDOWN,
            '.eml': DocumentType.EMAIL,
            '.msg': DocumentType.EMAIL,
            '.txt': DocumentType.TEXT,
        }
        
        return type_mapping.get(ext, DocumentType.TEXT)
    
    async def process_document(
        self,
        file_path: str,
        filename: str,
        mime_type: str,
    ) -> Document:
        """
        Process a document file
        
        Args:
            file_path: Path to the uploaded file
            filename: Original filename
            mime_type: MIME type of the file
            
        Returns:
            Document with processed content
        """
        # Generate document ID
        doc_id = str(uuid.uuid4())
        
        # Detect document type
        doc_type = self._detect_document_type(filename)
        
        # Create metadata
        file_size = os.path.getsize(file_path)
        metadata = DocumentMetadata(
            filename=filename,
            file_size=file_size,
            mime_type=mime_type,
            document_type=doc_type,
            status=ProcessingStatus.PROCESSING,
        )
        
        # Create document
        document = Document(id=doc_id, metadata=metadata)
        
        try:
            # Get appropriate processor
            processor = self.processors.get(doc_type)
            
            if not processor:
                raise ValueError(f"No processor available for document type: {doc_type}")
            
            # Validate file
            if not await processor.validate(file_path):
                raise ValueError(f"File validation failed for: {filename}")
            
            # Process document
            content = await processor.process(file_path)
            
            # Update document
            document.content = content
            document.metadata.status = ProcessingStatus.COMPLETED
            document.metadata.processed_at = datetime.now()
            
        except Exception as e:
            document.metadata.status = ProcessingStatus.FAILED
            document.error = str(e)
        
        return document
    
    def get_supported_types(self) -> list[DocumentType]:
        """Get list of supported document types"""
        return list(self.processors.keys())
