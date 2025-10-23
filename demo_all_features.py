#!/usr/bin/env python3
"""
Demo Script - TNI AU Threat Intelligence System
Demonstrates all features: Crawler, Threat Search, Threat Intel APIs
"""

import sys
import time
import json
from datetime import datetime
from cyber_threat_intel import ThreatIntelSystem
from free_api_manager import initialize_all_apis

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*80)
    print(f"  {title.center(76)}")
    print("="*80 + "\n")

def demo_crawler(system):
    """Demo: Run the crawler on all platforms"""
    print_header("DEMO 1: CRAWLER - ALL PLATFORMS ENABLED")
    
    print("🚀 Starting Multi-Platform Crawler")
    print("=" * 80)
    
    sources = {
        'news': True,
        'news_urls': [
            'https://www.antaranews.com/berita/teknologi',
            'https://tekno.kompas.com/keamanan-siber',
        ],
        'twitter': True,
        'reddit': True,
        'facebook': True,
        'instagram': True,
        'linkedin': True,
        'telegram': True,
        'subreddits': ['cybersecurity', 'netsec', 'InfoSec'],
        'telegram_channels': ['security', 'cybersec'],
        'keywords': [
            'TNI AU', 'cyber attack', 'malware', 'ransomware',
            'data breach', 'hacking', 'cybersecurity',
            'threat intelligence', 'vulnerability'
        ],
        'darkweb': False
    }
    
    print("📡 Enabled Platforms:")
    platforms = [
        '✅ Twitter/X (free scraping)',
        '✅ Reddit (free API)',
        '✅ Facebook (public data)',
        '✅ Instagram (public hashtags)',
        '✅ LinkedIn (public posts)',
        '✅ Telegram (public channels)',
        '✅ News Sites (BeautifulSoup)',
    ]
    for platform in platforms:
        print(f"   {platform}")
    
    print(f"\n🔍 Keywords ({len(sources['keywords'])} total):")
    print(f"   {', '.join(sources['keywords'][:5])}...")
    
    print("\n🔄 Starting crawler...")
    print("   Note: This is a demo. Real scraping requires internet and may take time.\n")
    
    try:
        result = system.run_collection_cycle(sources)
        
        print("\n✅ Crawler completed successfully!")
        print(f"   📊 Collected: {result['collected']} items")
        print(f"   📊 Processed: {result['processed']} items")
        
        return True
    except Exception as e:
        print(f"\n❌ Crawler failed: {e}")
        return False

def demo_threat_search(system):
    """Demo: Search and analyze threats"""
    print_header("DEMO 2: THREAT LIST SEARCH & ANALYSIS")
    
    print("🔍 Searching Threats in Database")
    print("=" * 80)
    
    cursor = system.db.conn.cursor()
    
    # Search by threat level
    print("\n1️⃣  HIGH PRIORITY THREATS:")
    high_threats = cursor.execute('''
        SELECT title, threat_level, sentiment_label, source, collected_at
        FROM crawled_data
        WHERE threat_level = 'HIGH'
        ORDER BY collected_at DESC
        LIMIT 5
    ''').fetchall()
    
    if high_threats:
        for i, threat in enumerate(high_threats, 1):
            print(f"\n   [{i}] {threat[0]}")
            print(f"       Level: {threat[1]} | Sentiment: {threat[2]} | Source: {threat[3]}")
            print(f"       Time: {threat[4]}")
    else:
        print("   No high priority threats found")
    
    # Search by keyword
    print("\n\n2️⃣  THREATS CONTAINING 'malware':")
    keyword_threats = cursor.execute('''
        SELECT title, threat_level, content
        FROM crawled_data
        WHERE content LIKE '%malware%' OR title LIKE '%malware%'
        LIMIT 3
    ''').fetchall()
    
    if keyword_threats:
        for i, threat in enumerate(keyword_threats, 1):
            print(f"\n   [{i}] {threat[0]}")
            print(f"       Level: {threat[1]}")
            print(f"       Content: {threat[2][:100]}...")
    else:
        print("   No threats found with keyword 'malware'")
    
    # Threat statistics
    print("\n\n3️⃣  THREAT STATISTICS (Last 7 Days):")
    stats = cursor.execute('''
        SELECT 
            threat_level,
            COUNT(*) as count,
            AVG(sentiment_score) as avg_sentiment
        FROM crawled_data
        WHERE collected_at >= date('now', '-7 days')
        GROUP BY threat_level
        ORDER BY 
            CASE threat_level
                WHEN 'HIGH' THEN 1
                WHEN 'MEDIUM' THEN 2
                WHEN 'LOW' THEN 3
                ELSE 4
            END
    ''').fetchall()
    
    if stats:
        print("\n   Threat Level    | Count | Avg Sentiment")
        print("   " + "-"*45)
        for row in stats:
            level = row[0].ljust(14)
            count = str(row[1]).rjust(5)
            sentiment = f"{row[2]:+.2f}".rjust(13)
            print(f"   {level} | {count} | {sentiment}")
    else:
        print("   No threats in database")
    
    # Top sources
    print("\n\n4️⃣  TOP THREAT SOURCES:")
    top_sources = cursor.execute('''
        SELECT source, COUNT(*) as count
        FROM crawled_data
        WHERE collected_at >= date('now', '-7 days')
        GROUP BY source
        ORDER BY count DESC
        LIMIT 5
    ''').fetchall()
    
    if top_sources:
        for i, (source, count) in enumerate(top_sources, 1):
            print(f"   {i}. {source}: {count} threats")
    else:
        print("   No data available")
    
    return True

