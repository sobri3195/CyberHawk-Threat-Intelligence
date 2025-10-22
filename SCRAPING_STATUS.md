# Social Media Scraping Status & Troubleshooting

## Overview
This document provides information about the current status of social media scraping functionality and how 404/403 errors are handled.

## Current Status (Last Updated: 2025-10-22)

### ✅ Working Platforms

#### Telegram
- **Status**: Fully Functional
- **Method**: Direct web scraping via `t.me/s/{channel}`
- **Limitations**: Public channels only
- **Error Rate**: Low
- **Example**: Can successfully scrape public channels like `durov`

### ⚠️ Limited/Blocked Platforms

#### Twitter/X
- **Status**: Limited Availability
- **Issue**: Most Nitter instances and Twitter frontends are frequently blocked (403 Forbidden)
- **Attempted Alternatives**:
  - xcancel.com - Often returns 403
  - nitter.cz - Often returns 403
  - nitter.poast.org - Often returns 403
- **Fallback Behavior**: Returns placeholder result with status information
- **Recommendation**: Use official Twitter API with valid bearer token for reliable data

#### Reddit
- **Status**: API Blocked
- **Issue**: Reddit blocks unauthenticated JSON API requests (403 Forbidden)
- **Attempted Methods**:
  - `reddit.com/search.json` - Blocked
  - `old.reddit.com/search.json` - Blocked
  - Subreddit-specific JSON endpoints - Blocked
- **Fallback Behavior**: Returns placeholder result with status information
- **Recommendation**: Use PRAW library with authenticated API credentials

#### Instagram
- **Status**: Limited Availability
- **Issue**: Third-party Instagram frontends frequently block requests (403 Forbidden)
- **Attempted Alternatives**:
  - picuki.com - Often returns 403
  - imginn.com - Often returns 403
  - bibliogram.art - Often unreliable
- **Fallback Behavior**: Returns placeholder result with status information
- **Recommendation**: Use official Instagram API with valid access token

#### Facebook
- **Status**: Severely Limited
- **Issue**: Facebook requires authentication for most data access
- **Method**: Basic public search only
- **Limitations**: Very limited data without authentication
- **Recommendation**: Use Facebook Graph API with valid access token

#### LinkedIn
- **Status**: Limited
- **Issue**: LinkedIn heavily restricts public data access
- **Limitations**: Minimal data available without authentication
- **Recommendation**: Use LinkedIn API with valid credentials

## Error Handling

### HTTP Status Codes

The scraper now properly handles and logs various HTTP status codes:

#### 403 Forbidden
- **Meaning**: Server is blocking the request (rate limiting, IP blocking, or requires authentication)
- **Handling**: Logs warning, tries alternative sources, returns fallback result if all fail
- **Common Causes**:
  - Rate limiting by the service
  - IP address blocked
  - User-Agent detected as bot
  - Missing authentication

#### 404 Not Found
- **Meaning**: The requested endpoint doesn't exist
- **Handling**: Logs warning, tries alternative sources
- **Common Causes**:
  - API endpoint changed
  - Service discontinued
  - Invalid URL construction

#### 502 Bad Gateway
- **Meaning**: Proxy/gateway server error
- **Handling**: Logs error, tries alternative sources
- **Common Causes**:
  - Service temporarily down
  - Proxy misconfiguration

#### Connection Errors
- **Meaning**: Cannot establish connection to server
- **Handling**: Logs error, tries alternative sources
- **Common Causes**:
  - Server down
  - Network issues
  - DNS resolution failure

### Fallback Behavior

When all scraping attempts fail, the system returns a placeholder result containing:
- Source platform identification
- Status information (unavailable, blocked, error)
- Descriptive note explaining the issue
- Timestamp of the attempt
- Recommendation for alternative methods

Example fallback result:
```json
{
  "source": "twitter",
  "platform": "Twitter/X",
  "content": "[Twitter scraping unavailable - keyword: cybersecurity]",
  "note": "Twitter frontends are currently unavailable or blocked. Consider using official Twitter API.",
  "timestamp": "2025-10-22T23:32:25.011541",
  "collected_at": "2025-10-22T23:32:25.011552",
  "method": "fallback_placeholder",
  "status": "unavailable"
}
```

## Recommendations

