# TNI AU Threat Intelligence System - API Documentation

## Overview

The TNI AU Threat Intelligence System provides a comprehensive REST API for cyber threat intelligence gathering, analysis, and reporting. The system includes:

- **Multi-platform crawler** (Twitter, Reddit, Facebook, Instagram, LinkedIn, Telegram)
- **Threat intelligence analysis** with free API integrations
- **Sentiment analysis** (multilanguage support)
- **Real-time threat monitoring**
- **Automated reporting**

## Architecture

The system runs two API servers:

1. **Python Flask API** (Port 5001) - Main threat intelligence engine
2. **Node.js Express API** (Port 5000) - Frontend API with mock data support

## Getting Started

### Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install
```

### Start the APIs

```bash
# Start both APIs
./start_api.sh

# Or start individually:
# Python API: python3 api.py
# Node.js API: npm run server
```

## API Endpoints

### Health Check

#### GET `/api/health`

Check API status and available features.

**Response:**
```json
{
  "status": "online",
  "service": "TNI AU Threat Intelligence System",
  "version": "2.0.0",
  "timestamp": "2024-01-01T00:00:00",
  "features": {
    "crawler": true,
    "threat_analysis": true,
    "sentiment_analysis": true,
    "free_scraping": true,
    "threat_intel_apis": true,
    "all_platforms_enabled": true
  }
}
```

---

### Crawler Operations

#### POST `/api/crawler/start`

Start the threat intelligence crawler.

**Request Body:**
```json
{
  "sources": ["twitter", "reddit", "facebook", "instagram", "linkedin", "telegram"],
  "keywords": [
    "cyber attack",
    "malware",
    "ransomware",
    "data breach",
    "hacking"
  ],
  "subreddits": ["cybersecurity", "netsec", "InfoSec"],
  "telegram_channels": ["security", "cybersec"],
  "news_urls": [
    "https://www.antaranews.com/berita/teknologi",
    "https://tekno.kompas.com/keamanan-siber"
  ]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Crawler started successfully",
  "platforms_enabled": [
    "Twitter/X",
    "Reddit",
    "Facebook",
    "Instagram",
    "LinkedIn",
    "Telegram",
    "News Sites"
  ]
}
```

#### GET `/api/crawler/status`

Get current crawler status.

**Response:**
```json
{
  "inProgress": false,
  "progress": 100,
  "message": "Completed! Collected 150 items",
  "lastRun": "2024-01-01T00:00:00",
  "allPlatformsEnabled": true,
  "freeScrapingEnabled": true
}
```

---

### Threat Management

#### GET `/api/threats/recent`

Get recent threats from database.

**Query Parameters:**
- `limit` (optional, default: 50) - Maximum number of results
- `days` (optional, default: 7) - Look back period in days

**Response:**
```json
[
  {
    "id": 1,
    "source": "twitter",
    "url": "https://twitter.com/...",
    "title": "HIGH: cyber attack",
    "content": "Critical vulnerability discovered...",
    "author": "analyst_123",
    "timestamp": "2024-01-01T00:00:00",
    "sentiment_score": -0.5,
    "sentiment_label": "negative",
    "keywords": "{\"ip_addresses\": [], \"domains\": []}",
    "threat_level": "HIGH",
    "collected_at": "2024-01-01T00:00:00"
  }
]
```

#### POST `/api/threats/search`

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

**Response:** Array of threat objects (same format as `/api/threats/recent`)

#### GET `/api/threats/level/<level>`

Get threats filtered by threat level.

**Parameters:**
- `level` - Threat level: HIGH, MEDIUM, LOW, INFO

**Response:** Array of threat objects

#### GET `/api/threats/stats`

Get threat statistics.

**Query Parameters:**
- `days` (optional, default: 7) - Statistics period in days

**Response:**
```json
{
  "total": 150,
  "by_threat_level": {
    "HIGH": 25,
    "MEDIUM": 50,
    "LOW": 50,
    "INFO": 25
  },
  "by_sentiment": {
    "positive": 30,
    "negative": 60,
    "neutral": 60
  },
  "top_sources": [
    {"source": "twitter", "count": 50},
    {"source": "reddit", "count": 40}
  ],
  "period_days": 7
}
```

---

### Dashboard

#### GET `/api/dashboard/summary`

Get dashboard summary data.

**Query Parameters:**
- `days` (optional, default: 7) - Summary period in days

**Response:**
```json
{
  "totalThreats": 150,
  "highPriorityThreats": 25,
  "activeSources": 6,
  "avgSentiment": -0.15,
  "lastUpdate": "2024-01-01T00:00:00"
}
```

#### GET `/api/dashboard/timeline`

Get threat timeline data for charts.

**Query Parameters:**
- `days` (optional, default: 30) - Timeline period in days

**Response:**
```json
[
  {
    "date": "2024-01-01",
    "HIGH": 5,
    "MEDIUM": 10,
    "LOW": 15,
    "INFO": 5
  }
]
```

---

### Analytics

#### GET `/api/analytics/sentiment`

Get sentiment analysis data.

**Query Parameters:**
- `days` (optional, default: 7) - Analysis period in days

**Response:**
```json
{
  "distribution": {
    "positive": {
      "count": 30,
      "avgScore": 0.45
    },
    "negative": {
      "count": 60,
      "avgScore": -0.35
    },
    "neutral": {
      "count": 60,
      "avgScore": 0.05
    }
  },
  "total": 150
}
```

#### GET `/api/analytics/trends`

Get trending keywords and topics.

**Query Parameters:**
- `days` (optional, default: 7) - Trend analysis period in days

**Response:**
```json
[
  {
    "keywords": "malware, ransomware",
    "count": 25
  },
  {
    "keywords": "cyber attack, breach",
    "count": 20
  }
]
```

---

### Threat Intelligence APIs

#### GET `/api/threat-intel/check-ip/<ip_address>`

Check IP reputation using multiple threat intelligence sources.

**Example:** `/api/threat-intel/check-ip/8.8.8.8`

**Response:**
```json
{
  "ip": "8.8.8.8",
  "reputation": {
    "ipinfo": {
      "ip": "8.8.8.8",
      "country": "US",
      "city": "Mountain View",
      "org": "AS15169 Google LLC",
      "timezone": "America/Los_Angeles"
    },
    "ipapi": {
      "ip": "8.8.8.8",
      "country": "United States",
      "city": "Mountain View",
      "threat_level": "INFO",
      "asn": "AS15169"
    }
  },
  "timestamp": "2024-01-01T00:00:00"
}
```

#### GET `/api/threat-intel/check-domain/<domain>`

Check domain reputation.

**Example:** `/api/threat-intel/check-domain/example.com`

**Response:**
```json
{
  "domain": "example.com",
  "reputation": {
    "whois": {
      "registrar": "Example Registrar",
      "created_date": "1995-08-14"
    }
  },
  "timestamp": "2024-01-01T00:00:00"
}
```

#### GET `/api/threat-intel/feeds`

Get latest threat intelligence feeds.

**Response:**
```json
{
  "feeds": [
    {
      "source": "Emerging Threats",
      "type": "compromised_hosts",
      "data": "...",
      "timestamp": "2024-01-01T00:00:00"
    }
  ],
  "timestamp": "2024-01-01T00:00:00"
}
```

---

### Reports

#### GET `/api/reports/daily`

Generate daily threat intelligence report.

**Query Parameters:**
- `date` (optional) - Report date in ISO format (default: today)

**Response:**
```json
{
  "date": "2024-01-01",
  "summary": {
    "HIGH": 25,
    "MEDIUM": 50,
    "LOW": 50,
    "INFO": 25
  },
  "by_source": {
    "twitter": 50,
    "reddit": 40,
    "facebook": 30,
    "instagram": 30
  },
  "sentiment": {
    "positive": 30,
    "negative": 60,
    "neutral": 60
  }
}
```

#### GET `/api/reports/strategic`

Generate strategic analysis report.

**Query Parameters:**
- `days` (optional, default: 30) - Analysis period in days

**Response:**
```json
{
  "period": "30 days",
  "total_events": 4500,
  "high_threats": 750,
  "avg_daily_events": 150,
  "sentiment_trend": -0.15,
  "recommendations": [
    "PRIORITAS TINGGI: Peningkatan signifikan ancaman level tinggi",
    "PERHATIAN: Sentimen negatif dominan, perlu monitoring intensif"
  ]
}
```

---

### Configuration

#### GET `/api/config/sources`

Get list of available data sources and features.

**Response:**
```json
{
  "sources": [
    {"id": "twitter", "name": "Twitter/X", "enabled": true, "free": true},
    {"id": "reddit", "name": "Reddit", "enabled": true, "free": true},
    {"id": "facebook", "name": "Facebook", "enabled": true, "free": true},
    {"id": "instagram", "name": "Instagram", "enabled": true, "free": true},
    {"id": "linkedin", "name": "LinkedIn", "enabled": true, "free": true},
    {"id": "telegram", "name": "Telegram", "enabled": true, "free": true},
    {"id": "news", "name": "News Sites", "enabled": true, "free": true},
    {"id": "forums", "name": "Forums", "enabled": true, "free": true}
  ],
  "features": {
    "all_platforms_enabled": true,
    "free_scraping": true,
    "no_api_keys_required": true,
    "threat_intel_apis": true,
    "sentiment_analysis": true,
    "multilanguage": true
  }
}
```

---

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200` - Success
- `400` - Bad Request (invalid parameters)
- `404` - Not Found
- `500` - Internal Server Error

