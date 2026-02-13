"""
Integration test for Power Assist system
"""
import asyncio
import os
import sys
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from power_assist.processors.document_processor import DocumentProcessor
from power_assist.agents.super_agent import SuperAgent
from power_assist.models.document import ProcessingStatus


async def test_document_processing():
    """Test document processing functionality"""
    print("=" * 70)
    print("INTEGRATION TEST: Document Processing")
    print("=" * 70)
    
    processor = DocumentProcessor()
    passed = 0
    failed = 0
    
    # Test 1: Markdown processing
    print("\n[TEST 1] Processing Markdown document...")
    try:
        md_content = "# Test\n\nThis is a test document."
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(md_content)
            temp_md = f.name
        
        doc = await processor.process_document(temp_md, "test.md", "text/markdown")
        assert doc.metadata.status == ProcessingStatus.COMPLETED
        assert doc.content is not None
        print("✓ PASS: Markdown processing works")
        passed += 1
        os.unlink(temp_md)
    except Exception as e:
        print(f"✗ FAIL: {str(e)}")
        failed += 1
    
    # Test 2: Document type detection
    print("\n[TEST 2] Document type detection...")
    try:
        assert processor._detect_document_type("test.pdf").value == "pdf"
        assert processor._detect_document_type("test.docx").value == "word"
        print("✓ PASS: Document type detection works")
        passed += 1
    except Exception as e:
        print(f"✗ FAIL: {str(e)}")
        failed += 1
    
    print("\n" + "=" * 70)
    print(f"Document Processing Tests: {passed} passed, {failed} failed")
    print("=" * 70)
    return passed, failed


async def test_super_agent():
    """Test super agent functionality"""
    print("\n" + "=" * 70)
    print("INTEGRATION TEST: Super Agent")
    print("=" * 70)
    
    super_agent = SuperAgent()
    passed = 0
    failed = 0
    
    # Create test document
    from power_assist.models.document import (
        Document, DocumentMetadata, DocumentContent,
        DocumentType, ProcessingStatus
    )
    import uuid
    
    test_doc = Document(
        id=str(uuid.uuid4()),
        metadata=DocumentMetadata(
            filename="test.md",
            file_size=1000,
            mime_type="text/markdown",
            document_type=DocumentType.MARKDOWN,
            status=ProcessingStatus.COMPLETED,
        ),
        content=DocumentContent(
            text="# Test Document\n\nTest content for agent processing.",
            metadata={"test": True},
        ),
    )
    
    # Test 1: Document registration
    print("\n[TEST 1] Document registration...")
    try:
        doc_id = await super_agent.register_document(test_doc)
        assert doc_id == test_doc.id
        print("✓ PASS: Document registration works")
        passed += 1
    except Exception as e:
        print(f"✗ FAIL: {str(e)}")
        failed += 1
    
    # Test 2: Task execution
    print("\n[TEST 2] Task execution...")
    try:
        task = await super_agent.create_task(
            task_type="extract",
            document_id=test_doc.id,
            parameters={"extract_type": "keywords"}
        )
        result = await super_agent.execute_task(task.task_id)
        assert result.status == ProcessingStatus.COMPLETED
        print("✓ PASS: Task execution works")
        passed += 1
    except Exception as e:
        print(f"✗ FAIL: {str(e)}")
        failed += 1
    
    print("\n" + "=" * 70)
    print(f"Super Agent Tests: {passed} passed, {failed} failed")
    print("=" * 70)
    return passed, failed


async def main():
    """Run all integration tests"""
    print("\n" + "=" * 70)
    print("POWER ASSIST - INTEGRATION TEST SUITE")
    print("=" * 70)
    
    total_passed = 0
    total_failed = 0
    
    passed, failed = await test_document_processing()
    total_passed += passed
    total_failed += failed
    
    passed, failed = await test_super_agent()
    total_passed += passed
    total_failed += failed
    
    print("\n" + "=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)
    print(f"Total Tests: {total_passed + total_failed}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_failed}")
    
    if total_failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n❌ {total_failed} TESTS FAILED")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
