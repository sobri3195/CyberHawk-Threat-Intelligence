# TNI AU Cyber Threat Intelligence System - Complete Guide

## 🚀 Overview

The TNI AU Cyber Threat Intelligence System is a comprehensive platform for cyber threat intelligence gathering, analysis, and reporting. It combines:

- **Multi-platform crawler** (7+ platforms)
- **Free API integration** (no API keys required)
- **Threat intelligence analysis** with sentiment analysis
- **Real-time monitoring** with automated reporting
- **REST API** for integration with other systems

## ✨ Key Features

### 🌐 All Platforms Enabled

✅ **Twitter/X** - Free scraping via Nitter  
✅ **Reddit** - Free JSON API  
✅ **Facebook** - Public data scraping  
✅ **Instagram** - Public hashtag scraping  
✅ **LinkedIn** - Public post scraping  
✅ **Telegram** - Public channel scraping  
✅ **News Sites** - BeautifulSoup scraping  
✅ **Forums** - Public forum scraping  

### 🔍 Threat Intelligence

✅ **Free APIs** integrated:
- IPInfo - IP geolocation
- IPAPI - IP information  
- Emerging Threats - Threat feeds
- WhoisXML - Domain reputation

✅ **Analysis Features**:
- Sentiment Analysis (multilanguage)
- Threat Level Assessment
- IOC Extraction (IP, domain, email, hash)
- Trend Analysis with pandas

### 🎯 No API Keys Required

All social media crawling works without API keys using free scraping methods!

---

## 📦 Installation

### Prerequisites

- Python 3.8+
- Node.js 16+
- SQLite3
- Virtual environment (recommended)

### Quick Setup

```bash
# 1. Clone the repository
cd /path/to/project

# 2. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install Node.js dependencies
npm install

# 5. Initialize the system
python3 free_api_manager.py
```

---

## 🚀 Quick Start

### Option 1: Run Full System Test

```bash
python3 test_full_system.py
```

This will test all components:
- ✅ API initialization
- ✅ System initialization
- ✅ Crawler functionality
- ✅ Threat intelligence APIs
- ✅ Database operations
- ✅ Reporting features

### Option 2: Run Interactive Demo

```bash
python3 demo_all_features.py
```

This will demonstrate:
1. Multi-platform crawler
2. Threat list search & analysis
3. Threat intelligence API integration
4. Automated reporting

### Option 3: Start API Servers

```bash
# Start both Python Flask API and Node.js Express API
./start_api.sh

# Or start individually:
# Python API (port 5001)
python3 api.py

# Node.js API (port 5000)
npm run server
```

### Option 4: Run Main System

```bash
python3 cyber_threat_intel.py
```

---

## 📡 API Usage

### Check API Health

```bash
# Python API
curl http://localhost:5001/api/health

# Node.js API
curl http://localhost:5000/api/health
```

### Start Crawler

```bash
curl -X POST http://localhost:5001/api/crawler/start \
  -H "Content-Type: application/json" \
  -d '{
    "sources": ["twitter", "reddit", "facebook"],
    "keywords": ["cyber attack", "malware", "ransomware"]
  }'
```

### Search Threats

```bash
curl -X POST http://localhost:5001/api/threats/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "malware",
    "filters": {
      "level": "HIGH"
    }
  }'
```

### Check IP Reputation

```bash
curl http://localhost:5001/api/threat-intel/check-ip/8.8.8.8
```

### Get Dashboard Summary

```bash
curl http://localhost:5001/api/dashboard/summary?days=7
```

**See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete API reference.**

---

## 🎯 Use Cases

### 1. Automated Threat Monitoring

Set up automated crawling to continuously monitor threats:

```python
from cyber_threat_intel import ThreatIntelSystem
from free_api_manager import initialize_all_apis

# Initialize
api_manager = initialize_all_apis()
system = ThreatIntelSystem()

# Configure sources
sources = {
    'twitter': True,
    'reddit': True,
    'keywords': ['cyber attack', 'malware'],
    'subreddits': ['cybersecurity', 'netsec']
}

# Run collection cycle
result = system.run_collection_cycle(sources)
print(f"Collected {result['collected']} items")
```

