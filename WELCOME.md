# 🎉 Welcome to TNI AU Threat Intelligence System!

```
████████╗███╗   ██╗██╗     █████╗ ██╗   ██╗
╚══██╔══╝████╗  ██║██║    ██╔══██╗██║   ██║
   ██║   ██╔██╗ ██║██║    ███████║██║   ██║
   ██║   ██║╚██╗██║██║    ██╔══██║██║   ██║
   ██║   ██║ ╚████║██║    ██║  ██║╚██████╔╝
   ╚═╝   ╚═╝  ╚═══╝╚═╝    ╚═╝  ╚═╝ ╚═════╝
   
   CYBER THREAT INTELLIGENCE SYSTEM
   Version 1.0.0 | January 2024
```

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies (1 minute)
```bash
npm install
```

### Step 2: Start Application (30 seconds)
```bash
./start.sh
```

### Step 3: Open Browser
```
http://localhost:3000
```

**That's it! You're ready to hunt threats! 🎯**

---

## 📚 Where to Go Next?

### 🆕 First Time User?
Start here → **[QUICK_START.md](QUICK_START.md)**
- 5-minute quick guide
- Basic commands
- First demo walkthrough

### 🎬 Need to Present?
Check this → **[DEMO.md](DEMO.md)**
- Complete demo scenarios
- Q&A preparation
- Presentation tips

### 💻 Developer?
Read this → **[DEVELOPMENT.md](DEVELOPMENT.md)**
- Setup environment
- Code structure
- Contributing guide

### 🔍 Exploring?
Browse → **[INDEX.md](INDEX.md)**
- All documentation indexed
- Quick navigation
- Role-based guides

---

## ⚡ Quick Commands

```bash
# Start everything (recommended)
./start.sh

# Start backend only
npm run server

# Start frontend only
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 🎯 What Can You Do?

### 🔴 Monitor Real-time Threats
- View dashboard with live statistics
- Track threat levels (HIGH, MEDIUM, LOW, INFO)
- Analyze sentiment (Positive, Negative, Neutral)

### 🌐 Multi-language Crawling
- 🇮🇩 Bahasa Indonesia
- 🇺🇸 English
- 🇨🇳 Chinese (中文)
- 🇸🇦 Arabic (العربية)

### 📊 Advanced Analytics
- Trend analysis over time
- Source distribution
- Keyword frequency
- Automated insights

### 🔍 Powerful Search
- Filter by threat level
- Filter by sentiment
- Filter by source
- Full-text search
- Export to JSON

---

## 💡 Pro Tips

1. **Use the demo data** - Perfect for presentations and testing
2. **Try all languages** - See multi-language capabilities
3. **Export data** - Share findings with your team
4. **Check analytics** - Discover patterns and trends
5. **Combine filters** - Get laser-focused results

---

## 📖 Documentation Hub

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [INDEX.md](INDEX.md) | Documentation navigation | 5 min |
| [QUICK_START.md](QUICK_START.md) | Quick start guide | 10 min |
| [README.md](README.md) | Complete documentation | 30 min |
| [DEMO.md](DEMO.md) | Demo scenarios | 20 min |
| [API.md](API.md) | API reference | 25 min |
| [FEATURES.md](FEATURES.md) | Feature details | 20 min |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Developer guide | 40 min |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Project overview | 15 min |

**Total**: ~2.5 hours for complete understanding

---

## 🎓 Learning Path

### Day 1: Getting Started
- [ ] Install and run application
- [ ] Explore dashboard
- [ ] Try crawler with different languages
- [ ] Apply filters in threat list

### Day 2: Deep Dive
- [ ] Read README.md
- [ ] Practice all demo scenarios
- [ ] Test API endpoints
- [ ] Export and analyze data

### Day 3: Master Level
- [ ] Read DEVELOPMENT.md
- [ ] Understand architecture
- [ ] Explore source code
- [ ] Try customizations

---

## 🆘 Need Help?

### Quick Answers
- **Installation issues?** → See QUICK_START.md troubleshooting
- **How do I...?** → Check README.md usage section
- **API not responding?** → Verify server is running on port 5000
- **Frontend not loading?** → Check if dev server is on port 3000

### Resources
- 📚 Complete docs in [INDEX.md](INDEX.md)
- 🐛 Troubleshooting in [QUICK_START.md](QUICK_START.md)
- 💬 Contact development team
- 📧 Check official channels

---

## ✨ Features at a Glance

```
✓ Real-time threat monitoring
✓ Multi-language support (4 languages)
✓ Sentiment analysis
✓ Advanced filtering & search
✓ Data visualization & charts
✓ Export capabilities
✓ Dark professional UI
✓ Responsive design
✓ RESTful API
✓ Modern tech stack
```

---

## 🎯 System Requirements

```
✓ Node.js 18+
✓ npm or yarn
✓ Modern browser (Chrome, Firefox, Edge)
✓ 4GB RAM minimum
✓ 20GB disk space
```

---

## 🚦 System Status

After starting the application:

**Frontend**: http://localhost:3000  
**Backend**: http://localhost:5000  
**Health Check**: http://localhost:5000/api/health

Test health:
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "online",
  "message": "TNI AU Threat Intelligence System API",
  "version": "1.0.0"
}
```

---

## 🎉 Ready to Begin?

Choose your adventure:

### 🏃 Want to Start Immediately?
```bash
./start.sh
```

### 📖 Want to Learn First?
Read [QUICK_START.md](QUICK_START.md)

### 🎯 Want the Full Picture?
Browse [INDEX.md](INDEX.md)

### 🎬 Need to Demo Soon?
Check [DEMO.md](DEMO.md)

---

## 📱 Screenshots Preview

### Dashboard
```
┌─────────────────────────────────────────────┐
│  📊 Total: 247  |  🔴 High: 23  | 🟠 Mid: 68 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│  Threat Distribution | Sentiment Analysis    │
│  [Pie Chart]        | [Bar Chart]           │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│  Recent Threats                              │
│  • Malware campaign (HIGH) - 2h ago         │
│  • Ransomware variant (HIGH) - 4h ago       │
│  • Cyber defense upgrade (INFO) - 6h ago    │
└─────────────────────────────────────────────┘
```

### Crawler
```
┌─────────────────────────────────────────────┐
│  🌐 Language: 🇮🇩 🇺🇸 🇨🇳 🇸🇦             │
│  🔍 Keywords: malware, cyber attack...      │
│  📡 Sources: ☑ News ☑ Social ☑ Forums      │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│         [Start Crawling Button]             │
└─────────────────────────────────────────────┘
```

---

## 🎊 You're All Set!

Everything is ready for you to explore. Choose where to start and happy hunting! 🛡️

### Final Checklist
- [x] Application installed
- [x] Documentation available
- [x] Demo scenarios ready
- [ ] Your first threat hunt!

---

**Built with ❤️ for TNI AU Cyber Defense**

*"Real-time Intelligence for National Security"*

---

**Ready? Let's go! → [QUICK_START.md](QUICK_START.md)** 🚀
