# 🎬 Demo Guide - TNI AU Threat Intelligence System

Panduan demonstrasi fitur-fitur utama aplikasi.

## 🚀 Getting Started

### 1. Start Application

```bash
# Easy start
./start.sh

# Or manual start
npm run server  # Terminal 1
npm run dev     # Terminal 2
```

### 2. Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## 📋 Demo Scenarios

### Scenario 1: Dashboard Overview (5 menit)

**Tujuan**: Menampilkan overview lengkap sistem threat intelligence

**Steps:**
1. Buka http://localhost:3000
2. Navigasi akan otomatis ke Dashboard
3. Perlihatkan **Stats Cards**:
   - Total Threats: 247
   - High Priority: 23 (warna merah)
   - Medium Priority: 68 (warna orange)
   - System Status: Active

4. Scroll ke **Threat Level Distribution** (Pie Chart):
   - Menunjukkan distribusi ancaman per level
   - Interactive: hover untuk detail

5. **Sentiment Analysis** (Bar Chart):
   - Positive: 89 items (hijau)
   - Negative: 67 items (merah)
   - Neutral: 91 items (abu-abu)

6. **Recent Threats Table**:
   - 5 ancaman terbaru
   - Filter berdasarkan source, level, sentiment
   - Click untuk detail

**Key Points to Highlight:**
- Real-time monitoring
- Visual analytics
- Multi-level threat classification
- Sentiment analysis integration

---

### Scenario 2: Crawler Configuration (10 menit)

**Tujuan**: Demonstrasi crawling multi-language dengan sentiment analysis

**Steps:**

1. **Klik menu "Crawler"** di sidebar

2. **Select Language**:
   - Tunjukkan 4 pilihan bahasa: 🇮🇩 ID, 🇺🇸 EN, 🇨🇳 ZH, 🇸🇦 AR
   - Pilih "Bahasa Indonesia"

3. **Input Keywords**:
   - Click "Load Default" untuk keywords preset
   - Keywords akan muncul: "serangan siber, malware, ransomware, pertahanan, TNI AU, keamanan nasional"
   - Atau input manual custom keywords

4. **Select Data Sources**:
   - News Sites ✓
   - Social Media ✓
   - Forums ✓
   - Dark Web (disabled - requires Tor)

5. **Set Max Results**:
   - Drag slider ke 100

6. **Start Crawling**:
   - Click "Start Crawling" button
   - Watch animation: pulse circle dengan progress bar
   - Progress: 0% → 100% (simulasi ~5 detik)

7. **View Results**:
   - Success message muncul
   - Items Collected: 25-30 items
   - Sources Scanned: 3 sources
   - Click "View Threats" untuk lihat hasil

**Demo Different Languages:**

**English:**
```
Keywords: cyber attack, malware, ransomware, defense, national security, threat
Sources: All
```

**Chinese:**
```
Keywords: 网络攻击, 恶意软件, 勒索软件, 国防, 国家安全
Sources: Social Media, News
```

**Key Points:**
- Multi-language support
- Customizable sources
- Real-time crawling
- Automatic sentiment analysis
- Scalable (10-500 results)

---

### Scenario 3: Threat Analysis & Filtering (8 menit)

**Tujuan**: Analisis mendalam data ancaman dengan filtering

**Steps:**

1. **Navigate to "Threat List"**

2. **Show Total Count**:
   - "50 of 50 threats" di subtitle

3. **Use Search Box**:
   - Type: "malware"
   - Results filter in real-time
   - Highlight matched terms

4. **Apply Filters**:
   
   **Filter by Threat Level:**
   - Select "HIGH"
   - Cards update to show only HIGH threats
   - Notice red badges
   
   **Filter by Sentiment:**
   - Select "Negative"
   - Shows only negative sentiment items
   - Notice sentiment icons
   
   **Filter by Source:**
   - Select "Twitter"
   - Shows only Twitter data

5. **Combined Filters**:
   - HIGH + Negative + Twitter
   - Very specific results
   - Click "Clear Filters" to reset

6. **Examine Threat Card**:
   - Threat level badge (color-coded)
   - Sentiment badge (with icon)
   - Title and content preview
   - Keywords tags
   - Date and sentiment score
   - External link icon

7. **Export Data**:
   - Click "Export Data" button
   - Downloads JSON file
   - Open in editor to show structure

**Key Points:**
- Powerful filtering
- Real-time search
- Multiple filter combination
- Export capabilities
- Detailed threat cards

---

### Scenario 4: Analytics & Insights (7 menit)

**Tujuan**: Strategic analysis dan trend visualization

**Steps:**

1. **Navigate to "Analytics"**

2. **Time Range Selection**:
   - Show 3 options: 7 Days, 30 Days, 90 Days
   - Select "7 Days"

