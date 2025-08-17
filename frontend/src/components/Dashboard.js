import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [stats, setStats] = useState({
    trendsMonitored: 0,
    contentGenerated: 0,
    postsPublished: 0,
    engagementRate: 0
  });
  const [recentTrends, setRecentTrends] = useState([]);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Fetch trends
      const trendsResponse = await axios.get('/api/v1/trends?limit=5');
      setRecentTrends(trendsResponse.data);
      
      // TODO: Fetch other dashboard stats
      setStats({
        trendsMonitored: trendsResponse.data.length,
        contentGenerated: 12,
        postsPublished: 8,
        engagementRate: 4.2
      });
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  return (
    <div className="dashboard">
      <h1>Based Labs Content Pipeline</h1>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Trends Monitored</h3>
          <p className="stat-number">{stats.trendsMonitored}</p>
        </div>
        <div className="stat-card">
          <h3>Content Generated</h3>
          <p className="stat-number">{stats.contentGenerated}</p>
        </div>
        <div className="stat-card">
          <h3>Posts Published</h3>
          <p className="stat-number">{stats.postsPublished}</p>
        </div>
        <div className="stat-card">
          <h3>Engagement Rate</h3>
          <p className="stat-number">{stats.engagementRate}%</p>
        </div>
      </div>

      <div className="recent-trends">
        <h2>Recent Trend Opportunities</h2>
        <div className="trends-list">
          {recentTrends.map((trend) => (
            <div key={trend.id} className="trend-item">
              <h4>{trend.title}</h4>
              <p>{trend.description}</p>
              <div className="trend-meta">
                <span className="source">Source: {trend.source}</span>
                <span className="score">Score: {trend.score.toFixed(2)}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;