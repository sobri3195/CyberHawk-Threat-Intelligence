import React, { useState } from 'react';
import { 
  Search, 
  Globe, 
  Twitter, 
  MessageSquare,
  PlayCircle,
  StopCircle,
  CheckCircle,
  AlertCircle
} from 'lucide-react';
import { threatIntelAPI } from '../services/api';
import { CrawlRequest, Language, Source } from '../types';
import './Crawler.css';

const Crawler: React.FC = () => {
  const [crawling, setCrawling] = useState(false);
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState<any>(null);
  const [selectedLanguage, setSelectedLanguage] = useState<string>('id');
  const [keywords, setKeywords] = useState<string>('');
  const [selectedSources, setSelectedSources] = useState<string[]>(['news', 'social']);
  const [maxResults, setMaxResults] = useState<number>(100);

  const languages: Language[] = [
    { code: 'id', name: 'Bahasa Indonesia', flag: '🇮🇩' },
    { code: 'en', name: 'English', flag: '🇺🇸' },
    { code: 'zh', name: '中文 (Chinese)', flag: '🇨🇳' },
    { code: 'ar', name: 'العربية (Arabic)', flag: '🇸🇦' },
  ];

  const sources: Source[] = [
    { id: 'news', name: 'News Sites', type: 'news', url: '', enabled: true },
    { id: 'social', name: 'Social Media', type: 'social', url: '', enabled: true },
    { id: 'forums', name: 'Forums', type: 'forum', url: '', enabled: true },
    { id: 'darkweb', name: 'Dark Web', type: 'darkweb', url: '', enabled: false },
  ];

  const defaultKeywords = {
    id: 'serangan siber, malware, ransomware, pertahanan, TNI AU, keamanan nasional',
    en: 'cyber attack, malware, ransomware, defense, national security, threat',
    zh: '网络攻击, 恶意软件, 勒索软件, 国防, 国家安全',
    ar: 'الهجوم السيبراني, البرمجيات الخبيثة, الأمن القومي'
  };

  const handleStartCrawl = async () => {
    if (!keywords.trim()) {
      alert('Please enter keywords to search');
      return;
    }

    setCrawling(true);
    setProgress(0);
    setResults(null);

    const keywordList = keywords.split(',').map(k => k.trim()).filter(k => k);
    
    const request: CrawlRequest = {
      sources: selectedSources,
      keywords: keywordList,
      language: selectedLanguage as any,
      maxResults: maxResults,
    };

    try {
      const progressInterval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 90) return prev;
          return prev + Math.random() * 10;
        });
      }, 1000);

      const result = await threatIntelAPI.startCrawl(request);
      
      clearInterval(progressInterval);
      setProgress(100);
      setResults(result);

      setTimeout(() => {
        setCrawling(false);
      }, 1000);
    } catch (error: any) {
      console.error('Crawl error:', error);
      setCrawling(false);
      setResults({
        success: false,
        message: 'Crawling failed',
        error: error.message
      });
    }
  };

  const handleStopCrawl = () => {
    setCrawling(false);
    setProgress(0);
  };

  const toggleSource = (sourceId: string) => {
    setSelectedSources(prev => 
      prev.includes(sourceId)
        ? prev.filter(id => id !== sourceId)
        : [...prev, sourceId]
    );
  };

  const loadDefaultKeywords = () => {
    setKeywords(defaultKeywords[selectedLanguage as keyof typeof defaultKeywords] || defaultKeywords.en);
  };

  return (
    <div className="crawler animate-fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">Threat Intelligence Crawler</h1>
          <p className="page-subtitle">Multi-language crawler with sentiment analysis</p>
        </div>
      </div>

      <div className="crawler-grid">
        <div className="card crawler-config">
          <div className="card-header">
            <h3 className="card-title">Configuration</h3>
          </div>

          <div className="config-section">
            <label className="config-label">
              <Globe size={18} />
              Language Selection
            </label>
            <div className="language-grid">
              {languages.map(lang => (
                <button
                  key={lang.code}
                  className={`language-btn ${selectedLanguage === lang.code ? 'active' : ''}`}
                  onClick={() => setSelectedLanguage(lang.code)}
                >
                  <span className="language-flag">{lang.flag}</span>
                  <span className="language-name">{lang.name}</span>
                </button>
              ))}
            </div>
          </div>

          <div className="config-section">
            <label className="config-label">
              <Search size={18} />
              Keywords
              <button 
                className="btn-link"
                onClick={loadDefaultKeywords}
              >
                Load Default
              </button>
            </label>
            <textarea
              className="keyword-input"
              value={keywords}
              onChange={(e) => setKeywords(e.target.value)}
              placeholder="Enter keywords separated by commas..."
              rows={4}
            />
            <p className="input-hint">
              Separate multiple keywords with commas. Example: malware, cyber attack, ransomware
            </p>
          </div>

          <div className="config-section">
            <label className="config-label">
              <MessageSquare size={18} />
              Data Sources
            </label>
            <div className="sources-grid">
              {sources.map(source => (
                <div
                  key={source.id}
                  className={`source-card ${selectedSources.includes(source.id) ? 'selected' : ''} ${!source.enabled ? 'disabled' : ''}`}
                  onClick={() => source.enabled && toggleSource(source.id)}
                >
                  <div className="source-icon">
                    {source.type === 'news' && <Globe />}
                    {source.type === 'social' && <Twitter />}
                    {source.type === 'forum' && <MessageSquare />}
                    {source.type === 'darkweb' && <AlertCircle />}
                  </div>
                  <div className="source-name">{source.name}</div>
                  {selectedSources.includes(source.id) && (
                    <CheckCircle className="source-check" size={20} />
                  )}
                </div>
              ))}
            </div>
          </div>

          <div className="config-section">
            <label className="config-label">
              Max Results: {maxResults}
            </label>
            <input
              type="range"
              min="10"
              max="500"
              step="10"
              value={maxResults}
              onChange={(e) => setMaxResults(Number(e.target.value))}
              className="slider"
            />
          </div>

          <div className="crawler-actions">
            {!crawling ? (
              <button 
                className="btn btn-primary btn-large"
                onClick={handleStartCrawl}
                disabled={selectedSources.length === 0}
              >
                <PlayCircle size={20} />
                Start Crawling
              </button>
            ) : (
              <button 
                className="btn btn-danger btn-large"
                onClick={handleStopCrawl}
              >
                <StopCircle size={20} />
                Stop Crawling
              </button>
            )}
          </div>
        </div>

        <div className="card crawler-status">
          <div className="card-header">
            <h3 className="card-title">Crawling Status</h3>
          </div>

          {crawling && (
            <div className="status-content">
              <div className="status-animation">
                <div className="pulse-circle"></div>
                <Search size={48} className="status-icon" />
              </div>
              <h3 className="status-text">Crawling in progress...</h3>
              <div className="progress-bar">
                <div 
                  className="progress-fill"
                  style={{ width: `${progress}%` }}
                />
              </div>
              <p className="progress-text">{Math.round(progress)}% completed</p>
            </div>
          )}

          {!crawling && !results && (
            <div className="empty-state">
              <Search size={64} className="empty-icon" />
              <p className="empty-text">Ready to start crawling</p>
              <p className="empty-subtext">Configure sources and keywords, then click "Start Crawling"</p>
            </div>
          )}

          {!crawling && results && (
            <div className="results-content">
              {results.success ? (
                <div className="results-success">
                  <CheckCircle size={64} className="success-icon" />
                  <h3>Crawling Completed</h3>
                  <p className="results-message">{results.message}</p>
                  
                  <div className="results-stats">
                    <div className="result-stat">
                      <div className="stat-value">{results.data?.length || 0}</div>
                      <div className="stat-label">Items Collected</div>
                    </div>
                    <div className="result-stat">
                      <div className="stat-value">{selectedSources.length}</div>
                      <div className="stat-label">Sources Scanned</div>
                    </div>
                  </div>

                  <button 
                    className="btn btn-primary"
                    onClick={() => window.location.href = '/threats'}
                  >
                    View Threats
                  </button>
                </div>
              ) : (
                <div className="results-error">
                  <AlertCircle size={64} className="error-icon" />
                  <h3>Crawling Failed</h3>
                  <p className="error-message">{results.error || results.message}</p>
                  <button 
                    className="btn btn-primary"
                    onClick={handleStartCrawl}
                  >
                    Try Again
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Crawler;
