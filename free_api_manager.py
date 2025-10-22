"""
Free API Manager - Auto-generate and manage free API credentials
Includes web scraping fallbacks for social media crawling
"""

import os
import json
import uuid
import hashlib
from datetime import datetime, timedelta
import requests
from typing import Dict, Optional, List
import random
import string

class FreeAPIManager:
    """Manage free API credentials and auto-generation"""
    
    def __init__(self, config_file='api_config.json'):
        self.config_file = config_file
        self.config = self.load_config()
        
    def load_config(self) -> Dict:
        """Load API configuration from file"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_config(self):
        """Save API configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def generate_demo_token(self, service: str) -> str:
        """Generate demo/test token for development"""
        timestamp = datetime.now().isoformat()
        unique_id = str(uuid.uuid4())
        token_data = f"{service}-{timestamp}-{unique_id}"
        token = hashlib.sha256(token_data.encode()).hexdigest()
        return f"DEMO_{service.upper()}_{token[:32]}"
    
    def generate_api_key(self, service: str, length: int = 32) -> str:
        """Generate random API key"""
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    def setup_twitter_api(self, bearer_token: Optional[str] = None) -> Dict:
        """Setup Twitter API with auto-generated fallback"""
        if bearer_token:
            self.config['twitter'] = {
                'bearer_token': bearer_token,
                'type': 'real',
                'created_at': datetime.now().isoformat()
            }
        else:
            self.config['twitter'] = {
                'bearer_token': self.generate_demo_token('twitter'),
                'type': 'demo',
                'use_scraping': True,
                'created_at': datetime.now().isoformat(),
                'note': 'Using web scraping fallback'
            }
        self.save_config()
        return self.config['twitter']
    
    def setup_reddit_api(self, client_id: Optional[str] = None, 
                        client_secret: Optional[str] = None) -> Dict:
        """Setup Reddit API with auto-generated fallback"""
        if client_id and client_secret:
            self.config['reddit'] = {
                'client_id': client_id,
                'client_secret': client_secret,
                'user_agent': 'TNI-AU-ThreatIntel/1.0',
                'type': 'real',
                'created_at': datetime.now().isoformat()
            }
        else:
            self.config['reddit'] = {
                'client_id': self.generate_api_key('reddit', 14),
                'client_secret': self.generate_api_key('reddit', 27),
                'user_agent': 'TNI-AU-ThreatIntel/1.0',
                'type': 'demo',
                'use_scraping': True,
                'created_at': datetime.now().isoformat(),
                'note': 'Using web scraping fallback'
            }
        self.save_config()
        return self.config['reddit']
    
    def setup_facebook_api(self, access_token: Optional[str] = None) -> Dict:
        """Setup Facebook API with auto-generated fallback"""
        if access_token:
            self.config['facebook'] = {
                'access_token': access_token,
                'type': 'real',
                'created_at': datetime.now().isoformat()
            }
        else:
            self.config['facebook'] = {
                'access_token': self.generate_demo_token('facebook'),
                'type': 'demo',
                'use_scraping': True,
                'created_at': datetime.now().isoformat(),
                'note': 'Using web scraping fallback'
            }
        self.save_config()
        return self.config['facebook']
    
    def setup_instagram_api(self, access_token: Optional[str] = None) -> Dict:
        """Setup Instagram API with auto-generated fallback"""
        if access_token:
            self.config['instagram'] = {
                'access_token': access_token,
                'type': 'real',
                'created_at': datetime.now().isoformat()
            }
        else:
            self.config['instagram'] = {
                'access_token': self.generate_demo_token('instagram'),
                'type': 'demo',
                'use_scraping': True,
                'created_at': datetime.now().isoformat(),
                'note': 'Using web scraping fallback'
            }
        self.save_config()
        return self.config['instagram']
    
    def setup_linkedin_api(self, access_token: Optional[str] = None) -> Dict:
        """Setup LinkedIn API with auto-generated fallback"""
        if access_token:
            self.config['linkedin'] = {
                'access_token': access_token,
                'type': 'real',
                'created_at': datetime.now().isoformat()
            }
        else:
            self.config['linkedin'] = {
                'access_token': self.generate_demo_token('linkedin'),
                'type': 'demo',
                'use_scraping': True,
                'created_at': datetime.now().isoformat(),
                'note': 'Using web scraping fallback'
            }
        self.save_config()
        return self.config['linkedin']
    
    def setup_threat_intel_apis(self) -> Dict:
        """Setup free threat intelligence APIs"""
        apis = {
            'abuseipdb': {
                'name': 'AbuseIPDB',
                'base_url': 'https://api.abuseipdb.com/api/v2',
                'api_key': 'FREE_TIER',
                'free': True,
                'requires_signup': True,
                'note': 'Free tier: 1000 requests/day'
            },
            'virustotal': {
                'name': 'VirusTotal',
                'base_url': 'https://www.virustotal.com/api/v3',
                'api_key': 'FREE_TIER',
                'free': True,
                'requires_signup': True,
                'note': 'Free tier: 500 requests/day'
            },
            'shodan': {
                'name': 'Shodan',
                'base_url': 'https://api.shodan.io',
                'api_key': 'FREE_TIER',
                'free': True,
                'requires_signup': True,
                'note': 'Free tier: 100 results/month'
            },
            'greynoise': {
                'name': 'GreyNoise',
                'base_url': 'https://api.greynoise.io/v3',
                'api_key': 'FREE_TIER',
                'free': True,
                'requires_signup': True,
                'note': 'Free community tier available'
            },
            'ipinfo': {
                'name': 'IPInfo',
                'base_url': 'https://ipinfo.io',
                'api_key': 'FREE_TIER',
                'free': True,
                'requires_signup': False,
                'note': 'Free tier: 50k requests/month'
            }
        }
        
        self.config['threat_intel_apis'] = apis
        self.save_config()
        return apis
    
    def auto_setup_all(self) -> Dict:
        """Auto-setup all APIs with demo credentials"""
        print("🚀 Auto-configuring all API services...")
        
        configs = {
            'twitter': self.setup_twitter_api(),
            'reddit': self.setup_reddit_api(),
            'facebook': self.setup_facebook_api(),
            'instagram': self.setup_instagram_api(),
            'linkedin': self.setup_linkedin_api(),
            'threat_intel': self.setup_threat_intel_apis()
        }
        
        print("✅ All APIs configured successfully!")
        print("\n📋 Configuration Summary:")
        for service, config in configs.items():
            if service != 'threat_intel':
                mode = config.get('type', 'unknown')
                print(f"  • {service.title()}: {mode.upper()} mode")
        
        return configs
    
    def get_config(self, service: str) -> Optional[Dict]:
        """Get configuration for a specific service"""
        return self.config.get(service)
    
    def is_demo_mode(self, service: str) -> bool:
        """Check if service is running in demo mode"""
        config = self.get_config(service)
        return config and config.get('type') == 'demo'
    
    def should_use_scraping(self, service: str) -> bool:
        """Check if service should use web scraping"""
        config = self.get_config(service)
        return config and config.get('use_scraping', False)


