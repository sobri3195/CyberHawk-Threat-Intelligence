export const getDashboardStats = async (req, res) => {
  try {
    const mockData = {
      total_threats: 247,
      high_priority: 23,
      medium_priority: 68,
      low_priority: 98,
      sentiment_summary: {
        positive: 89,
        negative: 67,
        neutral: 91,
        total: 247,
        positive_ratio: 0.36
      },
      recent_threats: [
        {
          id: 1,
          source: 'twitter',
          url: 'https://twitter.com/example',
          title: 'Malware campaign targeting Indonesian defense sector',
          content: 'A sophisticated malware campaign has been detected targeting defense infrastructure in Southeast Asia, with particular focus on Indonesian military networks.',
          author: 'security_researcher',
          timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
          sentiment_score: -0.65,
          sentiment_label: 'negative',
          keywords: 'malware, defense, Indonesia, cyber attack',
          threat_level: 'HIGH',
          collected_at: new Date().toISOString()
        },
        {
          id: 2,
          source: 'reddit',
          url: 'https://reddit.com/r/cybersecurity',
          title: 'New ransomware variant discovered',
          content: 'Security researchers have identified a new ransomware variant that exploits vulnerabilities in government systems across Asia-Pacific region.',
          author: 'cyber_analyst',
          timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(),
          sentiment_score: -0.78,
          sentiment_label: 'negative',
          keywords: 'ransomware, vulnerability, government',
          threat_level: 'HIGH',
          collected_at: new Date().toISOString()
        },
        {
          id: 3,
          source: 'news',
          url: 'https://example.com/news',
          title: 'Cyber defense improvements announced by military',
          content: 'TNI AU announces major upgrades to cyber defense capabilities, including new threat detection systems and enhanced monitoring infrastructure.',
          author: 'defense_news',
          timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString(),
          sentiment_score: 0.72,
          sentiment_label: 'positive',
          keywords: 'TNI AU, cyber defense, upgrade',
          threat_level: 'INFO',
          collected_at: new Date().toISOString()
        },
        {
          id: 4,
          source: 'forum',
          url: 'https://forum.example.com',
          title: 'Discussion on APT group activities',
          content: 'Security forum discusses recent activities of advanced persistent threat groups targeting military installations in the region.',
          author: 'security_expert',
          timestamp: new Date(Date.now() - 8 * 60 * 60 * 1000).toISOString(),
          sentiment_score: -0.45,
          sentiment_label: 'negative',
          keywords: 'APT, military, threat group',
          threat_level: 'MEDIUM',
          collected_at: new Date().toISOString()
        },
        {
          id: 5,
          source: 'twitter',
          url: 'https://twitter.com/infosec',
          title: 'Phishing campaign targeting government employees',
          content: 'A widespread phishing campaign has been detected targeting government and military personnel with sophisticated social engineering tactics.',
          author: 'threat_intel',
          timestamp: new Date(Date.now() - 10 * 60 * 60 * 1000).toISOString(),
          sentiment_score: -0.55,
          sentiment_label: 'negative',
          keywords: 'phishing, social engineering, government',
          threat_level: 'MEDIUM',
          collected_at: new Date().toISOString()
        }
      ],
      trends: [
        { date: '2024-01-15', HIGH: 3, MEDIUM: 8, LOW: 12, INFO: 15 },
        { date: '2024-01-16', HIGH: 5, MEDIUM: 10, LOW: 14, INFO: 18 },
        { date: '2024-01-17', HIGH: 4, MEDIUM: 12, LOW: 16, INFO: 20 },
        { date: '2024-01-18', HIGH: 7, MEDIUM: 15, LOW: 18, INFO: 22 },
        { date: '2024-01-19', HIGH: 6, MEDIUM: 13, LOW: 20, INFO: 24 },
        { date: '2024-01-20', HIGH: 8, MEDIUM: 16, LOW: 22, INFO: 26 },
        { date: '2024-01-21', HIGH: 9, MEDIUM: 18, LOW: 24, INFO: 28 }
      ]
    };

    res.json(mockData);
  } catch (error) {
    console.error('Error in getDashboardStats:', error);
    res.status(500).json({ 
      error: 'Failed to fetch dashboard stats',
      message: error.message 
    });
  }
};
