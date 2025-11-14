import React, { useState, useEffect } from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Search, TrendingUp, Users, AlertCircle, Phone, Mail, MapPin, Calendar, ChevronRight, BarChart3, Filter, Download, RefreshCw, MessageSquare, Zap, Target } from 'lucide-react';
import './App.css';

const API_URL = 'http://localhost:8000';

const COLORS = ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#06b6d4', '#ef4444'];

const App = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [stats, setStats] = useState(null);
  const [topIssues, setTopIssues] = useState([]);
  const [campaigns, setCampaigns] = useState([]);
  const [leads, setLeads] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('internet_connectivity');
  const [query, setQuery] = useState('');
  const [queryResult, setQueryResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [topics, setTopics] = useState([]);

  useEffect(() => {
    fetchStats();
    fetchTopIssues();
    fetchCampaigns();
    fetchTopics();
  }, []);

  useEffect(() => {
    if (selectedCategory) {
      fetchLeads(selectedCategory);
    }
  }, [selectedCategory]);

  const fetchStats = async () => {
    try {
      const response = await fetch(`${API_URL}/stats`);
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const fetchTopIssues = async () => {
    try {
      const response = await fetch(`${API_URL}/top-issues?limit=10`);
      const data = await response.json();
      setTopIssues(data);
      if (data.length > 0) {
        setSelectedCategory(data[0].category);
      }
    } catch (error) {
      console.error('Error fetching issues:', error);
    }
  };

  const fetchCampaigns = async () => {
    try {
      const response = await fetch(`${API_URL}/campaigns`);
      const data = await response.json();
      setCampaigns(data.slice(0, 6));
    } catch (error) {
      console.error('Error fetching campaigns:', error);
    }
  };

  const fetchLeads = async (category) => {
    try {
      const response = await fetch(`${API_URL}/leads/${category}?limit=30`);
      const data = await response.json();
      setLeads(data);
    } catch (error) {
      console.error('Error fetching leads:', error);
    }
  };

  const fetchTopics = async () => {
    try {
      const response = await fetch(`${API_URL}/topic-modeling?sample_size=100`);
      const data = await response.json();
      if (data.topics) {
        setTopics(data.topics);
      }
    } catch (error) {
      console.error('Error fetching topics:', error);
    }
  };

  const handleQuery = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: query, max_context_rows: 50 })
      });
      const data = await response.json();
      setQueryResult(data);
    } catch (error) {
      console.error('Error querying:', error);
    } finally {
      setLoading(false);
    }
  };

  const StatCard = ({ title, value, icon: Icon, trend, color }) => (
    <div className="stat-card" style={{ borderColor: color }}>
      <div className="stat-card-content">
        <div>
          <p className="stat-title">{title}</p>
          <h3 className="stat-value" style={{ color }}>{value}</h3>
          {trend && (
            <p className="stat-trend">
              <TrendingUp className="icon-sm" />
              {trend}
            </p>
          )}
        </div>
        <div className="stat-icon-wrapper">
          <Icon className="stat-icon" style={{ color }} />
        </div>
      </div>
    </div>
  );

  const DashboardView = () => {
    if (!stats) return (
      <div className="loading-container">
        <RefreshCw className="loading-spinner" />
      </div>
    );

    const categoryData = Object.entries(stats.by_category).map(([name, value]) => ({
      name: name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
      value
    }));

    const sentimentData = Object.entries(stats.by_sentiment).map(([name, value]) => ({
      name: name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
      value
    }));

    const churnData = Object.entries(stats.by_churn_risk).map(([name, value]) => ({
      name: name.charAt(0).toUpperCase() + name.slice(1),
      value
    }));

    return (
      <div className="view-container">
        {/* Header */}
        <div className="header-banner">
          <h1 className="header-title">Smart Campaign Targeting</h1>
          <p className="header-subtitle">AI-Powered Telecom Customer Intelligence Platform</p>
        </div>

        {/* Key Metrics */}
        <div className="stats-grid">
          <StatCard
            title="Total Interactions"
            value={stats.total_interactions.toLocaleString()}
            icon={MessageSquare}
            trend="+12% this month"
            color="#3b82f6"
          />
          <StatCard
            title="Active Customers"
            value={stats.total_customers.toLocaleString()}
            icon={Users}
            trend="3K+ unique users"
            color="#8b5cf6"
          />
          <StatCard
            title="Critical Issues"
            value={stats.unresolved_count.toLocaleString()}
            icon={AlertCircle}
            trend="Requires attention"
            color="#ef4444"
          />
          <StatCard
            title="Avg Resolution Time"
            value={`${stats.avg_resolution_time.toFixed(1)}h`}
            icon={Zap}
            trend="Below target"
            color="#10b981"
          />
        </div>

        {/* Charts Row */}
        <div className="charts-grid">
          {/* Category Distribution */}
          <div className="card">
            <h3 className="card-title">
              <BarChart3 className="icon-md text-blue" />
              Top Issue Categories
            </h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={categoryData.slice(0, 7)}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} fontSize={12} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#3b82f6" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Sentiment Distribution */}
          <div className="card">
            <h3 className="card-title">
              <Target className="icon-md text-purple" />
              Sentiment Analysis
            </h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={sentimentData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {sentimentData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Churn Risk Distribution */}
        <div className="card">
          <h3 className="card-title">
            <AlertCircle className="icon-md text-red" />
            Churn Risk Distribution
          </h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={churnData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="name" type="category" />
              <Tooltip />
              <Bar dataKey="value" fill="#ec4899" radius={[0, 8, 8, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Top Issues Table */}
        <div className="card">
          <h3 className="card-title">Top Customer Issues</h3>
          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Category</th>
                  <th>Count</th>
                  <th>% of Total</th>
                  <th>Avg Churn Score</th>
                  <th>High Risk</th>
                </tr>
              </thead>
              <tbody>
                {topIssues.slice(0, 5).map((issue, idx) => (
                  <tr key={idx}>
                    <td>
                      <span className="font-medium">
                        {issue.category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      </span>
                    </td>
                    <td>{issue.count}</td>
                    <td>
                      <span className="badge badge-blue">
                        {issue.percentage}%
                      </span>
                    </td>
                    <td>
                      <span className={`font-semibold ${
                        issue.avg_churn_score > 0.7 ? 'text-red' : 
                        issue.avg_churn_score > 0.5 ? 'text-orange' : 'text-green'
                      }`}>
                        {issue.avg_churn_score}
                      </span>
                    </td>
                    <td>
                      <span className="badge badge-red">
                        {issue.high_churn_count}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
  };

  const LeadsView = () => (
    <div className="view-container">
      <div className="card">
        <div className="card-header">
          <h2 className="card-title-large">
            <Target className="icon-lg text-blue" />
            High-Value Lead Generation
          </h2>
          <div className="button-group">
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="select-input"
            >
              {topIssues.map((issue) => (
                <option key={issue.category} value={issue.category}>
                  {issue.category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </option>
              ))}
            </select>
            <button className="btn btn-primary">
              <Download className="icon-sm" />
              Export
            </button>
          </div>
        </div>

        <div className="leads-grid">
          {leads.map((lead, idx) => (
            <div key={idx} className="lead-card">
              <div className="lead-content">
                <div className="lead-info">
                  <div className="lead-header">
                    <h4 className="lead-name">{lead.customer_name}</h4>
                    <span className={`badge ${
                      lead.churn_risk === 'critical' ? 'badge-red' :
                      lead.churn_risk === 'high' ? 'badge-orange' :
                      'badge-yellow'
                    }`}>
                      {lead.churn_risk.toUpperCase()} RISK
                    </span>
                    <span className="lead-id">{lead.customer_id}</span>
                  </div>
                  
                  <p className="lead-summary">{lead.issue_summary}</p>
                  
                  <div className="lead-details">
                    <span className="detail-item">
                      <MapPin className="icon-sm" />
                      {lead.geography}
                    </span>
                    <span className="detail-item">
                      <Phone className="icon-sm" />
                      {lead.operator}
                    </span>
                    <span className="detail-item">
                      <Calendar className="icon-sm" />
                      {lead.tenure_months} months tenure
                    </span>
                    <span className="detail-item detail-price">
                      ₹{lead.current_plan_value}/month
                    </span>
                  </div>
                </div>
                
                <div className="lead-action">
                  <div className="churn-score">
                    {(lead.churn_score * 100).toFixed(0)}%
                  </div>
                  <button className="btn btn-gradient">
                    Target
                    <ChevronRight className="icon-sm" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const CampaignsView = () => (
    <div className="view-container">
      <div className="card">
        <h2 className="card-title-large">
          <Zap className="icon-lg text-purple" />
          Campaign Performance
        </h2>
        
        <div className="campaigns-grid">
          {campaigns.map((campaign, idx) => (
            <div key={idx} className="campaign-card">
              <div className="campaign-header">
                <div>
                  <h3 className="campaign-name">{campaign.campaign_name}</h3>
                  <div className="campaign-meta">
                    <span className="badge badge-purple">
                      {campaign.campaign_type}
                    </span>
                    <span className="campaign-date">{campaign.start_date} to {campaign.end_date}</span>
                    <span className={`badge ${
                      campaign.status === 'Active' ? 'badge-green' : 'badge-gray'
                    }`}>
                      {campaign.status}
                    </span>
                  </div>
                </div>
                <div className="campaign-roi">
                  <div className="roi-value">
                    {campaign.roi > 0 ? '+' : ''}{(campaign.roi * 100).toFixed(0)}%
                  </div>
                  <p className="roi-label">ROI</p>
                </div>
              </div>

              <div className="campaign-metrics">
                <div className="metric-box metric-blue">
                  <div className="metric-value">{campaign.total_targeted}</div>
                  <div className="metric-label">Targeted</div>
                </div>
                <div className="metric-box metric-indigo">
                  <div className="metric-value">{campaign.total_contacted}</div>
                  <div className="metric-label">Contacted</div>
                </div>
                <div className="metric-box metric-purple">
                  <div className="metric-value">{campaign.total_responded}</div>
                  <div className="metric-label">Responded</div>
                </div>
                <div className="metric-box metric-green">
                  <div className="metric-value">{campaign.total_converted}</div>
                  <div className="metric-label">Converted</div>
                </div>
                <div className="metric-box metric-emerald">
                  <div className="metric-value">₹{(campaign.revenue_generated / 1000).toFixed(0)}K</div>
                  <div className="metric-label">Revenue</div>
                </div>
              </div>

              <div className="campaign-footer">
                <div className="campaign-rates">
                  <span className="rate-item">
                    Conversion: <span className="rate-value">{campaign.conversion_rate}%</span>
                  </span>
                  <span className="rate-item">
                    Response: <span className="rate-value">{campaign.response_rate}%</span>
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const AnalyticsView = () => (
    <div className="view-container">
      <div className="card">
        <h2 className="card-title-large">
          <Search className="icon-lg text-blue" />
          AI-Powered Query Engine
        </h2>
        
        <div className="query-section">
          <div className="query-input-group">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleQuery()}
              placeholder="Ask anything about your customer data... (e.g., 'Which customers are most likely to churn?')"
              className="query-input"
            />
            <button
              onClick={handleQuery}
              disabled={loading}
              className="btn btn-gradient"
            >
              {loading ? <RefreshCw className="icon-md loading-spinner" /> : <Search className="icon-md" />}
              Analyze
            </button>
          </div>
          
          {/* Sample Questions */}
          <div style={{ marginTop: '1rem', display: 'flex', flexWrap: 'wrap', gap: '0.5rem', alignItems: 'center' }}>
            <span style={{ fontSize: '0.875rem', color: '#6b7280' }}>Try:</span>
            {[
              'Which customers are at high churn risk?',
              'What are the top complaint categories?',
              'Show me billing issue trends in Delhi'
            ].map((q, i) => (
              <button
                key={i}
                onClick={() => setQuery(q)}
                style={{
                  fontSize: '0.875rem',
                  padding: '0.25rem 0.75rem',
                  background: '#f3f4f6',
                  color: '#374151',
                  borderRadius: '9999px',
                  border: 'none',
                  cursor: 'pointer',
                  transition: 'background 0.2s'
                }}
                onMouseEnter={(e) => e.target.style.background = '#e5e7eb'}
                onMouseLeave={(e) => e.target.style.background = '#f3f4f6'}
              >
                {q}
              </button>
            ))}
          </div>
        </div>

        {/* Conversational AI Response */}
        {queryResult && queryResult.conversational && (
          <div style={{
            background: 'white',
            borderRadius: '1rem',
            padding: '2rem',
            marginTop: '1.5rem',
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
            animation: 'fadeIn 0.5s ease-out'
          }}>
            <div style={{ display: 'flex', alignItems: 'start', gap: '1rem', marginBottom: '1.5rem' }}>
              <div style={{
                width: '2.5rem',
                height: '2.5rem',
                background: 'linear-gradient(to bottom right, #3b82f6, #8b5cf6)',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                flexShrink: 0
              }}>
                <Zap style={{ width: '1.25rem', height: '1.25rem', color: 'white' }} />
              </div>
              <div style={{ flex: 1 }}>
                <h3 style={{ fontSize: '1.25rem', fontWeight: 600, color: '#111827', marginBottom: '0.25rem' }}>
                  AI Analysis
                </h3>
                <p style={{ fontSize: '0.875rem', color: '#6b7280' }}>
                  Generated insights from your customer data
                </p>
              </div>
            </div>

            {/* Render Conversational Response */}
            <div style={{ lineHeight: '1.75', color: '#374151' }}>
              {queryResult.answer.split('\n\n').map((paragraph, idx) => {
                // Check if it's a header (starts with **)
                if (paragraph.startsWith('**') && paragraph.includes(':**')) {
                  return (
                    <h3 key={idx} style={{
                      fontSize: '1.125rem',
                      fontWeight: 600,
                      color: '#111827',
                      marginTop: '1.5rem',
                      marginBottom: '0.75rem',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.5rem'
                    }}>
                      <TrendingUp style={{ width: '1.25rem', height: '1.25rem', color: '#3b82f6' }} />
                      {paragraph.replace(/\*\*/g, '').replace(':', '')}
                    </h3>
                  );
                }
                
                // Check if it's a numbered recommendation
                if (/^\d+\./.test(paragraph)) {
                  const [number, ...rest] = paragraph.split('.');
                  const content = rest.join('.').trim();
                  const [title, ...description] = content.split(':');
                  
                  return (
                    <div key={idx} style={{
                      background: 'linear-gradient(to right, #eff6ff, #f3e8ff)',
                      borderLeft: '4px solid #3b82f6',
                      padding: '1rem',
                      marginTop: '1rem',
                      marginBottom: '1rem',
                      borderRadius: '0 0.5rem 0.5rem 0'
                    }}>
                      <div style={{ display: 'flex', alignItems: 'start', gap: '0.75rem' }}>
                        <div style={{
                          width: '2rem',
                          height: '2rem',
                          background: '#3b82f6',
                          color: 'white',
                          borderRadius: '50%',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          fontWeight: 700,
                          flexShrink: 0
                        }}>
                          {number}
                        </div>
                        <div>
                          <h4 style={{ fontWeight: 600, color: '#111827', marginBottom: '0.25rem' }}>
                            {title.replace(/\*\*/g, '')}
                          </h4>
                          <p style={{ color: '#374151', fontSize: '0.875rem', lineHeight: '1.5', margin: 0 }}>
                            {description.join(':').trim()}
                          </p>
                        </div>
                      </div>
                    </div>
                  );
                }
                
                // Regular paragraph - handle bold text
                return (
                  <p key={idx} style={{ marginBottom: '1rem', lineHeight: '1.75' }}>
                    {paragraph.split('**').map((part, i) => 
                      i % 2 === 0 ? part : <strong key={i} style={{ color: '#111827', fontWeight: 600 }}>{part}</strong>
                    )}
                  </p>
                );
              })}
            </div>

            {/* Action Buttons */}
            <div style={{ marginTop: '1.5rem', display: 'flex', gap: '0.75rem' }}>
              <button className="btn btn-primary" style={{ flex: 1 }}>
                <Download className="icon-sm" />
                Export Analysis
              </button>
              <button 
                className="btn" 
                style={{ flex: 1, background: '#f3f4f6', color: '#374151' }}
                onClick={() => setQuery('')}
              >
                Ask Another Question
              </button>
            </div>
          </div>
        )}

        {/* Legacy Response Format (for non-conversational responses) */}
        {queryResult && !queryResult.conversational && (
          <div className="query-results">
            <div className="result-box result-blue">
              <h3 className="result-title">Answer</h3>
              <p className="result-text">{queryResult.answer}</p>
            </div>

            {queryResult.insights && queryResult.insights.length > 0 && (
              <div className="result-box result-green">
                <h3 className="result-title">Key Insights</h3>
                <ul className="result-list">
                  {queryResult.insights.map((insight, idx) => (
                    <li key={idx} className="result-item">
                      <span className="bullet-green">•</span>
                      {insight}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {queryResult.recommendations && queryResult.recommendations.length > 0 && (
              <div className="result-box result-purple">
                <h3 className="result-title">Recommendations</h3>
                <ul className="result-list">
                  {queryResult.recommendations.map((rec, idx) => (
                    <li key={idx} className="result-item">
                      <span className="bullet-purple">→</span>
                      {rec}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* Empty State */}
        {!queryResult && !loading && (
          <div style={{
            background: 'white',
            borderRadius: '1rem',
            padding: '3rem',
            textAlign: 'center',
            marginTop: '1.5rem',
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)'
          }}>
            <div style={{
              width: '4rem',
              height: '4rem',
              background: '#eff6ff',
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto 1rem'
            }}>
              <AlertCircle style={{ width: '2rem', height: '2rem', color: '#3b82f6' }} />
            </div>
            <h3 style={{ fontSize: '1.25rem', fontWeight: 600, color: '#111827', marginBottom: '0.5rem' }}>
              Ready to analyze your data
            </h3>
            <p style={{ color: '#6b7280' }}>
              Ask a question about your customers, campaigns, or churn risk to get started
            </p>
          </div>
        )}
      </div>

      {/* Topic Modeling */}
      {topics.length > 0 && (
        <div className="card">
          <h2 className="card-title-large">AI-Discovered Topics</h2>
          <div className="topics-grid">
            {topics.map((topic, idx) => (
              <div key={idx} className="topic-card">
                <div className="topic-header">
                  <h4 className="topic-title">{topic.topic}</h4>
                  <span className={`badge ${
                    topic.severity === 'critical' ? 'badge-red' :
                    topic.severity === 'high' ? 'badge-orange' :
                    topic.severity === 'medium' ? 'badge-yellow' :
                    'badge-green'
                  }`}>
                    {topic.severity}
                  </span>
                </div>
                <p className="topic-description">{topic.description}</p>
                <div className="topic-progress">
                  <div className="progress-bar">
                    <div
                      className="progress-fill"
                      style={{ width: `${topic.percentage}%` }}
                    />
                  </div>
                  <span className="progress-label">{topic.percentage}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );

  return (
    <div className="app">
      {/* Navigation */}
      <nav className="navbar">
        <div className="nav-container">
          <div className="nav-brand">
            <div className="brand-icon">
              <Zap className="icon-md brand-icon-svg" />
            </div>
            <div>
              <h1 className="brand-title">TelecomAI</h1>
              <p className="brand-subtitle">Campaign Intelligence Platform</p>
            </div>
          </div>
          
          <div className="nav-tabs">
            {['dashboard', 'leads', 'campaigns', 'analytics'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`nav-tab ${activeTab === tab ? 'nav-tab-active' : ''}`}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="main-content">
        {activeTab === 'dashboard' && <DashboardView />}
        {activeTab === 'leads' && <LeadsView />}
        {activeTab === 'campaigns' && <CampaignsView />}
        {activeTab === 'analytics' && <AnalyticsView />}
      </main>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <p>© 2025 TelecomAI - Smart Campaign Targeting Platform | Powered by AI & Data Analytics</p>
        </div>
      </footer>
    </div>
  );
};

export default App;