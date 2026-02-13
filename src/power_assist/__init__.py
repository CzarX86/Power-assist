"""
Power Assist - Mobile-first Document Processing Application
Built with Agno framework and Dockling library
"""

__version__ = "0.1.0"
__author__ = "CzarX86"

from .agents.super_agent import SuperAgent
from .processors.document_processor import DocumentProcessor
from .api.main import app

__all__ = ["SuperAgent", "DocumentProcessor", "app"]
