import React, { useState, useEffect } from 'react';
import { 
  Filter, 
  Download, 
  Search,
  ExternalLink,
  Calendar,
  TrendingUp
} from 'lucide-react';
import { threatIntelAPI } from '../services/api';
import { ThreatData } from '../types';
import './ThreatList.css';

const ThreatList: React.FC = () => {
  const [threats, setThreats] = useState<ThreatData[]>([]);
  const [filteredThreats, setFilteredThreats] = useState<ThreatData[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [levelFilter, setLevelFilter] = useState<string>('all');
  const [sentimentFilter, setSentimentFilter] = useState<string>('all');
  const [sourceFilter, setSourceFilter] = useState<string>('all');

  useEffect(() => {
    loadThreats();
  }, []);

  useEffect(() => {
    filterThreats();
  }, [threats, searchQuery, levelFilter, sentimentFilter, sourceFilter]);

  const loadThreats = async () => {
    try {
      setLoading(true);
      const data = await threatIntelAPI.getRecentThreats(200);
      setThreats(data);
    } catch (error) {
      console.error('Failed to load threats:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterThreats = () => {
    let filtered = threats;

    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(t => 
        t.title?.toLowerCase().includes(query) ||
        t.content.toLowerCase().includes(query) ||
        t.keywords?.toLowerCase().includes(query)
      );
    }

    if (levelFilter !== 'all') {
      filtered = filtered.filter(t => t.threat_level === levelFilter);
    }

    if (sentimentFilter !== 'all') {
      filtered = filtered.filter(t => t.sentiment_label === sentimentFilter);
    }

    if (sourceFilter !== 'all') {
      filtered = filtered.filter(t => t.source.includes(sourceFilter));
    }

    setFilteredThreats(filtered);
  };

  const handleExport = async () => {
    try {
      const blob = await threatIntelAPI.exportData('json', {
        level: levelFilter,
        sentiment: sentimentFilter,
        source: sourceFilter
      });
      
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `threats_${new Date().toISOString()}.json`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Export failed:', error);
    }
  };

  const uniqueSources = Array.from(new Set(threats.map(t => t.source)));

  return (
    <div className="threat-list animate-fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">Threat Intelligence Data</h1>
          <p className="page-subtitle">
            {filteredThreats.length} of {threats.length} threats
          </p>
        </div>
        <button className="btn btn-primary" onClick={handleExport}>
          <Download size={18} />
          Export Data
        </button>
      </div>

      <div className="filters-card card">
        <div className="search-box">
          <Search size={20} className="search-icon" />
          <input
            type="text"
            className="search-input"
            placeholder="Search threats by title, content, or keywords..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        <div className="filters-row">
          <div className="filter-group">
            <Filter size={16} />
            <label>Threat Level</label>
            <select 
              value={levelFilter} 
              onChange={(e) => setLevelFilter(e.target.value)}
              className="filter-select"
            >
              <option value="all">All Levels</option>
              <option value="HIGH">High</option>
              <option value="MEDIUM">Medium</option>
              <option value="LOW">Low</option>
              <option value="INFO">Info</option>
            </select>
          </div>

          <div className="filter-group">
            <label>Sentiment</label>
            <select 
              value={sentimentFilter} 
              onChange={(e) => setSentimentFilter(e.target.value)}
              className="filter-select"
            >
              <option value="all">All Sentiments</option>
              <option value="positive">Positive</option>
              <option value="negative">Negative</option>
              <option value="neutral">Neutral</option>
            </select>
          </div>

          <div className="filter-group">
            <label>Source</label>
            <select 
              value={sourceFilter} 
              onChange={(e) => setSourceFilter(e.target.value)}
              className="filter-select"
            >
              <option value="all">All Sources</option>
              {uniqueSources.map(source => (
                <option key={source} value={source}>{source}</option>
              ))}
            </select>
          </div>

          {(levelFilter !== 'all' || sentimentFilter !== 'all' || sourceFilter !== 'all' || searchQuery) && (
            <button 
              className="btn btn-secondary"
              onClick={() => {
                setLevelFilter('all');
                setSentimentFilter('all');
                setSourceFilter('all');
                setSearchQuery('');
              }}
            >
              Clear Filters
            </button>
          )}
        </div>
      </div>

      {loading ? (
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading threats...</p>
        </div>
      ) : filteredThreats.length > 0 ? (
        <div className="threats-grid">
          {filteredThreats.map(threat => (
            <div key={threat.id} className="threat-card card">
              <div className="threat-card-header">
                <div className="threat-badges">
                  <span className={`badge badge-${threat.threat_level.toLowerCase()}`}>
                    {threat.threat_level}
                  </span>
                  <span className={`badge badge-${threat.sentiment_label}`}>
                    {threat.sentiment_label}
                  </span>
                </div>
                <span className="threat-source">{threat.source}</span>
              </div>

              <h3 className="threat-card-title">
                {threat.title || threat.content.substring(0, 100) + '...'}
              </h3>

              <p className="threat-card-content">
                {threat.content.substring(0, 200)}
                {threat.content.length > 200 && '...'}
              </p>

              {threat.keywords && (
                <div className="threat-keywords">
                  {threat.keywords.split(',').slice(0, 5).map((keyword, idx) => (
                    <span key={idx} className="keyword-tag">
                      {keyword.trim()}
                    </span>
                  ))}
                </div>
              )}

              <div className="threat-card-footer">
                <div className="threat-meta">
                  <Calendar size={14} />
                  <span>{new Date(threat.timestamp).toLocaleDateString('id-ID')}</span>
                </div>
                <div className="threat-meta">
                  <TrendingUp size={14} />
                  <span>Sentiment: {threat.sentiment_score.toFixed(2)}</span>
                </div>
                {threat.url && (
                  <a 
                    href={threat.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="threat-link"
                  >
                    <ExternalLink size={14} />
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state card">
          <Search size={64} />
          <p className="empty-state-text">No threats found</p>
          <p className="empty-state-subtext">
            Try adjusting your filters or start a new crawl
          </p>
        </div>
      )}
    </div>
  );
};

export default ThreatList;
