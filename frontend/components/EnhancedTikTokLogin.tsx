'use client';

import { useState } from 'react';

interface EnhancedTikTokLoginProps {
  onSuccess: (accountData: any) => void;
  onCancel: () => void;
}

export default function EnhancedTikTokLogin({ onSuccess, onCancel }: EnhancedTikTokLoginProps) {
  const [credentials, setCredentials] = useState({
    username: '',
    ms_token: ''
  });
  const [isConnecting, setIsConnecting] = useState(false);
  const [error, setError] = useState('');
  const [showInstructions, setShowInstructions] = useState(false);

  const handleLogin = async () => {
    if (!credentials.username || !credentials.ms_token) {
      setError('Please enter both username and ms_token');
      return;
    }

    try {
      setIsConnecting(true);
      setError('');

      console.log('🔑 Connecting TikTok account with ms_token:', credentials.username);

      // Call enhanced backend endpoint
      const response = await fetch('http://localhost:8000/enhanced-tiktok-login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: credentials.username,
          ms_token: credentials.ms_token,
          user_id: '550e8400-e29b-41d4-a716-446655440000'
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`Account connection failed: ${errorData.detail || 'Unknown error'}`);
      }

      const loginData = await response.json();
      console.log('✅ TikTok account connected successfully with enhanced API');
      
      // Step 2: Start data collection
      console.log('📊 Starting follower data collection...');
      setError('Connected! Collecting follower data...');
      
      try {
        const collectResponse = await fetch('http://localhost:8000/collect-tiktok-data', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: credentials.username,
            ms_token: credentials.ms_token
          }),
        });
        
        if (collectResponse.ok) {
          const collectData = await collectResponse.json();
          console.log('✅ Data collection successful:', collectData);
          
          onSuccess({
            ...loginData.account,
            username: credentials.username,
            platform: 'tiktok',
            followers: collectData.data.followers,
            following: collectData.data.following,
            engagement_rate: collectData.data.engagement_rate,
            message: `Account connected! ${collectData.data.followers} followers collected.`
          });
        } else {
          // Login succeeded but data collection failed - still consider success
          console.warn('⚠️ Data collection failed, but account connected');
          onSuccess({
            ...loginData.account,
            username: credentials.username,
            platform: 'tiktok',
            message: 'Account connected. Data collection will retry automatically.'
          });
        }
      } catch (collectError) {
        console.warn('⚠️ Data collection error:', collectError);
        onSuccess({
          ...loginData.account,
          username: credentials.username,
          platform: 'tiktok',
          message: 'Account connected. Data collection will retry automatically.'
        });
      }

    } catch (error: any) {
      console.error('❌ Enhanced TikTok login failed:', error);
      setError(error.message || 'Failed to connect TikTok account');
    } finally {
      setIsConnecting(false);
    }
  };

  const getMsTokenInstructions = () => {
    return (
      <div className="mb-6 p-4 bg-blue-900 rounded-lg text-sm">
        <h3 className="font-semibold mb-2 text-blue-200">📋 How to get your ms_token:</h3>
        <ol className="list-decimal list-inside space-y-1 text-blue-100 text-xs">
          <li>Open TikTok in your browser and log in normally</li>
          <li>Press F12 or right-click → Inspect</li>
          <li>Go to Application tab → Cookies → tiktok.com</li>
          <li>Find 'msToken' and copy its value</li>
          <li>Paste it in the field below</li>
        </ol>
        <p className="mt-2 text-yellow-200 text-xs">⚠️ Keep this token private - it gives access to your account</p>
      </div>
    );
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-black text-white rounded-2xl p-8 max-w-md w-full mx-4 relative">
        {/* Close button */}
        <button
          onClick={onCancel}
          className="absolute top-4 right-4 text-gray-400 hover:text-white transition-colors"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        {/* Header */}
        <div className="text-center mb-6">
          <div className="flex justify-center mb-4">
            <div className="w-16 h-16 bg-gradient-to-r from-pink-500 to-violet-500 rounded-full flex items-center justify-center">
              <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.05-2.83-.14-4.08-.72-2.26-1.17-3.96-3.66-4.6-6.34-.44-1.8-.6-3.69-.6-5.58 0-1.79.13-3.56.6-5.31.69-2.67 2.51-4.96 5.08-6.08 1.97-1.11 4.08-1.26 6.2-1.29z"/>
              </svg>
            </div>
          </div>
          <h2 className="text-2xl font-bold mb-2">SocialSeed</h2>
          <p className="text-gray-300 text-sm">Enhanced TikTok Account Connection</p>
          <p className="text-gray-400 text-xs mt-1">Fast & reliable API access</p>
        </div>

        {/* Instructions toggle */}
        <div className="mb-4">
          <button
            onClick={() => setShowInstructions(!showInstructions)}
            className="text-blue-400 hover:text-blue-300 text-sm underline"
          >
            {showInstructions ? '🔼 Hide instructions' : '🔽 How to get ms_token?'}
          </button>
        </div>

        {/* Instructions */}
        {showInstructions && getMsTokenInstructions()}

        {/* Form */}
        <div className="space-y-4">
          {/* Username */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              TikTok Username
            </label>
            <input
              type="text"
              placeholder="@yourusername"
              value={credentials.username}
              onChange={(e) => setCredentials({...credentials, username: e.target.value})}
              className="w-full px-4 py-3 bg-yellow-100 text-black rounded-xl placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-pink-500"
            />
          </div>

          {/* MS Token */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              ms_token
            </label>
            <textarea
              placeholder="Paste your msToken from browser cookies..."
              value={credentials.ms_token}
              onChange={(e) => setCredentials({...credentials, ms_token: e.target.value})}
              className="w-full px-4 py-3 bg-yellow-100 text-black rounded-xl placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-pink-500 h-20 resize-none text-xs"
            />
          </div>
        </div>

        {/* Error message */}
        {error && (
          <div className="mt-4 p-3 bg-red-900 border border-red-700 rounded-lg">
            <p className="text-red-200 text-sm">{error}</p>
          </div>
        )}

        {/* Connect button */}
        <button
          onClick={handleLogin}
          disabled={isConnecting || !credentials.username || !credentials.ms_token}
          className="w-full mt-6 flex items-center justify-center py-3 px-4 bg-gradient-to-r from-pink-500 to-violet-500 text-white rounded-xl font-semibold hover:from-pink-600 hover:to-violet-600 focus:outline-none focus:ring-2 focus:ring-pink-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          {isConnecting ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
              Connecting...
            </>
          ) : (
            <>
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                <path d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
              Connect Account
            </>
          )}
        </button>

        {/* Footer */}
        <div className="mt-6 text-center">
          <p className="text-gray-400 text-xs">
            SocialSeed v2.0 - Enhanced TikTok Integration
          </p>
          <p className="text-gray-500 text-xs mt-1">
            ⚡ Powered by TikTok-Api Library
          </p>
        </div>

        {/* Status indicator */}
        {credentials.username && (
          <div className="mt-4 text-center">
            <p className="text-sm text-gray-300">
              Connecting as @{credentials.username}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
