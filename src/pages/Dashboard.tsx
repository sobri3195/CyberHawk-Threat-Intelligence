import React, { useState, useEffect } from 'react';
import { 
  AlertTriangle, 
  TrendingUp, 
  Activity, 
  Database,
  Shield,
  ThumbsUp,
  ThumbsDown,
  Minus
} from 'lucide-react';
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { threatIntelAPI } from '../services/api';
import { DashboardStats } from '../types';
import './Dashboard.css';

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDashboardData();
    const interval = setInterval(loadDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const data = await threatIntelAPI.getDashboardStats();
      setStats(data);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load dashboard data');
      console.error('Error loading dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading && !stats) {
    return (
      <div className="dashboard">
        <div className="page-header">
          <h1 className="page-title">Dashboard</h1>
          <p className="page-subtitle">Real-time Threat Intelligence Overview</p>
        </div>
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading dashboard data...</p>
        </div>
      </div>
    );
  }

  if (error && !stats) {
    return (
      <div className="dashboard">
        <div className="page-header">
          <h1 className="page-title">Dashboard</h1>
          <p className="page-subtitle">Real-time Threat Intelligence Overview</p>
        </div>
        <div className="error-container">
          <AlertTriangle size={48} />
          <p>{error}</p>
          <button className="btn btn-primary" onClick={loadDashboardData}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  const COLORS = {
    HIGH: '#ef4444',
    MEDIUM: '#f97316',
    LOW: '#eab308',
    INFO: '#3b82f6',
  };

  const threatDistribution = [
    { name: 'High', value: stats?.high_priority || 0, color: COLORS.HIGH },
    { name: 'Medium', value: stats?.medium_priority || 0, color: COLORS.MEDIUM },
    { name: 'Low', value: stats?.low_priority || 0, color: COLORS.LOW },
  ];

  const sentimentData = [
    { 
      name: 'Positive', 
      value: stats?.sentiment_summary.positive || 0, 
      color: '#10b981' 
    },
    { 
      name: 'Negative', 
      value: stats?.sentiment_summary.negative || 0, 
      color: '#ef4444' 
    },
    { 
      name: 'Neutral', 
      value: stats?.sentiment_summary.neutral || 0, 
      color: '#6b7280' 
    },
  ];

  return (
    <div className="dashboard animate-fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">Dashboard</h1>
          <p className="page-subtitle">Real-time Threat Intelligence Overview - TNI AU</p>
        </div>
        <button className="btn btn-primary" onClick={loadDashboardData}>
          <Activity size={18} />
          Refresh
        </button>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)' }}>
            <Database />
          </div>
          <div className="stat-content">
            <div className="stat-label">Total Threats</div>
            <div className="stat-value">{stats?.total_threats || 0}</div>
            <div className="stat-change positive">
              <TrendingUp size={12} /> +12% from last week
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)' }}>
            <AlertTriangle />
          </div>
          <div className="stat-content">
            <div className="stat-label">High Priority</div>
            <div className="stat-value">{stats?.high_priority || 0}</div>
            <div className="stat-change negative">
              <TrendingUp size={12} /> Requires attention
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #f97316 0%, #ea580c 100%)' }}>
            <Shield />
          </div>
          <div className="stat-content">
            <div className="stat-label">Medium Priority</div>
            <div className="stat-value">{stats?.medium_priority || 0}</div>
            <div className="stat-change">Monitor closely</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)' }}>
            <Activity />
          </div>
          <div className="stat-content">
            <div className="stat-label">System Status</div>
            <div className="stat-value">Active</div>
            <div className="stat-change positive">All systems operational</div>
          </div>
        </div>
      </div>

      <div className="charts-grid">
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Threat Level Distribution</h3>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={threatDistribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {threatDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Sentiment Analysis</h3>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={sentimentData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="name" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip 
                contentStyle={{ 
                  background: '#1e293b', 
                  border: '1px solid #334155',
                  borderRadius: '8px'
                }} 
              />
              <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                {sentimentData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Recent Threats</h3>
          <span className="badge badge-info">
            Last 24 hours
          </span>
        </div>
        <div className="threat-table">
          {stats?.recent_threats && stats.recent_threats.length > 0 ? (
            <table>
              <thead>
                <tr>
                  <th>Source</th>
                  <th>Title</th>
                  <th>Threat Level</th>
                  <th>Sentiment</th>
                  <th>Time</th>
                </tr>
              </thead>
              <tbody>
                {stats.recent_threats.slice(0, 10).map((threat) => (
                  <tr key={threat.id}>
                    <td>
                      <span className="source-badge">{threat.source}</span>
                    </td>
                    <td className="threat-title">
                      {threat.title || threat.content.substring(0, 80) + '...'}
                    </td>
                    <td>
                      <span className={`badge badge-${threat.threat_level.toLowerCase()}`}>
                        {threat.threat_level}
                      </span>
                    </td>
                    <td>
                      <span className={`badge badge-${threat.sentiment_label}`}>
                        {threat.sentiment_label === 'positive' && <ThumbsUp size={12} />}
                        {threat.sentiment_label === 'negative' && <ThumbsDown size={12} />}
                        {threat.sentiment_label === 'neutral' && <Minus size={12} />}
                        {threat.sentiment_label}
                      </span>
                    </td>
                    <td className="threat-time">
                      {new Date(threat.timestamp).toLocaleString('id-ID')}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="empty-state">
              <div className="empty-state-icon">
                <Database />
              </div>
              <div className="empty-state-text">No recent threats</div>
              <div className="empty-state-subtext">Start crawling to collect threat data</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
