# 🔌 API Documentation

REST API documentation untuk TNI AU Threat Intelligence System.

## Base URL
```
Development: http://localhost:5000/api
Production: https://your-domain.com/api
```

## Authentication
Currently no authentication required (demo mode).
Production will require API key or JWT token.

## Response Format

### Success Response
```json
{
  "success": true,
  "data": { ... }
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message",
  "message": "Detailed error description"
}
```

---

## Endpoints

### 1. Health Check

**GET** `/health`

Check if API server is running.

**Response:**
```json
{
  "status": "online",
  "message": "TNI AU Threat Intelligence System API",
  "version": "1.0.0",
  "timestamp": "2024-01-22T10:00:00.000Z"
}
```

**Example:**
```bash
curl http://localhost:5000/api/health
```

---

### 2. Dashboard

#### Get Dashboard Statistics

**GET** `/dashboard/stats`

Get overview statistics for dashboard.

**Response:**
```json
{
  "total_threats": 247,
  "high_priority": 23,
  "medium_priority": 68,
  "low_priority": 98,
  "sentiment_summary": {
    "positive": 89,
    "negative": 67,
    "neutral": 91,
    "total": 247,
    "positive_ratio": 0.36
  },
  "recent_threats": [
    {
      "id": 1,
      "source": "twitter",
      "url": "https://twitter.com/example",
      "title": "Threat title",
      "content": "Threat description...",
      "author": "security_researcher",
      "timestamp": "2024-01-22T08:00:00.000Z",
      "sentiment_score": -0.65,
      "sentiment_label": "negative",
      "keywords": "malware, cyber attack",
      "threat_level": "HIGH",
      "collected_at": "2024-01-22T10:00:00.000Z"
    }
  ],
  "trends": [
    {
      "date": "2024-01-15",
      "HIGH": 3,
      "MEDIUM": 8,
      "LOW": 12,
      "INFO": 15
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:5000/api/dashboard/stats
```

---

### 3. Crawler

#### Start Crawling

**POST** `/crawl/start`

Start a new crawling operation.

**Request Body:**
```json
{
  "sources": ["news", "social", "forums"],
  "keywords": ["malware", "cyber attack", "ransomware"],
  "language": "en",
  "maxResults": 100
}
```

**Parameters:**
- `sources` (array, required): List of sources to crawl
  - Options: `"news"`, `"social"`, `"forums"`, `"darkweb"`
- `keywords` (array, required): List of keywords to search
- `language` (string, required): Language code
  - Options: `"id"`, `"en"`, `"zh"`, `"ar"`
- `maxResults` (number, required): Maximum number of results (10-500)

**Response:**
```json
{
  "success": true,
  "message": "Successfully crawled 25 items from 3 sources",
  "data": [
    {
      "id": 1234567890,
      "source": "Twitter",
      "url": "https://example.com/threat/1",
      "title": "HIGH: malware",
      "content": "Critical vulnerability discovered...",
      "author": "analyst_42",
      "timestamp": "2024-01-22T09:30:00.000Z",
      "sentiment_score": -0.5,
      "sentiment_label": "negative",
      "keywords": "malware, cyber attack, ransomware",
      "threat_level": "HIGH",
      "collected_at": "2024-01-22T10:00:00.000Z"
    }
  ]
}
```

**Error Response:**
```json
{
  "success": false,
  "message": "Crawl failed",
  "error": "Invalid parameters"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/crawl/start \
  -H "Content-Type: application/json" \
  -d '{
    "sources": ["news", "social"],
    "keywords": ["malware", "cyber attack"],
    "language": "en",
    "maxResults": 50
  }'
```

#### Get Crawl Status

**GET** `/crawl/status`

Get current crawling status.

**Response:**
```json
{
  "inProgress": false,
  "progress": 100
}
```

**Example:**
```bash
curl http://localhost:5000/api/crawl/status
```

---

### 4. Threats

#### Get Recent Threats

**GET** `/threats/recent`

Get list of recent threats.

**Query Parameters:**
- `limit` (number, optional): Number of results (default: 50, max: 200)

**Response:**
```json
[
  {
    "id": 1,
    "source": "Twitter",
    "url": "https://example.com/threat/1",
    "title": "Threat Report #1",
    "content": "Threat description...",
    "author": "analyst_1",
    "timestamp": "2024-01-22T09:00:00.000Z",
    "sentiment_score": -0.5,
    "sentiment_label": "negative",
    "keywords": "malware, cyber attack",
    "threat_level": "HIGH",
    "collected_at": "2024-01-22T10:00:00.000Z"
  }
]
```

**Example:**
```bash
curl http://localhost:5000/api/threats/recent?limit=10
```

#### Get Threats by Level

**GET** `/threats/level/:level`

Get threats filtered by threat level.

**Path Parameters:**
- `level` (string, required): Threat level
  - Options: `"HIGH"`, `"MEDIUM"`, `"LOW"`, `"INFO"`

**Response:**
```json
[
  {
    "id": 1,
    "threat_level": "HIGH",
    ...
  }
]
```

**Example:**
```bash
curl http://localhost:5000/api/threats/level/HIGH
```

#### Search Threats

**POST** `/threats/search`

Search threats with filters.

**Request Body:**
```json
{
  "query": "malware",
  "filters": {
    "level": "HIGH",
    "sentiment": "negative",
    "source": "twitter"
  }
}
```

