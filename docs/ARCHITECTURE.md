# Power Assist Architecture

## Overview

Power Assist is a mobile-first document processing application that combines the power of Dockling for document processing, Agno framework for agent orchestration, and modern technologies for a seamless user experience.

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Mobile Frontend                      │
│  ┌──────────────┐              ┌──────────────┐       │
│  │ Flutter App  │              │  Agno UI     │       │
│  │  (Native)    │              │  (Web)       │       │
│  └──────────────┘              └──────────────┘       │
└────────────────┬───────────────────┬───────────────────┘
                 │                   │
                 │    REST API       │
                 └─────────┬─────────┘
                           │
┌──────────────────────────▼────────────────────────────┐
│                  FastAPI Backend                      │
│                                                        │
│  ┌─────────────────────────────────────────────────┐ │
│  │           Document Processor                    │ │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐  │ │
│  │  │  PDF   │ │  Word  │ │  PPT   │ │ Email  │  │ │
│  │  └────────┘ └────────┘ └────────┘ └────────┘  │ │
│  └─────────────────────────────────────────────────┘ │
│                                                        │
│  ┌─────────────────────────────────────────────────┐ │
│  │              Super Agent                        │ │
│  │  ┌─────────────────┐ ┌─────────────────┐       │ │
│  │  │ Extraction Team │ │ Analysis Team   │       │ │
│  │  └─────────────────┘ └─────────────────┘       │ │
│  │  ┌─────────────────┐                           │ │
│  │  │Transform Team   │                           │ │
│  │  └─────────────────┘                           │ │
│  └─────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────┘
                           │
┌──────────────────────────▼────────────────────────────┐
│                 Document Storage                       │
│              (File System / Database)                  │
└───────────────────────────────────────────────────────┘
```

## Components

### 1. Frontend Layer

#### Flutter Mobile App
- **Purpose**: Native mobile experience for iOS and Android
- **Features**:
  - Document upload from mobile device
  - Document list view
  - Status tracking
  - Task execution interface
- **Technology**: Flutter 3.0+, Dart

#### Agno UI (Web)
- **Purpose**: Mobile-first web interface
- **Features**:
  - Responsive components
  - Document cards
  - Processing indicators
  - Task panels
- **Technology**: Agno UI framework

### 2. Backend Layer

#### FastAPI REST API
- **Endpoints**:
  - `/api/v1/upload` - Document upload
  - `/api/v1/documents` - List/get documents
  - `/api/v1/tasks` - Create/execute/get tasks
  - `/api/v1/supported-types` - Get supported formats
- **Features**:
  - Async processing
  - CORS support for mobile
  - OpenAPI documentation
  - Error handling

#### Document Processor
- **Purpose**: Extract content from various document formats
- **Processors**:
  - **PDF Processor**: Uses Dockling with PyPDF2 fallback
  - **Word Processor**: Uses python-docx
  - **PowerPoint Processor**: Uses python-pptx
  - **Email Processor**: Uses email library
  - **Markdown Processor**: Native markdown support
- **Output**: Unified DocumentContent model

#### Super Agent System
- **Purpose**: Orchestrate intelligent document processing
- **Architecture**: Multi-agent system with specialized teams
- **Teams**:
  
  **Extraction Team**:
  - Extract summaries
  - Extract keywords
  - Extract metadata
  
  **Analysis Team**:
  - Basic statistics
  - Content analysis
  - Structure analysis
  
  **Transformation Team**:
  - Format conversion (Markdown, JSON)
  - Content restructuring
  - Data export

### 3. Data Layer

#### Models
- **Document**: Complete document representation
- **DocumentMetadata**: File information and status
- **DocumentContent**: Extracted text, images, tables
- **AgentTask**: Task definition and results

#### Storage
- **Current**: In-memory dictionaries
- **Production**: 
  - File storage for uploads
  - Database for metadata (PostgreSQL/MongoDB)
  - Object storage for processed content (S3/MinIO)

## Technology Stack

### Backend
- **Python 3.10+**: Core language
- **FastAPI**: Web framework
- **Pydantic**: Data validation
- **Dockling 2.0+**: Advanced document processing
- **Agno Framework**: Agent orchestration
- **PyPDF2**: PDF fallback processing
- **python-docx**: Word document processing
- **python-pptx**: PowerPoint processing

### Frontend
- **Flutter 3.0+**: Mobile framework
- **Dart**: Flutter language
- **Provider**: State management
- **File Picker**: File selection
- **HTTP**: API communication

### DevOps
- **Uvicorn**: ASGI server
- **Poetry**: Dependency management
- **Git**: Version control

## Data Flow

### Document Upload Flow
```
1. User uploads document via mobile/web
   ↓
