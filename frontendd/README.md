# Smart_Campaign_Targetting_System

AI-powered Telecom Customer Intelligence Dashboard built for analyzing customer issues, churn risk, campaign performance, and insights using FastAPI, React, and the Llama3.2:1b LLM.

---

## Overview

Smart_Campaign_Targetting_System is an end-to-end telecom analytics platform designed to help identify customer churn, analyze complaints, generate targeted campaigns, and run natural-language queries using a lightweight local LLM.

The system includes:

- FastAPI Backend
- Ollama Llama3.2:1b Local LLM
- React Frontend (Vodafone Red Theme + Dark Mode)
- Recharts Visual Dashboards
- CSV-based telecom datasets (inside the data folder)

---

## Project Structure



Smart_Campaign_Targetting_System/
├── backend/
│ ├── main.py
│ ├── ollama_analyzer.py
│ ├── test_ollama.py
│ └── requirements.txt
│
├── data/
│ ├── campaign_customer_mapping.csv
│ ├── campaign_history.csv
│ ├── customer_interactions.csv
│ ├── customer_profiles.csv
│ ├── issue_trends.csv
│ ├── product_catalog.csv
│ └── dataset_summary.json
│
└── frontend/
├── public/
├── src/
│ ├── App.js
│ ├── App.css
│ ├── index.js
│ ├── index.css
├── package.json
└── README.md


---

## Backend Setup (FastAPI + Ollama)

### 1. Install Python Dependencies



pip install fastapi uvicorn ollama python-multipart pydantic


### 2. Install Ollama

Download from: https://ollama.com/download

### 3. Pull LLM Model



ollama pull llama3.2:1b


### 4. Start Backend Server



cd backend
python main.py


Backend URL:



http://localhost:8000


---

## Frontend Setup (React + Vodafone Theme)

### 1. Create React App



npx create-react-app frontend
cd frontend


### 2. Install Required Libraries



npm install lucide-react recharts


### 3. Replace Files

Replace these files entirely:

- public/index.html
- src/index.js
- src/index.css
- src/App.js
- src/App.css
- package.json

Remove:

- App.test.js
- reportWebVitals.js
- setupTests.js
- logo.svg

### 4. Start Frontend



npm start


Frontend URL:



http://localhost:3000


---

## Dataset (Inside /data Folder)

The dataset contains telecom-related CSV files including:

- customer profiles
- customer interactions
- campaign performance
- issue trends
- product catalog
- mapping of campaigns to customers

`dataset_summary.json` contains a textual summary of the dataset.

---

## Features

### Dashboard
- Total interactions
- Total customers
- Churn risk distribution
- Issue category distribution
- Sentiment analysis
- Top issues table

### Leads View
- Filter customers by issue category
- High risk customer identification
- Churn score visualization
- Customer profile summary

### Campaigns View
- Campaign performance analytics
- ROI
- Conversion funnel
- Revenue insights

### Analytics (AI Query Engine)
- Natural language queries powered by Llama3.2:1b
- AI-generated summaries, insights, and recommendations

### Topic Modeling
- AI-detected issue clusters
- Severity levels
- Percentage distribution

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /stats | Returns platform statistics |
| GET | /top-issues | Returns top customer issue categories |
| GET | /campaigns | Returns campaign analytics |
| GET | /leads/{category} | Returns customer leads for a specific issue |
| GET | /topic-modeling | Returns AI topic clusters |
| POST | /query | Processes natural language queries |

---

## Troubleshooting

### Backend not responding
Ensure Ollama is running:



ollama serve
ollama run llama3.2:1b


### CORS Issues
Add this inside main.py:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Frontend cannot fetch data

Verify:

Backend is running on port 8000

Frontend is running on port 3000

API URL is correctly set

Production Build
npm run build
serve -s build

License

This project is part of the Smart Campaign Targetting System for telecom data analytics and churn prediction.


