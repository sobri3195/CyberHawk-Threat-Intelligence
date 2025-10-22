# 📸 Application Screenshots & Visual Guide

Panduan visual untuk TNI AU Threat Intelligence System.

> **Note**: Untuk screenshot actual, jalankan aplikasi dan capture dari browser. File ini menyediakan deskripsi visual dari setiap halaman.

---

## 🏠 Dashboard Page

### URL: `http://localhost:3000/dashboard`

**Layout**:
```
┌─────────────────────────────────────────────────────────────┐
│  📊 DASHBOARD - Real-time Threat Intelligence Overview      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Total    │  │ High     │  │ Medium   │  │ System   │   │
│  │ Threats  │  │ Priority │  │ Priority │  │ Status   │   │
│  │  247     │  │   23     │  │   68     │  │ Active   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                              │
│  ┌─────────────────────┐  ┌─────────────────────┐          │
│  │  Threat Level       │  │  Sentiment Analysis │          │
│  │  Distribution       │  │                     │          │
│  │                     │  │                     │          │
│  │  [PIE CHART]        │  │  [BAR CHART]        │          │
│  │  • High: 23         │  │  • Positive: 89     │          │
│  │  • Medium: 68       │  │  • Negative: 67     │          │
│  │  • Low: 98          │  │  • Neutral: 91      │          │
│  └─────────────────────┘  └─────────────────────┘          │
│                                                              │
│  Recent Threats (Last 24 hours)                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Source  │ Title              │ Level  │ Sentiment │ ... │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │ Twitter │ Malware campaign   │ HIGH   │ Negative  │ ... │ │
│  │ Reddit  │ Ransomware variant │ HIGH   │ Negative  │ ... │ │
│  │ News    │ Cyber defense...   │ INFO   │ Positive  │ ... │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Key Elements**:
- 4 stat cards at top (Total, High, Medium, Status)
- Pie chart showing threat distribution
- Bar chart showing sentiment analysis
- Recent threats table with 5 latest items
- Color coding: Red (HIGH), Orange (MEDIUM), Yellow (LOW), Blue (INFO)
- Auto-refresh every 30 seconds

---

## 🔍 Crawler Page

### URL: `http://localhost:3000/crawler`

**Layout**:
```
┌─────────────────────────────────────────────────────────────┐
│  🔍 THREAT INTELLIGENCE CRAWLER                             │
│  Multi-language crawler with sentiment analysis             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Configuration                    │  Crawling Status        │
│  ──────────────────────────────── │  ─────────────────────  │
│                                    │                         │
│  🌐 Language Selection             │  Ready to start         │
│  ┌────────┐ ┌────────┐            │  crawling              │
│  │🇮🇩 ID  │ │🇺🇸 EN  │            │                         │
│  └────────┘ └────────┘            │  Configure sources      │
│  ┌────────┐ ┌────────┐            │  and keywords,          │
│  │🇨🇳 ZH  │ │🇸🇦 AR  │            │  then click             │
│  └────────┘ └────────┘            │  "Start Crawling"       │
│                                    │                         │
│  🔍 Keywords                       │                         │
│  ┌──────────────────────────────┐ │                         │
│  │ malware, cyber attack,       │ │                         │
│  │ ransomware, defense...       │ │                         │
│  └──────────────────────────────┘ │                         │
│  [Load Default]                    │                         │
│                                    │                         │
│  📡 Data Sources                   │                         │
│  ┌────────┐ ┌────────┐            │                         │
│  │☑ News  │ │☑Social │            │                         │
│  └────────┘ └────────┘            │                         │
│  ┌────────┐ ┌────────┐            │                         │
│  │☑Forums │ │☐Dark Web│           │                         │
│  └────────┘ └────────┘            │                         │
│                                    │                         │
│  Max Results: 100 [========○--]   │                         │
│                                    │                         │
│  [  START CRAWLING  ]              │                         │
└─────────────────────────────────────────────────────────────┘
```

**Key Elements**:
- 4 language buttons (ID, EN, ZH, AR)
- Keyword input area with default button
- 4 source selection cards
- Slider for max results (10-500)
- Large "Start Crawling" button
- Status panel showing progress when active

