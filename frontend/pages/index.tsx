import React, { useState, useEffect } from 'react';
import Dashboard from '../components/Dashboard';
import MarketingLandingPage from '../components/MarketingLandingPage';

export default function Home() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if user is authenticated
    // This is a simple check - in a real app you'd validate tokens
    const checkAuthState = () => {
      // Check for stored auth data or tokens
      const hasAuthData = localStorage.getItem('socialseed_auth') || 
                         sessionStorage.getItem('socialseed_auth') ||
                         // Check if we're returning from OAuth callback
                         window.location.search.includes('code=');
      
      setIsAuthenticated(!!hasAuthData);
      setIsLoading(false);
    };

    checkAuthState();

    // Listen for auth state changes
    const handleStorageChange = () => {
      checkAuthState();
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  const handleLogin = () => {
    // Set auth state and redirect to dashboard
    localStorage.setItem('socialseed_auth', 'true');
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    // Clear auth state and redirect to landing page
    localStorage.removeItem('socialseed_auth');
    sessionStorage.removeItem('socialseed_auth');
    setIsAuthenticated(false);
  };

  const handleGetStarted = () => {
    // This could trigger the OAuth flow or registration
    // For now, let's just show the dashboard with instructions to connect accounts
    handleLogin();
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-400 via-pink-500 to-red-500">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-white mx-auto mb-4"></div>
          <h2 className="text-2xl font-bold text-white">Loading SocialSeed...</h2>
        </div>
      </div>
    );
  }

  return (
    <>
      {isAuthenticated ? (
        <Dashboard onLogout={handleLogout} />
      ) : (
        <MarketingLandingPage onGetStarted={handleGetStarted} />
      )}
    </>
  );
}