import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';

export default function TikTokCallback() {
  const router = useRouter();
  const [status, setStatus] = useState('Processing...');
  const [error, setError] = useState('');

  useEffect(() => {
    const handleCallback = async () => {
      try {
        const { code, state } = router.query;
        
        if (!code) {
          setError('No authorization code received from TikTok');
          return;
        }

        if (!state) {
          setError('No state parameter received from TikTok');
          return;
        }

        // Verify state parameter
        const storedState = localStorage.getItem('tiktok_oauth_state');
        if (state !== storedState) {
          setError('State parameter mismatch. Possible CSRF attack.');
          return;
        }

        setStatus('Authorization successful! Redirecting...');

        // Store the authorization code for the parent window to use
        localStorage.setItem('tiktok_auth_code', code as string);
        localStorage.removeItem('tiktok_oauth_state');

        // Close this window and notify the parent
        if (window.opener) {
          window.opener.postMessage({ type: 'TIKTOK_OAUTH_SUCCESS', code }, window.location.origin);
          window.close();
        } else {
          // Fallback: redirect back to dashboard
          setTimeout(() => {
            router.push('/');
          }, 2000);
        }

      } catch (err) {
        console.error('TikTok callback error:', err);
        setError('Failed to process TikTok callback');
      }
    };

    if (router.isReady) {
      handleCallback();
    }
  }, [router.isReady, router.query]);

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="max-w-md w-full bg-white rounded-lg shadow-md p-8">
        <div className="text-center">
          <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-blue-100 mb-4">
            <svg className="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            TikTok Authorization
          </h3>
          
          {error ? (
            <div className="text-red-600">
              <p className="text-sm">{error}</p>
              <button
                onClick={() => router.push('/')}
                className="mt-4 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
              >
                Return to Dashboard
              </button>
            </div>
          ) : (
            <div className="text-gray-600">
              <p className="text-sm">{status}</p>
              <div className="mt-4 animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
