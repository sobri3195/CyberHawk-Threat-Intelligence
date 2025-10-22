import Sentiment from 'sentiment';

const sentiment = new Sentiment();
let crawlStatus = {
  inProgress: false,
  progress: 0
};

const mockCrawlData = (keywords, sources, language) => {
  const threats = [];
  const sourceTypes = {
    'news': ['CNN', 'BBC', 'Reuters', 'Kompas', 'Detik'],
    'social': ['Twitter', 'Reddit', 'Facebook', 'LinkedIn'],
    'forums': ['Security Forum', 'Hacker News', 'Stack Exchange'],
    'darkweb': ['Onion Forum', 'Dark Market']
  };

  const sampleContent = {
    'en': {
      high: [
        'Critical vulnerability discovered in defense systems allowing remote code execution',
        'Massive cyber attack targeting military infrastructure across Southeast Asia',
        'Zero-day exploit being actively used against government networks'
      ],
      medium: [
        'Suspicious network activity detected in regional defense systems',
        'Phishing campaign targeting military personnel with credential harvesting',
        'New malware variant identified with capabilities to bypass security measures'
      ],
      low: [
        'Security advisory issued for outdated software in government systems',
        'Potential threat actor reconnaissance activities observed',
        'Minor vulnerability patched in widely-used defense application'
      ]
    },
    'id': {
      high: [
        'Kerentanan kritis ditemukan di sistem pertahanan memungkinkan eksekusi kode jarak jauh',
        'Serangan siber masif menargetkan infrastruktur militer di Asia Tenggara',
        'Eksploitasi zero-day aktif digunakan terhadap jaringan pemerintah'
      ],
      medium: [
        'Aktivitas jaringan mencurigakan terdeteksi di sistem pertahanan regional',
        'Kampanye phishing menargetkan personel militer dengan pencurian kredensial',
        'Varian malware baru teridentifikasi dengan kemampuan melewati langkah keamanan'
      ],
      low: [
        'Peringatan keamanan dikeluarkan untuk perangkat lunak usang di sistem pemerintah',
        'Aktivitas pengintaian aktor ancaman potensial diamati',
        'Kerentanan minor diperbaiki di aplikasi pertahanan yang banyak digunakan'
      ]
    }
  };

  const contentLang = language in sampleContent ? language : 'en';
  const levels = ['high', 'medium', 'low'];
  
  sources.forEach(sourceType => {
    const sourceList = sourceTypes[sourceType] || sourceTypes['news'];
    
    for (let i = 0; i < 5; i++) {
      const level = levels[Math.floor(Math.random() * levels.length)];
      const levelUpper = level.toUpperCase();
      const contentArray = sampleContent[contentLang][level];
      const content = contentArray[Math.floor(Math.random() * contentArray.length)];
      
      const sentimentAnalysis = sentiment.analyze(content);
      let sentimentLabel = 'neutral';
      if (sentimentAnalysis.score > 1) sentimentLabel = 'positive';
      else if (sentimentAnalysis.score < -1) sentimentLabel = 'negative';

      threats.push({
        id: Date.now() + Math.random(),
        source: sourceList[Math.floor(Math.random() * sourceList.length)],
        url: `https://example.com/threat/${Date.now()}`,
        title: `${levelUpper}: ${keywords[Math.floor(Math.random() * keywords.length)]}`,
        content: content,
        author: `analyst_${Math.floor(Math.random() * 100)}`,
        timestamp: new Date(Date.now() - Math.random() * 24 * 60 * 60 * 1000).toISOString(),
        sentiment_score: sentimentAnalysis.score / 10,
        sentiment_label: sentimentLabel,
        keywords: keywords.slice(0, 3).join(', '),
        threat_level: levelUpper,
        collected_at: new Date().toISOString()
      });
    }
  });

  return threats;
};

export const startCrawl = async (req, res) => {
  try {
    const { sources, keywords, language, maxResults } = req.body;

    if (!sources || !keywords || sources.length === 0 || keywords.length === 0) {
      return res.status(400).json({
        success: false,
        message: 'Sources and keywords are required'
      });
    }

    crawlStatus.inProgress = true;
    crawlStatus.progress = 0;

    setTimeout(() => {
      crawlStatus.progress = 100;
      crawlStatus.inProgress = false;
    }, 5000);

    const threats = mockCrawlData(keywords, sources, language);

    res.json({
      success: true,
      message: `Successfully crawled ${threats.length} items from ${sources.length} sources`,
      data: threats
    });

  } catch (error) {
    console.error('Error in startCrawl:', error);
    crawlStatus.inProgress = false;
    res.status(500).json({
      success: false,
      message: 'Crawl failed',
      error: error.message
    });
  }
};

export const getCrawlStatus = async (req, res) => {
  try {
    res.json(crawlStatus);
  } catch (error) {
    console.error('Error in getCrawlStatus:', error);
    res.status(500).json({
      error: 'Failed to fetch crawl status',
      message: error.message
    });
  }
};
