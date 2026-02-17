# Power Assist - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Optional: Flutter SDK for mobile app

### Step 1: Clone the Repository
```bash
git clone https://github.com/CzarX86/Power-assist.git
cd Power-assist
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Demo
```bash
python src/main.py demo
```

Expected output:
```
Power Assist - Super Agent Demo
============================================================
Registered document: [UUID]
Creating extraction task...
Task created: [UUID]
Executing task...
Status: COMPLETED
Result: {'keywords': [...]}
...
============================================================
Demo completed!
```

### Step 4: Start the Server
```bash
python src/main.py server
```

Server will start at: http://localhost:8000
API docs available at: http://localhost:8000/docs

### Step 5: Test Document Processing
```bash
# Create a test markdown file
echo "# Test Document

This is a test." > test.md

# Process it
python src/main.py process test.md
```

## 📱 Mobile App Setup (Optional)

### Install Flutter
Follow: https://docs.flutter.dev/get-started/install

### Run the App
```bash
cd flutter/power_assist_mobile
flutter pub get
flutter run
```

## 🔧 Configuration

Create a `.env` file (optional):
```env
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false
```

## 📚 Usage Examples

### 1. Upload Document via API

```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
  -F "file=@document.pdf"
```

### 2. List Documents

```bash
curl "http://localhost:8000/api/v1/documents"
```

### 3. Create Agent Task

```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "YOUR_DOCUMENT_ID",
    "task_type": "extract",
    "parameters": {"extract_type": "keywords"}
  }'
```

### 4. Execute Task

```bash
curl -X POST "http://localhost:8000/api/v1/tasks/YOUR_TASK_ID/execute"
```

## 🎯 Common Tasks

### Process Different Document Types

```bash
# PDF
python src/main.py process document.pdf

# Word
python src/main.py process document.docx

# PowerPoint
python src/main.py process presentation.pptx

# Markdown
python src/main.py process readme.md

# Email
python src/main.py process message.eml
```

### Use Python API Directly

```python
import asyncio
from power_assist.processors.document_processor import DocumentProcessor
from power_assist.agents.super_agent import SuperAgent

async def main():
    # Process document
    processor = DocumentProcessor()
    doc = await processor.process_document(
        "document.pdf",
        "document.pdf",
        "application/pdf"
    )
    
    # Use super agent
    agent = SuperAgent()
    await agent.register_document(doc)
    
    # Create and execute task
    task = await agent.create_task(
        task_type="extract",
        document_id=doc.id,
        parameters={"extract_type": "summary"}
    )
    result = await agent.execute_task(task.task_id)
    print(result.result)

asyncio.run(main())
```

## 🧪 Running Tests

```bash
python tests/integration_test.py
```

Expected output:
```
POWER ASSIST - INTEGRATION TEST SUITE
======================================================================
...
🎉 ALL TESTS PASSED!
```

## 📖 Next Steps

1. **Read the Documentation**
   - [Architecture](docs/ARCHITECTURE.md) - System design
   - [API Documentation](docs/API.md) - API reference
   - [Flutter Guide](flutter/README.md) - Mobile app

2. **Try Examples**
   - Check `examples/` directory
   - Run `python examples/basic_usage.py`

3. **Customize**
   - Add new document processors
   - Create custom agent teams
   - Extend the API

## 🛟 Troubleshooting

### Import Errors
```bash
# Make sure dependencies are installed
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Change port in .env or use command line
python src/main.py server  # Uses port from config
```

### Module Not Found
```bash
# Run from project root
cd /path/to/Power-assist
python src/main.py demo
```

### Flutter Issues
```bash
# Clean and reinstall
cd flutter/power_assist_mobile
flutter clean
flutter pub get
flutter run
```

## 💡 Tips

- Use the interactive API docs at `/docs` endpoint
- Check logs for debugging
- Start with the demo to understand the flow
- Test with simple documents first
- Read the architecture document for deep understanding

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📞 Support

- Open an issue on GitHub
- Check documentation in `docs/`
- Read code comments

---

**Happy document processing! 🎉**