2. FastAPI receives file
   ↓
3. Document Processor detects type
   ↓
4. Appropriate processor extracts content
   ↓
5. DocumentContent created
   ↓
6. Document registered with Super Agent
   ↓
7. Response sent to client
```

### Agent Task Flow
```
1. Client creates task via API
   ↓
2. Super Agent creates AgentTask
   ↓
3. Task routed to appropriate team
   ↓
4. Team processes document
   ↓
5. Results stored in task
   ↓
6. Client retrieves results
```

## Design Patterns

### 1. Strategy Pattern
- **Used in**: Document processors
- **Purpose**: Different processing strategies for each document type
- **Implementation**: BaseProcessor abstract class with specific implementations

### 2. Factory Pattern
- **Used in**: Document processor selection
- **Purpose**: Create appropriate processor based on file type
- **Implementation**: DocumentProcessor coordinator

### 3. Command Pattern
- **Used in**: Agent tasks
- **Purpose**: Encapsulate requests as objects
- **Implementation**: AgentTask model with execute method

### 4. Team Pattern
- **Used in**: Agent teams
- **Purpose**: Organize agents by specialization
- **Implementation**: ExtractionTeam, AnalysisTeam, TransformationTeam

## Security Considerations

### Current Implementation
- No authentication (development)
- CORS open to all origins
- No rate limiting
- No input validation beyond file types

### Production Recommendations
- Implement JWT authentication
- Configure CORS for specific origins
- Add rate limiting
- Implement file size limits
- Scan uploads for malware
- Validate document content
- Encrypt sensitive data
- Use HTTPS only

## Performance Considerations

### Optimization Strategies
1. **Async Processing**: All I/O operations are async
2. **Lazy Loading**: Documents loaded on demand
3. **Background Tasks**: Long-running tasks in background
4. **Caching**: Consider Redis for frequent queries
5. **CDN**: Static assets served via CDN
6. **Database Indexing**: Index frequently queried fields

### Scalability
- **Horizontal Scaling**: Multiple API instances behind load balancer
- **Queue System**: Celery/RabbitMQ for task processing
- **Microservices**: Split into document processor and agent services
- **Container Orchestration**: Kubernetes for deployment

## Future Enhancements

### Phase 1 (Current)
- ✅ Basic document processing
- ✅ Super agent with teams
- ✅ REST API
- ✅ Flutter scaffolding
- ✅ Agno UI components

### Phase 2 (Next)
- [ ] Authentication and authorization
- [ ] Database integration
- [ ] Real-time updates (WebSocket)
- [ ] Advanced Dockling features
- [ ] Complete Flutter app
- [ ] Offline support

### Phase 3 (Future)
- [ ] OCR for scanned documents
- [ ] Multi-language support
- [ ] Advanced AI features
- [ ] Collaborative editing
- [ ] Version control
- [ ] Cloud sync

## Testing Strategy

### Unit Tests
- Test individual processors
- Test agent teams
- Test API endpoints

### Integration Tests
- Test document flow end-to-end
- Test agent task execution
- Test API with real files

### Mobile Tests
- Flutter widget tests
- Integration tests
- Platform-specific tests

## Deployment

### Development
```bash
python src/main.py server
```

### Production
```bash
# Using Docker
docker build -t power-assist .
docker run -p 8000:8000 power-assist

# Using systemd
systemctl start power-assist

# Using Kubernetes
kubectl apply -f k8s/
```

## Monitoring

### Metrics
- Request count/latency
- Document processing time
- Agent task success rate
- Error rates
- Resource usage

### Logging
- Structured logging (JSON)
- Log levels: DEBUG, INFO, WARNING, ERROR
- Log aggregation (ELK stack)

### Alerting
- High error rates
- Slow response times
- Resource exhaustion
- Failed tasks

## Documentation

- **README.md**: Getting started guide
- **ARCHITECTURE.md**: This document
- **API.md**: API documentation
- **Flutter/README.md**: Mobile app guide
- **Code comments**: Inline documentation
