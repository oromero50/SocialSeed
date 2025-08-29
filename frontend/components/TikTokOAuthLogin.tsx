'use client';

import React, { useState, useEffect } from 'react';

interface TikTokOAuthLoginProps {
  onSuccess: (accountData: any) => void;
  onClose: () => void;
  isOpen: boolean;
}

const TikTokOAuthLogin: React.FC<TikTokOAuthLoginProps> = ({ onSuccess, onClose, isOpen }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [authUrl, setAuthUrl] = useState<string | null>(null);

  useEffect(() => {
    // Check if we're returning from OAuth callback
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    const state = urlParams.get('state');
    const error = urlParams.get('error');

    if (error) {
      setError(`Authentication failed: ${error}`);
      return;
    }

    if (code && state) {
      handleOAuthCallback(code, state);
    }
  }, []);

  const handleOAuthCallback = async (code: string, state: string) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`http://localhost:8000/tiktok/auth/callback?code=${code}&state=${state}`);
      const data = await response.json();

      if (data.success) {
        onSuccess(data.account);
        
        // Clean up URL parameters
        window.history.replaceState({}, document.title, window.location.pathname);
      } else {
        setError(data.error || 'Authentication failed');
      }
    } catch (error) {
      console.error('OAuth callback error:', error);
      setError('Failed to complete authentication');
    } finally {
      setLoading(false);
    }
  };

  const initiateOAuth = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/tiktok/auth/login');
      const data = await response.json();

      if (data.success) {
        setAuthUrl(data.auth_url);
        
        // Open TikTok OAuth in the same window
        window.location.href = data.auth_url;
      } else {
        setError(data.error || 'Failed to initiate login');
      }
    } catch (error) {
      console.error('OAuth initiation error:', error);
      setError('Failed to start authentication process');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg max-w-md w-full mx-4 p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold text-gray-900">Connect TikTok Account</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="text-center">
          <div className="w-16 h-16 bg-gradient-to-r from-pink-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-10 h-10 text-white" fill="currentColor" viewBox="0 0 24 24">
              <path d="M19.589 6.686a4.793 4.793 0 01-3.77-4.245V2h-3.445v13.672a2.896 2.896 0 01-2.909 2.909 2.896 2.896 0 01-2.909-2.909 2.896 2.896 0 012.909-2.909c.301 0 .591.041.864.119V9.438a6.331 6.331 0 00-.864-.058A6.448 6.448 0 003 15.672a6.448 6.448 0 006.465 6.421 6.448 6.448 0 006.465-6.421V8.55a8.282 8.282 0 004.659 1.453V6.686c-.016.003-.039.009-.055.009z"/>
            </svg>
          </div>

          <h3 className="text-lg font-medium text-gray-900 mb-2">Connect with TikTok</h3>
          <p className="text-gray-600 mb-6">
            Securely connect your TikTok account to access analytics and automation features
          </p>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
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

          <div className="space-y-4">
            <button
              onClick={initiateOAuth}
              disabled={loading}
              className="w-full bg-gradient-to-r from-pink-500 to-purple-600 text-white py-3 px-4 rounded-lg font-medium hover:from-pink-600 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-3"></div>
                  Connecting...
                </>
              ) : (
                <>
                  <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M19.589 6.686a4.793 4.793 0 01-3.77-4.245V2h-3.445v13.672a2.896 2.896 0 01-2.909 2.909 2.896 2.896 0 01-2.909-2.909 2.896 2.896 0 012.909-2.909c.301 0 .591.041.864.119V9.438a6.331 6.331 0 00-.864-.058A6.448 6.448 0 003 15.672a6.448 6.448 0 006.465 6.421 6.448 6.448 0 006.465-6.421V8.55a8.282 8.282 0 004.659 1.453V6.686c-.016.003-.039.009-.055.009z"/>
                  </svg>
                  Login with TikTok
                </>
              )}
            </button>

            <div className="text-xs text-gray-500 space-y-2">
              <p>✓ Secure OAuth 2.0 authentication</p>
              <p>✓ Read-only access to your account data</p>
              <p>✓ No passwords stored</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TikTokOAuthLogin;