### 2. Threat Intelligence Search

Search and analyze threats in the database:

```python
# Search by threat level
cursor = system.db.conn.cursor()
high_threats = cursor.execute('''
    SELECT * FROM crawled_data
    WHERE threat_level = 'HIGH'
    ORDER BY collected_at DESC
    LIMIT 10
''').fetchall()

# Search by keyword
keyword_threats = cursor.execute('''
    SELECT * FROM crawled_data
    WHERE content LIKE '%ransomware%'
''').fetchall()
```

### 3. IP/Domain Reputation Check

Check reputation using free threat intel APIs:

```python
from free_api_manager import FreeThreatIntelAPIs

threat_apis = FreeThreatIntelAPIs()

# Check IP
ip_result = threat_apis.check_ip_reputation('8.8.8.8')
print(ip_result)

# Check domain
domain_result = threat_apis.check_domain_reputation('example.com')
print(domain_result)
```

### 4. Automated Reporting

Generate reports for strategic analysis:

```python
# Daily report
daily_report = system.reporter.generate_daily_report()

# Strategic analysis (30 days)
strategic = system.reporter.generate_strategic_analysis(days=30)

# Export to file
system.reporter.export_report(
    strategic,
    'threat_report_2024.json',
    format='json'
)
```

---

## 📊 Database Schema

### crawled_data

Stores all collected threat intelligence data:

```sql
CREATE TABLE crawled_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,                    -- Data source (twitter, reddit, etc)
    url TEXT,                       -- Original URL
    title TEXT,                     -- Title/headline
    content TEXT,                   -- Full content
    author TEXT,                    -- Author/username
    timestamp DATETIME,             -- Original post time
    sentiment_score REAL,           -- -1.0 to 1.0
    sentiment_label TEXT,           -- positive/negative/neutral
    keywords TEXT,                  -- JSON with IOCs
    threat_level TEXT,              -- HIGH/MEDIUM/LOW/INFO
    collected_at DATETIME           -- Collection time
)
```

### threat_indicators

Stores extracted indicators of compromise:

```sql
CREATE TABLE threat_indicators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    indicator_type TEXT,            -- IP, domain, email, hash
    indicator_value TEXT,           -- Actual value
    threat_category TEXT,           -- Category
    confidence_score REAL,          -- 0.0 to 1.0
    first_seen DATETIME,
    last_seen DATETIME,
    source TEXT
)
```

---

## 🔧 Configuration

### API Configuration

API configurations are stored in `api_config.json`:

```json
{
  "twitter": {
    "bearer_token": "DEMO_TWITTER_...",
    "type": "demo",
    "use_scraping": true
  },
  "reddit": {
    "client_id": "...",
    "client_secret": "...",
    "user_agent": "TNI-AU-ThreatIntel/1.0",
    "type": "demo",
    "use_scraping": true
  },
  "threat_intel_apis": {
    "abuseipdb": {...},
    "virustotal": {...},
    "shodan": {...}
  }
}
```

### System Configuration

System settings in `system_config.json`:

```json
{
  "crawler": {
    "max_results_per_source": 100,
    "timeout": 30,
    "rate_limit_delay": 2
  },
  "analysis": {
    "threat_keywords": {...},
    "sentiment_threshold": 0.1
  }
}
```

---

## 📁 Project Structure

```
/home/engine/project/
├── api.py                          # Flask REST API
├── cyber_threat_intel.py           # Main threat intel system
├── free_api_manager.py             # API credential manager
├── social_media_crawler_free.py    # Free social media scraper
├── test_full_system.py             # System test suite
├── demo_all_features.py            # Interactive demo
├── start_api.sh                    # API startup script
├── requirements.txt                # Python dependencies
├── package.json                    # Node.js dependencies
├── threat_intel.db                 # SQLite database
├── api_config.json                 # API configuration
├── server/                         # Node.js API server
│   ├── index.js
│   ├── routes/
│   └── controllers/
├── src/                            # Frontend source
└── docs/
    ├── API_DOCUMENTATION.md        # Complete API docs
    ├── COMPLETE_GUIDE.md           # This file
    └── ...
```

---

