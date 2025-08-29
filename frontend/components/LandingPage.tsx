'use client';

import React, { useState, useEffect } from 'react';
import TikTokOAuthLogin from './TikTokOAuthLogin';

interface LandingPageProps {
  onLogin?: () => void;
}

const LandingPage: React.FC<LandingPageProps> = ({ onLogin }) => {
  const [showTikTokLogin, setShowTikTokLogin] = useState(false);
  const [activeSection, setActiveSection] = useState('overview');

  useEffect(() => {
    // Initialize charts when component mounts
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
    script.onload = () => {
      initializeCharts();
    };
    document.head.appendChild(script);

    return () => {
      document.head.removeChild(script);
    };
  }, []);

  const initializeCharts = () => {
    // Growth Chart
    const growthCanvas = document.getElementById('growthChart') as HTMLCanvasElement;
    if (growthCanvas && window.Chart) {
      const growthCtx = growthCanvas.getContext('2d');
      new window.Chart(growthCtx, {
        type: 'line',
        data: {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
          datasets: [{
            label: 'Followers',
            data: [0, 20, 45, 80, 120, 140, 150],
            borderColor: 'rgba(102, 126, 234, 1)',
            backgroundColor: 'rgba(102, 126, 234, 0.1)',
            borderWidth: 3,
            fill: true,
            tension: 0.4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              labels: { color: 'white' }
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: { color: 'white' },
              grid: { color: 'rgba(255, 255, 255, 0.1)' }
            },
            x: {
              ticks: { color: 'white' },
              grid: { color: 'rgba(255, 255, 255, 0.1)' }
            }
          }
        }
      });
    }

    // Engagement Chart
    const engagementCanvas = document.getElementById('engagementChart') as HTMLCanvasElement;
    if (engagementCanvas && window.Chart) {
      const engagementCtx = engagementCanvas.getContext('2d');
      new window.Chart(engagementCtx, {
        type: 'doughnut',
        data: {
          labels: ['Likes', 'Comments', 'Shares', 'Views'],
          datasets: [{
            data: [45, 25, 15, 15],
            backgroundColor: [
              'rgba(255, 99, 132, 0.8)',
              'rgba(54, 162, 235, 0.8)',
              'rgba(255, 205, 86, 0.8)',
              'rgba(75, 192, 192, 0.8)'
            ],
            borderWidth: 0
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              labels: { color: 'white' }
            }
          }
        }
      });
    }
  };

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
      setActiveSection(sectionId);
    }
  };

  const handleConnectAccount = () => {
    setShowTikTokLogin(true);
  };

  const handleLoginSuccess = (accountData: any) => {
    console.log('Account connected:', accountData);
    setShowTikTokLogin(false);
    if (onLogin) {
      onLogin();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-400 via-pink-500 to-red-500">
      <style jsx>{`
        .glass-effect {
          backdrop-filter: blur(10px);
          background: rgba(255, 255, 255, 0.1);
          border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .gradient-text {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }
        
        .card-hover {
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .card-hover:hover {
          transform: translateY(-2px);
          box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        }
        
        .btn-primary {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          transition: all 0.3s ease;
        }
        
        .btn-primary:hover {
          transform: scale(1.05);
          box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        }
        
        .progress-bar {
          background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
          animation: progress-fill 2s ease-in-out;
        }
        
        @keyframes progress-fill {
          from { width: 0%; }
          to { width: 75%; }
        }
        
        .bounce {
          animation: bounce 2s infinite;
        }
        
        @keyframes bounce {
          0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
          40% { transform: translateY(-10px); }
          60% { transform: translateY(-5px); }
        }
        
        .pulse-glow {
          animation: pulse-glow 2s infinite;
        }
        
        @keyframes pulse-glow {
          0% { box-shadow: 0 0 5px rgba(102, 126, 234, 0.5); }
          50% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.8); }
          100% { box-shadow: 0 0 5px rgba(102, 126, 234, 0.5); }
        }
        
        .counter-animation {
          animation: counter-up 2s ease-out;
        }
        
        @keyframes counter-up {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        
        .fun-icon {
          transition: transform 0.3s ease;
        }
        
        .fun-icon:hover {
          transform: rotate(10deg) scale(1.1);
        }
        
        .toggle-switch {
          position: relative;
          width: 60px;
          height: 30px;
          background: #e2e8f0;
          border-radius: 15px;
          cursor: pointer;
          transition: all 0.3s ease;
        }
        
        .toggle-switch.active {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .toggle-slider {
          position: absolute;
          top: 3px;
          left: 3px;
          width: 24px;
          height: 24px;
          background: white;
          border-radius: 50%;
          transition: all 0.3s ease;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        
        .toggle-switch.active .toggle-slider {
          transform: translateX(30px);
        }
        
        .chart-container {
          height: 300px;
        }
        
        .celebration {
          animation: celebration 0.6s ease-in-out;
        }
        
        @keyframes celebration {
          0% { transform: scale(1); }
          50% { transform: scale(1.1); }
          100% { transform: scale(1); }
        }
        
        .tiktok-gradient {
          background: linear-gradient(135deg, #ff0050 0%, #ff4081 100%);
        }
        
        .instagram-gradient {
          background: linear-gradient(135deg, #833ab4 0%, #fd1d1d 50%, #fcb045 100%);
        }
        
        .twitter-gradient {
          background: linear-gradient(135deg, #1da1f2 0%, #0d8bd9 100%);
        }
      `}</style>

      {/* Header */}
      <header className="glass-effect sticky top-0 z-50 p-4 mb-8">
        <div className="container mx-auto">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-white rounded-xl flex items-center justify-center fun-icon">
                <svg className="w-8 h-8 gradient-text" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">SocialSeed</h1>
                <p className="text-sm text-white opacity-80">Multi-platform social media growth</p>
              </div>
            </div>
            <nav className="flex space-x-8">
              <button
                onClick={() => scrollToSection('overview')}
                className={`text-white hover:text-yellow-300 transition-colors duration-300 font-semibold ${
                  activeSection === 'overview' ? 'border-b-2 border-yellow-300' : ''
                }`}
              >
                <i className="fas fa-chart-line mr-2"></i>Platform Overview
              </button>
              <button
                onClick={() => scrollToSection('accounts')}
                className={`text-white hover:text-yellow-300 transition-colors duration-300 font-semibold ${
                  activeSection === 'accounts' ? 'border-b-2 border-yellow-300' : ''
                }`}
              >
                <i className="fas fa-users mr-2"></i>Manage Accounts
              </button>
              <button
                onClick={() => scrollToSection('settings')}
                className={`text-white hover:text-yellow-300 transition-colors duration-300 font-semibold ${
                  activeSection === 'settings' ? 'border-b-2 border-yellow-300' : ''
                }`}
              >
                <i className="fas fa-cog mr-2"></i>Settings
              </button>
            </nav>
            <div className="flex items-center space-x-4">
              <button className="text-white hover:text-yellow-300 transition-colors duration-300">
                <i className="fas fa-bell text-xl"></i>
              </button>
              <button
                onClick={handleConnectAccount}
                className="w-10 h-10 bg-white rounded-full flex items-center justify-center hover:bg-gray-100 transition-colors"
              >
                <i className="fas fa-plus text-purple-600"></i>
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 pb-8">
        {/* Welcome Section */}
        <div id="overview" className="mb-12">
          <h1 className="text-4xl font-bold mb-4 text-white flex items-center">
            🚀 Welcome to Your Growth Dashboard
          </h1>
          <p className="text-xl text-white opacity-90 mb-8">Track your social media journey and watch your audience grow across multiple platforms!</p>
        </div>

        {/* Dashboard Overview */}
        <section className="mb-12">
          <h2 className="text-3xl font-bold mb-6 text-white flex items-center">
            📊 Dashboard Overview
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {/* Total Accounts Card */}
            <div className="glass-effect rounded-2xl p-6 card-hover">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center">
                  <i className="fas fa-user-friends text-white text-xl"></i>
                </div>
                <span className="text-2xl bounce">📱</span>
              </div>
              <h3 className="text-lg font-semibold mb-2 text-white">Total Accounts</h3>
              <p className="text-3xl font-bold text-white counter-animation">0</p>
              <p className="text-sm text-white opacity-70">Connected platforms</p>
            </div>

            {/* Active Accounts Card */}
            <div className="glass-effect rounded-2xl p-6 card-hover pulse-glow">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center">
                  <i className="fas fa-check-circle text-white text-xl"></i>
                </div>
                <span className="text-2xl bounce">✅</span>
              </div>
              <h3 className="text-lg font-semibold mb-2 text-white">Active Accounts</h3>
              <p className="text-3xl font-bold text-white counter-animation">0</p>
              <p className="text-sm text-white opacity-70">Currently growing</p>
            </div>

            {/* Total Followers Card */}
            <div className="glass-effect rounded-2xl p-6 card-hover">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-purple-500 rounded-xl flex items-center justify-center">
                  <i className="fas fa-heart text-white text-xl"></i>
                </div>
                <span className="text-2xl bounce">❤️</span>
              </div>
              <h3 className="text-lg font-semibold mb-2 text-white">Total Followers</h3>
              <p className="text-3xl font-bold text-white counter-animation">0</p>
              <p className="text-sm text-white opacity-70">Across all platforms</p>
            </div>

            {/* Engagement Card */}
            <div className="glass-effect rounded-2xl p-6 card-hover">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-yellow-500 rounded-xl flex items-center justify-center">
                  <i className="fas fa-chart-line text-white text-xl"></i>
                </div>
                <span className="text-2xl bounce">📈</span>
              </div>
              <h3 className="text-lg font-semibold mb-2 text-white">Avg. Engagement</h3>
              <p className="text-3xl font-bold text-white counter-animation">--</p>
              <p className="text-sm text-white opacity-70">Connect accounts to see data</p>
            </div>
          </div>
        </section>

        {/* Phase 1: TikTok Foundation */}
        <section className="mb-12">
          <h2 className="text-3xl font-bold mb-6 text-white flex items-center">
            🎯 Phase 1: TikTok Foundation
          </h2>
          <div className="glass-effect rounded-2xl p-8 mb-6">
            <h3 className="text-xl font-semibold mb-4 text-white">Build viral content and grow your TikTok presence</h3>
            <div className="mb-6">
              <div className="flex justify-between items-center mb-2">
                <span className="text-white font-semibold">Progress</span>
                <span className="text-white text-sm">Phase 1/3</span>
              </div>
              <div className="w-full bg-white bg-opacity-20 rounded-full h-4">
                <div className="progress-bar h-4 rounded-full flex items-center justify-end pr-2" style={{width: '0%'}}>
                  <span className="text-xs text-white font-bold">0%</span>
                </div>
              </div>
            </div>
            <div className="grid grid-cols-3 gap-4 text-center">
              <div className="text-white opacity-50">
                <div className="w-8 h-8 bg-gray-400 rounded-full mx-auto mb-2 flex items-center justify-center">
                  <i className="fab fa-tiktok text-white"></i>
                </div>
                <p className="text-sm font-semibold">TikTok</p>
                <p className="text-xs opacity-80">Connect to start</p>
              </div>
              <div className="text-white opacity-30">
                <div className="w-8 h-8 bg-gray-400 rounded-full mx-auto mb-2 flex items-center justify-center">
                  <i className="fab fa-instagram text-white"></i>
                </div>
                <p className="text-sm font-semibold">Instagram</p>
                <p className="text-xs opacity-80">Locked</p>
              </div>
              <div className="text-white opacity-30">
                <div className="w-8 h-8 bg-gray-400 rounded-full mx-auto mb-2 flex items-center justify-center">
                  <i className="fab fa-twitter text-white"></i>
                </div>
                <p className="text-sm font-semibold">Twitter</p>
                <p className="text-xs opacity-80">Locked</p>
              </div>
            </div>
            <div className="mt-6 p-4 bg-yellow-400 bg-opacity-20 rounded-xl">
              <p className="text-white text-center">
                <i className="fas fa-rocket mr-2 text-yellow-400"></i>
                <strong>Get Started:</strong> Connect your first TikTok account to begin your growth journey! 🎉
              </p>
            </div>
          </div>
        </section>

        {/* TikTok Accounts */}
        <section id="accounts" className="mb-12">
          <h2 className="text-3xl font-bold mb-6 text-white flex items-center">
            🎵 TikTok Accounts
          </h2>
          <div className="glass-effect rounded-2xl p-6 mb-6">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-semibold text-white">Connect Your First Account</h3>
              <button
                onClick={handleConnectAccount}
                className="btn-primary px-6 py-2 rounded-xl text-white font-semibold flex items-center hover:scale-105 transition-transform"
              >
                <i className="fas fa-plus mr-2"></i>Add TikTok Account
              </button>
            </div>
            
            {/* Empty State */}
            <div className="bg-white bg-opacity-10 rounded-xl p-12 text-center">
              <div className="w-24 h-24 tiktok-gradient rounded-full mx-auto flex items-center justify-center mb-6">
                <i className="fab fa-tiktok text-white text-4xl"></i>
              </div>
              <h4 className="text-white font-semibold text-xl mb-4">Ready to grow your TikTok presence?</h4>
              <p className="text-white opacity-70 mb-6">Connect your TikTok account to start tracking followers, engagement, and growth metrics.</p>
              <button
                onClick={handleConnectAccount}
                className="btn-primary px-8 py-3 rounded-xl text-white font-semibold flex items-center mx-auto"
              >
                <i className="fab fa-tiktok mr-3"></i>Connect TikTok Account
              </button>
            </div>
          </div>
        </section>

        {/* Analytics & Insights */}
        <section className="mb-12">
          <h2 className="text-3xl font-bold mb-6 text-white flex items-center">
            📊 Analytics & Insights
          </h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Growth Chart */}
            <div className="glass-effect rounded-2xl p-6">
              <h3 className="text-xl font-semibold mb-4 text-white flex items-center">
                📈 Follower Growth Trend
              </h3>
              <div className="chart-container">
                <canvas id="growthChart"></canvas>
              </div>
            </div>

            {/* Engagement Chart */}
            <div className="glass-effect rounded-2xl p-6">
              <h3 className="text-xl font-semibold mb-4 text-white flex items-center">
                💫 Engagement Rate
              </h3>
              <div className="chart-container">
                <canvas id="engagementChart"></canvas>
              </div>
            </div>
          </div>
        </section>

        {/* Settings Section */}
        <section id="settings" className="mb-12">
          <h2 className="text-3xl font-bold mb-6 text-white flex items-center">
            ⚙️ Automation Settings
          </h2>
          <div className="glass-effect rounded-2xl p-6 mb-8">
            <h3 className="text-xl font-semibold mb-4 text-white">Configure your SocialSeed preferences and automation settings</h3>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Notifications */}
              <div>
                <h3 className="text-lg font-semibold mb-6 text-white flex items-center">
                  🔔 Notifications
                </h3>
                
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 bg-white bg-opacity-10 rounded-xl">
                    <div>
                      <h4 className="text-white font-semibold">Email Notifications</h4>
                      <p className="text-white opacity-70 text-sm">Receive important updates via email</p>
                    </div>
                    <div className="toggle-switch active">
                      <div className="toggle-slider"></div>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between p-4 bg-white bg-opacity-10 rounded-xl">
                    <div>
                      <h4 className="text-white font-semibold">Push Notifications</h4>
                      <p className="text-white opacity-70 text-sm">Get real-time alerts in your browser</p>
                    </div>
                    <div className="toggle-switch">
                      <div className="toggle-slider"></div>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between p-4 bg-white bg-opacity-10 rounded-xl">
                    <div>
                      <h4 className="text-white font-semibold">Analytics Reports</h4>
                      <p className="text-white opacity-70 text-sm">Weekly analytics summaries</p>
                    </div>
                    <div className="toggle-switch active">
                      <div className="toggle-slider"></div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Automation */}
              <div>
                <h3 className="text-lg font-semibold mb-6 text-white flex items-center">
                  🤖 Automation
                </h3>
                
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 bg-white bg-opacity-10 rounded-xl">
                    <div>
                      <h4 className="text-white font-semibold">Auto Follow</h4>
                      <p className="text-white opacity-70 text-sm">Automatically follow relevant accounts</p>
                    </div>
                    <div className="toggle-switch">
                      <div className="toggle-slider"></div>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between p-4 bg-white bg-opacity-10 rounded-xl">
                    <div>
                      <h4 className="text-white font-semibold">Auto Like</h4>
                      <p className="text-white opacity-70 text-sm">Automatically like relevant content</p>
                    </div>
                    <div className="toggle-switch active">
                      <div className="toggle-slider"></div>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between p-4 bg-white bg-opacity-10 rounded-xl">
                    <div>
                      <h4 className="text-white font-semibold">Auto Comment</h4>
                      <p className="text-white opacity-70 text-sm">Automatically comment on relevant posts</p>
                    </div>
                    <div className="toggle-switch">
                      <div className="toggle-slider"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Success Message */}
        <div className="glass-effect rounded-2xl p-8 text-center">
          <div className="celebration">
            <h2 className="text-2xl font-bold mb-4 text-white flex items-center justify-center">
              🎉 Ready to Grow Your Social Presence!
            </h2>
            <p className="text-white opacity-90 mb-6">Your SocialSeed dashboard is configured and ready to help you build an amazing social media presence across multiple platforms.</p>
            <button
              onClick={handleConnectAccount}
              className="btn-primary px-8 py-4 rounded-xl text-white font-bold text-lg flex items-center mx-auto"
            >
              <i className="fas fa-rocket mr-3"></i>Start Growing Now!
            </button>
          </div>
        </div>
      </div>

      {/* TikTok OAuth Login Modal */}
      <TikTokOAuthLogin
        isOpen={showTikTokLogin}
        onClose={() => setShowTikTokLogin(false)}
        onSuccess={handleLoginSuccess}
      />

      {/* Chart.js Script */}
      <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </div>
  );
};

// Extend window object for Chart.js
declare global {
  interface Window {
    Chart: any;
  }
}

export default LandingPage;
