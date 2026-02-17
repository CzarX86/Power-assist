"""Base document processor interface"""
from abc import ABC, abstractmethod
from typing import Optional
from ..models.document import DocumentContent, DocumentType


class BaseProcessor(ABC):
    """Abstract base class for document processors"""
    
    @property
    @abstractmethod
    def supported_type(self) -> DocumentType:
        """Return the document type this processor supports"""
        pass
    
    @abstractmethod
    async def process(self, file_path: str) -> DocumentContent:
        """
        Process a document and extract its content
        
        Args:
            file_path: Path to the document file
            
        Returns:
            DocumentContent with extracted text, images, and metadata
        """
        pass
    
    @abstractmethod
    async def validate(self, file_path: str) -> bool:
        """
        Validate if the file can be processed
        
        Args:
            file_path: Path to the document file
            
        Returns:
            True if file is valid, False otherwise
        """
        pass
