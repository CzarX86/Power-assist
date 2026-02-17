"""FastAPI application for Power Assist - Mobile-first Document Processing"""
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import os
import shutil
import uuid

from ..config import settings
from ..models.document import (
    Document,
    ProcessingRequest,
    ProcessingResponse,
    ProcessingStatus,
    AgentTask,
)
from ..processors.document_processor import DocumentProcessor
from ..agents.super_agent import SuperAgent

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Mobile-first document processing with Agno framework and Dockling",
)

# Configure CORS for mobile access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
document_processor = DocumentProcessor()
super_agent = SuperAgent()

# In-memory storage (use database in production)
documents_db: dict[str, Document] = {}


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "supported_formats": [
            "PDF", "PowerPoint", "Word", "Email", "Markdown"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/api/v1/upload", response_model=Document)
async def upload_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    """
    Upload and process a document
    
    Args:
        file: Document file to upload
        
    Returns:
        Document with processing status
    """
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in settings.allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not supported. Allowed: {settings.allowed_extensions}"
        )
    
    # Generate unique filename
    file_id = str(uuid.uuid4())
    file_path = os.path.join(settings.upload_dir, f"{file_id}{file_ext}")
    
    # Save uploaded file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Process document
    try:
        document = await document_processor.process_document(
            file_path=file_path,
            filename=file.filename,
            mime_type=file.content_type or "application/octet-stream",
        )
        
        # Store in database
        documents_db[document.id] = document
        
        # Register with super agent
        await super_agent.register_document(document)
        
        return document
        
    except Exception as e:
        # Clean up file on error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@app.get("/api/v1/documents", response_model=List[Document])
async def list_documents():
    """List all uploaded documents"""
    return list(documents_db.values())


@app.get("/api/v1/documents/{document_id}", response_model=Document)
async def get_document(document_id: str):
    """
    Get document details
    
    Args:
        document_id: Document ID
        
    Returns:
        Document details
    """
    document = documents_db.get(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@app.post("/api/v1/tasks", response_model=AgentTask)
async def create_task(
    document_id: str,
    task_type: str,
    parameters: Optional[dict] = None,
):
    """
    Create an agent task for a document
    
    Args:
        document_id: Document ID
        task_type: Type of task (extract, analyze, transform)
        parameters: Task parameters
        
    Returns:
        Created AgentTask
    """
    if document_id not in documents_db:
        raise HTTPException(status_code=404, detail="Document not found")
    
    task = await super_agent.create_task(
        task_type=task_type,
        document_id=document_id,
        parameters=parameters or {},
    )
    
    return task


@app.post("/api/v1/tasks/{task_id}/execute", response_model=AgentTask)
async def execute_task(task_id: str):
    """
    Execute an agent task
    
    Args:
        task_id: Task ID
        
    Returns:
        Updated AgentTask with results
    """
    try:
        task = await super_agent.execute_task(task_id)
        return task
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Task execution failed: {str(e)}")


@app.get("/api/v1/tasks/{task_id}", response_model=AgentTask)
async def get_task(task_id: str):
    """
    Get task status
    
    Args:
        task_id: Task ID
        
    Returns:
        AgentTask status
    """
    task = await super_agent.get_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.get("/api/v1/documents/{document_id}/tasks", response_model=List[AgentTask])
async def get_document_tasks(document_id: str):
    """
    Get all tasks for a document
    
    Args:
        document_id: Document ID
        
    Returns:
        List of AgentTasks
    """
    if document_id not in documents_db:
        raise HTTPException(status_code=404, detail="Document not found")
    
    tasks = await super_agent.get_document_tasks(document_id)
    return tasks


@app.get("/api/v1/supported-types")
async def get_supported_types():
    """Get list of supported document types"""
    return {
        "types": [t.value for t in document_processor.get_supported_types()]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "power_assist.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
