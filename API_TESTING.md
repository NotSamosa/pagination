# API Testing Documentation & Sample Responses

This document provides sample requests and JSON responses for all three pagination tasks.

---

## Task 1 & 2: Standard & Global Pagination Endpoint (`/api/articles/`)

### 1. Default Page Request (Page 1, 15 items default)
**Request:**
```bash
curl -X GET http://127.0.0.1:8000/api/articles/
```

**Response (HTTP 200 OK):**
```json
{
  "count": 52,
  "next": "http://127.0.0.1:8000/api/articles/?page=2",
  "previous": null,
  "results": [
    {
      "id": 52,
      "title": "Securing Web Applications with OAuth2 and JWT - Part 52",
      "content": "This article explores technical details, benchmarks, and real-world architectures regarding securing web applications with oauth2 and jwt...",
      "author": "Priya Patel",
      "created_at": "2026-10-18T22:59:14.606611Z",
      "is_published": true
    },
    {
      "id": 51,
      "title": "Asynchronous Programming with Asyncio and Celery - Part 51",
      "content": "This article explores technical details, benchmarks, and real-world architectures regarding asynchronous programming with asyncio and celery...",
      "author": "David Miller",
      "created_at": "2026-10-18T00:00:14.606611Z",
      "is_published": true
    }
  ]
}
```

### 2. Page Navigation (Page 2)
**Request:**
```bash
curl -X GET "http://127.0.0.1:8000/api/articles/?page=2"
```

**Response (HTTP 200 OK):**
```json
{
  "count": 52,
  "next": "http://127.0.0.1:8000/api/articles/?page=3",
  "previous": "http://127.0.0.1:8000/api/articles/",
  "results": [
    {
      "id": 37,
      "title": "Containerizing Django Applications with Docker and Compose - Part 37",
      "author": "Elena Rostova",
      "created_at": "2026-10-03T14:14:14.606611Z",
      "is_published": true
    }
  ]
}
```

### 3. Out-of-Range Page Number
**Request:**
```bash
curl -X GET "http://127.0.0.1:8000/api/articles/?page=999"
```

**Response (HTTP 404 Not Found):**
```json
{
  "detail": "Invalid page."
}
```

### 4. Non-Integer Page Number
**Request:**
```bash
curl -X GET "http://127.0.0.1:8000/api/articles/?page=invalid"
```

**Response (HTTP 404 Not Found):**
```json
{
  "detail": "Invalid page."
}
```

### 5. Dynamic Page Size via Query Parameter (`?page_size=20`)
**Request:**
```bash
curl -X GET "http://127.0.0.1:8000/api/articles/?page_size=20"
```

**Response (HTTP 200 OK):**
```json
{
  "count": 52,
  "next": "http://127.0.0.1:8000/api/articles/?page=2&page_size=20",
  "previous": null,
  "results": [
    {
      "id": 52,
      "title": "Securing Web Applications with OAuth2 and JWT - Part 52",
      "author": "Priya Patel",
      "is_published": true
    }
  ]
}
```

### 6. Maximum Page Size Limit Enforced (`?page_size=100` clamped to 50)
**Request:**
```bash
curl -X GET "http://127.0.0.1:8000/api/articles/?page_size=100"
```

**Response (HTTP 200 OK - Results count clamped to 50):**
```json
{
  "count": 52,
  "next": "http://127.0.0.1:8000/api/articles/?page=2&page_size=100",
  "previous": null,
  "results": [
    {
      "id": 52,
      "title": "Securing Web Applications with OAuth2 and JWT - Part 52",
      "author": "Priya Patel",
      "is_published": true
    }
  ]
}
```

---

## Task 3: Custom Pagination Endpoint (`/api/articles/custom/`)

### 1. Default Page Request (8 items, Enriched Metadata)
**Request:**
```bash
curl -X GET http://127.0.0.1:8000/api/articles/custom/
```

**Response (HTTP 200 OK):**
```json
{
  "page_info": {
    "current_page": 1,
    "total_pages": 7,
    "has_next": true,
    "has_previous": false,
    "next": "http://127.0.0.1:8000/api/articles/custom/?page=2",
    "previous": null
  },
  "items_info": {
    "total_items": 52,
    "page_items_count": 8,
    "page_size": 8
  },
  "results": [
    {
      "id": 52,
      "title": "Securing Web Applications with OAuth2 and JWT - Part 52",
      "content": "This article explores technical details, benchmarks, and real-world architectures...",
      "author": "Priya Patel",
      "created_at": "2026-10-18T22:59:14.606611Z",
      "is_published": true
    }
  ]
}
```

### 2. Custom Pagination Dynamic Size (`?page_size=12`)
**Request:**
```bash
curl -X GET "http://127.0.0.1:8000/api/articles/custom/?page_size=12"
```

**Response (HTTP 200 OK):**
```json
{
  "page_info": {
    "current_page": 1,
    "total_pages": 5,
    "has_next": true,
    "has_previous": false,
    "next": "http://127.0.0.1:8000/api/articles/custom/?page=2&page_size=12",
    "previous": null
  },
  "items_info": {
    "total_items": 52,
    "page_items_count": 12,
    "page_size": 12
  },
  "results": [
    {
      "id": 52,
      "title": "Securing Web Applications with OAuth2 and JWT - Part 52",
      "author": "Priya Patel",
      "is_published": true
    }
  ]
}
```

### 3. Invalid Non-Integer Page Size (`?page_size=invalid`)
**Request:**
```bash
curl -X GET "http://127.0.0.1:8000/api/articles/custom/?page_size=invalid"
```

**Response (HTTP 400 Bad Request):**
```json
{
  "page_size": "Invalid page_size. Must be a valid positive integer."
}
```

### 4. Zero or Negative Page Size (`?page_size=0`)
**Request:**
```bash
curl -X GET "http://127.0.0.1:8000/api/articles/custom/?page_size=0"
```

**Response (HTTP 400 Bad Request):**
```json
{
  "page_size": "Invalid page_size. Value must be greater than 0."
}
```