---

## 📋 Threat List Page

### URL: `http://localhost:3000/threats`

**Layout**:
```
┌─────────────────────────────────────────────────────────────┐
│  📋 THREAT INTELLIGENCE DATA                                │
│  50 of 50 threats                        [Export Data]      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🔍 [Search threats by title, content, or keywords...]      │
│                                                              │
│  Filters:                                                    │
│  [Threat Level ▼] [Sentiment ▼] [Source ▼] [Clear Filters] │
│                                                              │
│  ┌────────────────────┐  ┌────────────────────┐            │
│  │ HIGH  Negative     │  │ MEDIUM  Neutral    │            │
│  │ Twitter            │  │ Reddit             │            │
│  │                    │  │                    │            │
│  │ Malware Campaign   │  │ Phishing Attempt   │            │
│  │ Targeting Defense  │  │ Detected in...     │            │
│  │ Infrastructure...  │  │                    │            │
│  │                    │  │                    │            │
│  │ Keywords: malware, │  │ Keywords: phishing,│            │
│  │ cyber attack       │  │ social engineering │            │
│  │                    │  │                    │            │
│  │ 📅 2h ago  📊 -0.65│  │ 📅 4h ago  📊 -0.45│            │
│  │ [🔗]               │  │ [🔗]               │            │
│  └────────────────────┘  └────────────────────┘            │
│                                                              │
│  ┌────────────────────┐  ┌────────────────────┐            │
│  │ ... more cards ... │  │ ... more cards ... │            │
│  └────────────────────┘  └────────────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

**Key Elements**:
- Search bar at top
- Filter dropdowns (Level, Sentiment, Source)
- Clear filters button
- Grid of threat cards (2-3 columns)
- Each card shows: badge, title, content preview, keywords, metadata
- Export button for downloading data

---

## 📊 Analytics Page

### URL: `http://localhost:3000/analytics`

**Layout**:
```
┌─────────────────────────────────────────────────────────────┐
│  📊 ANALYTICS & INSIGHTS                                    │
│  Deep dive into threat intelligence patterns                 │
│                            [7 Days] [30 Days] [90 Days]      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Threat Level Trends                                         │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                         [AREA CHART]                    │ │
│  │  HIGH ────                                              │ │
│  │  MED  ────                                              │ │
│  │  LOW  ────                                              │ │
│  │  ├───┼───┼───┼───┼───┼───┼───┤                        │ │
│  │  Mon Tue Wed Thu Fri Sat Sun                            │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌──────────────────────┐  ┌──────────────────────┐        │
│  │ Sentiment Over Time  │  │ Source Distribution  │        │
│  │                      │  │                      │        │
│  │  [LINE CHART]        │  │  [PIE CHART]         │        │
│  │  • Positive ────     │  │  • Twitter: 37%      │        │
│  │  • Negative ────     │  │  • Reddit: 27%       │        │
│  │  • Neutral  ────     │  │  • News: 23%         │        │
│  └──────────────────────┘  └──────────────────────┘        │
│                                                              │
│  Top Keywords                                                │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ malware        ████████████████████████ 245            │ │
│  │ cyber attack   ██████████████████ 198                  │ │
│  │ ransomware     ███████████████ 167                     │ │
│  │ phishing       ████████████ 142                        │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Automated Insights                                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 🔴 Increasing Threat Activity                        │   │
│  │ High-priority threats increased by 23% in last 7 days│   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Key Elements**:
- Time range selector (7, 30, 90 days)
- Large area chart for threat trends
- Two medium charts (sentiment line, source pie)
- Horizontal bar chart for keywords
- Insight cards at bottom
- All charts are interactive (hover for details)

---

## 🎨 Color Scheme & Styling

### Threat Levels
- 🔴 **HIGH**: #ef4444 (Red) - Critical threats
- 🟠 **MEDIUM**: #f97316 (Orange) - Significant threats
- 🟡 **LOW**: #eab308 (Yellow) - Minor threats
- 🔵 **INFO**: #3b82f6 (Blue) - Informational

### Sentiments
- 🟢 **Positive**: #10b981 (Green)
- 🔴 **Negative**: #ef4444 (Red)
- ⚫ **Neutral**: #6b7280 (Gray)

### UI Theme
- **Background**: #0f172a (Dark blue)
- **Cards**: #1e293b (Slate)
- **Text Primary**: #f1f5f9 (Light)
- **Text Secondary**: #94a3b8 (Gray)
- **Accent**: #3b82f6 (Blue)

---

## 📱 Responsive Views

### Desktop (1920x1080)
- Full sidebar visible
- 3-column grid for threat cards
- All charts side-by-side
- Maximum data density

### Tablet (768-1024px)
- Collapsible sidebar
- 2-column grid
- Charts stack vertically
- Touch-friendly buttons

### Mobile (320-768px)
- Hidden sidebar (hamburger menu)
- Single column layout
- Full-width charts
- Larger touch targets

---

## 🎯 Interactive Elements

### Hover Effects
- Cards lift up slightly
- Buttons show subtle glow
- Charts highlight data points
- Links change color

### Animations
- Smooth page transitions (fade-in)
- Loading spinners
- Progress bars
- Pulse animations for active states

### Click Actions
- Cards expand for details
- Charts are clickable
- Filters apply instantly
- Badges show tooltips

---

## 📊 Chart Examples

### Pie Chart (Dashboard)
```
    Threat Distribution
        ╱────╲
      ╱  23   ╲    ← High (Red)
     │   98    │   ← Low (Yellow)
     │    68   │   ← Medium (Orange)
      ╲       ╱
        ╲────╱
