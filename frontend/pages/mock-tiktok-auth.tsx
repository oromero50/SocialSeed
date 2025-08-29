import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';

export default function MockTikTokAuth() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const { state } = router.query;

  const handleMockLogin = async () => {
    setLoading(true);
    
    // Simulate login delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Generate mock authorization code
    const mockCode = 'mock_auth_code_' + Math.random().toString(36).substr(2, 9);
    
    // Redirect back to the callback with mock credentials
    window.location.href = `http://localhost:3000/?code=${mockCode}&state=${state}`;
  };

  return (
    <div className="min-h-screen bg-black flex items-center justify-center">
      <div className="bg-white rounded-lg max-w-md w-full mx-4 p-8 text-center">
        {/* TikTok Logo */}
        <div className="w-16 h-16 bg-gradient-to-r from-pink-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg className="w-10 h-10 text-white" fill="currentColor" viewBox="0 0 24 24">
            <path d="M19.589 6.686a4.793 4.793 0 01-3.77-4.245V2h-3.445v13.672a2.896 2.896 0 01-2.909 2.909 2.896 2.896 0 01-2.909-2.909 2.896 2.896 0 012.909-2.909c.301 0 .591.041.864.119V9.438a6.331 6.331 0 00-.864-.058A6.448 6.448 0 003 15.672a6.448 6.448 0 006.465 6.421 6.448 6.448 0 006.465-6.421V8.55a8.282 8.282 0 004.659 1.453V6.686c-.016.003-.039.009-.055.009z"/>
          </svg>
        </div>

        <h1 className="text-2xl font-bold text-gray-900 mb-2">Mock TikTok Login</h1>
        <p className="text-gray-600 mb-6">
          This is a development simulation of TikTok's OAuth login process.
        </p>

        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
          <div className="flex">
            <svg className="h-5 w-5 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-yellow-800">Development Mode</h3>
              <p className="text-sm text-yellow-700 mt-1">
                This simulates TikTok login. Apply for real TikTok Developer access at{' '}
                <a href="https://developers.tiktok.com" target="_blank" rel="noopener noreferrer" className="underline">
                  developers.tiktok.com
                </a>
              </p>
            </div>
          </div>
        </div>

        <div className="space-y-4">
          <div className="bg-gray-50 rounded-lg p-4">
            <h3 className="font-medium text-gray-900 mb-2">Mock Account Details:</h3>
            <div className="text-sm text-gray-600 space-y-1">
              <p>👤 <strong>Username:</strong> @demo_creator</p>
              <p>👥 <strong>Followers:</strong> 125K</p>
              <p>❤️ <strong>Likes:</strong> 2.5M</p>
              <p>✅ <strong>Verified:</strong> Yes</p>
            </div>
          </div>

          <button
            onClick={handleMockLogin}
            disabled={loading}
            className="w-full bg-gradient-to-r from-pink-500 to-purple-600 text-white py-3 px-4 rounded-lg font-medium hover:from-pink-600 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-3"></div>
                Authorizing SocialSeed...
              </>
            ) : (
              <>
                <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M19.589 6.686a4.793 4.793 0 01-3.77-4.245V2h-3.445v13.672a2.896 2.896 0 01-2.909 2.909 2.896 2.896 0 01-2.909-2.909 2.896 2.896 0 012.909-2.909c.301 0 .591.041.864.119V9.438a6.331 6.331 0 00-.864-.058A6.448 6.448 0 003 15.672a6.448 6.448 0 006.465 6.421 6.448 6.448 0 006.465-6.421V8.55a8.282 8.282 0 004.659 1.453V6.686c-.016.003-.039.009-.055.009z"/>
                </svg>
                Authorize SocialSeed
              </>
            )}
          </button>

          <p className="text-xs text-gray-500">
            By clicking "Authorize", you're simulating giving SocialSeed permission to access your TikTok account data for analytics and management purposes.
          </p>
        </div>
      </div>
    </div>
  );
}
