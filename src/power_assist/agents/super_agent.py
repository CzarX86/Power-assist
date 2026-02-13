"""Super Agent for managing document processing workflows"""
from typing import List, Dict, Any, Optional
import json
from datetime import datetime

from ..models.document import Document, AgentTask, ProcessingStatus
from ..config import settings


class SuperAgent:
    """
    Super Agent that manages document processing workflows using Agno framework.
    Coordinates multiple specialized agents and teams for different tasks.
    """
    
    def __init__(self):
        """Initialize the Super Agent"""
        self.tasks: Dict[str, AgentTask] = {}
        self.documents: Dict[str, Document] = {}
        
        # Initialize agent teams
        self.extraction_team = ExtractionTeam()
        self.analysis_team = AnalysisTeam()
        self.transformation_team = TransformationTeam()
    
    async def register_document(self, document: Document) -> str:
        """
        Register a document with the super agent
        
        Args:
            document: Document to register
            
        Returns:
            Document ID
        """
        self.documents[document.id] = document
        return document.id
    
    async def create_task(
        self,
        task_type: str,
        document_id: str,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> AgentTask:
        """
        Create a new agent task
        
        Args:
            task_type: Type of task (extract, analyze, transform)
            document_id: ID of the document to process
            parameters: Additional task parameters
            
        Returns:
            Created AgentTask
        """
        import uuid
        
        task_id = str(uuid.uuid4())
        task = AgentTask(
            task_id=task_id,
            task_type=task_type,
            document_id=document_id,
            parameters=parameters or {},
        )
        
        self.tasks[task_id] = task
        return task
    
    async def execute_task(self, task_id: str) -> AgentTask:
        """
        Execute an agent task
        
        Args:
            task_id: ID of the task to execute
            
        Returns:
            Updated AgentTask
        """
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"Task not found: {task_id}")
        
        document = self.documents.get(task.document_id)
        if not document:
            raise ValueError(f"Document not found: {task.document_id}")
        
        task.status = ProcessingStatus.PROCESSING
        
        try:
            # Route task to appropriate team
            if task.task_type == "extract":
                result = await self.extraction_team.process(document, task.parameters)
            elif task.task_type == "analyze":
                result = await self.analysis_team.process(document, task.parameters)
            elif task.task_type == "transform":
                result = await self.transformation_team.process(document, task.parameters)
            else:
                raise ValueError(f"Unknown task type: {task.task_type}")
            
            task.result = result
            task.status = ProcessingStatus.COMPLETED
            task.completed_at = datetime.now()
            
        except Exception as e:
            task.status = ProcessingStatus.FAILED
            task.result = {"error": str(e)}
        
        return task
    
    async def get_task_status(self, task_id: str) -> Optional[AgentTask]:
        """Get status of a task"""
        return self.tasks.get(task_id)
    
    async def get_document_tasks(self, document_id: str) -> List[AgentTask]:
        """Get all tasks for a document"""
        return [
            task for task in self.tasks.values()
            if task.document_id == document_id
        ]


class ExtractionTeam:
    """Team of agents specialized in extracting information from documents"""
    
    async def process(self, document: Document, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract specific information from document
        
        Args:
            document: Document to process
            parameters: Extraction parameters (e.g., extract_type: "entities", "keywords")
            
        Returns:
            Extraction results
        """
        if not document.content:
            return {"error": "Document has no content"}
        
        extract_type = parameters.get("extract_type", "summary")
        
        result = {
            "extract_type": extract_type,
            "timestamp": datetime.now().isoformat(),
        }
        
        if extract_type == "summary":
            # Extract first 500 characters as summary
            result["summary"] = document.content.text[:500] + "..."
        
        elif extract_type == "metadata":
            result["metadata"] = document.content.metadata
        
        elif extract_type == "keywords":
            # Simple keyword extraction (word frequency)
            words = document.content.text.lower().split()
            word_freq = {}
            for word in words:
                if len(word) > 3:  # Only words longer than 3 chars
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Get top 10 keywords
            sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            result["keywords"] = [word for word, _ in sorted_words[:10]]
        
        return result


class AnalysisTeam:
    """Team of agents specialized in analyzing document content"""
    
    async def process(self, document: Document, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze document content
        
        Args:
            document: Document to analyze
            parameters: Analysis parameters
            
        Returns:
            Analysis results
        """
        if not document.content:
            return {"error": "Document has no content"}
        
        analysis_type = parameters.get("analysis_type", "basic")
        
        result = {
            "analysis_type": analysis_type,
            "timestamp": datetime.now().isoformat(),
        }
        
        if analysis_type == "basic":
            text = document.content.text
            result["stats"] = {
                "char_count": len(text),
                "word_count": len(text.split()),
                "line_count": len(text.splitlines()),
                "has_images": len(document.content.images) > 0,
                "has_tables": len(document.content.tables) > 0,
            }
        
        return result


class TransformationTeam:
    """Team of agents specialized in transforming documents"""
    
    async def process(self, document: Document, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform document to different format
        
        Args:
            document: Document to transform
            parameters: Transformation parameters
            
        Returns:
            Transformation results
        """
        if not document.content:
            return {"error": "Document has no content"}
        
        transform_type = parameters.get("transform_type", "markdown")
        
        result = {
            "transform_type": transform_type,
            "timestamp": datetime.now().isoformat(),
        }
        
        if transform_type == "markdown":
            result["output"] = document.content.text
            result["format"] = "markdown"
        
        elif transform_type == "json":
            result["output"] = json.dumps({
                "text": document.content.text,
                "metadata": document.content.metadata,
                "images": document.content.images,
                "tables": document.content.tables,
            }, indent=2)
            result["format"] = "json"
        
        return result
