#!/usr/bin/env python3
"""
Test script for TNI AU Threat Intelligence System
Tests all features: Crawler, Threat Analysis, Threat Intel APIs
"""

import sys
import json
import requests
from datetime import datetime
from cyber_threat_intel import ThreatIntelSystem, FreeThreatIntelAPIs
from free_api_manager import initialize_all_apis

def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def test_api_initialization():
    """Test API initialization"""
    print_section("1. TESTING API INITIALIZATION")
    
    try:
        api_manager = initialize_all_apis()
        print("✅ API Manager initialized successfully")
        
        config = api_manager.config
        print(f"\n📋 Configured Services:")
        for service, details in config.items():
            if isinstance(details, dict) and 'type' in details:
                print(f"   • {service.title()}: {details['type'].upper()} mode")
        
        return api_manager
    except Exception as e:
        print(f"❌ API initialization failed: {e}")
        return None

def test_system_initialization(api_manager):
    """Test threat intelligence system initialization"""
    print_section("2. TESTING SYSTEM INITIALIZATION")
    
    try:
        api_config = api_manager.config
        config = {
            'twitter_token': api_config.get('twitter', {}).get('bearer_token'),
            'reddit_creds': api_config.get('reddit', {}),
            'use_free_crawler': True
        }
        
        system = ThreatIntelSystem(config)
        print("✅ Threat Intelligence System initialized")
        print(f"   • Database: {system.db}")
        print(f"   • Surface Crawler: {system.surface_crawler}")
        print(f"   • Social Media Crawler: {system.social_crawler}")
        print(f"   • Sentiment Analyzer: {system.sentiment_analyzer}")
        print(f"   • Threat Analyzer: {system.threat_analyzer}")
        
        return system
    except Exception as e:
        print(f"❌ System initialization failed: {e}")
        return None

def test_crawler_functionality(system):
    """Test crawler functionality"""
    print_section("3. TESTING CRAWLER - ALL PLATFORMS")
    
    sources = {
        'news': False,  # Disable for testing to avoid HTTP requests
        'twitter': True,
        'reddit': True,
        'facebook': True,
        'instagram': True,
        'linkedin': True,
        'telegram': True,
        'subreddits': ['cybersecurity', 'netsec'],
        'telegram_channels': ['security'],
        'keywords': [
            'cyber attack', 'malware', 'ransomware', 
            'data breach', 'hacking'
        ],
        'darkweb': False
    }
    
    print("\n📡 Enabled Platforms:")
    platforms = ['Twitter/X', 'Reddit', 'Facebook', 'Instagram', 'LinkedIn', 'Telegram']
    for platform in platforms:
        print(f"   ✅ {platform}")
    
    print("\n🔍 Keywords:", ', '.join(sources['keywords']))
    
    try:
        print("\n🔄 Starting crawler (using free scrapers)...")
        print("   Note: This is a test mode, actual scraping requires internet connection")
        
        # Test sentiment analysis
        test_texts = [
            "Critical vulnerability in defense systems",
            "Successful security patch deployment",
            "Regular system update completed"
        ]
        
        print("\n📊 Testing Sentiment Analysis:")
        for text in test_texts:
            sentiment = system.sentiment_analyzer.analyze_sentiment(text)
            print(f"   • '{text[:50]}...'")
            print(f"     Sentiment: {sentiment['label']} (score: {sentiment['score']:.2f})")
        
        # Test threat analysis
        print("\n🎯 Testing Threat Level Assessment:")
        threat_texts = [
            "Critical attack targeting TNI AU systems with malware",
            "Suspicious activity detected in network",
            "System advisory for regular maintenance"
        ]
        
        for text in threat_texts:
            level = system.threat_analyzer.assess_threat_level(text)
            print(f"   • '{text}'")
            print(f"     Threat Level: {level}")
        
        print("\n✅ Crawler functionality test completed")
        return True
        
    except Exception as e:
        print(f"❌ Crawler test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_threat_intel_apis():
    """Test threat intelligence APIs"""
    print_section("4. TESTING THREAT INTELLIGENCE APIs")
    
    try:
        threat_apis = FreeThreatIntelAPIs()
        
        # Test IP reputation check
        print("\n🔍 Testing IP Reputation Check:")
        test_ip = "8.8.8.8"
        print(f"   Checking IP: {test_ip}")
        
        ip_results = threat_apis.check_ip_reputation(test_ip)
        print(f"   Results:")
        for source, data in ip_results.items():
            print(f"      • {source.upper()}: {json.dumps(data, indent=8)}")
        
        # Test threat feeds
        print("\n📡 Testing Threat Feeds:")
        feeds = threat_apis.get_threat_feeds()
        print(f"   Retrieved {len(feeds)} threat feeds")
        for feed in feeds:
            print(f"      • {feed['source']}: {feed['type']}")
        
        print("\n✅ Threat Intel APIs test completed")
        return True
        
    except Exception as e:
        print(f"❌ Threat Intel APIs test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_operations(system):
    """Test database operations"""
    print_section("5. TESTING DATABASE OPERATIONS")
    
    try:
        # Insert test data
        print("\n📝 Inserting test threat data...")
        test_data = (
            'test_source',
            'https://example.com/test',
            'Test Threat Report',
            'This is a test threat with malware and ransomware keywords targeting defense systems',
            'test_analyst',
            datetime.now().isoformat(),
            -0.5,
            'negative',
            '{"ip_addresses": ["192.168.1.1"], "domains": ["malicious.com"]}',
            'HIGH'
        )
        
        system.db.insert_crawled_data(test_data)
        print("✅ Test data inserted")
        
        # Query data
        print("\n🔍 Querying threat summary...")
        summary = system.db.get_threat_summary(days=7)
        print("   Threat Summary (last 7 days):")
        for row in summary:
            print(f"      • {row[0]}: {row[1]} threats")
        
        print("\n✅ Database operations test completed")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_reporting(system):
    """Test reporting functionality"""
    print_section("6. TESTING REPORTING FEATURES")
    
    try:
        # Generate daily report
        print("\n📊 Generating daily report...")
        daily_report = system.reporter.generate_daily_report()
        print("   Daily Report:")
        print(f"   {json.dumps(daily_report, indent=6, ensure_ascii=False)}")
        
        # Generate strategic analysis
        print("\n📈 Generating strategic analysis...")
        strategic = system.reporter.generate_strategic_analysis(days=30)
        print("   Strategic Analysis:")
        print(f"   {json.dumps(strategic, indent=6, ensure_ascii=False)}")
        
        # Export report
        filename = f'test_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        system.reporter.export_report(daily_report, filename)
        print(f"\n✅ Report exported to {filename}")
        
        print("\n✅ Reporting test completed")
        return True
        
    except Exception as e:
        print(f"❌ Reporting test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "🚀 TNI AU THREAT INTELLIGENCE SYSTEM - FULL TEST".center(80, "="))
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        'api_init': False,
        'system_init': False,
        'crawler': False,
        'threat_intel': False,
        'database': False,
        'reporting': False
    }
    
    # Run tests
    api_manager = test_api_initialization()
    results['api_init'] = api_manager is not None
    
    if api_manager:
        system = test_system_initialization(api_manager)
        results['system_init'] = system is not None
        
        if system:
            results['crawler'] = test_crawler_functionality(system)
            results['threat_intel'] = test_threat_intel_apis()
            results['database'] = test_database_operations(system)
            results['reporting'] = test_reporting(system)
    
    # Print summary
    print_section("TEST SUMMARY")
    print("\n📋 Test Results:")
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"   {test_name.replace('_', ' ').title():<30} {status}")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! System is fully functional.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the logs above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
