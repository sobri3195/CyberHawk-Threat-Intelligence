# ⚡ Quick Start Guide

Panduan cepat untuk menjalankan TNI AU Threat Intelligence System.

## 🎯 Prerequisites

```bash
# Check Node.js version (need 18+)
node --version

# Check npm version
npm --version
```

## 🚀 Installation (5 menit)

```bash
# 1. Clone repository
git clone <repository-url>
cd threat-intel-app

# 2. Install dependencies
npm install

# 3. Start application
./start.sh
```

## 🌐 Access

```
Frontend:  http://localhost:3000
Backend:   http://localhost:5000
API Docs:  See API.md
```

## 📋 Basic Commands

### Start Development
```bash
./start.sh              # Easy start (recommended)
npm run dev             # Frontend only
npm run server          # Backend only
```

### Build Production
```bash
npm run build           # Build for production
npm run preview         # Preview production build
```

### Stop All
```bash
# Press Ctrl+C in terminals
# Or kill processes:
pkill -f "node server"
lsof -ti:3000 | xargs kill -9
lsof -ti:5000 | xargs kill -9
```

## 🎮 Quick Tour (10 menit)

### 1. Dashboard (2 min)
```
→ http://localhost:3000
✓ View stats: 247 threats, 23 high priority
✓ See charts: Pie chart (distribution), Bar chart (sentiment)
✓ Recent threats table
```

### 2. Start Crawling (3 min)
```
→ Click "Crawler" in sidebar
✓ Select language: Indonesia/English/Chinese/Arabic
✓ Click "Load Default" for keywords
✓ Select sources: News, Social Media, Forums
✓ Click "Start Crawling"
✓ Wait ~5 seconds
✓ View results
```

### 3. Analyze Threats (3 min)
```
→ Click "Threat List"
✓ Use search: type "malware"
✓ Filter by level: Select "HIGH"
✓ Filter by sentiment: Select "Negative"
✓ Click "Export Data" to download
```

### 4. View Analytics (2 min)
```
→ Click "Analytics"
✓ Change time range: 7/30/90 days
✓ View area chart: Threat trends
✓ See line chart: Sentiment over time
✓ Check pie chart: Source distribution
✓ Review bar chart: Top keywords
```

## 🔑 Key Features

| Feature | Description | Location |
|---------|-------------|----------|
| **Real-time Dashboard** | Overview statistik ancaman | `/dashboard` |
| **Multi-language Crawler** | 4 bahasa, multiple sources | `/crawler` |
| **Advanced Filtering** | Search & filter threats | `/threats` |
| **Analytics & Charts** | Visual trend analysis | `/analytics` |
| **Export Data** | JSON export | Threat List page |

## 🎨 UI Elements

### Color Codes
- 🔴 **Red**: HIGH threat
- 🟠 **Orange**: MEDIUM threat
- 🟡 **Yellow**: LOW threat
- 🔵 **Blue**: INFO level
- 🟢 **Green**: Positive sentiment
- ⚫ **Gray**: Neutral sentiment

### Navigation
- **Dashboard**: Home overview
- **Crawler**: Start new crawl
- **Threat List**: Browse all threats
- **Analytics**: View insights

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

### Dependencies Issue
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
```

### Backend Not Responding
```bash
# Check if server is running
curl http://localhost:5000/api/health

# Restart server
npm run server
```

### Build Errors
```bash
# Clear cache and rebuild
rm -rf dist
npm run build
```

## 📊 Demo Keywords

### Bahasa Indonesia
```
serangan siber, malware, ransomware, pertahanan, TNI AU, keamanan nasional
```

### English
```
cyber attack, malware, ransomware, defense, military, national security
```

### Chinese
```
网络攻击, 恶意软件, 勒索软件, 国防, 国家安全
```

### Arabic
```
الهجوم السيبراني, البرمجيات الخبيثة, الأمن القومي
```

## 🎯 Quick Demo Flow

```
1. Start app (./start.sh)
2. Open browser → http://localhost:3000
3. View Dashboard stats
4. Go to Crawler
5. Select Indonesian language
6. Load default keywords
7. Check News + Social Media sources
8. Start Crawling
9. Wait for results
10. Click "View Threats"
11. Apply HIGH filter
12. Export data
```

## 📱 Keyboard Shortcuts

```
Ctrl + R       : Refresh page
Ctrl + F       : Search in page
Esc            : Close modals
Tab            : Navigate fields
Enter          : Submit forms
```

## 🔍 API Quick Test

```bash
# Test health
curl http://localhost:5000/api/health

# Get dashboard stats
curl http://localhost:5000/api/dashboard/stats

# Get recent threats
curl http://localhost:5000/api/threats/recent?limit=5

# Start crawl (POST)
curl -X POST http://localhost:5000/api/crawl/start \
  -H "Content-Type: application/json" \
  -d '{
    "sources": ["news"],
    "keywords": ["malware"],
    "language": "en",
    "maxResults": 50
  }'
```

## 📚 Documentation Links

| Document | Purpose |
|----------|---------|
| **README.md** | Complete documentation |
| **API.md** | API reference |
| **FEATURES.md** | Feature list |
| **DEMO.md** | Demo scenarios |
| **DEVELOPMENT.md** | Dev guide |
| **PROJECT_SUMMARY.md** | Overview |

## 🆘 Need Help?

1. Check README.md for detailed info
2. Review API.md for API details
3. See DEMO.md for step-by-step guide
4. Check DEVELOPMENT.md for technical docs
5. Contact development team

## ⚡ Pro Tips

1. **Use ./start.sh** - Easiest way to start
2. **Keep both terminals running** - Frontend + Backend
3. **Check browser console** - For errors
4. **Use mock data** - Perfect for demo
5. **Export data** - To analyze offline
6. **Change time ranges** - See different trends
7. **Try all languages** - Test multi-language
8. **Combine filters** - For specific analysis

## 🎓 Learning Path

### Beginner (30 min)
1. Read this Quick Start
2. Run the application
3. Click through all pages
4. Try basic features

### Intermediate (1 hour)
1. Run a crawl
2. Apply filters
3. Export data
4. Explore analytics

### Advanced (2 hours)
1. Read API.md
2. Test API endpoints
3. Read DEVELOPMENT.md
4. Understand architecture

## 🏁 Success Checklist

- [ ] Application starts without errors
- [ ] Can access http://localhost:3000
- [ ] Dashboard shows stats
- [ ] Can start a crawl
- [ ] Filters work in Threat List
- [ ] Analytics page loads
- [ ] Can export data
- [ ] API responds to curl

## 🎉 You're Ready!

Application is ready for:
- ✅ Demo presentations
- ✅ User testing
- ✅ Feature exploration
- ✅ Development

---

**Need more details?** → Read README.md

**Need API info?** → Read API.md

**Need demo script?** → Read DEMO.md

---

**Happy Intelligence Gathering! 🛡️**
