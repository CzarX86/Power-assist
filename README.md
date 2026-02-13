# Power Assist 🚀

Mobile-first document processing application built with Python, Dockling library, and Agno framework.

## 📋 Overview

Power Assist is a comprehensive document processing system that transforms various document formats (PDF, PowerPoint, Word, emails, Markdown) into a unified, manageable repository. The system leverages advanced agent orchestration using the Agno framework, with a mobile-first approach using Agno UI and Flutter.

## ✨ Key Features

- **Multi-format Support**: Process PDF, PowerPoint, Word, Email, and Markdown documents
- **Advanced Processing**: Powered by Dockling library for intelligent document extraction
- **Agent Orchestration**: Super agent system with specialized teams for different tasks
- **Mobile-First Design**: Built with Agno UI and Flutter for native mobile experience
- **REST API**: Complete FastAPI backend for document management
- **Flexible Architecture**: Extensible processor and agent system

## 🏗️ Architecture

### Backend (Python)
- **Processors**: Individual document processors for each format
- **Super Agent**: Orchestrates multiple agent teams
- **Agent Teams**:
  - Extraction Team: Extract information, keywords, summaries
  - Analysis Team: Analyze document content and structure
  - Transformation Team: Transform documents to different formats
- **REST API**: FastAPI with async support

### Frontend
- **Agno UI**: Mobile-first components for web
- **Flutter**: Native mobile application (iOS/Android)

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- pip or Poetry
- Flutter SDK (for mobile app)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/CzarX86/Power-assist.git
cd Power-assist
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start the API server:
```bash
python src/main.py server
```

The server will start at `http://localhost:8000`

### Processing a Document

Process a document from the command line:
```bash
python src/main.py process /path/to/document.pdf
```

### Running the Demo

See the super agent in action:
```bash
python src/main.py demo
```

## 📱 Mobile App (Flutter)

### Setup

1. Navigate to the Flutter project:
```bash
cd flutter/power_assist_mobile
```

2. Install dependencies:
```bash
flutter pub get
```

3. Run the app:
```bash
flutter run
```

## 📚 API Documentation

Once the server is running, visit:
- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

### Main Endpoints

#### Upload Document
```
POST /api/v1/upload
```
Upload a document for processing

#### List Documents
```
GET /api/v1/documents
```
Get all processed documents

#### Get Document
```
GET /api/v1/documents/{document_id}
```
Get specific document details

#### Create Task
```
POST /api/v1/tasks
```
Create an agent task for a document

#### Execute Task
```
POST /api/v1/tasks/{task_id}/execute
```
Execute an agent task

## 🛠️ Development

### Project Structure

```
Power-assist/
├── src/
│   ├── power_assist/
│   │   ├── agents/          # Agent orchestration
│   │   ├── processors/      # Document processors
│   │   ├── api/            # FastAPI application
│   │   ├── ui/             # Agno UI components
│   │   ├── models/         # Data models
│   │   └── config/         # Configuration
│   └── main.py             # CLI entry point
├── flutter/
│   └── power_assist_mobile/ # Flutter mobile app
├── requirements.txt
├── pyproject.toml
└── README.md
```

### Supported Document Types

- **PDF**: `.pdf` - Using Dockling with PyPDF2 fallback
- **PowerPoint**: `.ppt`, `.pptx` - Using python-pptx
- **Word**: `.doc`, `.docx` - Using python-docx
- **Email**: `.eml`, `.msg` - Using email library
- **Markdown**: `.md` - Using markdown library

### Agent Tasks

#### Extraction Tasks
- `extract` + `extract_type: "summary"` - Extract document summary
- `extract` + `extract_type: "keywords"` - Extract keywords
- `extract` + `extract_type: "metadata"` - Extract metadata

#### Analysis Tasks
- `analyze` + `analysis_type: "basic"` - Basic statistics

#### Transformation Tasks
- `transform` + `transform_type: "markdown"` - Convert to Markdown
- `transform` + `transform_type: "json"` - Convert to JSON

## 🔧 Configuration

Create a `.env` file in the project root:

```env
# Application
APP_NAME=Power Assist
DEBUG=false

# API
API_HOST=0.0.0.0
API_PORT=8000

# File Upload
MAX_UPLOAD_SIZE=104857600  # 100 MB
UPLOAD_DIR=uploads
PROCESSED_DIR=processed

# Agno Framework
AGNO_MODEL=gpt-4
AGNO_TEMPERATURE=0.7
AGNO_MAX_TOKENS=2000
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Dockling**: Advanced document processing library
- **Agno Framework**: Agent orchestration platform
- **FastAPI**: Modern web framework for building APIs
- **Flutter**: UI toolkit for building natively compiled applications

## 📞 Contact

For questions or support, please open an issue on GitHub.

---

Built with ❤️ using Python, Dockling, and Agno Framework
