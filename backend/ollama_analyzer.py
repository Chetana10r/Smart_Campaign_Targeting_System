import requests
import json
import re
import random

class OllamaAnalyzer:
    """Wrapper for Ollama LLM analysis"""

    def __init__(self, model="llama3.2:1b", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    # ==========================================================
    # 🔹 Internal Helper Function: Query Ollama API
    # ==========================================================
    def _query(self, prompt, timeout=120):
        """Send prompt to Ollama API and handle errors safely"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "num_predict": 1000  # Limit response length
                    }
                },
                timeout=timeout
            )

            # Check HTTP status
            if response.status_code != 200:
                print(f"❌ Ollama HTTP error {response.status_code}: {response.text}")
                return None

            # Parse JSON response
            data = response.json()
            
            # ✅ Extract response text
            if "response" in data:
                return data["response"]
            elif "error" in data:
                print(f"❌ Ollama error: {data['error']}")
                return None
            else:
                print(f"⚠️ Unexpected response format. Keys: {list(data.keys())}")
                return None

        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to Ollama at {self.base_url}")
            return None
        except requests.exceptions.Timeout:
            print(f"❌ Ollama request timed out after {timeout} seconds")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON response: {e}")
            return None
        except Exception as e:
            print(f"❌ Error querying Ollama: {type(e).__name__}: {str(e)}")
            return None

    # ==========================================================
    # 🔹 Extract JSON from Text Safely
    # ==========================================================
    def _extract_json(self, text):
        """Extract JSON object or array from a string"""
        if not text:
            return None
            
        try:
            # Remove markdown code blocks if present
            text = re.sub(r'```json\s*', '', text)
            text = re.sub(r'```\s*', '', text)
            
            # Try to find JSON object (handles nested objects)
            json_match = re.search(r'\{(?:[^{}]|(?:\{[^{}]*\}))*\}', text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass

            # Try to find JSON array
            json_match = re.search(r'\[(?:[^\[\]]|(?:\[[^\[\]]*\]))*\]', text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass

            # Try parsing entire text as JSON
            try:
                return json.loads(text.strip())
            except json.JSONDecodeError:
                pass

            print(f"⚠️ Could not extract valid JSON from response")
            print(f"Response preview: {text[:300]}")
            return None
            
        except Exception as e:
            print(f"⚠️ JSON extraction error: {type(e).__name__}: {e}")
            return None

    # ==========================================================
    # 🔹 1. Sentiment Analysis
    # ==========================================================
    def analyze_sentiment(self, text):
        """Analyze sentiment of customer complaint"""
        # Truncate very long text
        if len(text) > 500:
            text = text[:500] + "..."
            
        prompt = f"""Analyze this telecom customer complaint and return ONLY a JSON object (no extra text):

Complaint: "{text}"

Return this exact structure:
{{
  "sentiment": "positive",
  "sentiment_score": 0.5,
  "category": "internet_connectivity",
  "churn_risk": "medium",
  "key_issues": ["issue1", "issue2"],
  "recommended_action": "brief action"
}}

Valid values:
- sentiment: positive, neutral, negative, very_negative
- category: internet_connectivity, internet_speed, billing_overcharge, billing_downgrade, tv_channels, tv_technical, network_quality, account_issues, product_inquiry
- churn_risk: low, medium, high, critical

Return ONLY the JSON object."""

        response = self._query(prompt, timeout=30)
        return self._extract_json(response) if response else None

    # ==========================================================
    # 🔹 2. Topic Extraction (OPTIMIZED)
    # ==========================================================
    def extract_topics(self, texts, top_n=7):
        """Extract top complaint categories"""
        # Aggressively limit sample size for performance
        max_samples = min(30, len(texts))  # Reduced from 100 to 30
        sample_texts = random.sample(texts, max_samples) if len(texts) > max_samples else texts
        
        # Further truncate each text to 100 chars
        complaints_text = "\n".join([
            f"{i+1}. {text[:100]}..." 
            for i, text in enumerate(sample_texts)
        ])

        prompt = f"""Analyze these {len(sample_texts)} telecom complaints and identify the top {top_n} topics.

Complaints:
{complaints_text}

Return ONLY a JSON array:
[
  {{"topic": "Topic 1", "description": "brief", "percentage": 25, "severity": "high"}},
  {{"topic": "Topic 2", "description": "brief", "percentage": 20, "severity": "medium"}}
]

Valid severity: low, medium, high, critical
Return ONLY the JSON array."""

        response = self._query(prompt, timeout=120)  # Reduced timeout
        result = self._extract_json(response)
        return result if result and isinstance(result, list) else []

    # ==========================================================
    # 🔹 3. Personalized Recommendations
    # ==========================================================
    def generate_recommendations(self, customer_data, interaction_history):
        """Generate personalized retention suggestions"""
        # Truncate history
        if len(interaction_history) > 500:
            interaction_history = interaction_history[:500] + "..."
            
        prompt = f"""Based on customer profile, suggest offers.

Profile:
- Tenure: {customer_data.get('tenure_months', 'N/A')} months
- Plan: ₹{customer_data.get('current_plan_value', 'N/A')}/month
- Service: {customer_data.get('service_type', 'N/A')}
- Churn Risk: {customer_data.get('churn_risk', 'unknown')}

Recent Issues:
{interaction_history}

Return ONLY JSON:
{{
  "primary_recommendation": {{
    "product": "name",
    "reason": "why",
    "expected_impact": "outcome"
  }},
  "secondary_recommendations": [
    {{"product": "name2", "reason": "why"}}
  ],
  "retention_strategy": "strategy"
}}"""

        response = self._query(prompt, timeout=40)
        return self._extract_json(response) if response else None

    # ==========================================================
    # 🔹 4. Query Analytics (Q&A over data) - OPTIMIZED
    # ==========================================================
    def analyze_query(self, query, context_data):
        """Answer questions about customer data"""
        # Aggressively limit context size
        max_context_length = 3000  # Much smaller context
        if len(context_data) > max_context_length:
            context_data = context_data[:max_context_length] + '...]'
            
        prompt = f"""You are a telecom analyst. Answer this question using the data.

Data (sample):
{context_data}

Question: {query}

Return ONLY JSON:
{{
  "answer": "concise answer with key numbers",
  "insights": ["insight 1", "insight 2"],
  "recommendations": ["action 1", "action 2"],
  "data_citations": ["stat 1", "stat 2"]
}}

Be concise. Return ONLY the JSON object."""

        response = self._query(prompt, timeout=40)
        return self._extract_json(response) if response else None
    
    # ==========================================================
    # 🔹 5. Quick Summary (NEW - Faster alternative)
    # ==========================================================
    def quick_summary(self, text, max_length=100):
        """Generate a quick summary - much faster than full analysis"""
        if len(text) > 300:
            text = text[:300]
            
        prompt = f"""Summarize this complaint in one sentence (max {max_length} chars):

"{text}"

Return ONLY the summary sentence, no JSON."""

        response = self._query(prompt, timeout=15)
        return response.strip() if response else None