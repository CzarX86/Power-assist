#!/usr/bin/env python3
"""Main entry point for Power Assist application"""
import asyncio
import argparse
import sys
from pathlib import Path

from power_assist.config import settings
from power_assist.processors.document_processor import DocumentProcessor
from power_assist.agents.super_agent import SuperAgent


async def process_file(file_path: str):
    """Process a single file"""
    processor = DocumentProcessor()
    
    print(f"Processing: {file_path}")
    
    document = await processor.process_document(
        file_path=file_path,
        filename=Path(file_path).name,
        mime_type="application/octet-stream",
    )
    
    print(f"\n{'='*60}")
    print(f"Document ID: {document.id}")
    print(f"Status: {document.metadata.status}")
    print(f"Type: {document.metadata.document_type}")
    
    if document.content:
        print(f"\n{'='*60}")
        print("Content Preview:")
        print(f"{'='*60}")
        print(document.content.text[:500])
        if len(document.content.text) > 500:
            print("...")
        print(f"\n{'='*60}")
        print(f"Metadata: {document.content.metadata}")
    
    if document.error:
        print(f"\nError: {document.error}")
    
    return document


async def run_server():
    """Run the FastAPI server"""
    import uvicorn
    from power_assist.api.main import app
    
    print(f"Starting {settings.app_name} v{settings.app_version}")
    print(f"Server running at http://{settings.api_host}:{settings.api_port}")
    print(f"API documentation: http://{settings.api_host}:{settings.api_port}/docs")
    
    config = uvicorn.Config(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
    server = uvicorn.Server(config)
    await server.serve()


async def demo_agent():
    """Demo the super agent capabilities"""
    processor = DocumentProcessor()
    super_agent = SuperAgent()
    
    print("Power Assist - Super Agent Demo")
    print("=" * 60)
    
    # Create a sample document
    from power_assist.models.document import (
        Document,
        DocumentMetadata,
        DocumentContent,
        DocumentType,
        ProcessingStatus,
    )
    from datetime import datetime
    import uuid
    
    doc = Document(
        id=str(uuid.uuid4()),
        metadata=DocumentMetadata(
            filename="demo.md",
            file_size=1000,
            mime_type="text/markdown",
            document_type=DocumentType.MARKDOWN,
            status=ProcessingStatus.COMPLETED,
        ),
        content=DocumentContent(
            text="""# Power Assist Demo
            
This is a demonstration of the Power Assist document processing system.
It supports multiple document formats including PDF, Word, PowerPoint, and more.

The system uses:
- Dockling for advanced document processing
- Agno framework for agent orchestration
- FastAPI for the REST API
- Mobile-first design with Agno UI

Key features:
- Document extraction and analysis
- Multi-agent processing teams
- Flexible transformation pipelines
""",
            metadata={"source": "demo"},
        ),
    )
    
    await super_agent.register_document(doc)
    print(f"Registered document: {doc.id}\n")
    
    # Create and execute extraction task
    print("Creating extraction task...")
    task1 = await super_agent.create_task(
        task_type="extract",
        document_id=doc.id,
        parameters={"extract_type": "keywords"},
    )
    print(f"Task created: {task1.task_id}")
    
    print("Executing task...")
    result1 = await super_agent.execute_task(task1.task_id)
    print(f"Status: {result1.status}")
    print(f"Result: {result1.result}\n")
    
    # Create and execute analysis task
    print("Creating analysis task...")
    task2 = await super_agent.create_task(
        task_type="analyze",
        document_id=doc.id,
        parameters={"analysis_type": "basic"},
    )
    print(f"Task created: {task2.task_id}")
    
    print("Executing task...")
    result2 = await super_agent.execute_task(task2.task_id)
    print(f"Status: {result2.status}")
    print(f"Result: {result2.result}\n")
    
    print("=" * 60)
    print("Demo completed!")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Power Assist - Mobile-first Document Processing"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Server command
    subparsers.add_parser("server", help="Start the API server")
    
    # Process command
    process_parser = subparsers.add_parser("process", help="Process a document file")
    process_parser.add_argument("file", help="Path to the document file")
    
    # Demo command
    subparsers.add_parser("demo", help="Run agent demo")
    
    args = parser.parse_args()
    
    if args.command == "server":
        asyncio.run(run_server())
    elif args.command == "process":
        asyncio.run(process_file(args.file))
    elif args.command == "demo":
        asyncio.run(demo_agent())
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
