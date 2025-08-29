'use client';

import React, { useState } from 'react';
import { SocialAccount } from '../lib/supabase';
import TikTokOAuthLogin from './TikTokOAuthLogin';
import HistoricalAnalytics from './HistoricalAnalytics';

interface AccountManagerProps {
  accounts: SocialAccount[];
  onRefreshData: () => void;
}

export default function AccountManager({ accounts, onRefreshData }: AccountManagerProps) {
  const [showAddAccount, setShowAddAccount] = useState(false);
  const [selectedPlatform, setSelectedPlatform] = useState<'tiktok' | 'instagram' | 'twitter'>('tiktok');
  const [expandedAccount, setExpandedAccount] = useState<string | null>(null);
  const [showAnalytics, setShowAnalytics] = useState<string | null>(null);
  const [showTikTokLogin, setShowTikTokLogin] = useState(false);

  const formatNumber = (num: number) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  };

  const getPlatformColor = (platform: string) => {
    const colors = {
      tiktok: 'from-pink-500 to-purple-600',
      instagram: 'from-purple-500 to-pink-600',
      twitter: 'from-blue-400 to-blue-600'
    };
    return colors[platform as keyof typeof colors] || 'from-gray-400 to-gray-600';
  };

  const getPlatformIcon = (platform: string) => {
    const icons = {
      tiktok: (
        <path d="M19.589 6.686a4.793 4.793 0 01-3.77-4.245V2h-3.445v13.672a2.896 2.896 0 01-2.909 2.909 2.896 2.896 0 01-2.909-2.909 2.896 2.896 0 012.909-2.909c.301 0 .591.041.864.119V9.438a6.331 6.331 0 00-.864-.058A6.448 6.448 0 003 15.672a6.448 6.448 0 006.465 6.421 6.448 6.448 0 006.465-6.421V8.55a8.282 8.282 0 004.659 1.453V6.686c-.016.003-.039.009-.055.009z"/>
      ),
      instagram: (
        <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073z"/>
      ),
      twitter: (
        <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
      )
    };
    return icons[platform as keyof typeof icons];
  };

  const collectData = async (account: SocialAccount) => {
    const msToken = prompt(`Enter your ${account.platform.toUpperCase()} ms_token for data collection:`);
    if (!msToken) return;

    try {
      const response = await fetch('http://localhost:8000/collect-tiktok-data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: account.username,
          ms_token: msToken
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        alert(`✅ Data collected! Followers: ${data.data?.followers || 'N/A'}`);
        onRefreshData();
      } else {
        const error = await response.text();
        alert('❌ Data collection failed. Check console for details.');
        console.error('Data collection error:', error);
      }
    } catch (error) {
      console.error('Error collecting data:', error);
      alert('❌ Data collection error. Check console for details.');
    }
  };

  const testAccount = async (account: SocialAccount) => {
    try {
      // Simulate a test - in reality this would call a test endpoint
      const response = await fetch(`http://localhost:8000/test-account/${account.id}`, {
        method: 'POST'
      });
      
      if (response.ok) {
        alert(`✅ ${account.platform.toUpperCase()} account test successful!`);
      } else {
        alert(`❌ ${account.platform.toUpperCase()} account test failed.`);
      }
    } catch (error) {
      console.error('Test error:', error);
      alert('❌ Test failed. Check console for details.');
    }
  };

  const viewAnalytics = async (account: SocialAccount) => {
    setShowAnalytics(account.id);
    // In a real implementation, this would fetch analytics data
    try {
      const response = await fetch(`http://localhost:8000/tiktok-analytics/${account.username}`);
      if (response.ok) {
        const analyticsData = await response.json();
        console.log('Analytics data:', analyticsData);
      }
    } catch (error) {
      console.error('Analytics error:', error);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header with Add Account */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Account Management</h2>
          <p className="text-gray-600">Manage your social media accounts, view analytics, and collect data</p>
        </div>
        <button
          onClick={() => setShowAddAccount(true)}
          className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Connect Account
        </button>
      </div>

      {/* Platform Filter */}
      <div className="flex space-x-4">
        <button
          onClick={() => setSelectedPlatform('tiktok')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            selectedPlatform === 'tiktok'
              ? 'bg-pink-100 text-pink-800'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          TikTok
        </button>
        <button
          onClick={() => setSelectedPlatform('instagram')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            selectedPlatform === 'instagram'
              ? 'bg-purple-100 text-purple-800'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          Instagram
        </button>
        <button
          onClick={() => setSelectedPlatform('twitter')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            selectedPlatform === 'twitter'
              ? 'bg-blue-100 text-blue-800'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          Twitter
        </button>
      </div>

      {/* Accounts List */}
      <div className="space-y-4">
        {accounts
          .filter(account => !selectedPlatform || account.platform === selectedPlatform)
          .map(account => (
          <div key={account.id} className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className={`w-12 h-12 bg-gradient-to-r ${getPlatformColor(account.platform)} rounded-lg flex items-center justify-center`}>
                  <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 24 24">
                    {getPlatformIcon(account.platform)}
                  </svg>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">@{account.username}</h3>
                  <p className="text-sm text-gray-500 capitalize">{account.platform}</p>
                  <div className="flex items-center space-x-4 mt-1">
                    {account.follower_count !== undefined && (
                      <span className="text-sm text-gray-600">
                        <span className="font-medium">{formatNumber(account.follower_count)}</span> followers
                      </span>
                    )}
                    {account.following_count !== undefined && (
                      <span className="text-sm text-gray-600">
                        <span className="font-medium">{formatNumber(account.following_count)}</span> following
                      </span>
                    )}
                    {account.engagement_rate !== undefined && (
                      <span className="text-sm font-medium text-green-600">
                        {account.engagement_rate}% engagement
                      </span>
                    )}
                  </div>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <div className={`w-3 h-3 rounded-full ${account.is_active ? 'bg-green-500' : 'bg-red-500'}`}></div>
                <span className="text-sm text-gray-500">
                  {account.is_active ? 'Active' : 'Inactive'}
                </span>
                
                <button
                  onClick={() => setExpandedAccount(expandedAccount === account.id ? null : account.id)}
                  className="bg-gray-100 text-gray-700 px-3 py-1 rounded-lg text-sm hover:bg-gray-200 transition-colors"
                >
                  {expandedAccount === account.id ? 'Collapse' : 'Manage'}
                </button>
              </div>
            </div>

            {/* Expanded Account Management */}
            {expandedAccount === account.id && (
              <div className="mt-6 pt-6 border-t border-gray-200">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                  <button
                    onClick={() => collectData(account)}
                    className="bg-green-600 text-white px-4 py-3 rounded-lg hover:bg-green-700 transition-colors flex items-center justify-center gap-2"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    Collect Data
                  </button>

                  <button
                    onClick={() => viewAnalytics(account)}
                    className="bg-blue-600 text-white px-4 py-3 rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center gap-2"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                    View Analytics
                  </button>

                  <button
                    onClick={() => testAccount(account)}
                    className="bg-yellow-600 text-white px-4 py-3 rounded-lg hover:bg-yellow-700 transition-colors flex items-center justify-center gap-2"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    Test Account
                  </button>

                  <button
                    onClick={() => {
                      if (confirm('Are you sure you want to remove this account?')) {
                        // Handle account removal
                        console.log('Removing account:', account.id);
                      }
                    }}
                    className="bg-red-600 text-white px-4 py-3 rounded-lg hover:bg-red-700 transition-colors flex items-center justify-center gap-2"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                    Remove Account
                  </button>
                </div>

                {/* Historical Analytics */}
                {showAnalytics === account.id && (
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <HistoricalAnalytics
                      userId="550e8400-e29b-41d4-a716-446655440000" // Mock user ID
                      username={account.username}
                      platform={account.platform}
                    />
                  </div>
                )}
              </div>
            )}
          </div>
        ))}

        {accounts.filter(account => !selectedPlatform || account.platform === selectedPlatform).length === 0 && (
          <div className="text-center py-12 border-2 border-dashed border-gray-300 rounded-lg">
            <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 515.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No {selectedPlatform} accounts</h3>
            <p className="text-gray-500 mb-4">Connect your first {selectedPlatform} account to get started</p>
            <button
              onClick={() => setShowAddAccount(true)}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Connect {selectedPlatform.charAt(0).toUpperCase() + selectedPlatform.slice(1)} Account
            </button>
          </div>
        )}
      </div>

      {/* Add Account Modal */}
      {showAddAccount && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-lg font-semibold mb-4">Connect New Account</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Platform</label>
                <select
                  value={selectedPlatform}
                  onChange={(e) => setSelectedPlatform(e.target.value as 'tiktok' | 'instagram' | 'twitter')}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="tiktok">TikTok</option>
                  <option value="instagram">Instagram (Coming Soon)</option>
                  <option value="twitter">Twitter (Coming Soon)</option>
                </select>
              </div>

              <div className="flex space-x-3">
                <button
                  onClick={() => {
                    setShowAddAccount(false);
                    if (selectedPlatform === 'tiktok') {
                      setShowTikTokLogin(true);
                    } else {
                      alert(`${selectedPlatform.charAt(0).toUpperCase() + selectedPlatform.slice(1)} integration coming soon!`);
                    }
                  }}
                  className="flex-1 bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Connect
                </button>
                <button
                  onClick={() => setShowAddAccount(false)}
                  className="flex-1 bg-gray-300 text-gray-700 py-2 rounded-lg hover:bg-gray-400 transition-colors"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TikTok OAuth Login Modal */}
      <TikTokOAuthLogin
        isOpen={showTikTokLogin}
        onClose={() => setShowTikTokLogin(false)}
        onSuccess={(accountData) => {
          console.log('TikTok account connected:', accountData);
          setShowTikTokLogin(false);
          onRefreshData(); // Refresh the dashboard data
          alert(`✅ Successfully connected @${accountData.username}!`);
        }}
      />
    </div>
  );
}
