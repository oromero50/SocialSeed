'use client';

import React, { useEffect } from 'react';

interface MarketingLandingPageProps {
  onGetStarted: () => void;
}

const MarketingLandingPage: React.FC<MarketingLandingPageProps> = ({ onGetStarted }) => {
  useEffect(() => {
    // Initialize charts
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
    script.onload = () => {
      initializeCharts();
    };
    document.head.appendChild(script);

    return () => {
      if (document.head.contains(script)) {
        document.head.removeChild(script);
      }
    };
  }, []);

  const initializeCharts = () => {
    if (!window.Chart) return;

    // Trend Chart
    const trendCanvas = document.getElementById('trendChart') as HTMLCanvasElement;
    if (trendCanvas) {
      const trendCtx = trendCanvas.getContext('2d');
      new window.Chart(trendCtx, {
        type: 'line',
        data: {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
          datasets: [{
            label: 'Trending Score',
            data: [30, 45, 62, 58, 75, 89],
            borderColor: 'rgb(147, 51, 234)',
            backgroundColor: 'rgba(147, 51, 234, 0.1)',
            fill: true,
            tension: 0.4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            y: { beginAtZero: true, grid: { color: 'rgba(0,0,0,0.1)' } },
            x: { grid: { color: 'rgba(0,0,0,0.1)' } }
          }
        }
      });
    }

    // Performance Chart
    const performanceCanvas = document.getElementById('performanceChart') as HTMLCanvasElement;
    if (performanceCanvas) {
      const performanceCtx = performanceCanvas.getContext('2d');
      new window.Chart(performanceCtx, {
        type: 'bar',
        data: {
          labels: ['TikTok', 'Instagram', 'Twitter', 'YouTube'],
          datasets: [{
            label: 'Engagement Rate',
            data: [85, 72, 91, 68],
            backgroundColor: [
              'rgba(236, 72, 153, 0.8)',
              'rgba(147, 51, 234, 0.8)',
              'rgba(59, 130, 246, 0.8)',
              'rgba(239, 68, 68, 0.8)'
            ]
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            y: { beginAtZero: true, max: 100, grid: { color: 'rgba(0,0,0,0.1)' } },
            x: { grid: { color: 'rgba(0,0,0,0.1)' } }
          }
        }
      });
    }
  };

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="bg-gray-50">
      <style jsx>{`
        * { font-family: 'Inter', sans-serif; }
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .gradient-text { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .hero-gradient { background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); }
        .card-shadow { box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04); }
        .platform-icon { transition: all 0.3s ease; }
        .platform-icon:hover { transform: scale(1.1) rotate(5deg); }
        .feature-card { transition: all 0.3s ease; }
        .feature-card:hover { transform: translateY(-8px); }
        .animate-float { animation: float 6s ease-in-out infinite; }
        @keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-20px); } }
        .animate-pulse-slow { animation: pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
        .mockup-dashboard { background: linear-gradient(145deg, #f8fafc, #e2e8f0); border: 2px solid #e2e8f0; }
        .chart-container { position: relative; height: 300px; }
      `}</style>

      {/* Navigation */}
      <nav className="bg-white shadow-lg fixed w-full z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <span className="text-2xl font-bold gradient-text">SocialSeed</span>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <button onClick={() => scrollToSection('features')} className="text-gray-700 hover:text-purple-600 px-3 py-2 text-sm font-medium">Features</button>
              <button onClick={() => scrollToSection('api')} className="text-gray-700 hover:text-purple-600 px-3 py-2 text-sm font-medium">Developer API</button>
              <button onClick={() => scrollToSection('pricing')} className="text-gray-700 hover:text-purple-600 px-3 py-2 text-sm font-medium">Pricing</button>
              <button 
                onClick={onGetStarted}
                className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
              >
                Get Started Free
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="hero-gradient pt-20 pb-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="animate-float">
            <h1 className="text-5xl md:text-6xl font-bold text-white mb-6">
              Supercharge Your Social Media Growth
            </h1>
            <p className="text-xl md:text-2xl text-purple-100 mb-8 max-w-3xl mx-auto">
              Seed videos across platforms, analyze trends, manage communications, and monitor performance - all in one powerful dashboard
            </p>
          </div>
          
          {/* Platform Icons */}
          <div className="flex justify-center space-x-8 mb-12">
            <div className="platform-icon bg-white rounded-full p-4">
              <i className="fab fa-tiktok text-3xl text-pink-500"></i>
            </div>
            <div className="platform-icon bg-white rounded-full p-4">
              <i className="fab fa-instagram text-3xl text-purple-500"></i>
            </div>
            <div className="platform-icon bg-white rounded-full p-4">
              <i className="fab fa-twitter text-3xl text-blue-500"></i>
            </div>
            <div className="platform-icon bg-white rounded-full p-4">
              <i className="fab fa-youtube text-3xl text-red-500"></i>
            </div>
          </div>

          {/* CTAs */}
          <div className="space-x-4">
            <button 
              onClick={onGetStarted}
              className="bg-white text-purple-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-100 transition-colors card-shadow"
            >
              <i className="fas fa-rocket mr-2"></i>Get Started Free
            </button>
            <button 
              onClick={() => scrollToSection('api')}
              className="border-2 border-white text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-white hover:text-purple-600 transition-all"
            >
              <i className="fas fa-code mr-2"></i>Request API Access
            </button>
          </div>

          {/* Hero Dashboard Mockup */}
          <div className="mt-16 max-w-5xl mx-auto">
            <div className="mockup-dashboard rounded-2xl p-6 card-shadow">
              <div className="bg-gradient-to-r from-purple-500 to-blue-600 h-12 rounded-t-lg mb-4 flex items-center px-4">
                <div className="flex space-x-2">
                  <div className="w-3 h-3 bg-red-400 rounded-full"></div>
                  <div className="w-3 h-3 bg-yellow-400 rounded-full"></div>
                  <div className="w-3 h-3 bg-green-400 rounded-full"></div>
                </div>
                <div className="flex-1 text-center">
                  <span className="text-white font-medium">SocialSeed Dashboard</span>
                </div>
              </div>
              <div className="grid grid-cols-4 gap-4 mb-4">
                <div className="bg-purple-100 p-4 rounded-lg text-center">
                  <div className="text-2xl font-bold text-purple-600">1,247</div>
                  <div className="text-sm text-gray-600">Total Followers</div>
                </div>
                <div className="bg-blue-100 p-4 rounded-lg text-center">
                  <div className="text-2xl font-bold text-blue-600">89.3%</div>
                  <div className="text-sm text-gray-600">Engagement</div>
                </div>
                <div className="bg-green-100 p-4 rounded-lg text-center">
                  <div className="text-2xl font-bold text-green-600">324</div>
                  <div className="text-sm text-gray-600">Posts Seeded</div>
                </div>
                <div className="bg-pink-100 p-4 rounded-lg text-center">
                  <div className="text-2xl font-bold text-pink-600">45.2K</div>
                  <div className="text-sm text-gray-600">Total Reach</div>
                </div>
              </div>
              <div className="bg-gray-100 h-32 rounded-lg flex items-center justify-center">
                <div className="text-gray-500 text-center">
                  <i className="fas fa-chart-line text-4xl mb-2"></i>
                  <div>Interactive Analytics Dashboard</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold gradient-text mb-4">Powerful Features for Modern Creators</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">Everything you need to grow your social media presence across multiple platforms</p>
          </div>

          {/* Video Seeding Feature */}
          <div className="mb-24">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              <div>
                <div className="flex items-center mb-6">
                  <div className="bg-purple-100 p-3 rounded-lg mr-4">
                    <i className="fas fa-video text-2xl text-purple-600"></i>
                  </div>
                  <h3 className="text-3xl font-bold text-gray-900">Video Seeding Across Platforms 🎬</h3>
                </div>
                <p className="text-lg text-gray-600 mb-6">Automatically distribute your content across TikTok, Instagram, Twitter, and more with intelligent optimization for each platform's unique requirements.</p>
                <ul className="space-y-3">
                  <li className="flex items-center">
                    <i className="fas fa-check text-green-500 mr-3"></i>
                    <span>Automated cross-platform distribution</span>
                  </li>
                  <li className="flex items-center">
                    <i className="fas fa-check text-green-500 mr-3"></i>
                    <span>Platform-specific optimization</span>
                  </li>
                  <li className="flex items-center">
                    <i className="fas fa-check text-green-500 mr-3"></i>
                    <span>Bulk scheduling and management</span>
                  </li>
                </ul>
              </div>
              <div className="bg-gradient-to-br from-purple-400 to-blue-500 rounded-2xl p-8 text-white">
                <div className="bg-white bg-opacity-20 rounded-lg p-6 mb-4">
                  <div className="flex items-center justify-between mb-4">
                    <span className="font-semibold">Content Distribution</span>
                    <i className="fas fa-share-alt"></i>
                  </div>
                  <div className="space-y-3">
                    <div className="flex items-center">
                      <i className="fab fa-tiktok mr-3"></i>
                      <div className="flex-1 bg-white bg-opacity-30 rounded-full h-2">
                        <div className="bg-pink-300 h-2 rounded-full" style={{width: '85%'}}></div>
                      </div>
                    </div>
                    <div className="flex items-center">
                      <i className="fab fa-instagram mr-3"></i>
                      <div className="flex-1 bg-white bg-opacity-30 rounded-full h-2">
                        <div className="bg-purple-300 h-2 rounded-full" style={{width: '72%'}}></div>
                      </div>
                    </div>
                    <div className="flex items-center">
                      <i className="fab fa-twitter mr-3"></i>
                      <div className="flex-1 bg-white bg-opacity-30 rounded-full h-2">
                        <div className="bg-blue-300 h-2 rounded-full" style={{width: '91%'}}></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Trends Analysis Feature */}
          <div className="mb-24">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              <div className="order-2 lg:order-1">
                <div className="bg-white border-2 border-gray-200 rounded-2xl p-6 card-shadow">
                  <div className="mb-4">
                    <h4 className="font-semibold text-gray-800 mb-2">Trending Topics Analysis</h4>
                    <div className="chart-container">
                      <canvas id="trendChart"></canvas>
                    </div>
                  </div>
                </div>
              </div>
              <div className="order-1 lg:order-2">
                <div className="flex items-center mb-6">
                  <div className="bg-blue-100 p-3 rounded-lg mr-4">
                    <i className="fas fa-chart-line text-2xl text-blue-600"></i>
                  </div>
                  <h3 className="text-3xl font-bold text-gray-900">Trends Analysis & Insights 📈</h3>
                </div>
                <p className="text-lg text-gray-600 mb-6">Stay ahead of the curve with real-time trend analysis and competitive insights across all your social platforms.</p>
                <ul className="space-y-3">
                  <li className="flex items-center">
                    <i className="fas fa-check text-green-500 mr-3"></i>
                    <span>Real-time trending topics detection</span>
                  </li>
                  <li className="flex items-center">
                    <i className="fas fa-check text-green-500 mr-3"></i>
                    <span>Competitive analysis and benchmarking</span>
                  </li>
                  <li className="flex items-center">
                    <i className="fas fa-check text-green-500 mr-3"></i>
                    <span>Predictive trend forecasting</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          {/* Message Management Feature */}
          <div className="mb-24">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              <div>
                <div className="flex items-center mb-6">
                  <div className="bg-green-100 p-3 rounded-lg mr-4">
                    <i className="fas fa-comments text-2xl text-green-600"></i>
                  </div>
                  <h3 className="text-3xl font-bold text-gray-900">Message & Communication Management 💬</h3>
                </div>
                <p className="text-lg text-gray-600 mb-6">Centralize all your social media interactions in one unified inbox with smart automation and response tools.</p>
                <ul className="space-y-3">
                  <li className="flex items-center">
                    <i className="fas fa-check text-green-500 mr-3"></i>
                    <span>Unified inbox for all platforms</span>
                  </li>
                  <li className="flex items-center">
                    <i className="fas fa-check text-green-500 mr-3"></i>
                    <span>AI-powered response suggestions</span>
                  </li>
                  <li className="flex items-center">
                    <i className="fas fa-check text-green-500 mr-3"></i>
                    <span>Team collaboration tools</span>
                  </li>
                </ul>
              </div>
              <div className="bg-gray-50 rounded-2xl p-6 border-2 border-gray-200">
                <div className="bg-white rounded-lg p-4 mb-3 border-l-4 border-pink-400">
                  <div className="flex items-center mb-2">
                    <i className="fab fa-tiktok text-pink-500 mr-2"></i>
                    <span className="font-semibold text-sm">TikTok</span>
                    <span className="text-xs text-gray-500 ml-auto">2m ago</span>
                  </div>
                  <p className="text-sm text-gray-700">"Love this content! Can you make more?"</p>
                </div>
                <div className="bg-white rounded-lg p-4 mb-3 border-l-4 border-purple-400">
                  <div className="flex items-center mb-2">
                    <i className="fab fa-instagram text-purple-500 mr-2"></i>
                    <span className="font-semibold text-sm">Instagram</span>
                    <span className="text-xs text-gray-500 ml-auto">5m ago</span>
                  </div>
                  <p className="text-sm text-gray-700">"Amazing tutorial! Following for more tips 🔥"</p>
                </div>
                <div className="bg-white rounded-lg p-4 border-l-4 border-blue-400">
                  <div className="flex items-center mb-2">
                    <i className="fab fa-twitter text-blue-500 mr-2"></i>
                    <span className="font-semibold text-sm">Twitter</span>
                    <span className="text-xs text-gray-500 ml-auto">8m ago</span>
                  </div>
                  <p className="text-sm text-gray-700">"Retweeted with comment: This is gold! 💎"</p>
                </div>
              </div>
            </div>
          </div>

          {/* Performance Monitoring Feature */}
          <div className="mb-24">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              <div className="order-2 lg:order-1">
                <div className="bg-white border-2 border-gray-200 rounded-2xl p-6 card-shadow">
                  <div className="grid grid-cols-2 gap-4 mb-4">
                    <div className="bg-purple-50 p-4 rounded-lg text-center">
                      <div className="text-2xl font-bold text-purple-600">234%</div>
                      <div className="text-sm text-gray-600">Growth Rate</div>
                    </div>
                    <div className="bg-blue-50 p-4 rounded-lg text-center">
                      <div className="text-2xl font-bold text-blue-600">$12.4K</div>
                      <div className="text-sm text-gray-600">Revenue</div>
                    </div>
                  </div>
                  <div className="chart-container">
                    <canvas id="performanceChart"></canvas>
                  </div>
                </div>
              </div>
              <div className="order-1 lg:order-2">
                <div className="flex items-center mb-6">
                  <div className="bg-orange-100 p-3 rounded-lg mr-4">
                    <i className="fas fa-chart-bar text-2xl text-orange-600"></i>
                  </div>
                  <h3 className="text-3xl font-bold text-gray-900">Performance Monitoring 📊</h3>
                </div>
                <p className="text-lg text-gray-600 mb-6">Track your growth across all platforms with detailed analytics, ROI measurements, and performance benchmarking.</p>
                <ul className="space-y-3">
                  <li className="flex items-center">
                    <i className="fas fa-check text-green-500 mr-3"></i>
                    <span>Cross-platform analytics dashboard</span>
                  </li>
                  <li className="flex items-center">
                    <i className="fas fa-check text-green-500 mr-3"></i>
                    <span>ROI tracking and optimization</span>
                  </li>
                  <li className="flex items-center">
                    <i className="fas fa-check text-green-500 mr-3"></i>
                    <span>Custom reporting and exports</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Developer API Section */}
      <section id="api" className="py-20 gradient-bg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">Developer API & Integration</h2>
            <p className="text-xl text-purple-100 max-w-3xl mx-auto">Powerful APIs and SDKs to integrate SocialSeed's capabilities into your own applications</p>
          </div>

          <div className="grid lg:grid-cols-3 gap-8">
            <div className="feature-card bg-white rounded-2xl p-8 card-shadow">
              <div className="bg-purple-100 w-16 h-16 rounded-lg flex items-center justify-center mb-6">
                <i className="fab fa-tiktok text-2xl text-purple-600"></i>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">TikTok API Integration</h3>
              <p className="text-gray-600 mb-4">Direct integration with TikTok's developer API for seamless content management and analytics.</p>
              <ul className="text-sm text-gray-600 space-y-2">
                <li>✓ Content publishing and management</li>
                <li>✓ User analytics and insights</li>
                <li>✓ Trend analysis and discovery</li>
              </ul>
            </div>

            <div className="feature-card bg-white rounded-2xl p-8 card-shadow">
              <div className="bg-blue-100 w-16 h-16 rounded-lg flex items-center justify-center mb-6">
                <i className="fas fa-code text-2xl text-blue-600"></i>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">RESTful APIs</h3>
              <p className="text-gray-600 mb-4">Complete REST API suite for all SocialSeed functionality with comprehensive documentation.</p>
              <ul className="text-sm text-gray-600 space-y-2">
                <li>✓ Easy integration and setup</li>
                <li>✓ Comprehensive documentation</li>
                <li>✓ Rate limiting and authentication</li>
              </ul>
            </div>

            <div className="feature-card bg-white rounded-2xl p-8 card-shadow">
              <div className="bg-green-100 w-16 h-16 rounded-lg flex items-center justify-center mb-6">
                <i className="fas fa-shield-alt text-2xl text-green-600"></i>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">Enterprise Security</h3>
              <p className="text-gray-600 mb-4">Enterprise-grade security with OAuth 2.0, API keys, and comprehensive audit logs.</p>
              <ul className="text-sm text-gray-600 space-y-2">
                <li>✓ OAuth 2.0 authentication</li>
                <li>✓ API key management</li>
                <li>✓ Audit logs and monitoring</li>
              </ul>
            </div>
          </div>

          {/* API Documentation Preview */}
          <div className="mt-16 bg-gray-900 rounded-2xl p-8 card-shadow">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-bold text-white">API Documentation Preview</h3>
              <button className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg text-sm transition-colors">
                View Full Docs
              </button>
            </div>
            <div className="bg-gray-800 rounded-lg p-4 text-sm">
              <div className="text-green-400 mb-2"># Seed content across platforms</div>
              <div className="text-white">
                <span className="text-purple-400">POST</span> 
                <span className="text-blue-400">/api/v1/content/seed</span>
              </div>
              <div className="text-gray-400 mt-2">
                {`{`}<br />
                &nbsp;&nbsp;"platforms": ["tiktok", "instagram", "twitter"],<br />
                &nbsp;&nbsp;"content": {`{`}<br />
                &nbsp;&nbsp;&nbsp;&nbsp;"video_url": "https://example.com/video.mp4",<br />
                &nbsp;&nbsp;&nbsp;&nbsp;"caption": "Check out this amazing content!"<br />
                &nbsp;&nbsp;{`}`}<br />
                {`}`}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Social Proof & Stats */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Trusted by Creators Worldwide</h2>
            <p className="text-xl text-gray-600">Join thousands of content creators and businesses growing their social presence</p>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
            <div className="text-center">
              <div className="text-4xl font-bold gradient-text mb-2">50K+</div>
              <div className="text-gray-600">Active Users</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold gradient-text mb-2">2M+</div>
              <div className="text-gray-600">Content Pieces Seeded</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold gradient-text mb-2">5+</div>
              <div className="text-gray-600">Platforms Supported</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold gradient-text mb-2">98%</div>
              <div className="text-gray-600">Customer Satisfaction</div>
            </div>
          </div>

          {/* Testimonials */}
          <div className="grid lg:grid-cols-3 gap-8">
            <div className="bg-purple-50 rounded-2xl p-6">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-purple-200 rounded-full flex items-center justify-center">
                  <i className="fas fa-user text-purple-600"></i>
                </div>
                <div className="ml-4">
                  <div className="font-semibold text-gray-900">Sarah Chen</div>
                  <div className="text-sm text-gray-600">Content Creator</div>
                </div>
              </div>
              <p className="text-gray-700">"SocialSeed helped me grow from 1K to 100K followers across all platforms in just 6 months. The automation features are a game-changer!"</p>
            </div>

            <div className="bg-blue-50 rounded-2xl p-6">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-blue-200 rounded-full flex items-center justify-center">
                  <i className="fas fa-user text-blue-600"></i>
                </div>
                <div className="ml-4">
                  <div className="font-semibold text-gray-900">Marcus Johnson</div>
                  <div className="text-sm text-gray-600">Marketing Director</div>
                </div>
              </div>
              <p className="text-gray-700">"The API integration was seamless. We've automated our entire social media workflow and seen a 300% increase in engagement."</p>
            </div>

            <div className="bg-green-50 rounded-2xl p-6">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-green-200 rounded-full flex items-center justify-center">
                  <i className="fas fa-user text-green-600"></i>
                </div>
                <div className="ml-4">
                  <div className="font-semibold text-gray-900">Lisa Rodriguez</div>
                  <div className="text-sm text-gray-600">Agency Owner</div>
                </div>
              </div>
              <p className="text-gray-700">"Managing multiple clients' social media accounts has never been easier. SocialSeed's unified dashboard is incredibly powerful."</p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Choose Your Plan</h2>
            <p className="text-xl text-gray-600">Start free and scale as you grow</p>
          </div>

          <div className="grid lg:grid-cols-3 gap-8">
            {/* Starter Plan */}
            <div className="bg-white rounded-2xl p-8 card-shadow">
              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold text-gray-900 mb-2">Starter</h3>
                <div className="text-4xl font-bold gradient-text mb-2">Free</div>
                <p className="text-gray-600">Perfect for individual creators</p>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center">
                  <i className="fas fa-check text-green-500 mr-3"></i>
                  <span>2 social platforms</span>
                </li>
                <li className="flex items-center">
                  <i className="fas fa-check text-green-500 mr-3"></i>
                  <span>10 posts per month</span>
                </li>
                <li className="flex items-center">
                  <i className="fas fa-check text-green-500 mr-3"></i>
                  <span>Basic analytics</span>
                </li>
                <li className="flex items-center">
                  <i className="fas fa-check text-green-500 mr-3"></i>
                  <span>Community support</span>
                </li>
              </ul>
              <button 
                onClick={onGetStarted}
                className="w-full bg-purple-600 hover:bg-purple-700 text-white py-3 rounded-lg font-semibold transition-colors"
              >
                Get Started Free
              </button>
            </div>

            {/* Pro Plan */}
            <div className="bg-gradient-to-br from-purple-500 to-blue-600 text-white rounded-2xl p-8 card-shadow transform scale-105">
              <div className="text-center mb-6">
                <div className="bg-yellow-400 text-purple-900 px-3 py-1 rounded-full text-sm font-semibold inline-block mb-2">Most Popular</div>
                <h3 className="text-2xl font-bold mb-2">Pro</h3>
                <div className="text-4xl font-bold mb-2">$29<span className="text-lg">/month</span></div>
                <p className="text-purple-100">For growing creators and businesses</p>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center">
                  <i className="fas fa-check text-green-300 mr-3"></i>
                  <span>All platforms supported</span>
                </li>
                <li className="flex items-center">
                  <i className="fas fa-check text-green-300 mr-3"></i>
                  <span>Unlimited posts</span>
                </li>
                <li className="flex items-center">
                  <i className="fas fa-check text-green-300 mr-3"></i>
                  <span>Advanced analytics & trends</span>
                </li>
                <li className="flex items-center">
                  <i className="fas fa-check text-green-300 mr-3"></i>
                  <span>Priority support</span>
                </li>
                <li className="flex items-center">
                  <i className="fas fa-check text-green-300 mr-3"></i>
                  <span>API access</span>
                </li>
              </ul>
              <button 
                onClick={onGetStarted}
                className="w-full bg-white text-purple-600 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
              >
                Start Pro Trial
              </button>
            </div>

            {/* Enterprise Plan */}
            <div className="bg-white rounded-2xl p-8 card-shadow">
              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold text-gray-900 mb-2">Enterprise</h3>
                <div className="text-4xl font-bold gradient-text mb-2">Custom</div>
                <p className="text-gray-600">For agencies and large teams</p>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center">
                  <i className="fas fa-check text-green-500 mr-3"></i>
                  <span>Unlimited everything</span>
                </li>
                <li className="flex items-center">
                  <i className="fas fa-check text-green-500 mr-3"></i>
                  <span>White-label solution</span>
                </li>
                <li className="flex items-center">
                  <i className="fas fa-check text-green-500 mr-3"></i>
                  <span>Custom integrations</span>
                </li>
                <li className="flex items-center">
                  <i className="fas fa-check text-green-500 mr-3"></i>
                  <span>Dedicated support</span>
                </li>
                <li className="flex items-center">
                  <i className="fas fa-check text-green-500 mr-3"></i>
                  <span>SLA guarantees</span>
                </li>
              </ul>
              <button className="w-full bg-gray-900 hover:bg-gray-800 text-white py-3 rounded-lg font-semibold transition-colors">
                Contact Sales
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 gradient-bg">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-white mb-6">Ready to Supercharge Your Social Media Growth?</h2>
          <p className="text-xl text-purple-100 mb-8">Join thousands of creators and businesses using SocialSeed to grow their social presence</p>
          <div className="space-x-4">
            <button 
              onClick={onGetStarted}
              className="bg-white text-purple-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-100 transition-colors card-shadow"
            >
              <i className="fas fa-rocket mr-2"></i>Start Free Trial
            </button>
            <button 
              onClick={() => scrollToSection('api')}
              className="border-2 border-white text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-white hover:text-purple-600 transition-all"
            >
              <i className="fas fa-code mr-2"></i>Request API Access
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-4 gap-8">
            <div className="lg:col-span-2">
              <div className="text-2xl font-bold gradient-text mb-4">SocialSeed</div>
              <p className="text-gray-400 mb-6 max-w-md">Empowering creators and businesses to grow their social media presence across multiple platforms with intelligent automation and analytics.</p>
              <div className="flex space-x-4">
                <a href="#" className="text-gray-400 hover:text-white transition-colors">
                  <i className="fab fa-twitter text-xl"></i>
                </a>
                <a href="#" className="text-gray-400 hover:text-white transition-colors">
                  <i className="fab fa-linkedin text-xl"></i>
                </a>
                <a href="#" className="text-gray-400 hover:text-white transition-colors">
                  <i className="fab fa-github text-xl"></i>
                </a>
              </div>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Product</h3>
              <ul className="space-y-2 text-gray-400">
                <li><button onClick={() => scrollToSection('features')} className="hover:text-white transition-colors">Features</button></li>
                <li><button onClick={() => scrollToSection('pricing')} className="hover:text-white transition-colors">Pricing</button></li>
                <li><button onClick={() => scrollToSection('api')} className="hover:text-white transition-colors">API</button></li>
                <li><a href="#" className="hover:text-white transition-colors">Documentation</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">About</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Privacy Policy</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Terms of Service</a></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-12 pt-8 text-center text-gray-400">
            <p>&copy; 2024 SocialSeed. All rights reserved.</p>
          </div>
        </div>
      </footer>

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

export default MarketingLandingPage;
