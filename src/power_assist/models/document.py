"""Data models for Power Assist application"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class DocumentType(str, Enum):
    """Supported document types"""
    PDF = "pdf"
    POWERPOINT = "powerpoint"
    WORD = "word"
    EMAIL = "email"
    MARKDOWN = "markdown"
    TEXT = "text"


class ProcessingStatus(str, Enum):
    """Document processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DocumentMetadata(BaseModel):
    """Metadata for uploaded documents"""
    filename: str
    file_size: int
    mime_type: str
    document_type: DocumentType
    uploaded_at: datetime = Field(default_factory=datetime.now)
    processed_at: Optional[datetime] = None
    status: ProcessingStatus = ProcessingStatus.PENDING


class DocumentContent(BaseModel):
    """Processed document content"""
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    images: List[str] = Field(default_factory=list)
    tables: List[Dict[str, Any]] = Field(default_factory=list)
    structure: Optional[Dict[str, Any]] = None


class Document(BaseModel):
    """Complete document model"""
    id: str
    metadata: DocumentMetadata
    content: Optional[DocumentContent] = None
    error: Optional[str] = None


class ProcessingRequest(BaseModel):
    """Request for document processing"""
    document_id: str
    options: Dict[str, Any] = Field(default_factory=dict)


class ProcessingResponse(BaseModel):
    """Response from document processing"""
    document_id: str
    status: ProcessingStatus
    message: str
    content: Optional[DocumentContent] = None


class AgentTask(BaseModel):
    """Task for agent processing"""
    task_id: str
    task_type: str
    document_id: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    status: ProcessingStatus = ProcessingStatus.PENDING
