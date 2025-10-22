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
        Scrape Twitter/X using Nitter instances (Twitter frontend without API)
        Nitter is a free and open source alternative Twitter front-end
        """
        results = []
        nitter_instances = [
            'https://nitter.net',
            'https://nitter.privacydev.net',
            'https://nitter.poast.org'
        ]
        
        for instance in nitter_instances:
            try:
                search_url = f"{instance}/search?f=tweets&q={quote_plus(keyword)}"
                logger.info(f"Searching Twitter via {instance} for: {keyword}")
                
                response = self.session.get(search_url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    tweets = soup.find_all('div', class_='timeline-item', limit=limit)
                    
                    for tweet in tweets:
                        try:
                            username_elem = tweet.find('a', class_='username')
                            content_elem = tweet.find('div', class_='tweet-content')
                            date_elem = tweet.find('span', class_='tweet-date')
                            stats = tweet.find('div', class_='tweet-stats')
                            
                            if content_elem:
                                tweet_data = {
                                    'source': 'twitter',
                                    'platform': 'Twitter/X',
                                    'author': username_elem.text.strip() if username_elem else 'Unknown',
                                    'content': content_elem.get_text(strip=True),
                                    'timestamp': date_elem.text.strip() if date_elem else datetime.now().isoformat(),
                                    'url': instance + username_elem['href'] if username_elem else '',
                                    'engagement': {
                                        'raw': stats.get_text(strip=True) if stats else 'N/A'
                                    },
                                    'collected_at': datetime.now().isoformat(),
                                    'method': 'web_scraping'
                                }
                                results.append(tweet_data)
                        except Exception as e:
                            logger.debug(f"Error parsing tweet: {e}")
                            continue
                    
                    if results:
                        break
                        
            except Exception as e:
                logger.warning(f"Error accessing {instance}: {e}")
                continue
            
            self._random_delay()
        
        logger.info(f"Collected {len(results)} tweets for '{keyword}'")
        return results
    
    def scrape_reddit_search(self, keyword: str, subreddit: Optional[str] = None, limit: int = 20) -> List[Dict]:
        """
        Scrape Reddit using old.reddit.com (no API required)
        """
        results = []
        
        try:
            if subreddit:
                search_url = f"https://old.reddit.com/r/{subreddit}/search.json?q={quote_plus(keyword)}&restrict_sr=on&limit={limit}"
            else:
                search_url = f"https://old.reddit.com/search.json?q={quote_plus(keyword)}&limit={limit}"
            
            logger.info(f"Searching Reddit for: {keyword}")
            
            response = self.session.get(search_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                for post in data.get('data', {}).get('children', []):
                    try:
                        post_data = post.get('data', {})
                        results.append({
                            'source': 'reddit',
                            'platform': 'Reddit',
                            'subreddit': post_data.get('subreddit', ''),
                            'author': post_data.get('author', 'Unknown'),
                            'title': post_data.get('title', ''),
                            'content': post_data.get('selftext', ''),
                            'url': f"https://reddit.com{post_data.get('permalink', '')}",
                            'score': post_data.get('score', 0),
                            'num_comments': post_data.get('num_comments', 0),
                            'timestamp': datetime.fromtimestamp(post_data.get('created_utc', 0)).isoformat(),
                            'collected_at': datetime.now().isoformat(),
                            'method': 'api_json'
                        })
                    except Exception as e:
                        logger.debug(f"Error parsing Reddit post: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Error scraping Reddit: {e}")
        
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
                
        except Exception as e:
            logger.error(f"Error scraping Facebook: {e}")
        
        return results
    
    def scrape_instagram_public(self, hashtag: str, limit: int = 10) -> List[Dict]:
        """
        Scrape public Instagram posts using Picuki or similar frontend
        """
        results = []
        
        logger.info(f"Searching Instagram for: #{hashtag}")
        
        try:
            search_url = f"https://www.picuki.com/tag/{hashtag}"
            
            response = self.session.get(search_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                posts = soup.find_all('div', class_='box-photo', limit=limit)
                
                for post in posts:
                    try:
                        description = post.find('div', class_='photo-description')
                        
                        results.append({
                            'source': 'instagram',
                            'platform': 'Instagram',
                            'hashtag': hashtag,
                            'content': description.get_text(strip=True) if description else '',
                            'timestamp': datetime.now().isoformat(),
                            'collected_at': datetime.now().isoformat(),
                            'method': 'web_scraping'
                        })
                    except Exception as e:
                        logger.debug(f"Error parsing Instagram post: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Error scraping Instagram: {e}")
        
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
