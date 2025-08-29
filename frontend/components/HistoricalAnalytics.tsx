'use client';

import React, { useState, useEffect } from 'react';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface HistoricalAnalyticsProps {
  userId: string;
  username: string;
  platform: string;
}

interface GrowthAnalytics {
  followers_start: number;
  followers_end: number;
  net_growth: number;
  growth_rate: number;
  avg_daily_growth: number;
  followers_gained?: number;
  followers_lost?: number;
}

interface ChartDataPoint {
  extracted_at: string;
  follower_count: number;
  following_count: number;
  like_count: number;
  date_label?: string;
}

const MetricCard: React.FC<{
  title: string;
  value: number | string;
  change?: string;
  positive?: boolean;
  suffix?: string;
  icon?: React.ReactNode;
}> = ({ title, value, change, positive, suffix, icon }) => (
  <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm font-medium text-gray-600">{title}</p>
        <p className="text-2xl font-bold text-gray-900">
          {typeof value === 'number' ? value.toLocaleString() : value}
          {suffix && <span className="text-sm text-gray-500 ml-1">{suffix}</span>}
        </p>
        {change && (
          <p className={`text-sm ${positive ? 'text-green-600' : 'text-red-600'} flex items-center`}>
            {positive ? '↗' : '↘'} {change}
          </p>
        )}
      </div>
      {icon && (
        <div className="flex-shrink-0">
          {icon}
        </div>
      )}
    </div>
  </div>
);

const HistoricalAnalytics: React.FC<HistoricalAnalyticsProps> = ({ userId, username, platform }) => {
  const [analyticsData, setAnalyticsData] = useState<GrowthAnalytics | null>(null);
  const [chartData, setChartData] = useState<ChartDataPoint[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [timeRange, setTimeRange] = useState(30);
  const [lastExtraction, setLastExtraction] = useState<string | null>(null);

  useEffect(() => {
    fetchAnalytics();
  }, [timeRange, username]);

  const fetchAnalytics = async () => {
    if (!userId || !username) return;
    
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`http://localhost:8000/tiktok/analytics/${userId}/${username}?days=${timeRange}`);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      
      if (data.analytics && data.analytics.success) {
        setAnalyticsData(data.analytics.analytics);
      }
      
      if (data.chart_data && data.chart_data.success) {
        const processedData = data.chart_data.chart_data.map((point: ChartDataPoint) => ({
          ...point,
          date_label: new Date(point.extracted_at).toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric'
          })
        }));
        setChartData(processedData);
      }
      
    } catch (error) {
      console.error('Analytics fetch error:', error);
      setError('Failed to load analytics data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const extractData = async (includeFollowers: boolean = false) => {
    setLoading(true);
    
    try {
      const response = await fetch('http://localhost:8000/tiktok/extract-comprehensive', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          username: username,
          include_followers: includeFollowers,
          follower_limit: includeFollowers ? 100 : 0
        })
      });

      if (response.ok) {
        const result = await response.json();
        setLastExtraction(new Date().toISOString());
        
        // Refresh analytics after extraction
        setTimeout(() => fetchAnalytics(), 2000);
        
        alert(`✅ Data extraction completed successfully!${includeFollowers ? ' Including follower analysis.' : ''}`);
      } else {
        throw new Error(`Extraction failed: ${response.statusText}`);
      }
    } catch (error) {
      console.error('Extraction error:', error);
      alert('❌ Data extraction failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (loading && !analyticsData) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span className="ml-3 text-gray-600">Loading analytics...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header with Controls */}
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">Growth Analytics</h3>
          <p className="text-gray-600">@{username} • {platform}</p>
        </div>
        
        <div className="flex items-center space-x-4">
          {/* Time Range Selector */}
          <div className="flex space-x-2">
            {[7, 30, 90].map(days => (
              <button
                key={days}
                onClick={() => setTimeRange(days)}
                className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
                  timeRange === days 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {days}d
              </button>
            ))}
          </div>

          {/* Data Collection Buttons */}
          <button
            onClick={() => extractData(false)}
            disabled={loading}
            className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50 transition-colors flex items-center gap-2"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Collect Profile Data
          </button>

          <button
            onClick={() => extractData(true)}
            disabled={loading}
            className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 disabled:opacity-50 transition-colors flex items-center gap-2"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            Full Analysis
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex">
            <svg className="h-5 w-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div className="ml-3">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Growth Metrics Cards */}
      {analyticsData && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <MetricCard
            title="Followers Gained"
            value={analyticsData.net_growth || 0}
            change={`${analyticsData.growth_rate || 0}%`}
            positive={(analyticsData.net_growth || 0) > 0}
            icon={
              <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
            }
          />
          
          <MetricCard
            title="Daily Average"
            value={Math.round(analyticsData.avg_daily_growth || 0)}
            suffix="per day"
            positive={(analyticsData.avg_daily_growth || 0) > 0}
            icon={
              <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            }
          />
          
          <MetricCard
            title="Growth Rate"
            value={`${analyticsData.growth_rate || 0}%`}
            positive={(analyticsData.growth_rate || 0) > 0}
            icon={
              <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
            }
          />
          
          <MetricCard
            title="Total Followers"
            value={analyticsData.followers_end || 0}
            change={`from ${analyticsData.followers_start || 0}`}
            icon={
              <div className="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
                <svg className="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 515.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
            }
          />
        </div>
      )}

      {/* Growth Chart */}
      {chartData.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
          <h4 className="text-lg font-semibold mb-4">Follower Growth Over Time</h4>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis 
                dataKey="date_label" 
                tick={{ fontSize: 12 }}
                stroke="#666"
              />
              <YAxis 
                tick={{ fontSize: 12 }}
                stroke="#666"
              />
              <Tooltip 
                contentStyle={{
                  backgroundColor: '#fff',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                }}
              />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="follower_count" 
                stroke="#3b82f6" 
                strokeWidth={3}
                dot={{ fill: '#3b82f6', strokeWidth: 2, r: 4 }}
                name="Followers"
              />
              <Line 
                type="monotone" 
                dataKey="following_count" 
                stroke="#10b981" 
                strokeWidth={2}
                dot={{ fill: '#10b981', strokeWidth: 2, r: 3 }}
                name="Following"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Engagement Trends */}
      {chartData.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
          <h4 className="text-lg font-semibold mb-4">Engagement Trends</h4>
          <ResponsiveContainer width="100%" height={250}>
            <AreaChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis 
                dataKey="date_label" 
                tick={{ fontSize: 12 }}
                stroke="#666"
              />
              <YAxis 
                tick={{ fontSize: 12 }}
                stroke="#666"
              />
              <Tooltip 
                contentStyle={{
                  backgroundColor: '#fff',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                }}
                formatter={(value: number) => [value.toLocaleString(), 'Total Likes']}
              />
              <Area 
                type="monotone" 
                dataKey="like_count" 
                stackId="1" 
                stroke="#f59e0b" 
                fill="#fbbf24" 
                fillOpacity={0.6}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Data Status */}
      <div className="bg-gray-50 p-4 rounded-lg">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-600">
              {chartData.length > 0 
                ? `Showing ${chartData.length} data points over ${timeRange} days`
                : 'No historical data available yet'
              }
            </p>
            {lastExtraction && (
              <p className="text-xs text-gray-500">
                Last extraction: {new Date(lastExtraction).toLocaleString()}
              </p>
            )}
          </div>
          
          {chartData.length === 0 && (
            <button
              onClick={() => extractData(false)}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm"
            >
              Start Collecting Data
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default HistoricalAnalytics;
