export interface ThreatData {
  id: number;
  source: string;
  url: string;
  title: string;
  content: string;
  author: string;
  timestamp: string;
  sentiment_score: number;
  sentiment_label: 'positive' | 'negative' | 'neutral';
  keywords: string;
  threat_level: 'HIGH' | 'MEDIUM' | 'LOW' | 'INFO';
  collected_at: string;
}

export interface SentimentSummary {
  positive: number;
  negative: number;
  neutral: number;
  total: number;
  positive_ratio: number;
}

export interface ThreatSummary {
  HIGH: number;
  MEDIUM: number;
  LOW: number;
  INFO: number;
}

export interface CrawlRequest {
  sources: string[];
  keywords: string[];
  language: 'id' | 'en' | 'zh' | 'ar';
  maxResults: number;
}

export interface CrawlResult {
  success: boolean;
  message: string;
  data?: ThreatData[];
  error?: string;
}

export interface DashboardStats {
  total_threats: number;
  high_priority: number;
  medium_priority: number;
  low_priority: number;
  sentiment_summary: SentimentSummary;
  recent_threats: ThreatData[];
  trends: {
    date: string;
    count: number;
    threat_level: string;
  }[];
}

export interface Source {
  id: string;
  name: string;
  type: 'social' | 'news' | 'forum' | 'darkweb';
  url: string;
  enabled: boolean;
}

export interface Language {
  code: string;
  name: string;
  flag: string;
}
