import axios from 'axios';
import { CrawlRequest, CrawlResult, DashboardStats, ThreatData } from '../types';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const threatIntelAPI = {
  getDashboardStats: async (): Promise<DashboardStats> => {
    const response = await api.get('/dashboard/stats');
    return response.data;
  },

  getRecentThreats: async (limit = 50): Promise<ThreatData[]> => {
    const response = await api.get(`/threats/recent?limit=${limit}`);
    return response.data;
  },

  getThreatsByLevel: async (level: string): Promise<ThreatData[]> => {
    const response = await api.get(`/threats/level/${level}`);
    return response.data;
  },

  startCrawl: async (request: CrawlRequest): Promise<CrawlResult> => {
    const response = await api.post('/crawl/start', request);
    return response.data;
  },

  getCrawlStatus: async (): Promise<{ status: string; progress: number }> => {
    const response = await api.get('/crawl/status');
    return response.data;
  },

  searchThreats: async (query: string, filters?: any): Promise<ThreatData[]> => {
    const response = await api.post('/threats/search', { query, filters });
    return response.data;
  },

  exportData: async (format: 'json' | 'csv', filters?: any): Promise<Blob> => {
    const response = await api.post('/export', { format, filters }, {
      responseType: 'blob'
    });
    return response.data;
  },

  getSentimentAnalysis: async (days = 7): Promise<any> => {
    const response = await api.get(`/analytics/sentiment?days=${days}`);
    return response.data;
  },

  getTrendAnalysis: async (days = 30): Promise<any> => {
    const response = await api.get(`/analytics/trends?days=${days}`);
    return response.data;
  },
};

export default api;
