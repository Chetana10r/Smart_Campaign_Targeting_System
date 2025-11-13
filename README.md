# Smart Campaign Targeting - Frontend Setup Guide

## 📁 Project Structure

```
frontend/
├── public/
│   ├── index.html
│   ├── manifest.json
│   └── favicon.ico
├── src/
│   ├── App.js
│   ├── App.css
│   ├── index.js
│   └── index.css
├── package.json
└── README.md
```

## 🚀 Quick Start

### Step 1: Create React App

```bash
# Create new React application
npx create-react-app frontend

# Navigate to the project directory
cd frontend
```

### Step 2: Install Dependencies

```bash
npm install recharts lucide-react
```

### Step 3: Copy Files

Replace the following files with the provided code:

1. **package.json** - Replace entire file
2. **public/index.html** - Replace entire file
3. **src/index.js** - Replace entire file
4. **src/index.css** - Replace entire file
5. **src/App.js** - Replace entire file
6. **src/App.css** - Create new file

### Step 4: Start Backend Server

Make sure your backend is running:

```bash
cd backend
python main.py
```

The backend should be running on `http://localhost:8000`

### Step 5: Start Frontend

```bash
# In the frontend directory
npm start
```

The application will open at `http://localhost:3000`

## 📋 File Contents

### 1. package.json
Copy the provided package.json content

### 2. public/index.html
Copy the provided HTML content

### 3. src/index.js
```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

### 4. src/index.css
Copy the provided CSS content with Google Fonts import

### 5. src/App.js
Copy the complete React component code

### 6. src/App.css
Copy the complete styling code

## 🎨 Features

### Dashboard View
- **Key Metrics Cards**: Total Interactions, Active Customers, Critical Issues, Avg Resolution Time
- **Charts**: 
  - Bar chart for top issue categories
  - Pie chart for sentiment analysis
  - Horizontal bar chart for churn risk distribution
- **Issues Table**: Detailed breakdown of customer issues

### Leads View
- **Category Filter**: Select different issue categories
- **Lead Cards**: Display high-risk customers with:
  - Customer details and contact info
  - Issue summaries
  - Churn risk scores
  - Action buttons

### Campaigns View
- **Campaign Performance Cards**: 
  - ROI calculations
  - Funnel metrics (Targeted → Contacted → Responded → Converted)
  - Revenue generated
  - Conversion rates

### Analytics View
- **AI Query Engine**: Natural language questions about data
- **Results Display**: 
  - Direct answers
  - Key insights
  - Actionable recommendations
- **Topic Modeling**: AI-discovered customer issue patterns

## 🛠️ Troubleshooting

### CORS Issues
If you get CORS errors, ensure your backend has CORS middleware enabled:

```python
# In main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### API Connection Issues
- Verify backend is running on port 8000
- Check `API_URL` in App.js matches your backend URL
- Ensure all backend endpoints are accessible

### Missing Dependencies
If you see module not found errors:

```bash
npm install recharts lucide-react
```

### Port Already in Use
If port 3000 is busy:

```bash
# The prompt will ask if you want to use another port
# Or manually specify port:
PORT=3001 npm start
```

## 🎯 API Endpoints Used

The frontend connects to these backend endpoints:

- `GET /stats` - Overall statistics
- `GET /top-issues` - Top customer issues
- `GET /campaigns` - Campaign performance data
- `GET /leads/{category}` - High-value leads by category
- `POST /query` - Natural language queries
- `GET /topic-modeling` - AI-discovered topics

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop (1280px+)
- Tablet (768px - 1279px)
- Mobile (< 768px)

## 🎨 Color Palette

- **Primary Blue**: #3b82f6
- **Purple**: #8b5cf6
- **Pink**: #ec4899
- **Orange**: #f59e0b
- **Green**: #10b981
- **Cyan**: #06b6d4
- **Red**: #ef4444

## 🔧 Customization

### Change API URL
Edit `API_URL` constant in `src/App.js`:

```javascript
const API_URL = 'http://your-backend-url:8000';
```

### Modify Colors
Edit color variables in `src/App.css` or update the `COLORS` array in `src/App.js`

### Add New Tabs
1. Add new tab name to the tabs array in navigation
2. Create new view function component
3. Add conditional render in main content area

## 📊 Data Flow

1. **Component Mount**: Fetches initial data (stats, issues, campaigns, topics)
2. **Tab Switch**: Renders different views based on active tab
3. **User Interactions**: 
   - Select category → Fetch leads
   - Enter query → Call AI analysis
   - View campaigns → Display performance metrics

## 🚀 Production Build

To create a production build:

```bash
npm run build
```

This creates an optimized build in the `build/` folder.

To serve the production build:

```bash
npm install -g serve
serve -s build
```

## 📝 Notes

- Ensure backend is running before starting frontend
- All API calls are asynchronous with error handling
- Loading states are displayed during data fetching
- Charts are rendered using Recharts library
- Icons are from Lucide React library

## 🆘 Support

If you encounter issues:

1. Check browser console for errors
2. Verify backend is accessible
3. Ensure all dependencies are installed
4. Check API endpoint responses in Network tab

## 📄 License

This project is part of the Smart Campaign Targeting system for telecom customer intelligence.