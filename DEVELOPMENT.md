# 🛠️ Development Guide

Panduan pengembangan untuk TNI AU Threat Intelligence System.

## 🏗️ Arsitektur Aplikasi

### Frontend (React + TypeScript)
```
src/
├── components/          # Reusable components
│   └── Layout.tsx      # Main layout with sidebar navigation
├── pages/              # Route pages
│   ├── Dashboard.tsx   # Main dashboard with stats
│   ├── Crawler.tsx     # Crawler configuration
│   ├── ThreatList.tsx  # Threat data list
│   └── Analytics.tsx   # Analytics and insights
├── services/           # API integration
│   └── api.ts         # Axios HTTP client
├── types/             # TypeScript type definitions
│   └── index.ts       # All interface definitions
└── App.tsx            # Root component with routing
```

### Backend (Node.js + Express)
```
server/
├── controllers/        # Business logic
│   ├── dashboardController.js
│   ├── crawlerController.js
│   ├── threatsController.js
│   └── analyticsController.js
├── routes/            # API routes
│   ├── dashboard.js
│   ├── crawler.js
│   ├── threats.js
│   └── analytics.js
└── index.js          # Express server setup
```

## 🔧 Development Workflow

### 1. Setup Development Environment

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

# Start development servers
./start.sh
```

### 2. Development Commands

```bash
# Frontend only
npm run dev

# Backend only
npm run server

# Build for production
npm run build

# Preview production build
npm run preview
```

### 3. Code Structure Guidelines

#### React Components
- Use functional components with hooks
- Follow component naming convention: `ComponentName.tsx`
- Keep components focused and single-purpose
- Extract reusable logic to custom hooks

Example:
```tsx
import React, { useState, useEffect } from 'react';
import { threatIntelAPI } from '../services/api';

const MyComponent: React.FC = () => {
  const [data, setData] = useState([]);
  
  useEffect(() => {
    loadData();
  }, []);
  
  const loadData = async () => {
    const result = await threatIntelAPI.getData();
    setData(result);
  };
  
  return (
    <div>
      {/* Component JSX */}
    </div>
  );
};

export default MyComponent;
```

#### API Controllers
- One controller per resource
- Use async/await for asynchronous operations
- Always handle errors with try/catch
- Return consistent response format

Example:
```javascript
export const getData = async (req, res) => {
  try {
    const data = await fetchData();
    res.json({
      success: true,
      data: data
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
};
```

## 🎨 Styling Guidelines

### CSS Conventions
- Use BEM-like naming: `.component__element--modifier`
- Keep styles modular (one CSS file per component)
- Use CSS variables for colors and common values
- Mobile-first responsive design

### Color Palette
```css
/* Background */
--bg-primary: #0f172a;
--bg-secondary: #1e293b;
--bg-tertiary: #334155;

/* Text */
--text-primary: #f1f5f9;
--text-secondary: #94a3b8;
--text-tertiary: #64748b;

/* Accent */
--accent-blue: #3b82f6;
--accent-red: #ef4444;
--accent-orange: #f97316;
--accent-yellow: #eab308;
--accent-green: #10b981;
```

## 📊 Data Flow

### 1. Crawler Flow
```
User Input → Crawler Config → API Request → Backend Processing
→ Data Collection → Sentiment Analysis → Database Storage
→ API Response → Frontend Update → UI Display
```

### 2. Dashboard Flow
```
Component Mount → API Request → Backend Query → Data Aggregation
→ API Response → State Update → Recharts Rendering
```

## 🔌 API Integration

### Adding New Endpoint

1. **Create Controller**
```javascript
// server/controllers/newController.js
export const newFunction = async (req, res) => {
  try {
    // Implementation
    res.json({ success: true, data: result });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
```

2. **Create Route**
```javascript
// server/routes/new.js
import express from 'express';
import { newFunction } from '../controllers/newController.js';

const router = express.Router();
router.get('/endpoint', newFunction);

export default router;
```

3. **Register Route**
```javascript
// server/index.js
import newRoutes from './routes/new.js';
app.use('/api/new', newRoutes);
```

4. **Add Frontend Service**
```typescript
// src/services/api.ts
export const threatIntelAPI = {
  // ...existing methods
  newMethod: async (): Promise<DataType> => {
    const response = await api.get('/new/endpoint');
    return response.data;
  },
};
```

## 🧪 Testing

### Manual Testing Checklist

- [ ] Dashboard loads with correct stats
- [ ] Crawler accepts all language options
- [ ] Threat list filters work correctly
- [ ] Analytics charts render properly
- [ ] Export functionality works
- [ ] Responsive design on mobile
- [ ] API endpoints return expected data
- [ ] Error handling works for failed requests

### Testing API Endpoints

```bash
# Health check
curl http://localhost:5000/api/health

# Dashboard stats
curl http://localhost:5000/api/dashboard/stats

# Recent threats
curl http://localhost:5000/api/threats/recent?limit=10

# Start crawl
curl -X POST http://localhost:5000/api/crawl/start \
  -H "Content-Type: application/json" \
  -d '{
    "sources": ["news", "social"],
    "keywords": ["malware", "cyber attack"],
    "language": "en",
    "maxResults": 100
  }'
```

## 🚀 Deployment

### Production Build

```bash
# Build frontend
npm run build

# Output will be in /dist folder
# Serve with any static file server or integrate with backend
```

### Environment Variables for Production

```env
NODE_ENV=production
PORT=5000

# Add real API keys for production
TWITTER_BEARER_TOKEN=your_real_token
REDDIT_CLIENT_ID=your_real_id
REDDIT_CLIENT_SECRET=your_real_secret
```

## 🐛 Debugging

### Common Issues

1. **Port already in use**
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

2. **CORS errors**
- Ensure backend CORS is configured correctly
- Check API base URL in frontend

3. **Module not found**
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
```

## 📝 Code Quality

### Best Practices
- Write descriptive variable and function names
- Add comments for complex logic
- Keep functions small and focused
- Use TypeScript types consistently
- Handle all error cases
- Validate user input
- Sanitize data before display

### Code Review Checklist
- [ ] Code follows style guidelines
- [ ] No console.log statements (use proper logging)
- [ ] Error handling implemented
- [ ] Types properly defined
- [ ] No hardcoded credentials
- [ ] Responsive design tested
- [ ] Performance optimized

## 🔐 Security Considerations

1. **Never commit sensitive data**
   - Use .env for secrets
   - Add .env to .gitignore

2. **Validate all inputs**
   - Check API request parameters
   - Sanitize user-provided data

3. **Rate limiting**
   - Implement for production API
   - Prevent abuse and DoS

4. **HTTPS in production**
   - Use SSL certificates
   - Enforce HTTPS only

## 📚 Resources

- [React Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Express.js Guide](https://expressjs.com/en/guide/routing.html)
- [Vite Documentation](https://vitejs.dev)
- [Recharts Examples](https://recharts.org/en-US/examples)

## 🤝 Contributing

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request
5. Wait for code review

---

Happy Coding! 🚀
