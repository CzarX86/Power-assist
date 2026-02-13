"""
Example: Using Power Assist to process a document
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from power_assist.processors.document_processor import DocumentProcessor
from power_assist.agents.super_agent import SuperAgent


async def main():
    print("Power Assist - Document Processing Example")
    print("=" * 60)
    
    # Initialize processor and super agent
    processor = DocumentProcessor()
    super_agent = SuperAgent()
    
    # Example 1: Process a Markdown document
    print("\n1. Processing a sample Markdown document...")
    
    # Create a sample markdown file
    sample_md = """# Sample Document

This is a sample document for testing Power Assist.

## Features

- Document processing
- Agent orchestration
- Mobile-first design

## Content

Lorem ipsum dolor sit amet, consectetur adipiscing elit.
"""
    
    # Save to temp file
    import tempfile
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(sample_md)
        temp_file = f.name
    
    try:
        # Process the document
        document = await processor.process_document(
            file_path=temp_file,
            filename="sample.md",
            mime_type="text/markdown",
        )
        
        print(f"\nDocument processed successfully!")
        print(f"- ID: {document.id}")
        print(f"- Type: {document.metadata.document_type}")
        print(f"- Status: {document.metadata.status}")
        
        # Register with super agent
        print("\n2. Registering document with super agent...")
        await super_agent.register_document(document)
        
        # Extract keywords
        print("\n3. Extracting keywords...")
        task = await super_agent.create_task(
            task_type="extract",
            document_id=document.id,
            parameters={"extract_type": "keywords"}
        )
        
        result = await super_agent.execute_task(task.task_id)
        print(f"Keywords: {result.result.get('keywords', [])}")
        
        print("\n" + "=" * 60)
        print("Example completed successfully!")
        
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


if __name__ == "__main__":
    asyncio.run(main())
