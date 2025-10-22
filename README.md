# 🛡️ TNI AU - Threat Intelligence System

## 🚀 ALL FEATURES ENABLED - FREE API AUTO-GENERATION

Sistem Analisis Intelijen Ancaman Siber berbasis React.js untuk TNI AU dengan fitur crawling multi-bahasa, analisis sentimen real-time, dan **AUTO-SETUP untuk SEMUA platform media sosial TANPA API KEY!**

> 🎉 **NEW!** All social media platforms enabled with FREE scraping - NO API keys required!  
> 📚 **Documentation?** Check [INDEX.md](INDEX.md) or [AUTO_SETUP_GUIDE.md](AUTO_SETUP_GUIDE.md)  
> ⚡ **Quick start?** Run `python quick_start.py` for instant setup!

## ✨ Fitur Utama

### 🎉 **NEW: ALL Social Media Platforms - FREE Scraping**
- ✅ **Twitter/X** - Free scraping via Nitter (NO API key needed)
- ✅ **Reddit** - Free JSON API (NO authentication needed)
- ✅ **Facebook** - Public data scraping
- ✅ **Instagram** - Public hashtag scraping via Picuki
- ✅ **LinkedIn** - Public post scraping
- ✅ **Telegram** - Public channel scraping
- ✅ **Auto API Generation** - Demo credentials generated automatically
- ✅ **Zero Configuration** - Works out of the box!

### 🌐 Multi-Language Crawler
- **4 Bahasa**: Indonesia 🇮🇩, English 🇺🇸, Chinese 🇨🇳, Arabic 🇸🇦
- **Multi-Source**: SEMUA media sosial, portal berita, forum, dark web
- **Real-time**: Pengumpulan data ancaman siber secara real-time
- **No Rate Limits**: Free scraping methods with smart delays

### 📊 Sentiment Analysis
- Analisis sentimen otomatis untuk setiap data yang dikumpulkan
- Klasifikasi: Positive, Negative, Neutral
- Visualisasi trend sentimen dari waktu ke waktu
- Multi-language sentiment support

### 🎯 Threat Intelligence
- **4 Level Ancaman**: HIGH, MEDIUM, LOW, INFO
- Deteksi keyword ancaman otomatis
- Ekstraksi IOC (Indicators of Compromise)
- Kategorisasi berdasarkan sumber dan tingkat ancaman
- Free threat intel API integration

### 📈 Analytics & Insights
- Dashboard real-time dengan statistik lengkap
- Grafik trend ancaman
- Distribusi sumber data
- Top keywords dan pattern analysis
- Cross-platform correlation

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm atau yarn

### Installation

1. **Clone repository**
```bash
git clone <repository-url>
cd threat-intel-app
```

2. **Install dependencies**
```bash
npm install
```

3. **Start development server**

**Option 1 - Easy Start (Recommended):**
```bash
./start.sh
```

**Option 2 - Manual Start:**

Terminal 1 - Backend (Express API):
```bash
npm run server
```

Terminal 2 - Frontend (React):
```bash
npm run dev
```

4. **Akses aplikasi**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Health Check: http://localhost:5000/api/health

## 📁 Struktur Project

```
threat-intel-app/
├── src/                          # Frontend React
│   ├── components/               # Komponen React
│   │   └── Layout.tsx           # Layout utama dengan sidebar
│   ├── pages/                    # Halaman aplikasi
│   │   ├── Dashboard.tsx        # Dashboard overview
│   │   ├── Crawler.tsx          # Konfigurasi crawler
│   │   ├── ThreatList.tsx       # Daftar ancaman
│   │   └── Analytics.tsx        # Analitik dan insight
│   ├── services/                 # API services
│   │   └── api.ts               # HTTP client
│   ├── types/                    # TypeScript types
│   │   └── index.ts
│   └── App.tsx                   # Root component
├── server/                       # Backend Express
│   ├── controllers/              # Business logic
│   │   ├── dashboardController.js
│   │   ├── crawlerController.js
│   │   ├── threatsController.js
│   │   └── analyticsController.js
│   ├── routes/                   # API routes
│   │   ├── dashboard.js
│   │   ├── crawler.js
│   │   ├── threats.js
│   │   └── analytics.js
│   └── index.js                  # Server entry point
├── package.json
├── vite.config.ts
└── tsconfig.json
```

## 🎮 Penggunaan

### 1. Dashboard
- Lihat overview statistik ancaman real-time
- Monitor trend ancaman berdasarkan level
- Analisis distribusi sentimen
- Akses quick stats: Total threats, High priority, dll

### 2. Crawler
**Langkah-langkah:**
1. Pilih bahasa target (ID/EN/ZH/AR)
2. Masukkan keywords yang ingin dicari
3. Pilih sumber data (News, Social Media, Forums, Dark Web)
4. Atur jumlah maksimal hasil
5. Klik "Start Crawling"