```

### Bar Chart (Sentiment)
```
Positive  ████████████████ 89
Negative  ████████████ 67
Neutral   █████████████████ 91
```

### Area Chart (Trends)
```
HIGH  ╱╲  ╱╲
     ╱  ╲╱  ╲
MED ╱────────╲╱╲
   ╱            ╲
LOW────────────────
   Mon Tue Wed Thu
```

---

## 🎬 Animation Examples

### Loading State
```
⠋ Loading dashboard data...
⠙ Loading dashboard data...
⠹ Loading dashboard data...
⠸ Loading dashboard data...
```

### Crawling Progress
```
[████████████────────] 60%
Crawling in progress...
```

### Success Message
```
✓ Successfully crawled 25 items!
  View Threats →
```

---

## 💡 Tips for Screenshots

### Best Practices
1. **Use full HD resolution** (1920x1080)
2. **Capture during active state** (with data)
3. **Include hover states** for interactive elements
4. **Show filter results** to demonstrate functionality
5. **Capture charts** with meaningful data
6. **Include time stamps** to show real-time nature

### Recommended Screenshots
1. Dashboard - Full view with all charts
2. Crawler - Configuration panel
3. Crawler - Crawling in progress
4. Threat List - With filters applied
5. Threat Card - Detail view
6. Analytics - Multiple charts
7. Mobile view - Responsive design

### Screenshot Tools
- Browser DevTools (F12 → Device Toolbar)
- Lightshot / Greenshot
- macOS: Cmd+Shift+4
- Windows: Win+Shift+S

---

## 📸 How to Capture

```bash
# 1. Start application
./start.sh

# 2. Open browser
open http://localhost:3000

# 3. Navigate to each page:
# - Dashboard
# - Crawler
# - Threats
# - Analytics

# 4. Capture screenshots
# Use your preferred tool

# 5. Save to /docs/screenshots/
# Naming convention:
# - 01-dashboard.png
# - 02-crawler.png
# - 03-threats.png
# - 04-analytics.png
```

---

**Untuk screenshot berkualitas tinggi, pastikan:**
- ✅ Aplikasi berjalan dengan data
- ✅ UI elements fully loaded
- ✅ No loading spinners visible (unless showing loading state)
- ✅ Good lighting/contrast
- ✅ Clear text readable

---

*This document provides visual descriptions. For actual screenshots, run the application and capture from browser.*
