# 🚀 Auto-Setup Guide - Free API & All Social Media Crawlers

## ✨ ALL FEATURES ENABLED

This system now includes **automatic API configuration** and **free social media crawling** for ALL major platforms without requiring API keys!

## 🎯 What's Enabled

### Social Media Platforms (ALL ENABLED)
✅ **Twitter/X** - Free scraping via Nitter (no API key needed)  
✅ **Reddit** - Free scraping via JSON API (no authentication)  
✅ **Facebook** - Public post scraping  
✅ **Instagram** - Public hashtag scraping  
✅ **LinkedIn** - Public post scraping  
✅ **Telegram** - Public channel scraping  

### Additional Sources
✅ News sites crawling  
✅ Forums scraping  
✅ Dark web monitoring (requires Tor)  
✅ Free threat intelligence APIs  

## 🔧 Auto-Configuration

### Method 1: Automatic Setup (Recommended)

The system automatically generates demo API credentials and enables web scraping:

```bash
# Just run the main script - it auto-configures everything!
python cyber_threat_intel.py
```

The system will:
1. ✅ Auto-generate demo API credentials
2. ✅ Enable free web scraping for all platforms
3. ✅ Configure free threat intelligence APIs
4. ✅ Start collecting data immediately

### Method 2: Manual API Key Management

If you have real API keys, you can configure them:

```bash
# Initialize API manager
python free_api_manager.py
```

Then edit `api_config.json`:

```json
{
  "twitter": {
    "bearer_token": "your_real_token",
    "type": "real"
  },
  "reddit": {
    "client_id": "your_client_id",
    "client_secret": "your_client_secret",
    "user_agent": "TNI-AU-ThreatIntel/1.0",
    "type": "real"
  }
}
```

## 📋 Features Comparison

| Platform | Free Scraping | API Method | Rate Limit |
|----------|---------------|------------|------------|
| Twitter/X | ✅ Unlimited | Via Nitter | No limit |
| Reddit | ✅ Unlimited | JSON API | No auth needed |
| Facebook | ⚠️ Limited | Web scraping | Limited |
| Instagram | ✅ Good | Via Picuki | Moderate |
| LinkedIn | ⚠️ Limited | Web scraping | Limited |
| Telegram | ✅ Full | Web interface | No limit |

## 🎮 Usage Examples

### Example 1: Collect from ALL platforms

```python
from cyber_threat_intel import ThreatIntelSystem

# Auto-initialize with free crawlers
system = ThreatIntelSystem()

sources = {
    'twitter': True,
    'reddit': True,
    'facebook': True,
    'instagram': True,
    'linkedin': True,
    'telegram': True,
    'keywords': ['cybersecurity', 'data breach', 'hacking']
}

# Collect from all platforms
data = system.collect_intelligence(sources)
print(f"Collected {len(data)} items from all platforms!")
```

### Example 2: Use Free API Manager

```python
from free_api_manager import FreeAPIManager

# Initialize manager
manager = FreeAPIManager()

# Auto-setup all APIs
configs = manager.auto_setup_all()

# Check configuration
print(f"Twitter: {configs['twitter']['type']}")
print(f"Reddit: {configs['reddit']['type']}")
```

### Example 3: Free Social Media Scraper

```python
from social_media_crawler_free import SocialMediaScraperFree

# Initialize free scraper
scraper = SocialMediaScraperFree()

# Scrape Twitter
tweets = scraper.scrape_twitter_search('cybersecurity', limit=20)

# Scrape Reddit
posts = scraper.scrape_reddit_search('hacking', subreddit='cybersecurity')

# Scrape Instagram
ig_posts = scraper.scrape_instagram_public('cybersecurity')

# Scrape ALL platforms at once
all_data = scraper.scrape_all_platforms(
    keyword='data breach',
    platforms=['twitter', 'reddit', 'instagram', 'telegram']
)
```

## 🆓 Free Threat Intelligence APIs

The system includes integration with free threat intel APIs:

- **AbuseIPDB** - IP reputation (1000 requests/day)
- **VirusTotal** - File/URL scanning (500 requests/day)
- **Shodan** - Device search (100 results/month)
- **GreyNoise** - Internet noise detection (free tier)
- **IPInfo** - IP geolocation (50k requests/month)

```python
from free_api_manager import FreeThreatIntelAPIs

apis = FreeThreatIntelAPIs()

# Check IP reputation
result = apis.check_ip_reputation('8.8.8.8')

# Get threat feeds
feeds = apis.get_threat_feeds()
```

## 🔐 Security & Privacy

### Web Scraping Best Practices
- ✅ Random delays between requests
- ✅ Rotating user agents
- ✅ Respects robots.txt
- ✅ Rate limiting protection
- ✅ Error handling and retries

### Data Privacy
- 🔒 Only collects PUBLIC data
- 🔒 No authentication bypass
- 🔒 No personal data collection
- 🔒 Complies with platform ToS for public data

## 🚦 Rate Limiting

The free scraper includes automatic rate limiting:

```python
# Built-in delays
scraper._random_delay(min_seconds=1.0, max_seconds=3.0)

# Respects platform limits
scraper.scrape_twitter_search('keyword', limit=20)  # Limited to prevent abuse
```

## 🛠️ Troubleshooting

### Issue: "Free crawler modules not found"
**Solution:** Ensure `free_api_manager.py` and `social_media_crawler_free.py` are in the project directory.

### Issue: Selenium not working
**Solution:** Install ChromeDriver:
```bash
# Ubuntu/Debian
sudo apt-get install chromium-chromedriver

# Or disable Selenium
scraper = SocialMediaScraperFree(use_selenium=False)
```

### Issue: Twitter/Nitter not accessible
**Solution:** The scraper tries multiple Nitter instances automatically. If all fail, it will skip Twitter.

### Issue: Rate limiting errors
**Solution:** Increase delays:
```python
scraper._random_delay(min_seconds=3.0, max_seconds=5.0)
```

## 📊 Configuration Files

### api_config.json
Auto-generated configuration file containing:
- API credentials (real or demo)
- Service types (real/demo)
- Web scraping flags
- Creation timestamps

### threat_intel.db
SQLite database storing:
- Crawled data
- Threat indicators
- Sentiment analysis
- Trend data

## 🎯 Performance Tips

1. **Parallel Crawling**: The system collects from multiple platforms sequentially. For faster collection, consider async operations.

2. **Caching**: Results are cached in the database to avoid duplicate requests.

3. **Selective Sources**: Enable only the platforms you need:
```python
sources = {
    'twitter': True,
    'reddit': True,
    'facebook': False,  # Disable if not needed
    'instagram': False,
    'linkedin': False,
    'telegram': True
}
```

4. **Keyword Optimization**: Use specific keywords to reduce noise:
```python
keywords = [
    'TNI AU cyber attack',  # Specific
    'Indonesian military threat'  # Better than just 'threat'
]
```

## 🔄 Update & Maintenance

The free scraper may need updates if platforms change their structure:

```bash
# Check for updates
git pull origin main

# Re-initialize API manager
python free_api_manager.py
```

## 📞 Support

For issues or questions:
1. Check troubleshooting section
2. Review error logs
3. Verify internet connectivity
4. Test with a single platform first

## 🎓 Learning Resources

- [Web Scraping Ethics](https://docs.python.org/3/library/urllib.robotparser.html)
- [Nitter Documentation](https://github.com/zedeus/nitter)
- [OSINT Best Practices](https://osintframework.com/)
- [Threat Intelligence Fundamentals](https://www.mitre.org/publications/technical-papers)

## ✨ Summary

With this auto-setup system, you can:
- ✅ Start collecting intelligence immediately
- ✅ No API keys required for most platforms
- ✅ ALL social media platforms enabled
- ✅ Free threat intelligence integration
- ✅ Automatic configuration and setup
- ✅ Production-ready out of the box

**Just run `python cyber_threat_intel.py` and start collecting!** 🚀