## 🧪 Testing

### Run Full Test Suite

```bash
python3 test_full_system.py
```

Expected output:
```
✅ Api Init                       PASSED
✅ System Init                    PASSED
✅ Crawler                        PASSED
✅ Threat Intel                   PASSED
✅ Database                       PASSED
✅ Reporting                      PASSED

🎯 Overall: 6/6 tests passed (100%)
🎉 ALL TESTS PASSED! System is fully functional.
```

### Run Individual Tests

```python
# Test crawler only
from cyber_threat_intel import ThreatIntelSystem
system = ThreatIntelSystem()

sources = {
    'twitter': True,
    'keywords': ['test']
}
result = system.run_collection_cycle(sources)
print(f"Success! Collected {result['collected']} items")
```

---

## 🐛 Troubleshooting

### Issue: 404 Error on API Endpoints

**Solution:**
```bash
# Make sure both APIs are running
./start_api.sh

# Check API health
curl http://localhost:5001/api/health
curl http://localhost:5000/api/health
```

### Issue: Crawler Not Finding Data

**Possible causes:**
1. No internet connection
2. Target sites blocking requests
3. Rate limiting

**Solution:**
```python
# Use demo mode for testing
system.run_collection_cycle(sources)

# Or check crawler status
from api import crawler_status
print(crawler_status)
```

### Issue: Database Locked

**Solution:**
```bash
# Close all connections
python3 -c "import sqlite3; conn = sqlite3.connect('threat_intel.db'); conn.close()"

# Or delete and recreate
rm threat_intel.db
python3 -c "from cyber_threat_intel import ThreatIntelDatabase; ThreatIntelDatabase()"
```

### Issue: Import Errors

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check Python version
python3 --version  # Should be 3.8+
```

---

## 📈 Performance Tips

### 1. Optimize Crawler Performance

```python
# Limit results per source
sources = {
    'twitter': True,
    'max_results': 50,  # Instead of 100
    'keywords': ['test'][:5]  # Limit keywords
}
```

### 2. Database Optimization

```sql
-- Create indexes for faster queries
CREATE INDEX idx_threat_level ON crawled_data(threat_level);
CREATE INDEX idx_collected_at ON crawled_data(collected_at);
CREATE INDEX idx_source ON crawled_data(source);
```

### 3. API Rate Limiting

```python
# Add delays between requests
import time
for source in sources:
    result = crawler.crawl(source)
    time.sleep(2)  # 2 second delay
```

---

## 🔒 Security Considerations

### 1. API Security

- Use HTTPS in production
- Implement API key authentication
- Rate limit API endpoints
- Sanitize all inputs

### 2. Database Security

- Use prepared statements (already implemented)
- Regular backups
- Encrypt sensitive data
- Restrict database access

### 3. Crawler Security

- Respect robots.txt
- Use appropriate User-Agent
- Implement rate limiting
- Handle errors gracefully

---

## 📚 Additional Documentation

- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Complete API reference
- [FEATURES.md](FEATURES.md) - Detailed feature list
- [DEVELOPMENT.md](DEVELOPMENT.md) - Development guide
- [QUICK_START.md](QUICK_START.md) - Quick start guide

---

## 🤝 Support

For issues or questions:

1. Check the troubleshooting section above
2. Review the API documentation
3. Run the test suite to identify issues
4. Check logs: `flask_api.log` and `node_api.log`

---

## 📄 License

TNI AU Cyber Threat Intelligence System - Internal Use Only

---

## 🎉 Summary

This system provides:

✅ **Multi-platform crawler** - 7+ platforms, no API keys needed  
✅ **Threat intelligence** - Free APIs for IP/domain reputation  
✅ **Sentiment analysis** - Multilanguage support  
✅ **Automated reporting** - Daily and strategic reports  
✅ **REST API** - Full API for integration  
✅ **Database storage** - SQLite with proper schema  
✅ **Easy deployment** - One-command startup  

**Get started now:**

```bash
# Run the full test
python3 test_full_system.py

# Or run the interactive demo
python3 demo_all_features.py

# Or start the API servers
./start_api.sh
```

🚀 **All features enabled and ready to use!**
