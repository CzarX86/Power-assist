"""Mobile UI components using Agno UI"""
from typing import Dict, Any, Optional
import json


class AgnoUIComponent:
    """Base class for Agno UI components"""
    
    def __init__(self, component_type: str, props: Optional[Dict[str, Any]] = None):
        self.component_type = component_type
        self.props = props or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert component to dictionary representation"""
        return {
            "type": self.component_type,
            "props": self.props,
        }
    
    def to_json(self) -> str:
        """Convert component to JSON string"""
        return json.dumps(self.to_dict(), indent=2)


class DocumentCard(AgnoUIComponent):
    """Card component for displaying document information"""
    
    def __init__(
        self,
        title: str,
        subtitle: str,
        status: str,
        document_id: str,
        icon: str = "📄",
    ):
        props = {
            "title": title,
            "subtitle": subtitle,
            "status": status,
            "documentId": document_id,
            "icon": icon,
        }
        super().__init__("DocumentCard", props)


class UploadButton(AgnoUIComponent):
    """Button component for uploading documents"""
    
    def __init__(
        self,
        label: str = "Upload Document",
        accept_types: list = None,
    ):
        props = {
            "label": label,
            "acceptTypes": accept_types or [".pdf", ".docx", ".pptx", ".md", ".eml"],
        }
        super().__init__("UploadButton", props)


class ProcessingIndicator(AgnoUIComponent):
    """Loading indicator for document processing"""
    
    def __init__(self, message: str = "Processing document..."):
        props = {"message": message}
        super().__init__("ProcessingIndicator", props)


class DocumentViewer(AgnoUIComponent):
    """Component for viewing document content"""
    
    def __init__(
        self,
        document_id: str,
        content: str,
        metadata: Dict[str, Any],
    ):
        props = {
            "documentId": document_id,
            "content": content,
            "metadata": metadata,
        }
        super().__init__("DocumentViewer", props)


class TaskPanel(AgnoUIComponent):
    """Panel for managing agent tasks"""
    
    def __init__(
        self,
        document_id: str,
        available_tasks: list,
    ):
        props = {
            "documentId": document_id,
            "availableTasks": available_tasks,
        }
        super().__init__("TaskPanel", props)


class MobileLayout:
    """Mobile-first layout manager"""
    
    def __init__(self):
        self.components = []
    
    def add_component(self, component: AgnoUIComponent):
        """Add a component to the layout"""
        self.components.append(component)
    
    def render(self) -> Dict[str, Any]:
        """Render the complete layout"""
        return {
            "layout": "mobile-first",
            "components": [c.to_dict() for c in self.components],
        }
    
    def to_json(self) -> str:
        """Convert layout to JSON"""
        return json.dumps(self.render(), indent=2)


def create_document_upload_screen() -> MobileLayout:
    """Create the document upload screen"""
    layout = MobileLayout()
    
    # Add upload button
    layout.add_component(
        UploadButton(
            label="Upload Document",
            accept_types=[".pdf", ".docx", ".pptx", ".md", ".eml"],
        )
    )
    
    return layout


def create_document_list_screen(documents: list) -> MobileLayout:
    """Create the document list screen"""
    layout = MobileLayout()
    
    for doc in documents:
        layout.add_component(
            DocumentCard(
                title=doc.get("filename", "Untitled"),
                subtitle=f"Type: {doc.get('type', 'Unknown')}",
                status=doc.get("status", "Unknown"),
                document_id=doc.get("id", ""),
            )
        )
    
    return layout


def create_document_detail_screen(
    document_id: str,
    content: str,
    metadata: Dict[str, Any],
) -> MobileLayout:
    """Create the document detail screen"""
    layout = MobileLayout()
    
    # Add document viewer
    layout.add_component(
        DocumentViewer(
            document_id=document_id,
            content=content,
            metadata=metadata,
        )
    )
    
    # Add task panel
    layout.add_component(
        TaskPanel(
            document_id=document_id,
            available_tasks=[
                {"id": "extract", "label": "Extract Information"},
                {"id": "analyze", "label": "Analyze Content"},
                {"id": "transform", "label": "Transform Document"},
            ],
        )
    )
    
    return layout