**Parameters:**
- `query` (string, optional): Search query
- `filters` (object, optional): Filter options
  - `level`: Threat level filter
  - `sentiment`: Sentiment filter
  - `source`: Source filter

**Response:**
```json
[
  {
    "id": 1,
    "title": "Malware campaign detected",
    ...
  }
]
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/threats/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "malware",
    "filters": {
      "level": "HIGH",
      "sentiment": "negative"
    }
  }'
```

---

### 5. Analytics

#### Get Sentiment Analysis

**GET** `/analytics/sentiment`

Get sentiment analysis data.

**Query Parameters:**
- `days` (number, optional): Number of days to analyze (default: 7)

**Response:**
```json
{
  "period": "7 days",
  "summary": {
    "positive": 145,
    "negative": 98,
    "neutral": 187,
    "total": 430
  },
  "trend": [
    {
      "date": "2024-01-15",
      "positive": 18,
      "negative": 12,
      "neutral": 24
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:5000/api/analytics/sentiment?days=30
```

#### Get Trend Analysis

**GET** `/analytics/trends`

Get threat trend analysis.

**Query Parameters:**
- `days` (number, optional): Number of days to analyze (default: 30)

**Response:**
```json
{
  "period": "30 days",
  "threats_by_level": {
    "HIGH": 67,
    "MEDIUM": 142,
    "LOW": 198,
    "INFO": 234
  },
  "daily_trends": [
    {
      "date": "2024-01-15",
      "HIGH": 8,
      "MEDIUM": 18,
      "LOW": 25,
      "INFO": 32
    }
  ],
  "top_sources": [
    {
      "name": "Twitter",
      "count": 185
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:5000/api/analytics/trends?days=90
```

---

## Data Models

### Threat Object
```typescript
interface ThreatData {
  id: number;
  source: string;              // "twitter", "reddit", "news", etc.
  url: string;                 // Original source URL
  title: string;               // Threat title
  content: string;             // Full content
  author: string;              // Author/username
  timestamp: string;           // ISO 8601 datetime
  sentiment_score: number;     // -1.0 to 1.0
  sentiment_label: string;     // "positive", "negative", "neutral"
  keywords: string;            // Comma-separated keywords
  threat_level: string;        // "HIGH", "MEDIUM", "LOW", "INFO"
  collected_at: string;        // ISO 8601 datetime
}
```

### Sentiment Summary
```typescript
interface SentimentSummary {
  positive: number;
  negative: number;
  neutral: number;
  total: number;
  positive_ratio: number;
}
```

### Crawl Request
```typescript
interface CrawlRequest {
  sources: string[];           // ["news", "social", "forums"]
  keywords: string[];          // ["malware", "attack"]
  language: string;            // "id", "en", "zh", "ar"
  maxResults: number;          // 10-500
}
```

---

## Status Codes

- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid request
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Rate Limiting

Currently no rate limiting (demo mode).

Production limits:
- 100 requests per minute per IP
- 1000 requests per hour per API key

---

## CORS

CORS enabled for all origins in development.
Production will restrict to specific domains.

---

## Examples

### JavaScript/TypeScript (Axios)

```typescript
import axios from 'axios';

const API_BASE = 'http://localhost:5000/api';

// Get dashboard stats
const stats = await axios.get(`${API_BASE}/dashboard/stats`);
console.log(stats.data);

// Start crawling
const crawlResult = await axios.post(`${API_BASE}/crawl/start`, {
  sources: ['news', 'social'],
  keywords: ['malware', 'ransomware'],
  language: 'en',
  maxResults: 100
});
console.log(crawlResult.data);

// Search threats
const threats = await axios.post(`${API_BASE}/threats/search`, {
  query: 'cyber attack',
  filters: {
    level: 'HIGH'
  }
});
console.log(threats.data);
```

### Python (requests)

```python
import requests

API_BASE = 'http://localhost:5000/api'

# Get dashboard stats
response = requests.get(f'{API_BASE}/dashboard/stats')
stats = response.json()
print(stats)

# Start crawling
crawl_data = {
    'sources': ['news', 'social'],
    'keywords': ['malware', 'ransomware'],
    'language': 'en',
    'maxResults': 100
}
response = requests.post(f'{API_BASE}/crawl/start', json=crawl_data)
result = response.json()
print(result)

# Get recent threats
response = requests.get(f'{API_BASE}/threats/recent?limit=20')
threats = response.json()
print(threats)
```

### cURL

```bash
# Get dashboard stats
curl http://localhost:5000/api/dashboard/stats

# Start crawling with pretty print
curl -X POST http://localhost:5000/api/crawl/start \
  -H "Content-Type: application/json" \
  -d '{
    "sources": ["news", "social"],
    "keywords": ["malware", "cyber attack"],
    "language": "en",
    "maxResults": 100
  }' | jq '.'

# Get high threats only
curl http://localhost:5000/api/threats/level/HIGH | jq '.'

# Search with filters
curl -X POST http://localhost:5000/api/threats/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "malware",
    "filters": {"level": "HIGH"}
  }' | jq '.'
```

---

## Webhook Integration (Planned)

Future versions will support webhooks for real-time notifications:

```json
POST /webhooks/register
{
  "url": "https://your-system.com/webhook",
  "events": ["threat.high", "sentiment.negative"],
  "secret": "your_webhook_secret"
}
```

---

## Support

For API support and questions:
- Documentation: See README.md
- Issues: Contact development team
- Updates: Check CHANGELOG.md

---

**API Version: 1.0.0**
**Last Updated: January 22, 2024**
