🔴 TelecomAI – Vodafone Smart Campaign Targeting Platform

AI-Powered Customer Intelligence | Churn Prediction | Lead Targeting | Llama-Powered Analytics

🚀 Overview

TelecomAI is a fully AI-powered customer intelligence platform designed for telecom operations.
It helps Vodafone (VOIS) teams identify high-risk customers, optimize campaigns, analyze complaints, and generate insights automatically using Ollama LLM (llama3.2:1b).

This project contains:

FastAPI Backend

Ollama LLM Engine (llama3.2:1b)

React Frontend with Vodafone Red Theme + Dark Mode

Recharts Data Visualizations

📁 Project Structure
project/
├── backend/
│   ├── main.py
│   ├── ollama_analyzer.py
│   ├── test_ollama.py
│   ├── requirements.txt
│
└── frontend/
    ├── public/
    ├── src/
    │   ├── App.js
    │   ├── App.css
    │   ├── index.js
    │   ├── index.css
    ├── package.json
    └── README.md

⚙️ Backend Setup – FastAPI + Ollama (llama3.2:1b)
1️⃣ Install Python dependencies
pip install fastapi uvicorn ollama python-multipart pydantic

2️⃣ Install Ollama

Download: https://ollama.com/download

3️⃣ Pull required LLM
ollama pull llama3.2:1b

4️⃣ Start backend server
cd backend
python main.py


Backend runs at:

http://localhost:8000

🖥️ Frontend Setup – React (Vodafone Red Theme)
1️⃣ Create React App
npx create-react-app frontend
cd frontend

2️⃣ Install required libraries
npm install lucide-react recharts

3️⃣ Replace required files
File	Action
public/index.html	Replace
src/index.js	Replace
src/index.css	Replace
src/App.js	Replace (Vodafone red + dark mode)
src/App.css	Replace
package.json	Replace

⚠️ Remove boilerplate files:

logo.svg
App.test.js
reportWebVitals.js
setupTests.js

4️⃣ Recommended: Add .env
REACT_APP_API_URL=http://localhost:8000


Use it inside App.js:

const API_URL = process.env.REACT_APP_API_URL;

5️⃣ Start the frontend
npm start


Frontend runs at:

http://localhost:3000

🎨 Vodafone Red Theme

All blue UI colors were replaced with the official Vodafone palette:

Name	Hex Code
Primary Red	#E60000
Deep Red	#B00000
Medium Red	#FF4D4D
Soft Red	#FF9999
Light Red	#FFCCCC
Pale Red	#FFE5E5
Maroon	#990000

✔ Gradients updated
✔ Charts themed
✔ Stat cards, badges, buttons converted to red
✔ No blue remains anywhere

🌙 Dark Mode (Vodafone Theme)

Dark Mode Colors:

Purpose	Color
Background	#1A1A1A
Card	#242424
Text	#FFFFFF
Subtext	#B3B3B3
Red Accent	#FF3333

Frontend includes a dark mode toggle (Moon/Sun icons).

📊 Features
🔹 Dashboard

Total interactions

Active customers

Critical issues

Avg resolution time

Charts:

Top issue categories (Bar)

Sentiment analysis (Pie)

Churn risk distribution (Horizontal bar)

Top issue table

🔹 Leads View

Category filter

High-value customer cards

Customer details

Summary + location + operator + tenure

Churn risk score

Target button

🔹 Campaigns View

Campaign performance cards

ROI tracking

Funnel metrics (Target → Contact → Response → Conversion)

Revenue insights

Conversion rate details

🔹 Analytics – AI Query Engine (Powered by llama3.2:1b)

Ask natural language questions like:

“Which customers are at high churn risk?”

“Top complaints about network in Delhi?”

“Which segment needs campaign targeting?”

The LLM returns:

AI-generated answer

Summaries

Insights

Recommendations

🔹 Topic Modeling (AI Generated)

AI-discovered customer issue groups

Severity: High, Medium, Low

Issue percentage

Severity badges

Smooth progress bar

🔌 API Endpoints
Method	Endpoint	Description
GET	/stats	Overall platform stats
GET	/top-issues	Top 10 customer issues
GET	/campaigns	Campaign analytics
GET	/leads/{category}	Leads by category
GET	/topic-modeling	AI topic clusters
POST	/query	AI natural language analytics
🛠️ Troubleshooting
❗ CORS Error

Add this to backend:

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

❗ Model Not Loading

Ensure Ollama is running:

ollama run llama3.2:1b

❗ Wrong API URL

Set correct .env:

REACT_APP_API_URL=http://localhost:8000

❗ Missing libraries
npm install lucide-react recharts



🚀 Production Build
npm run build
serve -s build

📄 License

This project is part of the TelecomAI Smart Campaign Targeting System,
developed for Vodafone Intelligent Solutions (VOIS) for analytics, churn prediction, and customer experience optimization.
