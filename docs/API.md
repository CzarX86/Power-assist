# API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required. In production, implement JWT or OAuth2.

## Endpoints

### Health Check

**GET** `/health`

Check if the API is running.

### Upload Document

**POST** `/api/v1/upload`

Upload a document for processing.

### List Documents

**GET** `/api/v1/documents`

Get all uploaded documents.

### Get Document

**GET** `/api/v1/documents/{document_id}`

Get specific document details.

### Create Task

**POST** `/api/v1/tasks`

Create an agent task for a document.

### Execute Task

**POST** `/api/v1/tasks/{task_id}/execute`

Execute an agent task.

For detailed examples, visit http://localhost:8000/docs when server is running.
