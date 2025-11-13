"""
Complete Indian Telecom Customer Interaction Data Generator
============================================================
Generates realistic dataset for Smart Campaign Targeting project

Requirements:
    pip install pandas numpy requests beautifulsoup4 faker

Usage:
    python generate_complete_dataset.py
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json
import os
import requests
from bs4 import BeautifulSoup
import time

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# ============================================================
# CONFIGURATION
# ============================================================

CONFIG = {
    'num_customers': 3000,
    'num_interactions': 10000,
    'num_campaigns': 30,
    'num_products': 50,
    'scrape_complaints': False,  # Set True to try scraping (may fail)
    'output_dir': 'data'
}

# ============================================================
# INDIAN TELECOM CONTEXT DATA
# ============================================================

OPERATORS = ['Jio', 'Airtel', 'Vi', 'BSNL']

CITIES = {
    'metro': ['Mumbai', 'Delhi', 'Bangalore', 'Kolkata', 'Chennai', 'Hyderabad'],
    'tier1': ['Pune', 'Ahmedabad', 'Jaipur', 'Lucknow', 'Chandigarh', 'Indore'],
    'tier2': ['Nagpur', 'Coimbatore', 'Vadodara', 'Ludhiana', 'Agra', 'Nashik', 'Surat', 'Kochi']
}
ALL_CITIES = CITIES['metro'] + CITIES['tier1'] + CITIES['tier2']

REGIONS = {
    'Mumbai': 'West', 'Pune': 'West', 'Ahmedabad': 'West', 'Surat': 'West', 'Nagpur': 'West',
    'Delhi': 'North', 'Jaipur': 'North', 'Lucknow': 'North', 'Chandigarh': 'North', 'Ludhiana': 'North', 'Agra': 'North',
    'Bangalore': 'South', 'Chennai': 'South', 'Hyderabad': 'South', 'Kochi': 'South', 'Coimbatore': 'South',
    'Kolkata': 'East', 'Vadodara': 'West', 'Indore': 'West', 'Nashik': 'West'
}

PLANS = {
    'jio': {
        'prepaid': [239, 299, 399, 666, 719, 2999],
        'postpaid': [399, 599, 999, 1499],
        'fiber': [699, 999, 1499, 2499, 3999]
    },
    'airtel': {
        'prepaid': [265, 359, 549, 719, 3359],
        'postpaid': [499, 749, 999, 1599],
        'fiber': [799, 999, 1499, 3999]
    },
    'vi': {
        'prepaid': [239, 299, 409, 699, 3099],
        'postpaid': [399, 699, 999],
        'fiber': [699, 999, 1499]
    },
    'bsnl': {
        'prepaid': [199, 299, 399],
        'postpaid': [399, 599],
        'fiber': [499, 799, 999]
    }
}

# Realistic complaint templates
ISSUE_TEMPLATES = {
    'internet_connectivity': [
        "Internet not working for {days} days. Called customer care {times} times but no resolution. Very frustrated with {operator} service.",
        "WiFi keeps disconnecting every {frequency} minutes. Can't attend online meetings. Need urgent resolution from {operator}.",
        "Fiber cable cut during {event}. When will technician visit? Already {days} days without internet in {city}.",
        "Getting only {speed}Mbps speed instead of {plan_speed}Mbps as per my {operator} plan. This is cheating!",
        "Router showing {light_color} light. Internet completely down. Work from home affected badly.",
        "Network drops during evening hours {time}. Can't stream IPL matches. Very poor {operator} service.",
        "{operator} fiber ONT device not working. Red light blinking. Need replacement urgently in {city}.",
        "Complete internet outage in {city} area for last {days} days. {operator} not responding to complaints.",
        "Intermittent connectivity issues. Internet works for 10 mins then stops. Very irritating {operator} service."
    ],
    
    'internet_speed': [
        "Paid for {plan_speed}Mbps {operator} plan but getting only {actual_speed}Mbps. This is fraud!",
        "Speed test shows {actual_speed}Mbps but YouTube videos buffering on {operator}. What's the use?",
        "During peak hours {time}, speed drops to {actual_speed}Mbps on {operator}. Can't work properly.",
        "Promised {plan_speed}Mbps fiber connection but reality is {actual_speed}Mbps. Disappointed with {operator}.",
        "Upload speed is terrible - only {upload_speed}Mbps on {operator}. Can't do video calls for office work.",
        "Website loading very slow on {operator}. Latency is very high. Gaming impossible.",
        "{operator} speed inconsistent throughout day. Morning {morning_speed}Mbps, evening {evening_speed}Mbps."
    ],
    
    'billing_overcharge': [
        "Bill increased from ₹{old_bill} to ₹{new_bill} without any plan change on {operator}. Why?",
        "Charged ₹{extra} extra for international roaming I never used on {operator}. Want refund immediately.",
        "Plan is ₹{plan_price} but {operator} bill shows ₹{actual_bill}. What are these hidden charges?",
        "Double charged on {date} by {operator}. Money deducted twice - ₹{amount} from my account. Still not refunded.",
        "Cashback of ₹{cashback} promised during {operator} recharge not received. Cheating customers.",
        "GST calculation wrong on {operator} bill. Should be ₹{correct} but charged ₹{charged}. Please correct.",
        "Billed for premium channels I didn't subscribe on {operator}. Remove charges of ₹{extra}.",
        "{operator} charged ₹{amount} for calls to customer care. This is ridiculous!"
    ],
    
    'billing_downgrade': [
        "Current {operator} bill ₹{current_bill} is too high. Want to downgrade to ₹{target_plan} plan to save money.",
        "Planning to switch to {competitor} as they offer better rates. Can {operator} match their ₹{competitor_price} plan?",
        "After losing job, can't afford ₹{current_bill} {operator} plan. Please help me downgrade to basic plan.",
        "Family expenses increased. Need cheaper {operator} plan around ₹{budget}. What options available?",
        "Not satisfied with {operator} pricing. Thinking of porting to Jio/Airtel. Give me retention offer or I'm leaving.",
        "{operator} too expensive compared to competitors. Need ₹{budget} budget plan or will switch.",
        "Economic situation bad. Can't continue ₹{current_bill} plan. Help with downgrade to ₹{target_plan}."
    ],
    
    'tv_channels': [
        "Star Sports channels not working during IPL match on {operator}. This is unacceptable!",
        "{channel_count} channels missing after recharge on {operator}. Sony, Zee channels not showing.",
        "HD channels showing SD quality on {operator}. Paid for HD pack but getting poor picture quality.",
        "Regional channels (Tamil/Telugu) package not activated despite payment of ₹{amount} to {operator}.",
        "{operator} set-top box showing error code {error_code}. All channels stuck on loading screen.",
        "Colors, Star Plus channels black screen on {operator}. Other channels working fine.",
        "Subscribed to sports pack but not getting all matches on {operator}. Very disappointed."
    ],
    
    'tv_technical': [
        "{operator} DTH set-top box remote not working. Tried new batteries but no response.",
        "Picture freezing and pixelating on all channels on {operator}. Signal strength shows low.",
        "No audio on several channels including Colors, Star Plus on {operator}. Video playing but no sound.",
        "Recording feature not working in {operator} set-top box. Can't record favorite shows.",
        "Hotstar/JioCinema app on {operator} STB very slow. Takes 5 minutes to load one video.",
        "{operator} set-top box hanging frequently. Need to restart 10 times a day.",
        "HDMI connection issues with {operator} STB. Picture goes black randomly."
    ],
    
    'network_quality': [
        "Call drops frequently on {route} with {operator}. Very poor network quality.",
        "No {operator} network in metro/underground stations in {city}. Other operators working fine.",
        "VoLTE calls breaking with robot voice on {operator}. Can't understand what other person saying.",
        "Network fluctuates in apartment with {operator}. Ground floor has signal but 5th floor shows emergency only.",
        "5G icon showing but speed is like 3G on {operator}. What's the point of 5G tower in {city}?",
        "{operator} network very weak in {city}. Full bars but can't make calls.",
        "Indoor network penetration very poor with {operator}. Have to go to balcony to take calls."
    ],
    
    'account_issues': [
        "Porting from {old_operator} to {operator} taking more than 7 days. When will it complete?",
        "Can't login to My{operator} app. Password reset not working. Email not received.",
        "Want to change registered mobile number with {operator} but customer care says not possible. Why?",
        "Postpaid to prepaid conversion requested 15 days ago on {operator}. Still pending. Very slow process.",
        "Unable to update email address in {operator} account. System showing error every time.",
        "{operator} account locked after multiple login attempts. Can't access anything.",
        "KYC verification stuck on {operator}. Submitted documents 10 days ago, no update."
    ],
    
    'product_inquiry': [
        "What are current {operator} fiber plans available in {city} {pincode}? Need {speed}Mbps for work from home.",
        "Interested in upgrading from {current_plan} to {target_plan} on {operator}. What's the process and cost?",
        "Do you have WiFi mesh system for {operator}? Current router not covering full house. Need better solution.",
        "Want to add {operator} Black/Platinum plan. What are benefits and extra charges?",
        "Is 5G available in {area} for {operator}? My phone supports 5G but not getting 5G network.",
        "Looking for {operator} family plan for 4 connections. What packages available?",
        "Need information about {operator} international roaming packs for USA trip."
    ],
    
    'customer_retention': [
        "Competitor offering same plan for ₹{competitor_price} less. Why should I stay with {operator}?",
        "Been with {operator} for {tenure} years but no loyalty benefits. Feeling cheated.",
        "Received better offer from {competitor}. Will port out if {operator} can't match.",
        "Service quality deteriorated over last {months} months with {operator}. Thinking of switching.",
        "Friends using {competitor} very happy. Should I also switch from {operator}?"
    ]
}

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def create_output_directory():
    """Create output directory if not exists"""
    os.makedirs(CONFIG['output_dir'], exist_ok=True)
    print(f"✅ Output directory: {CONFIG['output_dir']}/")

def generate_customer_name():
    """Generate realistic Indian names"""
    first_names = ['Rahul', 'Priya', 'Amit', 'Sneha', 'Rajesh', 'Anjali', 'Vikram', 'Pooja', 
                   'Arjun', 'Kavita', 'Sanjay', 'Neha', 'Karan', 'Divya', 'Arun', 'Ritu',
                   'Varun', 'Simran', 'Suresh', 'Meera', 'Rohan', 'Shreya', 'Manish', 'Sakshi']
    last_names = ['Kumar', 'Sharma', 'Singh', 'Patel', 'Gupta', 'Reddy', 'Iyer', 'Joshi',
                  'Mehta', 'Nair', 'Desai', 'Rao', 'Pillai', 'Agarwal', 'Chopra', 'Kapoor']
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_email(name, domain='email.com'):
    """Generate email from name"""
    clean_name = name.lower().replace(' ', '.')
    return f"{clean_name}{random.randint(1, 999)}@{domain}"

def generate_phone():
    """Generate Indian phone number"""
    return f"+91-{random.randint(7000000000, 9999999999)}"

# ============================================================
# STEP 1: GENERATE CUSTOMER PROFILES
# ============================================================

def generate_customer_profiles(num_customers):
    """Generate customer profile dataset"""
    print(f"\n📊 Generating {num_customers} customer profiles...")
    
    customers = []
    
    for i in range(num_customers):
        customer_id = f'CUST_{10000 + i}'
        name = generate_customer_name()
        operator = random.choice(OPERATORS)
        city = random.choice(ALL_CITIES)
        
        # Service type distribution
        service_type = random.choices(
            ['fiber', 'postpaid', 'prepaid'],
            weights=[0.3, 0.3, 0.4]
        )[0]
        
        # Plan value based on service type
        plan_value = random.choice(PLANS[operator.lower()].get(service_type, [399, 699, 999]))
        
        # Tenure (months as customer)
        tenure = random.choices(
            range(1, 121),
            weights=[10]*12 + [8]*12 + [6]*24 + [4]*36 + [2]*36
        )[0]
        
        # Customer segment
        if plan_value >= 1500:
            segment = 'Premium'
        elif plan_value >= 700:
            segment = 'Standard'
        else:
            segment = 'Basic'
        
        customer = {
            'customer_id': customer_id,
            'customer_name': name,
            'email': generate_email(name),
            'phone': generate_phone(),
            'operator': operator,
            'account_created_date': (datetime.now() - timedelta(days=tenure*30)).strftime('%Y-%m-%d'),
            'tenure_months': tenure,
            'customer_segment': segment,
            'service_type': service_type,
            'current_plan': f"{operator} {service_type.title()} {plan_value}",
            'current_plan_value': plan_value,
            'products_subscribed': random.choice([
                'Internet',
                'Internet,TV',
                'Internet,Phone',
                'Internet,TV,Phone'
            ]),
            'auto_pay_enabled': random.choice([True, False]),
            'payment_method': random.choice(['Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'Cash']),
            'last_payment_date': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
            'outstanding_balance': random.choice([0, 0, 0, plan_value, plan_value*2]),
            'total_lifetime_value': plan_value * tenure,
            'geography': city,
            'region': REGIONS.get(city, 'West'),
            'address_pincode': random.randint(400001, 600100),
            'age_group': random.choice(['18-25', '26-35', '36-50', '50+']),
            'customer_type': random.choices(['Individual', 'SME', 'Enterprise'], weights=[0.8, 0.15, 0.05])[0]
        }
        
        customers.append(customer)
    
    df = pd.DataFrame(customers)
    output_file = f"{CONFIG['output_dir']}/customer_profiles.csv"
    df.to_csv(output_file, index=False)
    print(f"   ✅ Saved {len(df)} customer profiles to {output_file}")
    
    return df

# ============================================================
# STEP 2: GENERATE CUSTOMER INTERACTIONS
# ============================================================

def generate_customer_interactions(customers_df, num_interactions):
    """Generate realistic customer interaction dataset"""
    print(f"\n💬 Generating {num_interactions} customer interactions...")
    
    interactions = []
    
    for i in range(num_interactions):
        # Select random customer
        customer = customers_df.sample(1).iloc[0]
        
        # Select issue category (weighted by likelihood)
        if customer['service_type'] == 'fiber':
            category_weights = {
                'internet_connectivity': 0.25,
                'internet_speed': 0.20,
                'billing_overcharge': 0.15,
                'billing_downgrade': 0.10,
                'tv_channels': 0.10,
                'tv_technical': 0.05,
                'network_quality': 0.05,
                'account_issues': 0.05,
                'product_inquiry': 0.03,
                'customer_retention': 0.02
            }
        else:
            category_weights = {
                'network_quality': 0.25,
                'billing_overcharge': 0.20,
                'billing_downgrade': 0.15,
                'internet_connectivity': 0.10,
                'internet_speed': 0.10,
                'account_issues': 0.10,
                'product_inquiry': 0.05,
                'customer_retention': 0.03,
                'tv_channels': 0.01,
                'tv_technical': 0.01
            }
        
        category = random.choices(
            list(category_weights.keys()),
            weights=list(category_weights.values())
        )[0]
        
        # Generate interaction text
        template = random.choice(ISSUE_TEMPLATES[category])
        
        # Fill template with realistic values
        text = template.format(
            operator=customer['operator'],
            city=customer['geography'],
            days=random.randint(1, 7),
            times=random.randint(2, 5),
            frequency=random.choice(['5', '10', '15', 'few']),
            event=random.choice(['road construction', 'heavy rain', 'building work', 'cable theft']),
            speed=random.randint(10, 40),
            plan_speed=random.choice([50, 100, 200, 300, 500]),
            actual_speed=random.randint(15, 80),
            upload_speed=random.randint(5, 30),
            morning_speed=random.randint(80, 150),
            evening_speed=random.randint(20, 60),
            light_color=random.choice(['red', 'orange', 'blinking']),
            time=random.choice(['7-10 PM', 'evening', 'night', 'peak hours']),
            old_bill=customer['current_plan_value'],
            new_bill=customer['current_plan_value'] + random.randint(200, 800),
            extra=random.randint(100, 500),
            date=random.choice(['last week', '3 days ago', 'yesterday', '5th Nov']),
            amount=random.randint(500, 2000),
            plan_price=customer['current_plan_value'],
            actual_bill=customer['current_plan_value'] + random.randint(100, 500),
            cashback=random.randint(50, 500),
            correct=customer['current_plan_value'],
            charged=customer['current_plan_value'] + random.randint(50, 200),
            current_bill=customer['current_plan_value'],
            target_plan=max(299, customer['current_plan_value'] - random.randint(200, 500)),
            competitor=random.choice([op for op in OPERATORS if op != customer['operator']]),
            competitor_price=customer['current_plan_value'] - random.randint(100, 300),
            budget=random.randint(300, 700),
            channel_count=random.randint(10, 50),
            error_code=random.choice(['E-404', 'E-16', 'E-8', 'E-100', 'NO SIGNAL']),
            route=random.choice(['Mumbai-Pune highway', 'Delhi-Jaipur route', 'office commute']),
            area=customer['geography'],
            old_operator=random.choice([op for op in OPERATORS if op != customer['operator']]),
            pincode=customer['address_pincode'],
            current_plan=f"{random.choice([50, 100, 200])}Mbps",
            tenure=customer['tenure_months']//12 or 1,
            months=random.randint(3, 12)
        )
        
        # Determine sentiment based on keywords
        negative_keywords = ['frustrated', 'cheating', 'fraud', 'unacceptable', 'leaving', 'disappointed', 'poor', 'terrible']
        very_negative_keywords = ['switch', 'port', 'competitor', 'leaving']
        positive_keywords = ['interested', 'inquiry', 'upgrade', 'want to']
        
        text_lower = text.lower()
        
        if any(word in text_lower for word in very_negative_keywords):
            sentiment = 'very_negative'
            sentiment_score = round(random.uniform(-0.95, -0.70), 2)
            churn_risk = random.choice(['high', 'critical'])
            churn_score = round(random.uniform(0.70, 0.95), 2)
        elif any(word in text_lower for word in negative_keywords):
            sentiment = 'negative'
            sentiment_score = round(random.uniform(-0.70, -0.30), 2)
            churn_risk = random.choice(['medium', 'high'])
            churn_score = round(random.uniform(0.40, 0.70), 2)
        elif any(word in text_lower for word in positive_keywords):
            sentiment = 'positive'
            sentiment_score = round(random.uniform(0.30, 0.85), 2)
            churn_risk = 'low'
            churn_score = round(random.uniform(0.05, 0.25), 2)
        else:
            sentiment = 'neutral'
            sentiment_score = round(random.uniform(-0.20, 0.30), 2)
            churn_risk = random.choice(['low', 'medium'])
            churn_score = round(random.uniform(0.20, 0.50), 2)
        
        # Interaction date (last 90 days)
        interaction_date = datetime.now() - timedelta(days=random.randint(0, 90))
        
        # Resolution status
        if interaction_date < datetime.now() - timedelta(days=7):
            resolution_status = random.choices(
                ['resolved', 'pending', 'escalated', 'unresolved'],
                weights=[0.65, 0.15, 0.10, 0.10]
            )[0]
        else:
            resolution_status = random.choices(
                ['resolved', 'pending', 'escalated'],
                weights=[0.40, 0.45, 0.15]
            )[0]
        
        resolution_time = None
        if resolution_status == 'resolved':
            resolution_time = random.choice([2, 4, 8, 24, 48, 72])
        
        interaction = {
            'interaction_id': f'INT_{i:06d}',
            'customer_id': customer['customer_id'],
            'timestamp': interaction_date.strftime('%Y-%m-%d %H:%M:%S'),
            'date': interaction_date.strftime('%Y-%m-%d'),
            'week': interaction_date.strftime('%Y-W%U'),
            'month': interaction_date.strftime('%Y-%m'),
            'channel': random.choices(
                ['Call', 'Email', 'Chat', 'WhatsApp', 'App', 'Store Visit', 'Social Media'],
                weights=[0.35, 0.20, 0.20, 0.10, 0.08, 0.05, 0.02]
            )[0],
            'interaction_text': text,
            'category': category,
            'sentiment': sentiment,
            'sentiment_score': sentiment_score,
            'resolution_status': resolution_status,
            'resolution_time_hours': resolution_time,
            'agent_id': f'AGT_{random.randint(1, 100):03d}',
            'agent_name': generate_customer_name(),
            'geography': customer['geography'],
            'region': customer['region'],
            'churn_risk': churn_risk,
            'churn_score': churn_score,
            'escalation_count': random.choice([0, 0, 0, 1, 1, 2, 3]),
            'follow_up_required': random.choice([True, False]),
            'interaction_duration_min': random.randint(2, 45),
            'customer_tenure_months': customer['tenure_months'],
            'current_plan_value': customer['current_plan_value'],
            'operator': customer['operator'],
            'service_type': customer['service_type']
        }
        
        interactions.append(interaction)
    
    df = pd.DataFrame(interactions)
    output_file = f"{CONFIG['output_dir']}/customer_interactions.csv"
    df.to_csv(output_file, index=False)
    print(f"   ✅ Saved {len(df)} interactions to {output_file}")
    
    # Print summary statistics
    print(f"\n   📈 Dataset Statistics:")
    print(f"      • Unique customers: {df['customer_id'].nunique()}")
    print(f"      • Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"\n      Category Distribution:")
    for cat, count in df['category'].value_counts().head(5).items():
        print(f"         - {cat}: {count} ({count/len(df)*100:.1f}%)")
    print(f"\n      Sentiment Distribution:")
    for sent, count in df['sentiment'].value_counts().items():
        print(f"         - {sent}: {count} ({count/len(df)*100:.1f}%)")
    print(f"\n      Churn Risk Distribution:")
    for risk, count in df['churn_risk'].value_counts().items():
        print(f"         - {risk}: {count} ({count/len(df)*100:.1f}%)")
    
    return df

# ============================================================
# STEP 3: GENERATE CAMPAIGN DATA
# ============================================================

def generate_campaign_history(num_campaigns):
    """Generate campaign history dataset"""
    print(f"\n📢 Generating {num_campaigns} campaigns...")
    
    campaigns = []
    
    campaign_types = ['Upsell', 'Cross-sell', 'Retention', 'Winback', 'Upgrade']
    target_issues = list(ISSUE_TEMPLATES.keys())
    
    for i in range(num_campaigns):
        campaign_type = random.choice(campaign_types)
        target_issue = random.choice(target_issues)
        
        start_date = datetime.now() - timedelta(days=random.randint(30, 180))
        duration = random.randint(15, 60)
        end_date = start_date + timedelta(days=duration)
        
        targeted = random.randint(100, 2000)
        contacted = int(targeted * random.uniform(0.85, 0.98))
        responded = int(contacted * random.uniform(0.15, 0.45))
        converted = int(responded * random.uniform(0.20, 0.60))
        
        avg_deal_value = random.randint(500, 3000)
        revenue = converted * avg_deal_value
        campaign_cost = targeted * random.randint(20, 100)
        roi = round((revenue - campaign_cost) / campaign_cost, 2)
        
        campaign = {
            'campaign_id': f'CAMP_{i:03d}',
            'campaign_name': f'{campaign_type} - {target_issue.replace("_", " ").title()} Q{(start_date.month-1)//3 + 1}',
            'campaign_type': campaign_type,
            'target_issue': target_issue,
            'target_segment': random.choice(['High Churn', 'Speed Issues', 'Billing Complaints', 'All Customers']),
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'status': 'Completed' if end_date < datetime.now() else 'Active',
            'total_targeted': targeted,
            'total_contacted': contacted,
            'total_responded': responded,
            'total_converted': converted,
            'conversion_rate': round((converted / targeted) * 100, 2),
            'response_rate': round((responded / contacted) * 100, 2),
            'revenue_generated': revenue,
            'campaign_cost': campaign_cost,
            'roi': roi,
            'avg_deal_value': avg_deal_value,
            'offer_description': f"Special offer for {target_issue.replace('_', ' ')} customers",
            'channel_used': random.choice(['Email', 'SMS', 'Call', 'App Notification', 'Multi-channel'])
        }
        
        campaigns.append(campaign)
    
    df = pd.DataFrame(campaigns)
    output_file = f"{CONFIG['output_dir']}/campaign_history.csv"
    df.to_csv(output_file, index=False)
    print(f"   ✅ Saved {len(df)} campaigns to {output_file}")
    
    return df

# ============================================================
# STEP 4: GENERATE PRODUCT CATALOG
# ============================================================

def generate_product_catalog(num_products):
    """Generate product catalog dataset"""
    print(f"\n📦 Generating {num_products} products...")
    
    products = []
    
    product_templates = {
        'Internet Plans': [
            ('50Mbps Basic Fiber', 699, 'Fiber broadband with 50Mbps speed, unlimited data'),
            ('100Mbps Standard Fiber', 999, 'Fiber broadband with 100Mbps speed, unlimited data'),
            ('200Mbps Premium Fiber', 1499, 'High-speed fiber with 200Mbps, OTT subscription included'),
            ('300Mbps Ultra Fiber', 2499, 'Ultra-fast fiber broadband with 300Mbps symmetrical speed'),
            ('500Mbps Gig Fiber', 3999, 'Gigabit-ready fiber with 500Mbps and priority support'),
            ('Prepaid 1.5GB/Day', 299, '84 days validity, 1.5GB data per day, unlimited calls'),
            ('Prepaid 2GB/Day', 399, '84 days validity, 2GB data per day, unlimited calls'),
            ('Postpaid Unlimited', 599, 'Unlimited calls, 50GB data, OTT subscription'),
        ],
        'Hardware': [
            ('WiFi 6 Router', 2999, 'Dual-band WiFi 6 router with 4 antennas, covers 2000 sq ft'),
            ('WiFi Range Extender', 1499, 'Extends WiFi coverage up to 1500 sq ft'),
            ('Mesh WiFi System (2-pack)', 8999, 'Whole home mesh WiFi covering 4000 sq ft'),
            ('ONT Fiber Device', 1999, 'Optical Network Terminal for fiber connection'),
            ('4G WiFi Dongle', 999, 'Portable 4G WiFi hotspot, works with all networks'),
            ('WiFi Booster', 1299, 'Signal booster for better indoor coverage'),
        ],
        'TV Services': [
            ('Basic DTH Pack', 299, '150+ SD channels, all free-to-air channels'),
            ('Premium DTH Pack', 599, '250+ channels including HD, regional packs'),
            ('Sports Pack', 399, 'All sports channels including Star Sports, Sony Ten'),
            ('Movies Pack', 299, 'Premium movie channels including HBO, Sony Pix'),
            ('Regional Language Pack', 199, 'Regional channels - Tamil/Telugu/Bengali/Marathi'),
            ('HD Set-Top Box', 1500, 'HD quality set-top box with recording feature'),
        ],
        'Value Added Services': [
            ('International Roaming - USA', 2999, '30 days validity, 10GB data, unlimited calls'),
            ('International Roaming - Europe', 3499, '30 days validity, 15GB data, unlimited calls'),
            ('Caller Tune Service', 49, 'Monthly subscription for caller tunes'),
            ('OTT Bundle - Netflix', 199, 'Netflix Basic bundled with your plan'),
            ('OTT Bundle - Amazon Prime', 149, 'Amazon Prime Video subscription'),
            ('Cloud Storage 100GB', 99, '100GB cloud storage for photos and files'),
        ],
        'Upgrades': [
            ('Speed Upgrade to 200Mbps', 500, 'One-time upgrade fee to 200Mbps plan'),
            ('Speed Upgrade to 300Mbps', 1000, 'One-time upgrade fee to 300Mbps plan'),
            ('Add TV to Internet', 299, 'Bundle TV service with existing internet'),
            ('Add Phone Line', 199, 'Add landline phone service to bundle'),
        ]
    }
    
    product_id = 1
    for category, items in product_templates.items():
        for name, price, description in items:
            # Determine which issue this product solves
            target_issues = []
            if 'speed' in name.lower() or 'mbps' in name.lower():
                target_issues = ['internet_speed', 'internet_connectivity']
            elif 'wifi' in name.lower() or 'router' in name.lower() or 'booster' in name.lower():
                target_issues = ['internet_connectivity', 'network_quality']
            elif 'tv' in name.lower() or 'dth' in name.lower() or 'channels' in name.lower():
                target_issues = ['tv_channels', 'tv_technical']
            elif 'upgrade' in name.lower():
                target_issues = ['internet_speed', 'product_inquiry']
            elif 'ott' in name.lower():
                target_issues = ['customer_retention', 'product_inquiry']
            else:
                target_issues = ['product_inquiry']
            
            product = {
                'product_id': f'PROD_{product_id:03d}',
                'product_name': name,
                'product_category': category,
                'product_type': 'Service' if 'Pack' in name or 'Plan' in name else 'Hardware',
                'price': price,
                'description': description,
                'target_issues': ','.join(target_issues),
                'suitable_for_churn': random.choice([True, False]),
                'stock_status': random.choices(['In Stock', 'Low Stock', 'Out of Stock'], weights=[0.8, 0.15, 0.05])[0],
                'popularity_score': random.randint(1, 100),
                'avg_rating': round(random.uniform(3.5, 4.9), 1)
            }
            
            products.append(product)
            product_id += 1
    
    df = pd.DataFrame(products)
    output_file = f"{CONFIG['output_dir']}/product_catalog.csv"
    df.to_csv(output_file, index=False)
    print(f"   ✅ Saved {len(df)} products to {output_file}")
    
    return df

# ============================================================
# STEP 5: GENERATE ISSUE TRENDS
# ============================================================

def generate_issue_trends(interactions_df):
    """Generate weekly issue trends from interactions"""
    print(f"\n📈 Generating issue trends...")
    
    # Aggregate by week and category
    trends = interactions_df.groupby(['week', 'category', 'geography']).agg({
        'interaction_id': 'count',
        'churn_score': 'mean'
    }).reset_index()
    
    trends.columns = ['week', 'category', 'geography', 'issue_count', 'avg_churn_score']
    
    # Calculate week-over-week change
    trends = trends.sort_values(['category', 'geography', 'week'])
    trends['prev_week_count'] = trends.groupby(['category', 'geography'])['issue_count'].shift(1)
    trends['change_percentage'] = ((trends['issue_count'] - trends['prev_week_count']) / 
                                   trends['prev_week_count'] * 100).round(2)
    trends['change_percentage'] = trends['change_percentage'].fillna(0)
    
    # Determine trend direction
    trends['trend'] = trends['change_percentage'].apply(
        lambda x: 'increasing' if x > 5 else ('decreasing' if x < -5 else 'stable')
    )
    
    # Determine severity based on count and churn score
    trends['severity'] = trends.apply(
        lambda row: 'critical' if row['issue_count'] > 50 and row['avg_churn_score'] > 0.7
        else ('high' if row['issue_count'] > 30 and row['avg_churn_score'] > 0.5
        else ('medium' if row['issue_count'] > 15 else 'low')),
        axis=1
    )
    
    trends = trends.drop('prev_week_count', axis=1)
    
    output_file = f"{CONFIG['output_dir']}/issue_trends.csv"
    trends.to_csv(output_file, index=False)
    print(f"   ✅ Saved {len(trends)} trend records to {output_file}")
    
    return trends

# ============================================================
# STEP 6: GENERATE CAMPAIGN-CUSTOMER MAPPING
# ============================================================

def generate_campaign_customer_mapping(campaigns_df, customers_df, interactions_df):
    """Generate campaign-customer mapping dataset"""
    print(f"\n🎯 Generating campaign-customer mapping...")
    
    mappings = []
    
    for _, campaign in campaigns_df.iterrows():
        # Select customers based on campaign target
        target_issue = campaign['target_issue']
        
        # Get customers who had this issue
        relevant_interactions = interactions_df[interactions_df['category'] == target_issue]
        target_customers = relevant_interactions['customer_id'].unique()
        
        # If not enough customers, add random ones
        if len(target_customers) < campaign['total_targeted']:
            additional = customers_df[~customers_df['customer_id'].isin(target_customers)].sample(
                min(campaign['total_targeted'] - len(target_customers), len(customers_df))
            )['customer_id'].values
            target_customers = np.concatenate([target_customers, additional])
        
        # Sample exact number needed
        selected_customers = np.random.choice(
            target_customers, 
            size=min(campaign['total_targeted'], len(target_customers)), 
            replace=False
        )
        
        for customer_id in selected_customers:
            # Determine if contacted, responded, converted
            contacted = random.random() < (campaign['total_contacted'] / campaign['total_targeted'])
            
            if contacted:
                responded = random.random() < (campaign['total_responded'] / campaign['total_contacted'])
                if responded:
                    converted = random.random() < (campaign['total_converted'] / campaign['total_responded'])
                else:
                    converted = False
            else:
                responded = False
                converted = False
            
            contacted_date = None
            response_date = None
            conversion_date = None
            revenue = 0
            
            if contacted:
                contacted_date = (datetime.strptime(campaign['start_date'], '%Y-%m-%d') + 
                                 timedelta(days=random.randint(0, 10))).strftime('%Y-%m-%d')
                
                if responded:
                    response_date = (datetime.strptime(contacted_date, '%Y-%m-%d') + 
                                    timedelta(days=random.randint(1, 5))).strftime('%Y-%m-%d')
                    
                    if converted:
                        conversion_date = (datetime.strptime(response_date, '%Y-%m-%d') + 
                                         timedelta(days=random.randint(1, 7))).strftime('%Y-%m-%d')
                        revenue = campaign['avg_deal_value'] + random.randint(-200, 200)
            
            mapping = {
                'campaign_id': campaign['campaign_id'],
                'customer_id': customer_id,
                'contacted': contacted,
                'contacted_date': contacted_date,
                'responded': responded,
                'response_date': response_date,
                'converted': converted,
                'conversion_date': conversion_date,
                'offer_accepted': random.choice(['Speed Upgrade', 'WiFi Booster', 'Plan Downgrade', 
                                                'Retention Offer', 'Bundle Discount']) if converted else None,
                'revenue': revenue if converted else 0,
                'feedback': random.choice([
                    'Good offer, accepted',
                    'Not interested right now',
                    'Too expensive',
                    'Already solved the issue',
                    'Will think about it',
                    None
                ]) if responded else None
            }
            
            mappings.append(mapping)
    
    df = pd.DataFrame(mappings)
    output_file = f"{CONFIG['output_dir']}/campaign_customer_mapping.csv"
    df.to_csv(output_file, index=False)
    print(f"   ✅ Saved {len(df)} campaign mappings to {output_file}")
    
    return df

# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    """Main execution function"""
    print("="*60)
    print("🚀 Indian Telecom Data Generator")
    print("   Smart Campaign Targeting Project")
    print("="*60)
    
    # Create output directory
    create_output_directory()
    
    # Generate all datasets
    customers_df = generate_customer_profiles(CONFIG['num_customers'])
    interactions_df = generate_customer_interactions(customers_df, CONFIG['num_interactions'])
    campaigns_df = generate_campaign_history(CONFIG['num_campaigns'])
    products_df = generate_product_catalog(CONFIG['num_products'])
    trends_df = generate_issue_trends(interactions_df)
    mapping_df = generate_campaign_customer_mapping(campaigns_df, customers_df, interactions_df)
    
    # Generate summary report
    print("\n" + "="*60)
    print("✅ DATA GENERATION COMPLETE!")
    print("="*60)
    print(f"\n📁 All files saved in '{CONFIG['output_dir']}/' directory:")
    print(f"   1. customer_profiles.csv          ({len(customers_df)} records)")
    print(f"   2. customer_interactions.csv      ({len(interactions_df)} records)")
    print(f"   3. campaign_history.csv           ({len(campaigns_df)} records)")
    print(f"   4. product_catalog.csv            ({len(products_df)} records)")
    print(f"   5. issue_trends.csv               ({len(trends_df)} records)")
    print(f"   6. campaign_customer_mapping.csv  ({len(mapping_df)} records)")
    
    # Create data summary JSON
    summary = {
        'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_customers': len(customers_df),
        'total_interactions': len(interactions_df),
        'total_campaigns': len(campaigns_df),
        'total_products': len(products_df),
        'date_range': {
            'start': interactions_df['date'].min(),
            'end': interactions_df['date'].max()
        },
        'category_distribution': interactions_df['category'].value_counts().to_dict(),
        'sentiment_distribution': interactions_df['sentiment'].value_counts().to_dict(),
        'churn_risk_distribution': interactions_df['churn_risk'].value_counts().to_dict(),
        'operator_distribution': customers_df['operator'].value_counts().to_dict(),
        'geography_distribution': customers_df['geography'].value_counts().head(10).to_dict()
    }
    
    with open(f"{CONFIG['output_dir']}/dataset_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n📊 Dataset summary saved to '{CONFIG['output_dir']}/dataset_summary.json'")
    
    print("\n" + "="*60)
    print("🎉 Ready to use! Start building your project now!")
    print("="*60)
    
    return {
        'customers': customers_df,
        'interactions': interactions_df,
        'campaigns': campaigns_df,
        'products': products_df,
        'trends': trends_df,
        'mapping': mapping_df
    }

if __name__ == "__main__":
    datasets = main()