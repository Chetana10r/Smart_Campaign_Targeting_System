# 🔴 Smart_Campaign_Targetting_System  
AI-Powered Telecom Customer Intelligence | Vodafone Theme | Churn Prediction | Campaign Optimization

---

## 📌 Overview

**Smart_Campaign_Targetting_System** is an AI-powered analytics platform designed to help telecom companies—especially Vodafone (VOIS)—understand customer behavior, identify high churn risk segments, analyze complaints, and generate optimized marketing campaigns using **Llama3.2:1b (Ollama LLM)**.

The system includes:

- ⚙️ **FastAPI Backend**
- 🧠 **LLM Engine using Ollama (llama3.2:1b)**
- 🎨 **React Frontend (Vodafone Red Theme + Dark Mode)**
- 📊 **Interactive Dashboards using Recharts**
- 📁 **Customer Dataset & Insights (data folder)**

---

## 📁 Project Structure



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
│ └── dataset_summary.json ← summary of dataset 
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

# ⚙️ Backend Setup (FastAPI + Ollama)

## 1️⃣ Install Python dependencies

```bash
pip install fastapi uvicorn ollama python-multipart pydantic

2️⃣ Install Ollama

Download from:
👉 https://ollama.com/download

3️⃣ Pull the LLM model
ollama pull llama3.2:1b

4️⃣ Start the backend
cd backend
python main.py


Backend runs at:

http://localhost:8000

🖥️ Frontend Setup (React + Vodafone Red Theme)
1️⃣ Create React App
npx create-react-app frontend
cd frontend

2️⃣ Install dependencies
npm install lucide-react recharts

3️⃣ Replace these files fully:

public/index.html

src/index.js

src/index.css

src/App.js (Vodafone Red Theme + Dark Mode)

src/App.css

package.json

Remove boilerplate:

logo.svg
App.test.js
reportWebVitals.js
setupTests.js

4️⃣ Run frontend
npm start


Frontend URL:

http://localhost:3000

🎨 Vodafone Red Theme

The interface uses the official Vodafone color palette:

Purpose	Color
Primary Red	#E60000
Deep Red	#B00000
Medium Red	#FF4D4D
Soft Red	#FF9999
Light Red	#FFCCCC
Pale Red	#FFE5E5
Maroon	#990000

All blues were removed

Buttons, cards, charts, badges reflect Vodafone branding

Red gradients applied across the UI

🌙 Dark Mode Included

Fully implemented dark mode toggle using:

Element	Color
Background	#1A1A1A
Cards	#242424
Text	#FFFFFF
Subtext	#B3B3B3
Accent Red	#FF3333

Dark mode toggle is added in navigation.

📊 Features
🔹 Dashboard

Total interactions

Total customers

Churn risk distribution

Issue category analysis

Sentiment analysis

Top issues table

🔹 Leads View

Category-based filtering

High-value customer cards

Risk labels (Critical / High / Medium)

Lead churn scoring

Target action button

🔹 Campaigns View

Performance analytics

ROI visualization

Funnel metrics

Revenue impact

🔹 Analytics (AI Query Engine)

Powered by Ollama Llama3.2:1b
Supports natural language questions like:

“Which customers will churn?”

“Top billing issues in Pune?”

“Which campaign performed best?”

LLM generates:

Answers

Insights

Recommendations

🔹 Topic Modeling

Clusters discovered using AI

Severity levels

Progress indicators

🔌 API Endpoints
Method	Endpoint	Description
GET	/stats	Overall metrics
GET	/top-issues	Top complaint categories
GET	/campaigns	Campaign performance
GET	/leads/{category}	Leads by issue category
GET	/topic-modeling	AI topic clusters
POST	/query	LLM-based analytics
📁 Dataset Description (Inside data/ Folder)

Based on dataset_summary.json 

dataset_summary

:

3000 customers

10,000 interactions

30 campaigns

30 products

Date range: Aug 2025 → Nov 2025

Categories include:

Network quality

Billing overcharge

Internet speed

Product inquiry

TV technical issues

Sentiments: positive / neutral / negative

Churn risk: low / medium / high / critical

Operators: BSNL, Airtel, Jio, Vi

Geographies: Pune, Nagpur, Surat, Nashik, etc.

🛠 Troubleshooting
❗ CORS Issues

Add in main.py:

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

❗ API not connecting

Check:

Backend: http://localhost:8000
Frontend: http://localhost:3000

❗ Ollama not responding
ollama serve
ollama run llama3.2:1b

❗ Missing libraries
npm install lucide-react recharts

🚀 Production Build
npm run build
serve -s build

📄 License

This project is part of Smart Campaign Targetting System,
developed for telecom AI-based analytics and churn prediction.