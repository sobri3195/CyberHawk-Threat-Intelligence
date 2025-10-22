const mockThreats = [];

for (let i = 0; i < 50; i++) {
  const levels = ['HIGH', 'MEDIUM', 'LOW', 'INFO'];
  const sentiments = ['positive', 'negative', 'neutral'];
  const sources = ['Twitter', 'Reddit', 'News', 'Forum', 'Dark Web'];
  
  mockThreats.push({
    id: i + 1,
    source: sources[Math.floor(Math.random() * sources.length)],
    url: `https://example.com/threat/${i + 1}`,
    title: `Threat Report #${i + 1}: Suspicious Activity Detected`,
    content: `This is a detailed threat intelligence report about suspicious activity detected in system. The activity involves ${['malware', 'phishing', 'ransomware', 'ddos', 'exploit'][Math.floor(Math.random() * 5)]} targeting ${['government', 'military', 'infrastructure', 'private sector'][Math.floor(Math.random() * 4)]} networks.`,
    author: `analyst_${Math.floor(Math.random() * 20)}`,
    timestamp: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString(),
    sentiment_score: (Math.random() * 2 - 1),
    sentiment_label: sentiments[Math.floor(Math.random() * sentiments.length)],
    keywords: 'malware, cyber attack, threat intelligence, security',
    threat_level: levels[Math.floor(Math.random() * levels.length)],
    collected_at: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString()
  });
}

export const getRecentThreats = async (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 50;
    const threats = mockThreats.slice(0, limit);
    
    res.json(threats);
  } catch (error) {
    console.error('Error in getRecentThreats:', error);
    res.status(500).json({
      error: 'Failed to fetch threats',
      message: error.message
    });
  }
};

export const getThreatsByLevel = async (req, res) => {
  try {
    const { level } = req.params;
    const threats = mockThreats.filter(t => t.threat_level === level.toUpperCase());
    
    res.json(threats);
  } catch (error) {
    console.error('Error in getThreatsByLevel:', error);
    res.status(500).json({
      error: 'Failed to fetch threats by level',
      message: error.message
    });
  }
};

export const searchThreats = async (req, res) => {
  try {
    const { query, filters } = req.body;
    
    let threats = mockThreats;
    
    if (query) {
      const searchTerm = query.toLowerCase();
      threats = threats.filter(t => 
        t.title.toLowerCase().includes(searchTerm) ||
        t.content.toLowerCase().includes(searchTerm) ||
        t.keywords.toLowerCase().includes(searchTerm)
      );
    }
    
    if (filters) {
      if (filters.level && filters.level !== 'all') {
        threats = threats.filter(t => t.threat_level === filters.level);
      }
      if (filters.sentiment && filters.sentiment !== 'all') {
        threats = threats.filter(t => t.sentiment_label === filters.sentiment);
      }
      if (filters.source && filters.source !== 'all') {
        threats = threats.filter(t => t.source === filters.source);
      }
    }
    
    res.json(threats);
  } catch (error) {
    console.error('Error in searchThreats:', error);
    res.status(500).json({
      error: 'Search failed',
      message: error.message
    });
  }
};
