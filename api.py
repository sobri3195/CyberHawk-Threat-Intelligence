"""
Flask API for TNI AU Threat Intelligence System
Provides REST endpoints for crawler, threat analysis, and reporting
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import threading
import os

from cyber_threat_intel import (
    ThreatIntelSystem,
    ThreatIntelDatabase,
    FreeThreatIntelAPIs
)
from free_api_manager import FreeAPIManager, initialize_all_apis

app = Flask(__name__)
CORS(app)

threat_system = None
db = None
threat_apis = None
api_manager = None
crawler_status = {
    'in_progress': False,
    'progress': 0,
    'message': 'Ready',
    'last_run': None
}

def initialize_system():
    """Initialize threat intelligence system"""
    global threat_system, db, threat_apis, api_manager
    
    print("🚀 Initializing Threat Intelligence System...")
    
    api_manager = initialize_all_apis()
    
    api_config = api_manager.config
    config = {
        'twitter_token': api_config.get('twitter', {}).get('bearer_token'),
        'reddit_creds': api_config.get('reddit', {}),
        'use_free_crawler': True
    }
    
    threat_system = ThreatIntelSystem(config)
    db = threat_system.db
    threat_apis = FreeThreatIntelAPIs()
    
    print("✅ System initialized successfully!")

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'service': 'TNI AU Threat Intelligence System',
        'version': '2.0.0',
        'timestamp': datetime.now().isoformat(),
        'features': {
            'crawler': True,
            'threat_analysis': True,
            'sentiment_analysis': True,
            'free_scraping': True,
            'threat_intel_apis': True,
            'all_platforms_enabled': True
        }
    })

@app.route('/api/crawler/start', methods=['POST'])
def start_crawler():
    """Start crawler with specified sources and keywords"""
    global crawler_status
    
    if crawler_status['in_progress']:
        return jsonify({
            'success': False,
            'message': 'Crawler already running'
        }), 400
    
    try:
        data = request.json
        sources_config = {
            'news': data.get('sources', {}).get('news', False),
            'news_urls': data.get('news_urls', [
                'https://www.antaranews.com/berita/teknologi',
                'https://tekno.kompas.com/keamanan-siber',
            ]),
            'twitter': 'twitter' in data.get('sources', []) or 'social' in data.get('sources', []),
            'reddit': 'reddit' in data.get('sources', []) or 'social' in data.get('sources', []),
            'facebook': 'facebook' in data.get('sources', []) or 'social' in data.get('sources', []),
            'instagram': 'instagram' in data.get('sources', []) or 'social' in data.get('sources', []),
            'linkedin': 'linkedin' in data.get('sources', []) or 'social' in data.get('sources', []),
            'telegram': 'telegram' in data.get('sources', []) or 'social' in data.get('sources', []),
            'subreddits': data.get('subreddits', ['cybersecurity', 'netsec', 'InfoSec']),
            'telegram_channels': data.get('telegram_channels', ['security', 'cybersec']),
            'keywords': data.get('keywords', [
                'cyber attack', 'malware', 'ransomware', 'data breach',
                'hacking', 'cybersecurity', 'threat intelligence'
            ]),
            'darkweb': False,
            'onion_urls': []
        }
        
        def run_crawler():
            global crawler_status
            crawler_status['in_progress'] = True
            crawler_status['progress'] = 0
            crawler_status['message'] = 'Starting crawler...'
            
            try:
                crawler_status['progress'] = 20
                crawler_status['message'] = 'Collecting intelligence from sources...'
                
                result = threat_system.run_collection_cycle(sources_config)
                
                crawler_status['progress'] = 100
                crawler_status['message'] = f'Completed! Collected {result["collected"]} items'
                crawler_status['last_run'] = datetime.now().isoformat()
                crawler_status['in_progress'] = False
                
            except Exception as e:
                crawler_status['progress'] = 0
                crawler_status['message'] = f'Error: {str(e)}'
                crawler_status['in_progress'] = False
        
        thread = threading.Thread(target=run_crawler)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Crawler started successfully',
            'platforms_enabled': [
                'Twitter/X', 'Reddit', 'Facebook', 'Instagram', 
                'LinkedIn', 'Telegram', 'News Sites'
            ]
        })
        
    except Exception as e:
        crawler_status['in_progress'] = False
        return jsonify({
            'success': False,
            'message': f'Failed to start crawler: {str(e)}'
        }), 500

@app.route('/api/crawler/status', methods=['GET'])
def get_crawler_status():
    """Get current crawler status"""
    return jsonify({
        'inProgress': crawler_status['in_progress'],
        'progress': crawler_status['progress'],
        'message': crawler_status['message'],
        'lastRun': crawler_status['last_run'],
        'allPlatformsEnabled': True,
        'freeScrapingEnabled': True
    })

@app.route('/api/threats/recent', methods=['GET'])
def get_recent_threats():
    """Get recent threats from database"""
    try:
        limit = request.args.get('limit', 50, type=int)
        days = request.args.get('days', 7, type=int)
        
        cursor = db.conn.cursor()
        query = '''
            SELECT * FROM crawled_data
            WHERE collected_at >= date('now', '-{} days')
            ORDER BY collected_at DESC
            LIMIT ?
        '''.format(days)
        
        results = cursor.execute(query, (limit,)).fetchall()
        
        threats = []
        for row in results:
            threats.append({
                'id': row[0],
                'source': row[1],
                'url': row[2],
                'title': row[3],
                'content': row[4],
                'author': row[5],
                'timestamp': row[6],
                'sentiment_score': row[7],
                'sentiment_label': row[8],
                'keywords': row[9],
                'threat_level': row[10],
                'collected_at': row[11]
            })
        
        return jsonify(threats)
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to fetch threats: {str(e)}'
        }), 500

@app.route('/api/threats/search', methods=['POST'])
def search_threats():
    """Search threats with filters"""
    try:
        data = request.json
        query = data.get('query', '')
        filters = data.get('filters', {})
        
        cursor = db.conn.cursor()
        
        sql = 'SELECT * FROM crawled_data WHERE 1=1'
        params = []
        
        if query:
            sql += ' AND (title LIKE ? OR content LIKE ? OR keywords LIKE ?)'
            search_term = f'%{query}%'
            params.extend([search_term, search_term, search_term])
        
        if filters.get('level') and filters['level'] != 'all':
            sql += ' AND threat_level = ?'
            params.append(filters['level'])
        
        if filters.get('sentiment') and filters['sentiment'] != 'all':
            sql += ' AND sentiment_label = ?'
            params.append(filters['sentiment'])
        
        if filters.get('source') and filters['source'] != 'all':
            sql += ' AND source LIKE ?'
            params.append(f'%{filters["source"]}%')
        
        sql += ' ORDER BY collected_at DESC LIMIT 100'
        
        results = cursor.execute(sql, params).fetchall()
        
        threats = []
        for row in results:
            threats.append({
                'id': row[0],
                'source': row[1],
                'url': row[2],
                'title': row[3],
                'content': row[4],
                'author': row[5],
                'timestamp': row[6],
                'sentiment_score': row[7],
                'sentiment_label': row[8],
                'keywords': row[9],
                'threat_level': row[10],
                'collected_at': row[11]
            })
        
        return jsonify(threats)
        
    except Exception as e:
        return jsonify({
            'error': f'Search failed: {str(e)}'
        }), 500

@app.route('/api/threats/level/<level>', methods=['GET'])
def get_threats_by_level(level):
    """Get threats filtered by level"""
    try:
        cursor = db.conn.cursor()
        query = '''
            SELECT * FROM crawled_data
            WHERE threat_level = ?
            ORDER BY collected_at DESC
            LIMIT 100
        '''
        
        results = cursor.execute(query, (level.upper(),)).fetchall()
        
        threats = []
        for row in results:
            threats.append({
                'id': row[0],
                'source': row[1],
                'url': row[2],
                'title': row[3],
                'content': row[4],
                'author': row[5],
                'timestamp': row[6],
                'sentiment_score': row[7],
                'sentiment_label': row[8],
                'keywords': row[9],
                'threat_level': row[10],
                'collected_at': row[11]
            })
        
        return jsonify(threats)
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to fetch threats: {str(e)}'
        }), 500

@app.route('/api/threats/stats', methods=['GET'])
def get_threat_stats():
    """Get threat statistics"""
    try:
        days = request.args.get('days', 7, type=int)
        
        cursor = db.conn.cursor()
        
        summary_query = '''
            SELECT threat_level, COUNT(*) as count
            FROM crawled_data
            WHERE collected_at >= date('now', '-{} days')
            GROUP BY threat_level
        '''.format(days)
        
        summary = cursor.execute(summary_query).fetchall()
        
        sentiment_query = '''
            SELECT sentiment_label, COUNT(*) as count
            FROM crawled_data
            WHERE collected_at >= date('now', '-{} days')
            GROUP BY sentiment_label
        '''.format(days)
        
        sentiment = cursor.execute(sentiment_query).fetchall()
        
        source_query = '''
            SELECT source, COUNT(*) as count
            FROM crawled_data
            WHERE collected_at >= date('now', '-{} days')
            GROUP BY source
            ORDER BY count DESC
            LIMIT 10
        '''.format(days)
        
        sources = cursor.execute(source_query).fetchall()
        
        total_query = '''
            SELECT COUNT(*) FROM crawled_data
            WHERE collected_at >= date('now', '-{} days')
        '''.format(days)
        
        total = cursor.execute(total_query).fetchone()[0]
        
        stats = {
            'total': total,
            'by_threat_level': {row[0]: row[1] for row in summary},
            'by_sentiment': {row[0]: row[1] for row in sentiment},
            'top_sources': [{'source': row[0], 'count': row[1]} for row in sources],
            'period_days': days
        }
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to fetch stats: {str(e)}'
        }), 500

@app.route('/api/dashboard/summary', methods=['GET'])
def get_dashboard_summary():
    """Get dashboard summary data"""
    try:
        days = request.args.get('days', 7, type=int)
        
        cursor = db.conn.cursor()
        
        total_threats = cursor.execute('''
            SELECT COUNT(*) FROM crawled_data
            WHERE collected_at >= date('now', '-{} days')
        '''.format(days)).fetchone()[0]
        
        high_threats = cursor.execute('''
            SELECT COUNT(*) FROM crawled_data
            WHERE threat_level = 'HIGH' AND collected_at >= date('now', '-{} days')
        '''.format(days)).fetchone()[0]
        
        active_sources = cursor.execute('''
            SELECT COUNT(DISTINCT source) FROM crawled_data
            WHERE collected_at >= date('now', '-{} days')
        '''.format(days)).fetchone()[0]
        
        avg_sentiment = cursor.execute('''
            SELECT AVG(sentiment_score) FROM crawled_data
            WHERE collected_at >= date('now', '-{} days')
        '''.format(days)).fetchone()[0] or 0
        
        return jsonify({
            'totalThreats': total_threats,
            'highPriorityThreats': high_threats,
            'activeSources': active_sources,
            'avgSentiment': round(avg_sentiment, 2),
            'lastUpdate': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to fetch dashboard summary: {str(e)}'
        }), 500

@app.route('/api/dashboard/timeline', methods=['GET'])
def get_threat_timeline():
    """Get threat timeline data"""
    try:
        days = request.args.get('days', 30, type=int)
        
        cursor = db.conn.cursor()
        query = '''
            SELECT 
                DATE(collected_at) as date,
                threat_level,
                COUNT(*) as count
            FROM crawled_data
            WHERE collected_at >= date('now', '-{} days')
            GROUP BY DATE(collected_at), threat_level
            ORDER BY date ASC
        '''.format(days)
        
        results = cursor.execute(query).fetchall()
        
        timeline = {}
        for row in results:
            date = row[0]
            level = row[1]
            count = row[2]
            
            if date not in timeline:
                timeline[date] = {'date': date, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'INFO': 0}
            
            timeline[date][level] = count
        
        return jsonify(list(timeline.values()))
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to fetch timeline: {str(e)}'
        }), 500

@app.route('/api/analytics/sentiment', methods=['GET'])
def get_sentiment_analysis():
    """Get sentiment analysis data"""
    try:
        days = request.args.get('days', 7, type=int)
        
        cursor = db.conn.cursor()
        query = '''
            SELECT 
                sentiment_label,
                COUNT(*) as count,
                AVG(sentiment_score) as avg_score
            FROM crawled_data
            WHERE collected_at >= date('now', '-{} days')
            GROUP BY sentiment_label
        '''.format(days)
        
        results = cursor.execute(query).fetchall()
        
        sentiment_data = {
            'distribution': {},
            'total': 0
        }
        
        for row in results:
            label = row[0]
            count = row[1]
            avg_score = row[2]
            
            sentiment_data['distribution'][label] = {
                'count': count,
                'avgScore': round(avg_score, 2)
            }
            sentiment_data['total'] += count
        
        return jsonify(sentiment_data)
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to fetch sentiment analysis: {str(e)}'
        }), 500

@app.route('/api/analytics/trends', methods=['GET'])
def get_trends():
    """Get trending keywords and topics"""
    try:
        days = request.args.get('days', 7, type=int)
        
        cursor = db.conn.cursor()
        query = '''
            SELECT keywords, COUNT(*) as count
            FROM crawled_data
            WHERE collected_at >= date('now', '-{} days')
            AND keywords IS NOT NULL
            GROUP BY keywords
            ORDER BY count DESC
            LIMIT 20
        '''.format(days)
        
        results = cursor.execute(query).fetchall()
        
        trends = []
        for row in results:
            keywords = row[0]
            count = row[1]
            trends.append({
                'keywords': keywords,
                'count': count
            })
        
        return jsonify(trends)
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to fetch trends: {str(e)}'
        }), 500

@app.route('/api/threat-intel/check-ip/<ip_address>', methods=['GET'])
def check_ip_reputation(ip_address):
    """Check IP reputation using threat intel APIs"""
    try:
        results = threat_apis.check_ip_reputation(ip_address)
        return jsonify({
            'ip': ip_address,
            'reputation': results,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'error': f'Failed to check IP: {str(e)}'
        }), 500

@app.route('/api/threat-intel/check-domain/<domain>', methods=['GET'])
def check_domain_reputation(domain):
    """Check domain reputation using threat intel APIs"""
    try:
        results = threat_apis.check_domain_reputation(domain)
        return jsonify({
            'domain': domain,
            'reputation': results,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'error': f'Failed to check domain: {str(e)}'
        }), 500

@app.route('/api/threat-intel/feeds', methods=['GET'])
def get_threat_feeds():
    """Get threat intelligence feeds"""
    try:
        feeds = threat_apis.get_threat_feeds()
        return jsonify({
            'feeds': feeds,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'error': f'Failed to fetch threat feeds: {str(e)}'
        }), 500

@app.route('/api/reports/daily', methods=['GET'])
def get_daily_report():
    """Generate daily report"""
    try:
        date = request.args.get('date')
        if date:
            date = datetime.fromisoformat(date).date()
        else:
            date = datetime.now().date()
        
        report = threat_system.reporter.generate_daily_report(date)
        return jsonify(report)
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to generate report: {str(e)}'
        }), 500

@app.route('/api/reports/strategic', methods=['GET'])
def get_strategic_report():
    """Generate strategic analysis report"""
    try:
        days = request.args.get('days', 30, type=int)
        report = threat_system.reporter.generate_strategic_analysis(days)
        return jsonify(report)
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to generate report: {str(e)}'
        }), 500

@app.route('/api/config/sources', methods=['GET'])
def get_available_sources():
    """Get list of available data sources"""
    return jsonify({
        'sources': [
            {'id': 'twitter', 'name': 'Twitter/X', 'enabled': True, 'free': True},
            {'id': 'reddit', 'name': 'Reddit', 'enabled': True, 'free': True},
            {'id': 'facebook', 'name': 'Facebook', 'enabled': True, 'free': True},
            {'id': 'instagram', 'name': 'Instagram', 'enabled': True, 'free': True},
            {'id': 'linkedin', 'name': 'LinkedIn', 'enabled': True, 'free': True},
            {'id': 'telegram', 'name': 'Telegram', 'enabled': True, 'free': True},
            {'id': 'news', 'name': 'News Sites', 'enabled': True, 'free': True},
            {'id': 'forums', 'name': 'Forums', 'enabled': True, 'free': True}
        ],
        'features': {
            'all_platforms_enabled': True,
            'free_scraping': True,
            'no_api_keys_required': True,
            'threat_intel_apis': True,
            'sentiment_analysis': True,
            'multilanguage': True
        }
    })

if __name__ == '__main__':
    initialize_system()
    port = int(os.environ.get('PORT', 5001))
    print(f"\n🚀 Starting Threat Intelligence API on port {port}")
    print(f"📡 API Documentation: http://localhost:{port}/api/health")
    print(f"🔧 All features enabled: Crawler, Threat Analysis, Free Scraping")
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)
