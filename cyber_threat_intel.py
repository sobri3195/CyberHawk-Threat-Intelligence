"""
Sistem Analisis Intelijen Ancaman Siber - TNI AU
Fitur: Crawling media sosial, dark web monitoring, sentiment analysis multilanguage
"""

import requests
from bs4 import BeautifulSoup
import tweepy
import praw
from datetime import datetime, timedelta
import json
import pandas as pd
from textblob import TextBlob
import re
from urllib.parse import urlparse
import time
from collections import Counter
import sqlite3

# ===============================
# 1. KONFIGURASI DAN DATABASE
# ===============================

class ThreatIntelDatabase:
    """Database untuk menyimpan hasil intelijen"""
    
    def __init__(self, db_name='threat_intel.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Tabel untuk data crawling
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS crawled_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                url TEXT,
                title TEXT,
                content TEXT,
                author TEXT,
                timestamp DATETIME,
                sentiment_score REAL,
                sentiment_label TEXT,
                keywords TEXT,
                threat_level TEXT,
                collected_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabel untuk indikator ancaman
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS threat_indicators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                indicator_type TEXT,
                indicator_value TEXT,
                threat_category TEXT,
                confidence_score REAL,
                first_seen DATETIME,
                last_seen DATETIME,
                source TEXT
            )
        ''')
        
        # Tabel untuk analisis sentimen
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sentiment_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE,
                source TEXT,
                positive_count INTEGER,
                negative_count INTEGER,
                neutral_count INTEGER,
                avg_sentiment REAL,
                trending_topics TEXT
            )
        ''')
        
        self.conn.commit()
    
    def insert_crawled_data(self, data):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO crawled_data 
            (source, url, title, content, author, timestamp, sentiment_score, 
             sentiment_label, keywords, threat_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
        self.conn.commit()
    
    def get_threat_summary(self, days=7):
        cursor = self.conn.cursor()
        query = f'''
            SELECT threat_level, COUNT(*) as count
            FROM crawled_data
            WHERE collected_at >= date('now', '-{days} days')
            GROUP BY threat_level
        '''
        return cursor.execute(query).fetchall()

# ===============================
# 2. WEB SCRAPER (SURFACE WEB)
# ===============================

class SurfaceWebCrawler:
    """Crawler untuk media online dan portal berita"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()
    
    def crawl_news_site(self, url):
        """Crawl situs berita"""
        try:
            response = self.session.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract artikel (sesuaikan dengan struktur situs target)
            articles = []
            for article in soup.find_all('article', limit=20):
                title_elem = article.find(['h1', 'h2', 'h3'])
                content_elem = article.find(['p', 'div'], class_=re.compile('content|text|body'))
                link_elem = article.find('a')
                
                if title_elem and content_elem:
                    articles.append({
                        'title': title_elem.get_text(strip=True),
                        'content': content_elem.get_text(strip=True),
                        'url': link_elem['href'] if link_elem else url,
                        'source': urlparse(url).netloc,
                        'timestamp': datetime.now()
                    })
            
            return articles
        
        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")
            return []
    
    def crawl_forum(self, forum_url):
        """Crawl forum dan community boards"""
        try:
            response = self.session.get(forum_url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            posts = []
            # Sesuaikan selector dengan struktur forum target
            for post in soup.find_all(class_=re.compile('post|thread|message'), limit=30):
                author_elem = post.find(class_=re.compile('author|user|poster'))
                content_elem = post.find(class_=re.compile('content|message|text'))
                
                if content_elem:
                    posts.append({
                        'author': author_elem.get_text(strip=True) if author_elem else 'Unknown',
                        'content': content_elem.get_text(strip=True),
                        'source': 'forum',
                        'url': forum_url,
                        'timestamp': datetime.now()
                    })
            
            return posts
        
        except Exception as e:
            print(f"Error crawling forum {forum_url}: {str(e)}")
            return []

# ===============================
# 3. SOCIAL MEDIA CRAWLER
# ===============================

class SocialMediaCrawler:
    """Crawler untuk media sosial (Twitter/X, Reddit, dll)"""
    
    def __init__(self, twitter_bearer_token=None, reddit_credentials=None):
        self.twitter_token = twitter_bearer_token
        self.reddit_creds = reddit_credentials
    
    def crawl_twitter(self, keywords, max_results=100):
        """Crawl Twitter/X untuk keyword tertentu"""
        if not self.twitter_token:
            print("Twitter API token not configured")
            return []
        
        try:
            client = tweepy.Client(bearer_token=self.twitter_token)
            
            query = ' OR '.join([f'"{kw}"' for kw in keywords])
            tweets = client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=['created_at', 'author_id', 'lang', 'public_metrics']
            )
            
            results = []
            if tweets.data:
                for tweet in tweets.data:
                    results.append({
                        'source': 'twitter',
                        'content': tweet.text,
                        'author': tweet.author_id,
                        'timestamp': tweet.created_at,
                        'url': f'https://twitter.com/i/web/status/{tweet.id}',
                        'engagement': tweet.public_metrics
                    })
            
            return results
        
        except Exception as e:
            print(f"Error crawling Twitter: {str(e)}")
            return []
    
    def crawl_reddit(self, subreddits, keywords, limit=50):
        """Crawl Reddit untuk subreddit dan keyword tertentu"""
        if not self.reddit_creds:
            print("Reddit API credentials not configured")
            return []
        
        try:
            reddit = praw.Reddit(
                client_id=self.reddit_creds['client_id'],
                client_secret=self.reddit_creds['client_secret'],
                user_agent=self.reddit_creds['user_agent']
            )
            
            results = []
            for subreddit_name in subreddits:
                subreddit = reddit.subreddit(subreddit_name)
                
                for submission in subreddit.hot(limit=limit):
                    # Filter berdasarkan keywords
                    content = f"{submission.title} {submission.selftext}".lower()
                    if any(kw.lower() in content for kw in keywords):
                        results.append({
                            'source': f'reddit_{subreddit_name}',
                            'title': submission.title,
                            'content': submission.selftext,
                            'author': str(submission.author),
                            'url': submission.url,
                            'timestamp': datetime.fromtimestamp(submission.created_utc),
                            'score': submission.score
                        })
            
            return results
        
        except Exception as e:
            print(f"Error crawling Reddit: {str(e)}")
            return []

# ===============================
# 4. DARK WEB MONITORING (TOR)
# ===============================

class DarkWebMonitor:
    """Monitor untuk .onion sites dan dark web forums"""
    
    def __init__(self, tor_proxy='socks5h://localhost:9050'):
        self.proxies = {
            'http': tor_proxy,
            'https': tor_proxy
        }
        self.session = requests.Session()
        self.session.proxies.update(self.proxies)
    
    def check_onion_site(self, onion_url):
        """Cek ketersediaan dan crawl .onion site"""
        try:
            response = self.session.get(
                onion_url,
                timeout=30,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                text_content = soup.get_text(strip=True, separator=' ')
                
                return {
                    'url': onion_url,
                    'status': 'active',
                    'content': text_content[:5000],  # Limit content
                    'timestamp': datetime.now()
                }
        
        except Exception as e:
            return {
                'url': onion_url,
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now()
            }
    
    def monitor_dark_forums(self, forum_list):
        """Monitor daftar forum dark web"""
        results = []
        for forum_url in forum_list:
            print(f"Checking dark web forum: {forum_url}")
            result = self.check_onion_site(forum_url)
            results.append(result)
            time.sleep(5)  # Rate limiting
        
        return results

# ===============================
# 5. SENTIMENT ANALYSIS (MULTILANGUAGE)
# ===============================

class SentimentAnalyzer:
    """Analisis sentimen dengan support multilanguage"""
    
    def __init__(self):
        self.languages = ['id', 'en', 'zh', 'ar']  # Indonesia, English, Chinese, Arabic
    
    def analyze_sentiment(self, text, language='id'):
        """Analisis sentimen teks"""
        try:
            # TextBlob untuk analisis dasar
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            # Klasifikasi sentiment
            if polarity > 0.1:
                label = 'positive'
            elif polarity < -0.1:
                label = 'negative'
            else:
                label = 'neutral'
            
            return {
                'score': polarity,
                'label': label,
                'subjectivity': blob.sentiment.subjectivity
            }
        
        except Exception as e:
            return {'score': 0, 'label': 'neutral', 'error': str(e)}
    
    def analyze_batch(self, texts, language='id'):
        """Analisis batch untuk multiple texts"""
        results = []
        for text in texts:
            sentiment = self.analyze_sentiment(text, language)
            results.append(sentiment)
        
        return results
    
    def get_sentiment_summary(self, sentiments):
        """Ringkasan statistik sentimen"""
        labels = [s['label'] for s in sentiments]
        counter = Counter(labels)
        
        return {
            'positive': counter.get('positive', 0),
            'negative': counter.get('negative', 0),
            'neutral': counter.get('neutral', 0),
            'total': len(sentiments),
            'positive_ratio': counter.get('positive', 0) / len(sentiments) if sentiments else 0
        }

# ===============================
# 6. THREAT INTELLIGENCE ANALYZER
# ===============================

class ThreatAnalyzer:
    """Analisis ancaman dari data yang dikumpulkan"""
    
    def __init__(self):
        # Keywords untuk deteksi ancaman
        self.threat_keywords = {
            'high': ['serangan', 'attack', 'exploit', 'vulnerability', 'breach', 'hack', 
                     'malware', 'ransomware', 'ddos', 'infiltration', 'weaponized'],
            'medium': ['suspicious', 'mencurigakan', 'anomaly', 'unusual', 'unauthorized',
                       'phishing', 'scam', 'fraud', 'leak'],
            'low': ['warning', 'peringatan', 'alert', 'notice', 'advisory']
        }
        
        self.defense_keywords = ['TNI', 'AU', 'militer', 'pertahanan', 'defense', 'military',
                                 'airforce', 'angkatan udara', 'alutsista', 'radar']
    
    def assess_threat_level(self, text):
        """Tentukan level ancaman dari teks"""
        text_lower = text.lower()
        
        # Cek keywords ancaman
        high_count = sum(1 for kw in self.threat_keywords['high'] if kw in text_lower)
        medium_count = sum(1 for kw in self.threat_keywords['medium'] if kw in text_lower)
        low_count = sum(1 for kw in self.threat_keywords['low'] if kw in text_lower)
        
        # Cek keywords pertahanan
        defense_mentioned = any(kw in text_lower for kw in self.defense_keywords)
        
        # Scoring
        if high_count >= 2 or (high_count >= 1 and defense_mentioned):
            return 'HIGH'
        elif medium_count >= 2 or (medium_count >= 1 and defense_mentioned):
            return 'MEDIUM'
        elif low_count >= 1 or high_count == 1 or medium_count == 1:
            return 'LOW'
        else:
            return 'INFO'
    
    def extract_iocs(self, text):
        """Extract Indicators of Compromise (IOCs)"""
        iocs = {
            'ip_addresses': [],
            'domains': [],
            'emails': [],
            'hashes': []
        }
        
        # Regex patterns
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        domain_pattern = r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        hash_pattern = r'\b[a-fA-F0-9]{32,64}\b'
        
        iocs['ip_addresses'] = re.findall(ip_pattern, text)
        iocs['domains'] = re.findall(domain_pattern, text)
        iocs['emails'] = re.findall(email_pattern, text)
        iocs['hashes'] = re.findall(hash_pattern, text)
        
        return iocs
    
    def analyze_trends(self, data_points, window_days=7):
        """Analisis trend ancaman dalam periode waktu"""
        df = pd.DataFrame(data_points)
        
        if df.empty:
            return {'status': 'no_data'}
        
        # Group by date
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        daily_threats = df.groupby(['date', 'threat_level']).size().unstack(fill_value=0)
        
        return {
            'daily_summary': daily_threats.to_dict(),
            'total_threats': len(df),
            'high_priority': len(df[df['threat_level'] == 'HIGH']),
            'trend': 'increasing' if daily_threats.sum(axis=1).is_monotonic_increasing else 'stable'
        }

# ===============================
# 7. REPORTING DAN VISUALISASI
# ===============================

class ThreatIntelReporter:
    """Generate laporan intelijen ancaman"""
    
    def __init__(self, database):
        self.db = database
    
    def generate_daily_report(self, date=None):
        """Generate laporan harian"""
        if date is None:
            date = datetime.now().date()
        
        cursor = self.db.conn.cursor()
        
        # Query data harian
        query = '''
            SELECT threat_level, sentiment_label, source, COUNT(*) as count
            FROM crawled_data
            WHERE DATE(collected_at) = ?
            GROUP BY threat_level, sentiment_label, source
        '''
        
        results = cursor.execute(query, (date,)).fetchall()
        
        report = {
            'date': str(date),
            'summary': {},
            'by_source': {},
            'sentiment': {}
        }
        
        for row in results:
            threat_level, sentiment, source, count = row
            
            # Aggregate by threat level
            if threat_level not in report['summary']:
                report['summary'][threat_level] = 0
            report['summary'][threat_level] += count
            
            # Aggregate by source
            if source not in report['by_source']:
                report['by_source'][source] = 0
            report['by_source'][source] += count
            
            # Aggregate sentiment
            if sentiment not in report['sentiment']:
                report['sentiment'][sentiment] = 0
            report['sentiment'][sentiment] += count
        
        return report
    
    def generate_strategic_analysis(self, days=30):
        """Generate analisis strategis jangka panjang"""
        cursor = self.db.conn.cursor()
        
        query = '''
            SELECT 
                DATE(collected_at) as date,
                threat_level,
                COUNT(*) as count,
                AVG(sentiment_score) as avg_sentiment
            FROM crawled_data
            WHERE collected_at >= date('now', '-{} days')
            GROUP BY DATE(collected_at), threat_level
            ORDER BY date DESC
        '''.format(days)
        
        results = cursor.execute(query).fetchall()
        
        df = pd.DataFrame(results, columns=['date', 'threat_level', 'count', 'avg_sentiment'])
        
        analysis = {
            'period': f'{days} days',
            'total_events': df['count'].sum(),
            'high_threats': df[df['threat_level'] == 'HIGH']['count'].sum(),
            'avg_daily_events': df.groupby('date')['count'].sum().mean(),
            'sentiment_trend': df['avg_sentiment'].mean(),
            'recommendations': []
        }
        
        # Generate recommendations
        if analysis['high_threats'] > 10:
            analysis['recommendations'].append('PRIORITAS TINGGI: Peningkatan signifikan ancaman level tinggi')
        
        if analysis['sentiment_trend'] < -0.2:
            analysis['recommendations'].append('PERHATIAN: Sentimen negatif dominan, perlu monitoring intensif')
        
        return analysis
    
    def export_report(self, report, filename, format='json'):
        """Export laporan ke file"""
        if format == 'json':
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
        
        elif format == 'csv':
            df = pd.DataFrame(report)
            df.to_csv(filename, index=False, encoding='utf-8')
        
        print(f"Report exported to {filename}")

# ===============================
# 8. MAIN ORCHESTRATOR
# ===============================

class ThreatIntelSystem:
    """Sistem utama untuk orchestrate semua komponen"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.db = ThreatIntelDatabase()
        self.surface_crawler = SurfaceWebCrawler()
        self.social_crawler = SocialMediaCrawler(
            twitter_bearer_token=self.config.get('twitter_token'),
            reddit_credentials=self.config.get('reddit_creds')
        )
        self.dark_monitor = DarkWebMonitor()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.threat_analyzer = ThreatAnalyzer()
        self.reporter = ThreatIntelReporter(self.db)
    
    def collect_intelligence(self, sources):
        """Kumpulkan intelijen dari berbagai sumber"""
        all_data = []
        
        # Surface web
        if 'news' in sources:
            print("Crawling news sites...")
            for url in sources.get('news_urls', []):
                articles = self.surface_crawler.crawl_news_site(url)
                all_data.extend(articles)
        
        # Social media
        if 'twitter' in sources:
            print("Crawling Twitter...")
            tweets = self.social_crawler.crawl_twitter(
                keywords=sources.get('keywords', []),
                max_results=100
            )
            all_data.extend(tweets)
        
        if 'reddit' in sources:
            print("Crawling Reddit...")
            posts = self.social_crawler.crawl_reddit(
                subreddits=sources.get('subreddits', []),
                keywords=sources.get('keywords', [])
            )
            all_data.extend(posts)
        
        # Dark web
        if 'darkweb' in sources and sources.get('onion_urls'):
            print("Monitoring dark web...")
            dark_data = self.dark_monitor.monitor_dark_forums(sources['onion_urls'])
            all_data.extend(dark_data)
        
        return all_data
    
    def process_intelligence(self, raw_data):
        """Proses dan analisis data yang dikumpulkan"""
        processed = []
        
        for item in raw_data:
            # Sentiment analysis
            content = item.get('content', '') or item.get('title', '')
            sentiment = self.sentiment_analyzer.analyze_sentiment(content)
            
            # Threat assessment
            threat_level = self.threat_analyzer.assess_threat_level(content)
            
            # Extract IOCs
            iocs = self.threat_analyzer.extract_iocs(content)
            
            # Compile processed data
            processed_item = {
                'source': item.get('source', 'unknown'),
                'url': item.get('url', ''),
                'title': item.get('title', '')[:500],
                'content': content[:2000],
                'author': item.get('author', 'unknown'),
                'timestamp': item.get('timestamp', datetime.now()),
                'sentiment_score': sentiment['score'],
                'sentiment_label': sentiment['label'],
                'keywords': json.dumps(iocs),
                'threat_level': threat_level
            }
            
            # Save to database
            self.db.insert_crawled_data(tuple(processed_item.values()))
            processed.append(processed_item)
        
        return processed
    
    def run_collection_cycle(self, sources):
        """Jalankan satu siklus pengumpulan dan analisis"""
        print("=" * 60)
        print("MEMULAI SIKLUS PENGUMPULAN INTELIJEN")
        print(f"Waktu: {datetime.now()}")
        print("=" * 60)
        
        # Collect
        raw_data = self.collect_intelligence(sources)
        print(f"\nData terkumpul: {len(raw_data)} items")
        
        # Process
        processed_data = self.process_intelligence(raw_data)
        print(f"Data diproses: {len(processed_data)} items")
        
        # Generate report
        report = self.reporter.generate_daily_report()
        print("\n" + "=" * 60)
        print("RINGKASAN HARIAN")
        print("=" * 60)
        print(json.dumps(report, indent=2, ensure_ascii=False))
        
        return {
            'collected': len(raw_data),
            'processed': len(processed_data),
            'report': report
        }

# ===============================
# 9. CONTOH PENGGUNAAN
# ===============================

def main():
    """Contoh penggunaan sistem"""
    
    # Konfigurasi (isi dengan credential yang sebenarnya)
    config = {
        'twitter_token': 'YOUR_TWITTER_BEARER_TOKEN',
        'reddit_creds': {
            'client_id': 'YOUR_CLIENT_ID',
            'client_secret': 'YOUR_CLIENT_SECRET',
            'user_agent': 'ThreatIntel/1.0'
        }
    }
    
    # Inisialisasi sistem
    system = ThreatIntelSystem(config)
    
    # Definisi sumber data
    sources = {
        'news': True,
        'news_urls': [
            'https://www.antaranews.com/berita/teknologi',
            'https://tekno.kompas.com/keamanan-siber',
            # Tambahkan sumber berita lainnya
        ],
        'twitter': True,
        'reddit': True,
        'subreddits': ['cybersecurity', 'netsec', 'Indonesia'],
        'keywords': [
            'TNI AU', 'pertahanan', 'siber', 'cyber attack', 
            'data breach', 'hacking', 'malware', 'ransomware',
            'keamanan nasional', 'ancaman siber'
        ],
        'darkweb': False,  # Set True jika TOR sudah dikonfigurasi
        'onion_urls': [
            # Daftar .onion URLs yang akan dimonitor
        ]
    }
    
    # Jalankan siklus pengumpulan
    result = system.run_collection_cycle(sources)
    
    # Generate analisis strategis
    strategic_analysis = system.reporter.generate_strategic_analysis(days=30)
    print("\n" + "=" * 60)
    print("ANALISIS STRATEGIS (30 HARI)")
    print("=" * 60)
    print(json.dumps(strategic_analysis, indent=2, ensure_ascii=False))
    
    # Export laporan
    system.reporter.export_report(
        strategic_analysis,
        f'threat_intel_report_{datetime.now().strftime("%Y%m%d")}.json',
        format='json'
    )

if __name__ == "__main__":
    main()