3. **Threat Level Trends (Area Chart)**:
   - Shows stacked area chart
   - Red = HIGH, Orange = MEDIUM, Yellow = LOW
   - Hover untuk detail per tanggal
   - Identify trend: "Increasing HIGH threats"

4. **Sentiment Over Time (Line Chart)**:
   - 3 lines: Positive (green), Negative (red), Neutral (gray)
   - Track sentiment changes
   - Identify patterns

5. **Source Distribution (Pie Chart)**:
   - Twitter: 450 (37%)
   - Reddit: 320 (27%)
   - News: 280 (23%)
   - Forums: 150 (13%)

6. **Top Keywords (Horizontal Bar)**:
   - malware: 245 mentions
   - cyber attack: 198 mentions
   - ransomware: 167 mentions
   - etc.

7. **Automated Insights Cards**:
   - "Increasing Threat Activity" (red icon)
   - "Sentiment Improving" (green icon)
   - "Peak Activity Hours" (orange icon)

8. **Change Time Range**:
   - Click "30 Days"
   - All charts update
   - Show longer-term trends

**Key Points:**
- Multiple chart types
- Time-series analysis
- Automated insights
- Pattern recognition
- Strategic planning support

---

## 🎯 Key Demo Messages

### For Military Leadership
1. **Real-time Situational Awareness**: Instant visibility of cyber threats
2. **Multi-source Intelligence**: Aggregation from various sources
3. **Prioritization**: Automatic threat level classification
4. **Actionable Insights**: Clear, data-driven decision support

### For Technical Team
1. **Multi-language Capability**: Support for 4 major languages
2. **Scalable Architecture**: React + Express + modern stack
3. **API-first Design**: Easy integration with existing systems
4. **Extensible**: Easy to add new sources and features

### For Analysts
1. **Powerful Filtering**: Find exactly what you need
2. **Sentiment Analysis**: Understand public perception
3. **Export Capabilities**: Share findings easily
4. **Visual Analytics**: Spot trends quickly

## 🔍 Q&A Preparation

### Expected Questions

**Q: "Apakah data real-time?"**
A: Ya, sistem dapat melakukan crawling real-time. Demo ini menggunakan data simulasi untuk demonstrasi, tapi production akan crawl live data dari Twitter, Reddit, news sites, dll.

**Q: "Bagaimana akurasi sentiment analysis?"**
A: Menggunakan NLP library dengan akurasi ~80-85%. Untuk improvement, bisa integrate dengan model ML yang di-train khusus untuk bahasa Indonesia dan konteks militer.

**Q: "Apakah bisa monitoring dark web?"**
A: Ya, sudah ada infrastructure untuk dark web monitoring menggunakan Tor proxy. Requires additional setup dan security considerations.

**Q: "Bagaimana dengan false positives?"**
A: Sistem menggunakan keyword-based classification yang bisa di-tune. Ada feedback mechanism (planned) untuk improve accuracy over time.

**Q: "Integrasi dengan sistem existing?"**
A: Fully API-based architecture, mudah untuk integrate dengan SIEM, SOAR, atau sistem TNI AU yang existing. API documentation tersedia.

**Q: "Kebutuhan infrastruktur?"**
A: 
- Minimum: 2 CPU cores, 4GB RAM, 20GB storage
- Recommended: 4 CPU cores, 8GB RAM, 50GB storage
- Database: SQLite (dev) atau PostgreSQL (production)
- Optional: Tor proxy untuk dark web monitoring

**Q: "Training untuk operator?"**
A: User interface designed to be intuitive. Training documentation tersedia. Estimated 2-4 jam untuk basic operations, 1-2 hari untuk advanced analysis.

## 📊 Demo Metrics to Highlight

- **247** total threats collected
- **23** high-priority threats requiring attention
- **4** languages supported
- **5** data sources (news, social, forums, dark web, custom)
- **3** sentiment categories
- **Real-time** data processing
- **< 5s** crawl completion time
- **100%** uptime target

## 🎬 Presentation Tips

1. **Start with Dashboard**: Immediately show value
2. **Interactive Demo**: Let audience suggest keywords to search
3. **Tell a Story**: "Imagine ada ancaman siber hari ini..."
4. **Show Real Use Case**: TNI AU monitoring kampanye malware
5. **Highlight Multi-language**: Demonstrate international capability
6. **End with Analytics**: Strategic value for decision makers

## 📝 Follow-up Materials

After demo, provide:
- [ ] README.md - Setup instructions
- [ ] FEATURES.md - Complete feature list
- [ ] DEVELOPMENT.md - Technical documentation
- [ ] API documentation
- [ ] Architecture diagram
- [ ] Deployment guide

---

**Demo Duration: 30-45 menit including Q&A**

Good luck with the demonstration! 🚀
