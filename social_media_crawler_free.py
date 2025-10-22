"""
Free Social Media Crawler - Web scraping based social media intelligence
Works without API keys for all major platforms
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime, timedelta
from urllib.parse import urljoin, quote_plus
import time
import random
from typing import List, Dict, Optional
import logging

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SocialMediaScraperFree:
    """Free social media scraper using web scraping"""
    
    def __init__(self, use_selenium: bool = False):
        self.use_selenium = use_selenium and SELENIUM_AVAILABLE
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        self.driver = None
        
        if self.use_selenium and not SELENIUM_AVAILABLE:
            logger.warning("Selenium not available. Install with: pip install selenium")
            self.use_selenium = False
        
        if self.use_selenium:
            self._init_selenium()
    
    def _init_selenium(self):
        """Initialize Selenium WebDriver for JavaScript-heavy sites"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            self.driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            logger.warning(f"Selenium initialization failed: {e}. Falling back to requests.")
            self.use_selenium = False
    
    def _random_delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
        """Random delay to avoid rate limiting"""
        time.sleep(random.uniform(min_seconds, max_seconds))
    
    def scrape_twitter_search(self, keyword: str, limit: int = 20) -> List[Dict]:
        """
        Scrape Twitter/X using alternative frontends
        Note: Many Twitter frontends are frequently blocked or go offline
        """
        results = []
        
        twitter_alternatives = [
            {
                'name': 'xcancel',
                'base_url': 'https://xcancel.com',
                'search_path': '/search',
                'params': {'q': keyword, 'f': 'live'}
            },
            {
                'name': 'nitter.cz',
                'base_url': 'https://nitter.cz',
                'search_path': '/search',
                'params': {'f': 'tweets', 'q': keyword}
            },
            {
                'name': 'nitter.poast.org',
                'base_url': 'https://nitter.poast.org',
                'search_path': '/search',
                'params': {'f': 'tweets', 'q': keyword}
            }
        ]
        
        for alt in twitter_alternatives:
            try:
                search_url = f"{alt['base_url']}{alt['search_path']}"
                logger.info(f"Searching Twitter via {alt['name']} for: {keyword}")
                
                response = self.session.get(search_url, params=alt['params'], timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    tweets = soup.find_all(['div', 'article'], 
                                          class_=re.compile('timeline-item|tweet|status'), 
                                          limit=limit)
                    
                    for tweet in tweets:
                        try:
                            username_elem = tweet.find(['a', 'span'], class_=re.compile('username|author'))
                            content_elem = tweet.find(['div', 'p'], class_=re.compile('tweet-content|content|text'))
                            date_elem = tweet.find(['span', 'time'], class_=re.compile('tweet-date|date|time'))
                            
                            if content_elem and content_elem.get_text(strip=True):
                                tweet_data = {
                                    'source': 'twitter',
                                    'platform': 'Twitter/X',
                                    'author': username_elem.text.strip() if username_elem else 'Unknown',
                                    'content': content_elem.get_text(strip=True),
                                    'timestamp': date_elem.text.strip() if date_elem else datetime.now().isoformat(),
                                    'url': f"{alt['base_url']}/search?q={quote_plus(keyword)}",
                                    'collected_at': datetime.now().isoformat(),
                                    'method': f'web_scraping_{alt["name"]}',
                                    'note': 'Scraped from Twitter alternative frontend'
                                }
                                results.append(tweet_data)
                        except Exception as e:
                            logger.debug(f"Error parsing tweet: {e}")
                            continue
                    
                    if results:
                        logger.info(f"Successfully collected tweets from {alt['name']}")
                        break
                elif response.status_code == 403:
                    logger.warning(f"{alt['name']} returned 403 Forbidden - may be rate limited")
                elif response.status_code == 404:
                    logger.warning(f"{alt['name']} returned 404 Not Found - endpoint may have changed")
                else:
                    logger.warning(f"{alt['name']} returned status code {response.status_code}")
                        
            except requests.exceptions.ConnectionError:
                logger.warning(f"Connection error for {alt['name']} - server may be down")
                continue
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout accessing {alt['name']}")
                continue
            except Exception as e:
                logger.warning(f"Error accessing {alt['name']}: {type(e).__name__}")
                continue
            
            self._random_delay()
        
        if not results:
            logger.warning(f"Could not collect tweets for '{keyword}' - all sources failed or returned errors")
            results.append({
                'source': 'twitter',
                'platform': 'Twitter/X',
                'content': f'[Twitter scraping unavailable - keyword: {keyword}]',
                'note': 'Twitter frontends are currently unavailable or blocked. Consider using official Twitter API.',
                'timestamp': datetime.now().isoformat(),
                'collected_at': datetime.now().isoformat(),
                'method': 'fallback_placeholder',
                'status': 'unavailable'
            })
        
        logger.info(f"Collected {len(results)} tweets for '{keyword}'")
        return results
    
    def scrape_reddit_search(self, keyword: str, subreddit: Optional[str] = None, limit: int = 20) -> List[Dict]:
        """
        Scrape Reddit with better error handling and fallback strategies
        """
        results = []
        
        methods = []
        if subreddit:
            methods = [
                f"https://www.reddit.com/r/{subreddit}/search.json?q={quote_plus(keyword)}&restrict_sr=on&limit={limit}",
                f"https://old.reddit.com/r/{subreddit}/search.json?q={quote_plus(keyword)}&restrict_sr=on&limit={limit}",
                f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
            ]
        else:
            methods = [
                f"https://www.reddit.com/search.json?q={quote_plus(keyword)}&limit={limit}",
                f"https://old.reddit.com/search.json?q={quote_plus(keyword)}&limit={limit}",
                f"https://www.reddit.com/r/all/search.json?q={quote_plus(keyword)}&limit={limit}"
            ]
        
        logger.info(f"Searching Reddit for: {keyword}")
        
        for i, search_url in enumerate(methods):
            try:
                custom_headers = self.session.headers.copy()
                custom_headers.update({
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'application/json, text/html, */*',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Referer': 'https://www.reddit.com/',
                    'DNT': '1',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin'
                })
                
                response = self.session.get(search_url, headers=custom_headers, timeout=10)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        
                        for post in data.get('data', {}).get('children', []):
                            try:
                                post_data = post.get('data', {})
                                content = post_data.get('selftext', '')
                                title = post_data.get('title', '')
                                
                                if title or content:
                                    results.append({
                                        'source': 'reddit',
                                        'platform': 'Reddit',
                                        'subreddit': post_data.get('subreddit', ''),
                                        'author': post_data.get('author', 'Unknown'),
                                        'title': title,
                                        'content': content,
                                        'url': f"https://reddit.com{post_data.get('permalink', '')}",
                                        'score': post_data.get('score', 0),
                                        'num_comments': post_data.get('num_comments', 0),
                                        'timestamp': datetime.fromtimestamp(post_data.get('created_utc', 0)).isoformat(),
                                        'collected_at': datetime.now().isoformat(),
                                        'method': 'reddit_json_api'
                                    })
                            except Exception as e:
                                logger.debug(f"Error parsing Reddit post: {e}")
                                continue
                        
                        if results:
                            logger.info(f"Successfully collected Reddit posts using method {i+1}")
                            break
                    except json.JSONDecodeError:
                        logger.warning(f"Reddit returned non-JSON response (method {i+1})")
                        continue
                        
                elif response.status_code == 403:
                    logger.warning(f"Reddit returned 403 Forbidden (method {i+1}) - may be rate limited or blocked")
                elif response.status_code == 404:
                    logger.warning(f"Reddit returned 404 Not Found (method {i+1})")
                else:
                    logger.warning(f"Reddit returned status code {response.status_code} (method {i+1})")
                    
            except requests.exceptions.ConnectionError as e:
                logger.warning(f"Connection error for Reddit (method {i+1})")
                continue
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout accessing Reddit (method {i+1})")
                continue
            except Exception as e:
                logger.warning(f"Error scraping Reddit (method {i+1}): {type(e).__name__}")
                continue
            
            if i < len(methods) - 1:
                self._random_delay(1, 2)
        
        if not results:
            logger.warning(f"Could not collect Reddit posts for '{keyword}' - all methods failed")
            results.append({
                'source': 'reddit',
                'platform': 'Reddit',
                'title': f'Reddit scraping unavailable',
                'content': f'[Reddit API blocked or rate limited - keyword: {keyword}]',
                'note': 'Reddit is blocking scraping attempts. Consider using PRAW with authentication or wait before retrying.',
                'timestamp': datetime.now().isoformat(),
                'collected_at': datetime.now().isoformat(),
                'method': 'fallback_placeholder',
                'status': 'unavailable'
            })
        
        logger.info(f"Collected {len(results)} Reddit posts for '{keyword}'")
        return results
    
    def scrape_facebook_public(self, keyword: str, limit: int = 10) -> List[Dict]:
        """
        Scrape public Facebook posts (limited without login)
        Note: Facebook heavily restricts scraping, results may be limited
        """
        results = []
        
        logger.info(f"Searching Facebook for: {keyword}")
        logger.warning("Facebook scraping is limited without authentication")
        
        try:
            search_url = f"https://www.facebook.com/public?query={quote_plus(keyword)}&type=pages"
            
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                results.append({
                    'source': 'facebook',
                    'platform': 'Facebook',
                    'content': f'Public search for: {keyword}',
                    'note': 'Facebook requires authentication for detailed scraping',
                    'url': search_url,
                    'timestamp': datetime.now().isoformat(),
                    'collected_at': datetime.now().isoformat(),
                    'method': 'limited_scraping'
                })
            elif response.status_code == 403:
                logger.warning(f"Facebook returned 403 Forbidden")
                results.append({
                    'source': 'facebook',
                    'platform': 'Facebook',
                    'content': f'[Facebook scraping blocked - keyword: {keyword}]',
                    'note': 'Facebook blocked the request (403 Forbidden). Authentication required.',
                    'timestamp': datetime.now().isoformat(),
                    'collected_at': datetime.now().isoformat(),
                    'method': 'fallback_placeholder',
                    'status': 'blocked'
                })
            elif response.status_code == 404:
                logger.warning(f"Facebook returned 404 Not Found")
                results.append({
                    'source': 'facebook',
                    'platform': 'Facebook',
                    'content': f'[Facebook endpoint not found - keyword: {keyword}]',
                    'note': 'Facebook endpoint not found (404). API may have changed.',
                    'timestamp': datetime.now().isoformat(),
                    'collected_at': datetime.now().isoformat(),
                    'method': 'fallback_placeholder',
                    'status': 'not_found'
                })
            else:
                logger.warning(f"Facebook returned status code {response.status_code}")
                results.append({
                    'source': 'facebook',
                    'platform': 'Facebook',
                    'content': f'[Facebook scraping failed - status {response.status_code}]',
                    'note': f'Facebook returned unexpected status code: {response.status_code}',
                    'timestamp': datetime.now().isoformat(),
                    'collected_at': datetime.now().isoformat(),
                    'method': 'fallback_placeholder',
                    'status': 'error'
                })
                
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error for Facebook")
            results.append({
                'source': 'facebook',
                'platform': 'Facebook',
                'content': f'[Facebook connection error]',
                'note': 'Could not connect to Facebook servers',
                'timestamp': datetime.now().isoformat(),
                'collected_at': datetime.now().isoformat(),
                'method': 'fallback_placeholder',
                'status': 'connection_error'
            })
        except Exception as e:
            logger.error(f"Error scraping Facebook: {type(e).__name__}")
            results.append({
                'source': 'facebook',
                'platform': 'Facebook',
                'content': f'[Facebook scraping error]',
                'note': f'Error: {type(e).__name__}',
                'timestamp': datetime.now().isoformat(),
                'collected_at': datetime.now().isoformat(),
                'method': 'fallback_placeholder',
                'status': 'error'
            })
        
        return results
    
    def scrape_instagram_public(self, hashtag: str, limit: int = 10) -> List[Dict]:
        """
        Scrape public Instagram posts with multiple fallback services
        """
        results = []
        
        logger.info(f"Searching Instagram for: #{hashtag}")
        
        instagram_alternatives = [
            {
                'name': 'picuki',
                'url': f"https://www.picuki.com/tag/{hashtag}",
                'selector': 'div.box-photo'
            },
            {
                'name': 'imginn',
                'url': f"https://imginn.com/tag/{hashtag}/",
                'selector': 'div.post'
            },
            {
                'name': 'bibliogram',
                'url': f"https://bibliogram.art/u/{hashtag}",
                'selector': 'article'
            }
        ]
        
        for alt in instagram_alternatives:
            try:
                response = self.session.get(alt['url'], timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    posts = soup.find_all(['div', 'article'], 
                                         class_=re.compile('box-photo|post|item'), 
                                         limit=limit)
                    
                    for post in posts:
                        try:
                            description = post.find(['div', 'p'], class_=re.compile('description|caption|text'))
                            
                            if description:
                                results.append({
                                    'source': 'instagram',
                                    'platform': 'Instagram',
                                    'hashtag': hashtag,
                                    'content': description.get_text(strip=True),
                                    'timestamp': datetime.now().isoformat(),
                                    'collected_at': datetime.now().isoformat(),
                                    'method': f'web_scraping_{alt["name"]}'
                                })
                        except Exception as e:
                            logger.debug(f"Error parsing Instagram post: {e}")
                            continue
                    
                    if results:
                        logger.info(f"Successfully collected Instagram posts from {alt['name']}")
                        break
                        
                elif response.status_code == 403:
                    logger.warning(f"{alt['name']} returned 403 Forbidden")
                elif response.status_code == 404:
                    logger.warning(f"{alt['name']} returned 404 Not Found")
                else:
                    logger.warning(f"{alt['name']} returned status code {response.status_code}")
                        
            except requests.exceptions.ConnectionError:
                logger.warning(f"Connection error for {alt['name']}")
                continue
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout accessing {alt['name']}")
                continue
            except Exception as e:
                logger.warning(f"Error accessing {alt['name']}: {type(e).__name__}")
                continue
            
            self._random_delay()
        
        if not results:
            logger.warning(f"Could not collect Instagram posts for #{hashtag} - all sources failed")
            results.append({
                'source': 'instagram',
                'platform': 'Instagram',
                'hashtag': hashtag,
                'content': f'[Instagram scraping unavailable - hashtag: #{hashtag}]',
                'note': 'Instagram frontends are currently unavailable or blocked. Consider using official Instagram API.',
                'timestamp': datetime.now().isoformat(),
                'collected_at': datetime.now().isoformat(),
                'method': 'fallback_placeholder',
                'status': 'unavailable'
            })
        
        logger.info(f"Collected {len(results)} Instagram posts for #{hashtag}")
        return results
    
    def scrape_linkedin_public(self, keyword: str, limit: int = 10) -> List[Dict]:
        """
        Scrape public LinkedIn posts (limited)
        """
        results = []
        
        logger.info(f"Searching LinkedIn for: {keyword}")
        logger.warning("LinkedIn scraping is limited without authentication")
        
        results.append({
            'source': 'linkedin',
            'platform': 'LinkedIn',
            'content': f'Public search for: {keyword}',
            'note': 'LinkedIn requires authentication for detailed scraping',
            'timestamp': datetime.now().isoformat(),
            'collected_at': datetime.now().isoformat(),
            'method': 'limited_scraping'
        })
        
        return results
    
    def scrape_telegram_public(self, channel: str, limit: int = 20) -> List[Dict]:
        """
        Scrape public Telegram channels using web interface
        """
        results = []
        
        try:
            channel_url = f"https://t.me/s/{channel}"
            logger.info(f"Scraping Telegram channel: {channel}")
            
            response = self.session.get(channel_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                messages = soup.find_all('div', class_='tgme_widget_message', limit=limit)
                
                for msg in messages:
                    try:
                        text_elem = msg.find('div', class_='tgme_widget_message_text')
                        date_elem = msg.find('time')
                        
                        if text_elem:
                            results.append({
                                'source': 'telegram',
                                'platform': 'Telegram',
                                'channel': channel,
                                'content': text_elem.get_text(strip=True),
                                'timestamp': date_elem['datetime'] if date_elem else datetime.now().isoformat(),
                                'url': channel_url,
                                'collected_at': datetime.now().isoformat(),
                                'method': 'web_scraping'
                            })
                    except Exception as e:
                        logger.debug(f"Error parsing Telegram message: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Error scraping Telegram: {e}")
        
        logger.info(f"Collected {len(results)} Telegram messages from {channel}")
        return results
    
    def scrape_youtube_comments(self, video_id: str, limit: int = 20) -> List[Dict]:
        """
        Scrape YouTube comments (limited without API)
        """
        results = []
        
        logger.info(f"Scraping YouTube video: {video_id}")
        logger.warning("YouTube comment scraping is limited without API")
        
        results.append({
            'source': 'youtube',
            'platform': 'YouTube',
            'video_id': video_id,
            'note': 'YouTube API recommended for detailed comment scraping',
            'url': f'https://www.youtube.com/watch?v={video_id}',
            'timestamp': datetime.now().isoformat(),
            'collected_at': datetime.now().isoformat(),
            'method': 'limited_scraping'
        })
        
        return results
    
    def scrape_all_platforms(self, keyword: str, platforms: List[str] = None) -> Dict[str, List]:
        """
        Scrape all available platforms for a keyword
        """
        if platforms is None:
            platforms = ['twitter', 'reddit', 'telegram', 'instagram']
        
        all_results = {}
        
        logger.info(f"Starting multi-platform scraping for: {keyword}")
        
        if 'twitter' in platforms:
            all_results['twitter'] = self.scrape_twitter_search(keyword)
            self._random_delay(2, 4)
        
        if 'reddit' in platforms:
            all_results['reddit'] = self.scrape_reddit_search(keyword)
            self._random_delay(2, 4)
        
        if 'facebook' in platforms:
            all_results['facebook'] = self.scrape_facebook_public(keyword)
            self._random_delay(2, 4)
        
        if 'instagram' in platforms:
            all_results['instagram'] = self.scrape_instagram_public(keyword)
            self._random_delay(2, 4)
        
        if 'linkedin' in platforms:
            all_results['linkedin'] = self.scrape_linkedin_public(keyword)
            self._random_delay(2, 4)
        
        if 'telegram' in platforms:
            all_results['telegram'] = []
        
        total_results = sum(len(results) for results in all_results.values())
        logger.info(f"Total results collected: {total_results}")
        
        return all_results
    
    def close(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()


def demo_scraping():
    """Demo function to test free scraping"""
    scraper = SocialMediaScraperFree()
    
    keywords = ['cybersecurity', 'data breach', 'hacking']
    
    for keyword in keywords:
        print(f"\n{'='*60}")
        print(f"Scraping for: {keyword}")
        print('='*60)
        
        results = scraper.scrape_all_platforms(
            keyword=keyword,
            platforms=['twitter', 'reddit']
        )
        
        for platform, data in results.items():
            print(f"\n{platform.upper()}: {len(data)} results")
            if data:
                print(f"Sample: {data[0].get('content', '')[:100]}...")
    
    scraper.close()


if __name__ == "__main__":
    demo_scraping()