**Contoh Keywords:**
- Bahasa Indonesia: `serangan siber, malware, ransomware, pertahanan, TNI AU`
- English: `cyber attack, malware, ransomware, defense, military`
- Chinese: `网络攻击, 恶意软件, 国防`
- Arabic: `الهجوم السيبراني, الأمن القومي`

### 3. Threat List
- Filter berdasarkan threat level, sentiment, atau source
- Search dengan keyword
- View detail setiap threat
- Export data ke JSON/CSV

### 4. Analytics
- Visualisasi trend ancaman dari waktu ke waktu
- Analisis sentimen timeline
- Distribusi sumber data
- Top keywords yang sering muncul
- Insight otomatis berdasarkan data

## 🔧 Konfigurasi

### Environment Variables
Buat file `.env` di root directory:

```env
PORT=5000
NODE_ENV=development

# API Keys (optional untuk integrasi nyata)
TWITTER_BEARER_TOKEN=your_token
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_secret
```

### Kustomisasi Keywords

Edit file `src/pages/Crawler.tsx`:

```typescript
const defaultKeywords = {
  id: 'serangan siber, malware, ransomware, pertahanan, TNI AU, keamanan nasional',
  en: 'cyber attack, malware, ransomware, defense, national security, threat',
  zh: '网络攻击, 恶意软件, 勒索软件, 国防, 国家安全',
  ar: 'الهجوم السيبراني, البرمجيات الخبيثة, الأمن القومي'
};
```

## 🛠️ Development

### Build untuk Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## 📊 API Endpoints

### Dashboard
- `GET /api/dashboard/stats` - Dashboard statistics

### Crawler
- `POST /api/crawl/start` - Start crawling
- `GET /api/crawl/status` - Get crawl status

### Threats
- `GET /api/threats/recent?limit=50` - Get recent threats
- `GET /api/threats/level/:level` - Get threats by level
- `POST /api/threats/search` - Search threats

### Analytics
- `GET /api/analytics/sentiment?days=7` - Sentiment analysis
- `GET /api/analytics/trends?days=30` - Trend analysis

## 🎨 Tech Stack

**Frontend:**
- React 18
- TypeScript
- Vite
- React Router DOM
- Recharts (visualisasi)
- Axios
- Lucide React (icons)

**Backend:**
- Node.js
- Express.js
- Sentiment (analisis sentimen)
- Cheerio (web scraping)
- CORS

## 📝 Catatan Penting

1. **Demo Mode**: Aplikasi saat ini menggunakan data mock untuk demonstrasi
2. **Integrasi Real**: Untuk crawling real-time, perlu API keys dari platform (Twitter, Reddit, dll)
3. **Dark Web**: Monitoring dark web memerlukan Tor proxy (socks5h://localhost:9050)
4. **Database**: Untuk production, integrasikan dengan database (SQLite/PostgreSQL)

## 🔐 Security Considerations

- Jangan commit API keys ke repository
- Gunakan environment variables untuk credentials
- Implement rate limiting untuk API
- Validasi dan sanitasi semua input
- Gunakan HTTPS di production

## 🤝 Contributing

Untuk berkontribusi:
1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

Copyright © 2024 TNI AU - Threat Intelligence System

## 👨‍💻 Author

**Lettu Kes dr. Muhammad Sobri Maulana, S.Kom, CEH, OSCP, OSCE**

Certified Ethical Hacker (CEH), Offensive Security Certified Professional (OSCP), dan Offensive Security Certified Expert (OSCE) dengan spesialisasi dalam cyber threat intelligence dan security analysis.

### 📧 Contact

- **Email**: [muhammadsobrimaulana31@gmail.com](mailto:muhammadsobrimaulana31@gmail.com)
- **GitHub**: [github.com/sobri3195](https://github.com/sobri3195)
- **YouTube**: [@muhammadsobrimaulana6013](https://www.youtube.com/@muhammadsobrimaulana6013)
- **Telegram**: [@winlin_exploit](https://t.me/winlin_exploit)
- **TikTok**: [@dr.sobri](https://www.tiktok.com/@dr.sobri)

### 💬 Community

**WhatsApp Group**: [Join Community](https://chat.whatsapp.com/B8nwRZOBMo64GjTwdXV8Bl)

Bergabunglah dengan komunitas untuk diskusi tentang cyber security, threat intelligence, dan topik terkait keamanan siber lainnya.

## 💝 Support This Project

Jika project ini bermanfaat untuk Anda, dukung pengembangan lebih lanjut melalui donasi:

**Donate**: [https://lynk.id/muhsobrimaulana](https://lynk.id/muhsobrimaulana)

Dukungan Anda sangat berarti untuk pengembangan tools dan konten edukasi cyber security gratis untuk komunitas.

## 👥 Support

Untuk pertanyaan dan dukungan, hubungi tim development atau author melalui kontak di atas.

---

**Built with ❤️ for TNI AU Cyber Defense**
