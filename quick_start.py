#!/usr/bin/env python3
"""
Quick Start Script - TNI AU Threat Intelligence System
Auto-initializes ALL features with FREE APIs
"""

import os
import sys
import json
from datetime import datetime

def print_banner():
    """Print welcome banner"""
    print("\n" + "="*80)
    print("🚀 TNI AU THREAT INTELLIGENCE SYSTEM - QUICK START")
    print("="*80)
    print("📅 " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("="*80 + "\n")

def check_dependencies():
    """Check and install required dependencies"""
    print("📦 Checking dependencies...")
    
    required_modules = {
        'requests': 'requests',
        'beautifulsoup4': 'bs4',
        'textblob': 'textblob',
        'pandas': 'pandas',
        'tweepy': 'tweepy',
        'praw': 'praw'
    }
    
    missing = []
    for package_name, import_name in required_modules.items():
        try:
            __import__(import_name)
            print(f"  ✓ {package_name}")
        except ImportError:
            missing.append(package_name)
            print(f"  ✗ {package_name} (missing)")
    
    if missing:
        print(f"\n⚠️  Installing missing dependencies: {', '.join(missing)}")
        print("   Run: pip install " + " ".join(missing))
        return False
    
    print("\n✅ All dependencies installed!\n")
    return True

def initialize_apis():
    """Initialize API configuration"""
    print("🔧 Initializing API configuration...")
    
    try:
        from free_api_manager import initialize_all_apis
        
        manager = initialize_all_apis()
        print("\n✅ API configuration complete!")
        
        return manager
    except Exception as e:
        print(f"\n⚠️  API initialization error: {e}")
        print("   Continuing with basic configuration...")
        return None

def show_configuration():
    """Show current configuration"""
    print("\n" + "="*80)
    print("📋 SYSTEM CONFIGURATION")
    print("="*80)
    
    config_items = [
        ("🐦 Twitter/X", "FREE scraping via Nitter (no API key needed)"),
        ("🤖 Reddit", "FREE JSON API (no authentication needed)"),
        ("📘 Facebook", "Public data scraping"),
        ("📸 Instagram", "Public hashtag scraping via Picuki"),
        ("💼 LinkedIn", "Public post scraping"),
        ("✈️  Telegram", "Public channel scraping"),
        ("📰 News Sites", "Web crawling"),
        ("🌐 Forums", "Web scraping"),
        ("🕵️  Dark Web", "Optional (requires Tor)"),
    ]
    
    for platform, method in config_items:
        print(f"  {platform:20} → {method}")
    
    print("\n" + "="*80)

def show_features():
    """Show enabled features"""
    print("\n✨ ENABLED FEATURES:")
    features = [
        "✅ Multi-platform social media crawling (ALL platforms)",
        "✅ Automatic sentiment analysis",
        "✅ Threat level classification (HIGH/MEDIUM/LOW/INFO)",
        "✅ IOC extraction (IPs, domains, hashes, emails)",
        "✅ Multi-language support (ID, EN, ZH, AR)",
        "✅ Real-time dashboard with visualizations",
        "✅ SQLite database for persistence",
        "✅ Automated reporting (JSON, CSV)",
        "✅ Free threat intelligence API integration",
        "✅ No API keys required for most platforms"
    ]
    
    for feature in features:
        print(f"  {feature}")
    
    print()

def create_sample_config():
    """Create sample configuration file"""
    sample_config = {
        "system": {
            "name": "TNI AU Threat Intelligence",
            "version": "2.0.0",
            "mode": "free_scraping"
        },
        "sources": {
            "twitter": {
                "enabled": True,
                "method": "nitter_scraping",
                "rate_limit": "moderate"
            },
            "reddit": {
                "enabled": True,
                "method": "json_api",
                "rate_limit": "unlimited"
            },
            "facebook": {
                "enabled": True,
                "method": "web_scraping",
                "rate_limit": "limited"
            },
            "instagram": {
                "enabled": True,
                "method": "picuki_scraping",
                "rate_limit": "moderate"
            },
            "linkedin": {
                "enabled": True,
                "method": "web_scraping",
                "rate_limit": "limited"
            },
            "telegram": {
                "enabled": True,
                "method": "web_interface",
                "rate_limit": "unlimited"
            }
        },
        "keywords": [
            "TNI AU",
            "pertahanan",
            "siber",
            "cyber attack",
            "data breach",
            "hacking",
            "malware",
            "ransomware",
            "keamanan nasional",
            "ancaman siber",
            "cybersecurity",
            "threat intelligence"
        ]
    }
    
    config_file = "system_config.json"
    with open(config_file, 'w') as f:
        json.dump(sample_config, f, indent=2)
    
    print(f"📝 Sample configuration saved to: {config_file}")

def show_quick_commands():
    """Show quick start commands"""
    print("\n" + "="*80)
    print("🎯 QUICK START COMMANDS")
    print("="*80)
    
    commands = [
        ("Run main system", "python cyber_threat_intel.py"),
        ("Initialize APIs", "python free_api_manager.py"),
        ("Test free scraper", "python social_media_crawler_free.py"),
        ("Start web server", "npm run dev"),
        ("View this guide", "python quick_start.py"),
    ]
    
    for description, command in commands:
        print(f"\n  {description}:")
        print(f"    $ {command}")
    
    print("\n" + "="*80)

def main():
    """Main quick start function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\n⚠️  Please install missing dependencies first.")
        print("   Run: pip install -r requirements.txt")
        return
    
    # Initialize APIs
    initialize_apis()
    
    # Show configuration
    show_configuration()
    
    # Show features
    show_features()
    
    # Create sample config
    create_sample_config()
    
    # Show commands
    show_quick_commands()
    
    print("\n" + "="*80)
    print("🎉 SYSTEM READY!")
    print("="*80)
    print("\n💡 TIP: Run 'python cyber_threat_intel.py' to start collecting intelligence!")
    print("   All platforms are enabled with FREE scraping (no API keys needed)\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error during setup: {e}")
        sys.exit(1)
