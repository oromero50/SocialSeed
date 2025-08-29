'use client';

import React, { useState, useEffect } from 'react';

interface TikTokAccount {
  id: string;
  username: string;
  display_name?: string;
  follower_count: number;
  following_count: number;
  engagement_rate: number;
  is_active: boolean;
  last_sync?: string;
  growth_potential?: string;
}

interface TikTokAnalytics {
  followers_gained_today: number;
  followers_lost_today: number;
  net_growth: number;
  engagement_rate: number;
  recent_unfollowers: Array<{
    username: string;
    display_name: string;
    unfollowed_at: string;
  }>;
  growth_history: Array<{
    followers: number;
    following: number;
    date: string;
  }>;
}

interface TikTokSectionProps {
  accounts: TikTokAccount[];
  onAddAccount: () => void;
  onRefreshData: (username: string) => void;
}

export default function TikTokSection({ accounts, onAddAccount, onRefreshData }: TikTokSectionProps) {
  const [analytics, setAnalytics] = useState<{[username: string]: TikTokAnalytics}>({});
  const [isLoadingAnalytics, setIsLoadingAnalytics] = useState<{[username: string]: boolean}>({});
  const [expandedAccount, setExpandedAccount] = useState<string | null>(null);

  const loadAnalytics = async (username: string) => {
    setIsLoadingAnalytics(prev => ({ ...prev, [username]: true }));
    
    try {
      const response = await fetch(`http://localhost:8000/tiktok-analytics/${username}`);
      if (response.ok) {
        const data = await response.json();
        setAnalytics(prev => ({ ...prev, [username]: data }));
      } else {
        console.error('Failed to load analytics for', username);
      }
    } catch (error) {
      console.error('Error loading analytics:', error);
    } finally {
      setIsLoadingAnalytics(prev => ({ ...prev, [username]: false }));
    }
  };

  const collectData = async (username: string, msToken: string) => {
    try {
      const response = await fetch('http://localhost:8000/collect-tiktok-data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, ms_token: msToken })
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log('✅ Data collected:', data);
        onRefreshData(username);
        await loadAnalytics(username);
      } else {
        const error = await response.text();
        console.error('Data collection failed:', error);
      }
    } catch (error) {
      console.error('Error collecting data:', error);
    }
  };

  const detectUnfollowers = async (username: string) => {
    try {
      const response = await fetch(`http://localhost:8000/detect-unfollowers/${username}`, {
        method: 'POST'
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log('🔍 Unfollower detection results:', data);
        await loadAnalytics(username);
      }
    } catch (error) {
      console.error('Error detecting unfollowers:', error);
    }
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  };

  const getGrowthColor = (growth: number) => {
    if (growth > 0) return 'text-green-600';
    if (growth < 0) return 'text-red-600';
    return 'text-gray-600';
  };

  const getEngagementColor = (rate: number) => {
    if (rate >= 5) return 'text-green-600';
    if (rate >= 2) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getPotentialBadge = (potential: string) => {
    const colors = {
      High: 'bg-green-100 text-green-800',
      Medium: 'bg-yellow-100 text-yellow-800',
      Low: 'bg-red-100 text-red-800'
    };
    return colors[potential as keyof typeof colors] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 bg-gradient-to-r from-pink-500 to-purple-600 rounded-lg flex items-center justify-center">
            <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 24 24">
              <path d="M19.589 6.686a4.793 4.793 0 01-3.77-4.245V2h-3.445v13.672a2.896 2.896 0 01-2.909 2.909 2.896 2.896 0 01-2.909-2.909 2.896 2.896 0 012.909-2.909c.301 0 .591.041.864.119V9.438a6.331 6.331 0 00-.864-.058A6.448 6.448 0 003 15.672a6.448 6.448 0 006.465 6.421 6.448 6.448 0 006.465-6.421V8.55a8.282 8.282 0 004.659 1.453V6.686c-.016.003-.039.009-.055.009z"/>
            </svg>
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900">TikTok Accounts</h2>
            <p className="text-gray-500">{accounts.length} connected account{accounts.length !== 1 ? 's' : ''}</p>
          </div>
        </div>
        
        <button
          onClick={onAddAccount}
          className="bg-gradient-to-r from-pink-500 to-purple-600 text-white px-6 py-3 rounded-lg font-medium hover:from-pink-600 hover:to-purple-700 transition-all transform hover:scale-105 shadow-lg flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Add TikTok Account
        </button>
      </div>

      {accounts.length === 0 ? (
        <div className="text-center py-12 border-2 border-dashed border-gray-300 rounded-lg">
          <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No TikTok accounts connected</h3>
          <p className="text-gray-500 mb-4">Connect your first TikTok account to start tracking followers and growth</p>
          <button
            onClick={onAddAccount}
            className="bg-pink-600 text-white px-6 py-2 rounded-lg hover:bg-pink-700 transition-colors"
          >
            Connect TikTok Account
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {accounts.map(account => (
            <div key={account.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-gradient-to-r from-pink-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-lg">
                    {account.username.charAt(0).toUpperCase()}
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">@{account.username}</h3>
                    {account.display_name && (
                      <p className="text-gray-500 text-sm">{account.display_name}</p>
                    )}
                    <div className="flex items-center space-x-4 mt-1">
                      <span className="text-sm text-gray-600">
                        <span className="font-medium">{formatNumber(account.follower_count)}</span> followers
                      </span>
                      <span className="text-sm text-gray-600">
                        <span className="font-medium">{formatNumber(account.following_count)}</span> following
                      </span>
                      <span className={`text-sm font-medium ${getEngagementColor(account.engagement_rate)}`}>
                        {account.engagement_rate}% engagement
                      </span>
                      {account.growth_potential && (
                        <span className={`text-xs px-2 py-1 rounded-full font-medium ${getPotentialBadge(account.growth_potential)}`}>
                          {account.growth_potential} Growth
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  <div className={`w-3 h-3 rounded-full ${account.is_active ? 'bg-green-500' : 'bg-red-500'}`}></div>
                  <span className="text-sm text-gray-500">
                    {account.is_active ? 'Active' : 'Inactive'}
                  </span>
                  
                  <button
                    onClick={() => loadAnalytics(account.username)}
                    disabled={isLoadingAnalytics[account.username]}
                    className="bg-blue-100 text-blue-700 px-3 py-1 rounded-lg text-sm hover:bg-blue-200 transition-colors disabled:opacity-50"
                  >
                    {isLoadingAnalytics[account.username] ? 'Loading...' : 'Analytics'}
                  </button>
                  
                  <button
                    onClick={() => detectUnfollowers(account.username)}
                    className="bg-red-100 text-red-700 px-3 py-1 rounded-lg text-sm hover:bg-red-200 transition-colors"
                  >
                    Unfollowers
                  </button>

                  <button
                    onClick={() => setExpandedAccount(expandedAccount === account.id ? null : account.id)}
                    className="bg-gray-100 text-gray-700 px-3 py-1 rounded-lg text-sm hover:bg-gray-200 transition-colors"
                  >
                    {expandedAccount === account.id ? 'Collapse' : 'Expand'}
                  </button>
                </div>
              </div>

              {expandedAccount === account.id && (
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
                    <div className="bg-gradient-to-r from-blue-50 to-blue-100 p-4 rounded-lg">
                      <h4 className="text-sm font-medium text-blue-800">Followers</h4>
                      <p className="text-2xl font-bold text-blue-900">{formatNumber(account.follower_count)}</p>
                    </div>
                    <div className="bg-gradient-to-r from-green-50 to-green-100 p-4 rounded-lg">
                      <h4 className="text-sm font-medium text-green-800">Following</h4>
                      <p className="text-2xl font-bold text-green-900">{formatNumber(account.following_count)}</p>
                    </div>
                    <div className="bg-gradient-to-r from-purple-50 to-purple-100 p-4 rounded-lg">
                      <h4 className="text-sm font-medium text-purple-800">Engagement</h4>
                      <p className="text-2xl font-bold text-purple-900">{account.engagement_rate}%</p>
                    </div>
                    <div className="bg-gradient-to-r from-orange-50 to-orange-100 p-4 rounded-lg">
                      <h4 className="text-sm font-medium text-orange-800">Ratio</h4>
                      <p className="text-2xl font-bold text-orange-900">
                        {account.following_count > 0 ? (account.follower_count / account.following_count).toFixed(1) : '∞'}
                      </p>
                    </div>
                  </div>

                  {analytics[account.username] && (
                    <div className="space-y-4">
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <h4 className="font-medium text-gray-900 mb-3">Today's Activity</h4>
                        <div className="grid grid-cols-3 gap-4">
                          <div className="text-center">
                            <p className="text-2xl font-bold text-green-600">
                              +{analytics[account.username].followers_gained_today || 0}
                            </p>
                            <p className="text-sm text-gray-600">New Followers</p>
                          </div>
                          <div className="text-center">
                            <p className="text-2xl font-bold text-red-600">
                              -{analytics[account.username].followers_lost_today || 0}
                            </p>
                            <p className="text-sm text-gray-600">Lost Followers</p>
                          </div>
                          <div className="text-center">
                            <p className={`text-2xl font-bold ${getGrowthColor(analytics[account.username].net_growth || 0)}`}>
                              {analytics[account.username].net_growth > 0 ? '+' : ''}{analytics[account.username].net_growth || 0}
                            </p>
                            <p className="text-sm text-gray-600">Net Growth</p>
                          </div>
                        </div>
                      </div>

                      {analytics[account.username].recent_unfollowers && analytics[account.username].recent_unfollowers.length > 0 && (
                        <div className="bg-red-50 p-4 rounded-lg">
                          <h4 className="font-medium text-red-900 mb-3">Recent Unfollowers</h4>
                          <div className="space-y-2">
                            {analytics[account.username].recent_unfollowers.slice(0, 5).map((unfollower, index) => (
                              <div key={index} className="flex items-center justify-between bg-white p-2 rounded">
                                <span className="font-medium">@{unfollower.username}</span>
                                <span className="text-sm text-gray-500">
                                  {new Date(unfollower.unfollowed_at).toLocaleDateString()}
                                </span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}

                  <div className="flex space-x-2 mt-4">
                    <button
                      onClick={() => {
                        const msToken = prompt('Enter your TikTok ms_token for data collection:');
                        if (msToken) collectData(account.username, msToken);
                      }}
                      className="bg-green-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-green-700 transition-colors"
                    >
                      Collect Fresh Data
                    </button>
                    <button
                      onClick={() => loadAnalytics(account.username)}
                      className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-700 transition-colors"
                    >
                      Refresh Analytics
                    </button>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