Error responses include a message:

```json
{
  "error": "Error description",
  "message": "Detailed error message"
}
```

---

## Features

### ✅ All Platforms Enabled

- **Twitter/X** - Free scraping via Nitter
- **Reddit** - Free JSON API
- **Facebook** - Public data scraping
- **Instagram** - Public hashtag scraping
- **LinkedIn** - Public post scraping
- **Telegram** - Public channel scraping
- **News Sites** - BeautifulSoup scraping
- **Forums** - Public forum scraping

### ✅ Threat Intelligence

- **Free APIs** integrated:
  - IPInfo - IP geolocation
  - IPAPI - IP information
  - Emerging Threats - Threat feeds
  - WhoisXML - Domain reputation

### ✅ Analysis Features

- **Sentiment Analysis** - TextBlob-based multilanguage
- **Threat Level Assessment** - Keyword-based scoring
- **IOC Extraction** - IP, domain, email, hash detection
- **Trend Analysis** - pandas-based analytics

### ✅ No API Keys Required

All social media crawling works without API keys using free scraping methods.

---

## Testing

Run the full system test:

```bash
python3 test_full_system.py
```

This tests:
1. API initialization
2. System initialization
3. Crawler functionality
4. Threat intelligence APIs
5. Database operations
6. Reporting features

---

## Examples

### Example 1: Start Crawler

```bash
curl -X POST http://localhost:5001/api/crawler/start \
  -H "Content-Type: application/json" \
  -d '{
    "sources": ["twitter", "reddit"],
    "keywords": ["cyber attack", "malware"]
  }'
```

### Example 2: Search Threats

```bash
curl -X POST http://localhost:5001/api/threats/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "ransomware",
    "filters": {
      "level": "HIGH"
    }
  }'
```

### Example 3: Check IP Reputation

```bash
curl http://localhost:5001/api/threat-intel/check-ip/8.8.8.8
```

### Example 4: Get Dashboard Summary

```bash
curl http://localhost:5001/api/dashboard/summary?days=7
```

---

## Support

For issues or questions, please refer to the main documentation or contact the development team.

---

## License

TNI AU Cyber Threat Intelligence System - Internal Use Only