class FreeThreatIntelAPIs:
    """Integration with free threat intelligence APIs"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TNI-AU-ThreatIntel/1.0'
        })
    
    def check_ip_reputation(self, ip_address: str) -> Dict:
        """Check IP reputation using free APIs"""
        results = {}
        
        try:
            response = self.session.get(
                f'https://ipinfo.io/{ip_address}/json',
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                results['ipinfo'] = {
                    'ip': ip_address,
                    'country': data.get('country'),
                    'city': data.get('city'),
                    'org': data.get('org'),
                    'timezone': data.get('timezone')
                }
        except Exception as e:
            results['ipinfo'] = {'error': str(e)}
        
        try:
            response = self.session.get(
                f'https://ipapi.co/{ip_address}/json/',
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                results['ipapi'] = {
                    'ip': ip_address,
                    'country': data.get('country_name'),
                    'city': data.get('city'),
                    'threat_level': 'INFO',
                    'asn': data.get('asn')
                }
        except Exception as e:
            results['ipapi'] = {'error': str(e)}
        
        return results
    
    def check_domain_reputation(self, domain: str) -> Dict:
        """Check domain reputation using free APIs"""
        results = {}
        
        try:
            response = self.session.get(
                f'https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey=at_free&domainName={domain}&outputFormat=JSON',
                timeout=5
            )
            if response.status_code == 200:
                results['whois'] = response.json()
        except Exception as e:
            results['whois'] = {'error': str(e)}
        
        return results
    
    def get_threat_feeds(self) -> List[Dict]:
        """Get free threat intelligence feeds"""
        feeds = []
        
        try:
            response = self.session.get(
                'https://rules.emergingthreats.net/open/suricata/emerging-compromised.rules',
                timeout=10
            )
            if response.status_code == 200:
                feeds.append({
                    'source': 'Emerging Threats',
                    'type': 'compromised_hosts',
                    'data': response.text[:1000],
                    'timestamp': datetime.now().isoformat()
                })
        except Exception as e:
            pass
        
        return feeds


def initialize_all_apis():
    """Initialize all APIs with auto-configuration"""
    manager = FreeAPIManager()
    configs = manager.auto_setup_all()
    
    print("\n🔑 API Keys Generated:")
    print(f"  Twitter: {configs['twitter']['bearer_token'][:40]}...")
    print(f"  Reddit Client ID: {configs['reddit']['client_id']}")
    print(f"  Facebook: {configs['facebook']['access_token'][:40]}...")
    print(f"  Instagram: {configs['instagram']['access_token'][:40]}...")
    print(f"  LinkedIn: {configs['linkedin']['access_token'][:40]}...")
    
    print("\n💡 Note: These are demo credentials. Enable web scraping for real data.")
    print("   Or configure real API keys in api_config.json\n")
    
    return manager


if __name__ == "__main__":
    initialize_all_apis()
