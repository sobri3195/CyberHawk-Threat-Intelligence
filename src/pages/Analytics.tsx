import React, { useState, useEffect } from 'react';
import { 
  TrendingUp,
  BarChart3,
  PieChart as PieChartIcon,
  Calendar
} from 'lucide-react';
import { 
  LineChart, 
  Line, 
  BarChart, 
  Bar, 
  PieChart, 
  Pie, 
  Cell,
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer,
  Area,
  AreaChart
} from 'recharts';
import { threatIntelAPI } from '../services/api';
import './Analytics.css';

const Analytics: React.FC = () => {
  const [timeRange, setTimeRange] = useState<number>(7);

  useEffect(() => {
    loadAnalytics();
  }, [timeRange]);

  const loadAnalytics = async () => {
    try {
      await Promise.all([
        threatIntelAPI.getSentimentAnalysis(timeRange),
        threatIntelAPI.getTrendAnalysis(timeRange)
      ]);
    } catch (error) {
      console.error('Failed to load analytics:', error);
    }
  };

  const mockTrendData = [
    { date: '2024-01-15', HIGH: 12, MEDIUM: 25, LOW: 18, INFO: 32 },
    { date: '2024-01-16', HIGH: 15, MEDIUM: 22, LOW: 20, INFO: 28 },
    { date: '2024-01-17', HIGH: 10, MEDIUM: 28, LOW: 22, INFO: 35 },
    { date: '2024-01-18', HIGH: 18, MEDIUM: 30, LOW: 19, INFO: 30 },
    { date: '2024-01-19', HIGH: 14, MEDIUM: 26, LOW: 24, INFO: 33 },
    { date: '2024-01-20', HIGH: 20, MEDIUM: 32, LOW: 21, INFO: 29 },
    { date: '2024-01-21', HIGH: 16, MEDIUM: 28, LOW: 23, INFO: 31 },
  ];

  const mockSentimentTrend = [
    { date: '2024-01-15', positive: 120, negative: 80, neutral: 150 },
    { date: '2024-01-16', positive: 135, negative: 75, neutral: 160 },
    { date: '2024-01-17', positive: 125, negative: 85, neutral: 155 },
    { date: '2024-01-18', positive: 140, negative: 70, neutral: 165 },
    { date: '2024-01-19', positive: 130, negative: 90, neutral: 158 },
    { date: '2024-01-20', positive: 145, negative: 65, neutral: 170 },
    { date: '2024-01-21', positive: 138, negative: 78, neutral: 162 },
  ];

  const mockSourceDistribution = [
    { name: 'Twitter', value: 450, color: '#3b82f6' },
    { name: 'Reddit', value: 320, color: '#f97316' },
    { name: 'News Sites', value: 280, color: '#10b981' },
    { name: 'Forums', value: 150, color: '#8b5cf6' },
  ];

  const mockTopKeywords = [
    { keyword: 'malware', count: 245 },
    { keyword: 'cyber attack', count: 198 },
    { keyword: 'ransomware', count: 167 },
    { keyword: 'phishing', count: 142 },
    { keyword: 'vulnerability', count: 128 },
    { keyword: 'data breach', count: 115 },
    { keyword: 'ddos', count: 98 },
    { keyword: 'exploit', count: 87 },
  ];

  return (
    <div className="analytics animate-fade-in">
      <div className="page-header">
        <div>
          <h1 className="page-title">Analytics & Insights</h1>
          <p className="page-subtitle">Deep dive into threat intelligence patterns</p>
        </div>
        <div className="time-range-selector">
          <button 
            className={`time-btn ${timeRange === 7 ? 'active' : ''}`}
            onClick={() => setTimeRange(7)}
          >
            7 Days
          </button>
          <button 
            className={`time-btn ${timeRange === 30 ? 'active' : ''}`}
            onClick={() => setTimeRange(30)}
          >
            30 Days
          </button>
          <button 
            className={`time-btn ${timeRange === 90 ? 'active' : ''}`}
            onClick={() => setTimeRange(90)}
          >
            90 Days
          </button>
        </div>
      </div>

      <div className="analytics-grid">
        <div className="card analytics-card full-width">
          <div className="card-header">
            <h3 className="card-title">
              <TrendingUp size={20} />
              Threat Level Trends
            </h3>
          </div>
          <ResponsiveContainer width="100%" height={350}>
            <AreaChart data={mockTrendData}>
              <defs>
                <linearGradient id="colorHigh" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorMedium" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#f97316" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#f97316" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorLow" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#eab308" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#eab308" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="date" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip 
                contentStyle={{ 
                  background: '#1e293b', 
                  border: '1px solid #334155',
                  borderRadius: '8px'
                }} 
              />
              <Legend />
              <Area type="monotone" dataKey="HIGH" stroke="#ef4444" fillOpacity={1} fill="url(#colorHigh)" />
              <Area type="monotone" dataKey="MEDIUM" stroke="#f97316" fillOpacity={1} fill="url(#colorMedium)" />
              <Area type="monotone" dataKey="LOW" stroke="#eab308" fillOpacity={1} fill="url(#colorLow)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="card analytics-card">
          <div className="card-header">
            <h3 className="card-title">
              <BarChart3 size={20} />
              Sentiment Over Time
            </h3>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={mockSentimentTrend}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="date" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip 
                contentStyle={{ 
                  background: '#1e293b', 
                  border: '1px solid #334155',
                  borderRadius: '8px'
                }} 
              />
              <Legend />
              <Line type="monotone" dataKey="positive" stroke="#10b981" strokeWidth={2} />
              <Line type="monotone" dataKey="negative" stroke="#ef4444" strokeWidth={2} />
              <Line type="monotone" dataKey="neutral" stroke="#6b7280" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="card analytics-card">
          <div className="card-header">
            <h3 className="card-title">
              <PieChartIcon size={20} />
              Source Distribution
            </h3>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={mockSourceDistribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {mockSourceDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ 
                  background: '#1e293b', 
                  border: '1px solid #334155',
                  borderRadius: '8px'
                }} 
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="card analytics-card full-width">
          <div className="card-header">
            <h3 className="card-title">
              <TrendingUp size={20} />
              Top Keywords
            </h3>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={mockTopKeywords} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis type="number" stroke="#94a3b8" />
              <YAxis dataKey="keyword" type="category" stroke="#94a3b8" width={100} />
              <Tooltip 
                contentStyle={{ 
                  background: '#1e293b', 
                  border: '1px solid #334155',
                  borderRadius: '8px'
                }} 
              />
              <Bar dataKey="count" fill="#3b82f6" radius={[0, 8, 8, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="insights-grid">
        <div className="card insight-card">
          <div className="insight-icon" style={{ background: '#ef4444' }}>
            <TrendingUp size={24} />
          </div>
          <div className="insight-content">
            <h4>Increasing Threat Activity</h4>
            <p>High-priority threats increased by 23% in the last 7 days</p>
            <span className="insight-time">Last updated: 2 hours ago</span>
          </div>
        </div>

        <div className="card insight-card">
          <div className="insight-icon" style={{ background: '#10b981' }}>
            <BarChart3 size={24} />
          </div>
          <div className="insight-content">
            <h4>Sentiment Improving</h4>
            <p>Positive sentiment increased by 15% compared to last period</p>
            <span className="insight-time">Last updated: 1 hour ago</span>
          </div>
        </div>

        <div className="card insight-card">
          <div className="insight-icon" style={{ background: '#f97316' }}>
            <Calendar size={24} />
          </div>
          <div className="insight-content">
            <h4>Peak Activity Hours</h4>
            <p>Most threat activity occurs between 14:00 - 18:00 WIB</p>
            <span className="insight-time">Based on 30-day analysis</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
