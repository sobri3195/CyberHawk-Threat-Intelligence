export const getSentimentAnalysis = async (req, res) => {
  try {
    const days = parseInt(req.query.days) || 7;
    
    const mockData = {
      period: `${days} days`,
      summary: {
        positive: 145,
        negative: 98,
        neutral: 187,
        total: 430
      },
      trend: [
        { date: '2024-01-15', positive: 18, negative: 12, neutral: 24 },
        { date: '2024-01-16', positive: 22, negative: 15, neutral: 28 },
        { date: '2024-01-17', positive: 20, negative: 14, neutral: 26 },
        { date: '2024-01-18', positive: 24, negative: 16, neutral: 30 },
        { date: '2024-01-19', positive: 21, negative: 13, neutral: 27 },
        { date: '2024-01-20', positive: 25, negative: 17, neutral: 32 },
        { date: '2024-01-21', positive: 23, negative: 11, neutral: 29 }
      ]
    };
    
    res.json(mockData);
  } catch (error) {
    console.error('Error in getSentimentAnalysis:', error);
    res.status(500).json({
      error: 'Failed to fetch sentiment analysis',
      message: error.message
    });
  }
};

export const getTrendAnalysis = async (req, res) => {
  try {
    const days = parseInt(req.query.days) || 30;
    
    const mockData = {
      period: `${days} days`,
      threats_by_level: {
        HIGH: 67,
        MEDIUM: 142,
        LOW: 198,
        INFO: 234
      },
      daily_trends: [
        { date: '2024-01-15', HIGH: 8, MEDIUM: 18, LOW: 25, INFO: 32 },
        { date: '2024-01-16', HIGH: 10, MEDIUM: 20, LOW: 28, INFO: 35 },
        { date: '2024-01-17', HIGH: 7, MEDIUM: 22, LOW: 30, INFO: 38 },
        { date: '2024-01-18', HIGH: 12, MEDIUM: 24, LOW: 32, INFO: 40 },
        { date: '2024-01-19', HIGH: 9, MEDIUM: 19, LOW: 27, INFO: 36 },
        { date: '2024-01-20', HIGH: 11, MEDIUM: 21, LOW: 29, INFO: 39 },
        { date: '2024-01-21', HIGH: 10, MEDIUM: 18, LOW: 27, INFO: 34 }
      ],
      top_sources: [
        { name: 'Twitter', count: 185 },
        { name: 'Reddit', count: 142 },
        { name: 'News', count: 128 },
        { name: 'Forums', count: 96 }
      ]
    };
    
    res.json(mockData);
  } catch (error) {
    console.error('Error in getTrendAnalysis:', error);
    res.status(500).json({
      error: 'Failed to fetch trend analysis',
      message: error.message
    });
  }
};
