'use client';

import React, { useState } from 'react';

interface TwitterAccount {
  id: string;
  username: string;
  follower_count: number;
  following_count: number;
  tweet_count: number;
  engagement_rate: number;
  is_active: boolean;
  last_sync?: string;
}

interface TwitterSectionProps {
  accounts: TwitterAccount[];
  onAddAccount: () => void;
  onRefreshData: (username: string) => void;
  isEnabled: boolean;
}

export default function TwitterSection({ accounts, onAddAccount, onRefreshData, isEnabled }: TwitterSectionProps) {
  const [expandedAccount, setExpandedAccount] = useState<string | null>(null);

  const formatNumber = (num: number) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  };

  if (!isEnabled) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6 opacity-60">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-gradient-to-r from-blue-400 to-blue-600 rounded-lg flex items-center justify-center">
              <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
              </svg>
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Twitter/X Accounts</h2>
              <p className="text-gray-500">Available in Phase 3</p>
            </div>
          </div>
          
          <div className="bg-gray-100 text-gray-500 px-4 py-2 rounded-lg font-medium">
            Coming Soon
          </div>
        </div>

        <div className="text-center py-12 border-2 border-dashed border-gray-300 rounded-lg">
          <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
          <h3 className="text-lg font-medium text-gray-700 mb-2">Twitter/X Coming Soon</h3>
          <p className="text-gray-500 mb-4">Build your multi-platform presence with thought leadership content</p>
          <div className="bg-blue-50 p-4 rounded-lg max-w-md mx-auto">
            <p className="text-sm text-blue-800">
              <strong>Phase 3 Strategy:</strong> Twitter/X unlocks for thought leadership and community building once you've established TikTok + Instagram presence
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 bg-gradient-to-r from-blue-400 to-blue-600 rounded-lg flex items-center justify-center">
            <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 24 24">
              <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
            </svg>
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Twitter/X Accounts</h2>
            <p className="text-gray-500">{accounts.length} connected account{accounts.length !== 1 ? 's' : ''}</p>
          </div>
        </div>
        
        <button
          onClick={onAddAccount}
          className="bg-gradient-to-r from-blue-400 to-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:from-blue-500 hover:to-blue-700 transition-all transform hover:scale-105 shadow-lg flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Add Twitter Account
        </button>
      </div>

      {accounts.length === 0 ? (
        <div className="text-center py-12 border-2 border-dashed border-gray-300 rounded-lg">
          <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Twitter accounts connected</h3>
          <p className="text-gray-500 mb-4">Connect your Twitter account for thought leadership and community building</p>
          <button
            onClick={onAddAccount}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Connect Twitter Account
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {accounts.map(account => (
            <div key={account.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-gradient-to-r from-blue-400 to-blue-600 rounded-full flex items-center justify-center text-white font-bold text-lg">
                    {account.username.charAt(0).toUpperCase()}
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">@{account.username}</h3>
                    <div className="flex items-center space-x-4 mt-1">
                      <span className="text-sm text-gray-600">
                        <span className="font-medium">{formatNumber(account.follower_count)}</span> followers
                      </span>
                      <span className="text-sm text-gray-600">
                        <span className="font-medium">{formatNumber(account.following_count)}</span> following
                      </span>
                      <span className="text-sm text-gray-600">
                        <span className="font-medium">{formatNumber(account.tweet_count)}</span> tweets
                      </span>
                      <span className="text-sm font-medium text-blue-600">
                        {account.engagement_rate}% engagement
                      </span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  <div className={`w-3 h-3 rounded-full ${account.is_active ? 'bg-green-500' : 'bg-red-500'}`}></div>
                  <span className="text-sm text-gray-500">
                    {account.is_active ? 'Active' : 'Inactive'}
                  </span>
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
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <h4 className="font-medium text-blue-900 mb-3">Twitter Features</h4>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="text-center">
                        <p className="text-lg font-bold text-blue-600">Thread Creation</p>
                        <p className="text-sm text-gray-600">Long-form thought leadership</p>
                      </div>
                      <div className="text-center">
                        <p className="text-lg font-bold text-blue-600">Community Building</p>
                        <p className="text-sm text-gray-600">Engage with industry leaders</p>
                      </div>
                    </div>
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
