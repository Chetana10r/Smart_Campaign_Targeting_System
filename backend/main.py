from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import json
import os
from typing import Optional, List
from pathlib import Path

# Import from local module
from ollama_analyzer import OllamaAnalyzer

app = FastAPI(title="Smart Campaign Targeting API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],  # Added * for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the directory where main.py is located
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR.parent / 'data'

# Load data with error handling
try:
    interactions_df = pd.read_csv(DATA_DIR / 'customer_interactions.csv')
    customers_df = pd.read_csv(DATA_DIR / 'customer_profiles.csv')
    campaigns_df = pd.read_csv(DATA_DIR / 'campaign_history.csv')
    products_df = pd.read_csv(DATA_DIR / 'product_catalog.csv')
    print(f"✅ Loaded {len(interactions_df)} interactions")
    print(f"✅ Loaded {len(customers_df)} customers")
    print(f"✅ Loaded {len(campaigns_df)} campaigns")
    print(f"✅ Loaded {len(products_df)} products")
except FileNotFoundError as e:
    print(f"❌ Error loading data files: {e}")
    print(f"Expected data directory: {DATA_DIR}")
    raise

# Initialize LLM analyzer
llm = OllamaAnalyzer()

# Request models
class QueryRequest(BaseModel):
    question: str
    max_context_rows: Optional[int] = 50

class AnalyzeRequest(BaseModel):
    text: str

# ============================================================
# ENDPOINTS
# ============================================================

@app.get("/")
def root():
    return {
        "message": "Smart Campaign Targeting API",
        "version": "1.0",
        "status": "running",
        "endpoints": [
            "/stats",
            "/top-issues",
            "/trends",
            "/campaigns",
            "/query",
            "/analyze-text",
            "/leads/{category}",
            "/recommendations/{customer_id}",
            "/topic-modeling"
        ]
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ollama": "connected",
        "data_loaded": {
            "interactions": len(interactions_df),
            "customers": len(customers_df),
            "campaigns": len(campaigns_df),
            "products": len(products_df)
        }
    }

@app.get("/stats")
def get_stats():
    """Get overall statistics"""
    try:
        stats = {
            "total_interactions": int(len(interactions_df)),
            "total_customers": int(interactions_df['customer_id'].nunique()),
            "date_range": {
                "start": str(interactions_df['date'].min()),
                "end": str(interactions_df['date'].max())
            },
            "by_category": {k: int(v) for k, v in interactions_df['category'].value_counts().to_dict().items()},
            "by_sentiment": {k: int(v) for k, v in interactions_df['sentiment'].value_counts().to_dict().items()},
            "by_churn_risk": {k: int(v) for k, v in interactions_df['churn_risk'].value_counts().to_dict().items()},
            "by_geography": {k: int(v) for k, v in interactions_df['geography'].value_counts().head(10).to_dict().items()},
            "avg_resolution_time": float(interactions_df['resolution_time_hours'].mean()),
            "unresolved_count": int(len(interactions_df[interactions_df['resolution_status'] == 'unresolved']))
        }
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating stats: {str(e)}")

@app.get("/top-issues")
def get_top_issues(limit: int = 10):
    """Get top issues with LLM-powered insights"""
    try:
        # Get top categories
        top_cats = interactions_df['category'].value_counts().head(limit)
        
        issues = []
        for category, count in top_cats.items():
            cat_data = interactions_df[interactions_df['category'] == category]
            
            # Sample texts for this category
            sample_texts = cat_data['interaction_text'].head(5).tolist()
            
            issue = {
                "category": category,
                "count": int(count),
                "percentage": round((count / len(interactions_df)) * 100, 2),
                "avg_churn_score": round(float(cat_data['churn_score'].mean()), 2),
                "high_churn_count": int(len(cat_data[cat_data['churn_risk'].isin(['high', 'critical'])])),
                "unresolved_count": int(len(cat_data[cat_data['resolution_status'] == 'unresolved'])),
                "sample_complaints": sample_texts[:3]
            }
            
            issues.append(issue)
        
        return issues
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting top issues: {str(e)}")

@app.get("/trends")
def get_trends(category: Optional[str] = None, geography: Optional[str] = None):
    """Get week-over-week trends"""
    try:
        df = interactions_df.copy()
        
        if category:
            df = df[df['category'] == category]
        if geography:
            df = df[df['geography'] == geography]
        
        if len(df) == 0:
            return []
        
        # Group by week
        weekly = df.groupby(['week', 'category']).agg({
            'interaction_id': 'count',
            'churn_score': 'mean'
        }).reset_index()
        
        weekly.columns = ['week', 'category', 'count', 'avg_churn_score']
        weekly = weekly.sort_values('week')
        
        return json.loads(weekly.to_json(orient='records'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting trends: {str(e)}")

@app.get("/campaigns")
def get_campaigns():
    """Get campaign performance"""
    try:
        return json.loads(campaigns_df.to_json(orient='records'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting campaigns: {str(e)}")

@app.post("/query")
def natural_language_query(request: QueryRequest):
    """Answer natural language questions with LLM"""
    try:
        print(f"📝 Received query: {request.question}")
        
        # Get relevant context (simple keyword matching for now)
        query_lower = request.question.lower()
        
        # Filter data based on query keywords
        if any(word in query_lower for word in ['internet', 'wifi', 'speed', 'connectivity']):
            context_df = interactions_df[interactions_df['category'].str.contains('internet', case=False, na=False)]
        elif any(word in query_lower for word in ['billing', 'bill', 'charge', 'price']):
            context_df = interactions_df[interactions_df['category'].str.contains('billing', case=False, na=False)]
        elif any(word in query_lower for word in ['churn', 'leaving', 'switch']):
            context_df = interactions_df[interactions_df['churn_risk'].isin(['high', 'critical'])]
        else:
            context_df = interactions_df
        
        # Sample for context
        context_sample = context_df.head(request.max_context_rows)
        context_json = context_sample.to_json(orient='records')
        
        print(f"📊 Using {len(context_sample)} rows as context")
        
        # Query LLM
        result = llm.analyze_query(request.question, context_json)
        
        if not result:
            print("⚠️ LLM returned no result")
            return {
                "answer": "I couldn't analyze the data. Please try rephrasing your question.",
                "insights": [],
                "recommendations": [],
                "data_citations": []
            }
        
        print("✅ Query processed successfully")
        return result
        
    except Exception as e:
        print(f"❌ Error in query endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-text")
def analyze_text(request: AnalyzeRequest):
    """Analyze a single complaint text"""
    try:
        print(f"📝 Analyzing text: {request.text[:100]}...")
        result = llm.analyze_sentiment(request.text)
        
        if not result:
            print("⚠️ Failed to analyze text")
            return {"error": "Failed to analyze text"}
        
        print("✅ Text analyzed successfully")
        return result
        
    except Exception as e:
        print(f"❌ Error analyzing text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/leads/{category}")
def get_leads(category: str, limit: int = 50):
    """Extract high-value leads for targeting"""
    try:
        # Filter by category and high churn risk
        leads_df = interactions_df[
            (interactions_df['category'] == category) &
            (interactions_df['churn_risk'].isin(['high', 'critical']))
        ].sort_values('churn_score', ascending=False).head(limit)
        
        if len(leads_df) == 0:
            return []
        
        leads = []
        for _, row in leads_df.iterrows():
            # Get customer details
            customer_match = customers_df[customers_df['customer_id'] == row['customer_id']]
            if len(customer_match) == 0:
                continue
                
            customer = customer_match.iloc[0]
            
            lead = {
                "customer_id": row['customer_id'],
                "customer_name": customer['customer_name'],
                "geography": row['geography'],
                "issue_summary": row['interaction_text'][:150] + "..." if len(row['interaction_text']) > 150 else row['interaction_text'],
                "sentiment": row['sentiment'],
                "churn_risk": row['churn_risk'],
                "churn_score": round(float(row['churn_score']), 2),
                "tenure_months": int(row['customer_tenure_months']),
                "current_plan_value": int(row['current_plan_value']),
                "operator": row['operator']
            }
            
            leads.append(lead)
        
        return leads
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting leads: {str(e)}")

@app.get("/recommendations/{customer_id}")
def get_recommendations(customer_id: str):
    """Get personalized recommendations for a customer"""
    try:
        print(f"🔍 Getting recommendations for customer: {customer_id}")
        
        # Get customer data
        customer = customers_df[customers_df['customer_id'] == customer_id]
        if len(customer) == 0:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        customer = customer.iloc[0].to_dict()
        
        # Get interaction history
        history = interactions_df[interactions_df['customer_id'] == customer_id]
        if len(history) == 0:
            history_text = "No previous interactions"
        else:
            history_text = "\n".join(history['interaction_text'].tail(5).tolist())
        
        print(f"📊 Found {len(history)} interactions for customer")
        
        # Get LLM recommendations
        recommendations = llm.generate_recommendations(customer, history_text)
        
        if not recommendations:
            print("⚠️ Could not generate recommendations")
            return {"error": "Could not generate recommendations"}
        
        print("✅ Recommendations generated successfully")
        return {
            "customer_id": customer_id,
            "customer_name": customer['customer_name'],
            "current_plan": customer.get('current_plan', 'N/A'),
            "recommendations": recommendations
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error getting recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/topic-modeling")
def topic_modeling(sample_size: int = 50):
    """Perform LLM-based topic modeling (optimized)"""
    try:
        # Limit sample size for performance (max 50)
        actual_sample_size = min(sample_size, 50, len(interactions_df))
        print(f"🔍 Extracting topics from {actual_sample_size} samples")
        
        # Sample interactions
        sample = interactions_df['interaction_text'].sample(actual_sample_size).tolist()
        
        # Extract topics using LLM
        topics = llm.extract_topics(sample, top_n=7)
        
        if not topics:
            print("⚠️ Could not extract topics")
            return {
                "topics": [],
                "error": "Could not extract topics. Try reducing sample_size."
            }
        
        print(f"✅ Extracted {len(topics)} topics")
        return {"topics": topics, "sample_size": actual_sample_size}
        
    except Exception as e:
        print(f"❌ Error in topic modeling: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/categories-summary")
def get_categories_summary():
    """Get quick category statistics without LLM (fast alternative)"""
    try:
        categories = interactions_df['category'].value_counts().head(10)
        
        summary = []
        for category, count in categories.items():
            cat_data = interactions_df[interactions_df['category'] == category]
            
            summary.append({
                "category": category,
                "count": int(count),
                "percentage": round((count / len(interactions_df)) * 100, 2),
                "avg_churn_score": round(float(cat_data['churn_score'].mean()), 2),
                "high_risk_count": int(len(cat_data[cat_data['churn_risk'].isin(['high', 'critical'])])),
                "avg_resolution_time": round(float(cat_data['resolution_time_hours'].mean()), 2)
            })
        
        return {"categories": summary}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting category summary: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("🚀 Starting Smart Campaign Targeting API")
    print("=" * 60)
    print(f"📁 Data directory: {DATA_DIR}")
    print(f"🔗 API will be available at: http://localhost:8000")
    print(f"📚 API docs at: http://localhost:8000/docs")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000)