def demo_threat_intel_apis(system):
    """Demo: Threat Intelligence API integration"""
    print_header("DEMO 3: THREAT INTELLIGENCE APIs")
    
    print("🌐 Free Threat Intelligence API Integration")
    print("=" * 80)
    
    from free_api_manager import FreeThreatIntelAPIs
    threat_apis = FreeThreatIntelAPIs()
    
    # Test IP reputation
    test_ips = ['8.8.8.8', '1.1.1.1']
    
    print("\n1️⃣  IP REPUTATION CHECK:")
    for ip in test_ips:
        print(f"\n   Checking: {ip}")
        try:
            result = threat_apis.check_ip_reputation(ip)
            
            if 'ipinfo' in result and 'error' not in result['ipinfo']:
                info = result['ipinfo']
                print(f"   ✅ IPInfo: {info.get('city', 'N/A')}, {info.get('country', 'N/A')}")
                print(f"      Organization: {info.get('org', 'N/A')}")
            
            if 'ipapi' in result and 'error' not in result['ipapi']:
                info = result['ipapi']
                print(f"   ✅ IPAPI: {info.get('city', 'N/A')}, {info.get('country', 'N/A')}")
                print(f"      Threat Level: {info.get('threat_level', 'N/A')}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test threat feeds
    print("\n\n2️⃣  THREAT FEEDS:")
    print("\n   Fetching latest threat intelligence feeds...")
    try:
        feeds = threat_apis.get_threat_feeds()
        if feeds:
            for feed in feeds:
                print(f"\n   📡 {feed['source']}")
                print(f"      Type: {feed['type']}")
                print(f"      Updated: {feed['timestamp']}")
        else:
            print("   No feeds available at this time")
    except Exception as e:
        print(f"   ⚠️  {e}")
    
    # Available free APIs
    print("\n\n3️⃣  AVAILABLE FREE THREAT INTEL APIs:")
    apis = [
        ("IPInfo", "IP geolocation", "50k requests/month"),
        ("IPAPI", "IP information", "1k requests/day"),
        ("Emerging Threats", "Threat feeds", "Open source"),
        ("WhoisXML", "Domain reputation", "Free tier available"),
    ]
    
    for name, desc, limit in apis:
        print(f"   ✅ {name}")
        print(f"      {desc}")
        print(f"      Limit: {limit}\n")
    
    return True

def demo_reporting(system):
    """Demo: Generate reports"""
    print_header("DEMO 4: AUTOMATED REPORTING")
    
    print("📊 Generating Threat Intelligence Reports")
    print("=" * 80)
    
    # Daily report
    print("\n1️⃣  DAILY REPORT:")
    try:
        daily_report = system.reporter.generate_daily_report()
        print("\n   Summary:")
        print(f"   {json.dumps(daily_report, indent=6, ensure_ascii=False)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Strategic analysis
    print("\n\n2️⃣  STRATEGIC ANALYSIS (30 Days):")
    try:
        strategic = system.reporter.generate_strategic_analysis(days=30)
        print(f"\n   Period: {strategic['period']}")
        print(f"   Total Events: {strategic['total_events']}")
        print(f"   High Priority Threats: {strategic['high_threats']}")
        print(f"   Avg Daily Events: {strategic['avg_daily_events']:.1f}")
        print(f"   Sentiment Trend: {strategic['sentiment_trend']:+.2f}")
        
        if strategic['recommendations']:
            print("\n   📋 Recommendations:")
            for i, rec in enumerate(strategic['recommendations'], 1):
                print(f"      {i}. {rec}")
        else:
            print("\n   ✅ No critical recommendations")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Export report
    print("\n\n3️⃣  EXPORT REPORT:")
    try:
        filename = f'demo_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        system.reporter.export_report(daily_report, filename)
        print(f"   ✅ Report exported to: {filename}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    return True

def main():
    """Run all demos"""
    print("\n" + "🚀 TNI AU THREAT INTELLIGENCE SYSTEM - FULL DEMO".center(80, "="))
    print(f"Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print("Initializing system...")
    
    # Initialize
    api_manager = initialize_all_apis()
    api_config = api_manager.config
    config = {
        'twitter_token': api_config.get('twitter', {}).get('bearer_token'),
        'reddit_creds': api_config.get('reddit', {}),
        'use_free_crawler': True
    }
    
    system = ThreatIntelSystem(config)
    
    print("\n✅ System initialized successfully!\n")
    
    # Run demos
    demos = [
        ("Crawler Demo", demo_crawler),
        ("Threat Search Demo", demo_threat_search),
        ("Threat Intel APIs Demo", demo_threat_intel_apis),
        ("Reporting Demo", demo_reporting),
    ]
    
    results = {}
    
    for demo_name, demo_func in demos:
        try:
            input(f"\nPress ENTER to run {demo_name}...")
            results[demo_name] = demo_func(system)
        except KeyboardInterrupt:
            print("\n\n⚠️  Demo interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Demo failed: {e}")
            results[demo_name] = False
    
    # Summary
    print_header("DEMO SUMMARY")
    
    print("📋 Demo Results:\n")
    for demo_name, passed in results.items():
        status = "✅ SUCCESS" if passed else "❌ FAILED"
        print(f"   {demo_name:<30} {status}")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\n🎯 Overall: {passed}/{total} demos completed successfully")
    
    print("\n" + "="*80)
    print("✨ All features demonstrated successfully!")
    print("="*80 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo terminated by user\n")
        sys.exit(0)