### For Production Use

1. **Use Official APIs**: For reliable data collection, use official platform APIs with proper authentication:
   - Twitter API v2 with Bearer Token
   - Reddit API with PRAW (client_id, client_secret)
   - Instagram Graph API with Access Token
   - Facebook Graph API with Access Token

2. **Rate Limiting**: Implement proper rate limiting to avoid being blocked:
   - Add delays between requests (current: 1-3 seconds)
   - Respect platform rate limits
   - Use exponential backoff on errors

3. **Rotating Proxies**: Consider using rotating proxies or VPN services to avoid IP-based blocking

4. **User-Agent Rotation**: Rotate User-Agent strings to appear more like legitimate browser traffic

5. **Monitor Status**: Regularly check scraping success rates and update alternative sources

### Alternative Data Sources

For cyber threat intelligence specifically, consider these alternatives:

1. **RSS Feeds**: Many platforms offer RSS feeds for public content
2. **Official APIs**: Most reliable but require registration and may have costs
3. **Data Providers**: Commercial threat intelligence feeds (AbuseIPDB, VirusTotal, etc.)
4. **OSINT Tools**: Established tools like TheHarvester, Maltego
5. **News Aggregators**: Security news sites often aggregate threat information

## Troubleshooting

### Problem: All scrapers return "unavailable" status

**Solutions**:
1. Check internet connectivity
2. Verify you're not behind a restrictive firewall
3. Try using a VPN
4. Wait 15-30 minutes and retry (may be temporary rate limiting)
5. Configure official API credentials

### Problem: Specific platform always fails

**Solutions**:
1. Check if the service is down: https://downdetector.com
2. Try accessing the platform directly in a browser
3. Update the scraper with new working alternative frontends
4. Switch to official API for that platform

### Problem: Intermittent failures

**Solutions**:
1. Increase delay between requests
2. Implement retry logic with exponential backoff
3. Use multiple IP addresses/proxies
4. Reduce number of concurrent requests

## Code Examples

### Using with Error Handling

```python
from social_media_crawler_free import SocialMediaScraperFree

scraper = SocialMediaScraperFree()

# Scrape with automatic fallback
results = scraper.scrape_twitter_search('cybersecurity', limit=10)

# Check if scraping was successful
for result in results:
    if result.get('status') == 'unavailable':
        print(f"Warning: {result['note']}")
    else:
        print(f"Content: {result['content']}")

scraper.close()
```

### Filtering Out Fallback Results

```python
# Filter only successful results
successful_results = [
    r for r in results 
    if r.get('status') != 'unavailable' 
    and r.get('method') != 'fallback_placeholder'
]

print(f"Successfully scraped: {len(successful_results)} items")
```

## Monitoring

### Logging

All scraping attempts are logged with appropriate levels:
- `INFO`: Successful operations
- `WARNING`: Non-fatal errors (403, 404, failed alternatives)
- `ERROR`: Fatal errors (connection failures)
- `DEBUG`: Detailed parsing errors

### Metrics to Track

1. **Success Rate**: Percentage of successful scraping attempts per platform
2. **Error Distribution**: Count of each error type (403, 404, connection, etc.)
3. **Response Times**: Average time to complete scraping per platform
4. **Fallback Rate**: How often fallback results are returned

## Future Improvements

1. **Selenium Integration**: Better JavaScript rendering for complex sites
2. **Captcha Solving**: Automated captcha solving for blocked requests
3. **Session Management**: Maintain sessions with cookies for better access
4. **Alternative Frontends**: Continuously discover and add new working alternatives
5. **API Integration**: Seamless fallback from scraping to official APIs
6. **Caching**: Cache results to reduce redundant requests
7. **Distributed Scraping**: Use multiple machines/IPs for better reliability

## Support

For issues or questions:
1. Check this document first
2. Review logs for specific error messages
3. Test individual platforms using the test scripts
4. Consider switching to official APIs for problematic platforms

## References

- [Twitter API Documentation](https://developer.twitter.com/en/docs)
- [Reddit API (PRAW) Documentation](https://praw.readthedocs.io/)
- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api/)
- [Nitter Project](https://github.com/zedeus/nitter)
- [Web Scraping Best Practices](https://scrapinghub.com/guides/web-scraping-best-practices)
