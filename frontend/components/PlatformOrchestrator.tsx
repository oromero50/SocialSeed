'use client';

import React, { useState, useEffect } from 'react';
import TikTokSection from './platforms/TikTokSection';
import InstagramSection from './platforms/InstagramSection';
import TwitterSection from './platforms/TwitterSection';
import EnhancedTikTokLogin from './EnhancedTikTokLogin';

interface PlatformOrchestratorProps {
  dashboardData: any;
  onRefreshData: () => void;
}

export default function PlatformOrchestrator({ dashboardData, onRefreshData }: PlatformOrchestratorProps) {
  const [currentPhase, setCurrentPhase] = useState(1);
  const [showTikTokLogin, setShowTikTokLogin] = useState(false);
  const [showInstagramLogin, setShowInstagramLogin] = useState(false);
  const [showTwitterLogin, setShowTwitterLogin] = useState(false);

  // Calculate current phase based on TikTok followers
  useEffect(() => {
    const tiktokAccounts = dashboardData?.accounts?.filter((acc: any) => acc.platform === 'tiktok') || [];
    const totalFollowers = tiktokAccounts.reduce((sum: number, acc: any) => sum + (acc.follower_count || 0), 0);
    
    if (totalFollowers >= 5000) {
      setCurrentPhase(3); // Full platform suite
    } else if (totalFollowers >= 1000) {
      setCurrentPhase(2); // TikTok + Instagram
    } else {
      setCurrentPhase(1); // TikTok only
    }
  }, [dashboardData]);

  const getPhaseInfo = (phase: number) => {
    const phases = {
      1: {
        title: "Phase 1: TikTok Foundation",
        description: "Build viral content and grow your TikTok presence",
        platforms: ["TikTok"],
        goal: "Reach 1,000 followers to unlock Instagram",
        color: "from-pink-500 to-purple-600"
      },
      2: {
        title: "Phase 2: Cross-Platform Growth", 
        description: "Expand to Instagram for professional presence",
        platforms: ["TikTok", "Instagram"],
        goal: "Reach 5,000 followers to unlock Twitter",
        color: "from-purple-500 to-blue-600"
      },
      3: {
        title: "Phase 3: Full Platform Suite",
        description: "Complete multi-platform orchestration",
        platforms: ["TikTok", "Instagram", "Twitter"],
        goal: "Scale and monetize your audience",
        color: "from-blue-500 to-green-600"
      }
    };
    return phases[phase as keyof typeof phases];
  };

  const platformData = {
    tiktok: dashboardData?.accounts?.filter((acc: any) => acc.platform === 'tiktok') || [],
    instagram: dashboardData?.accounts?.filter((acc: any) => acc.platform === 'instagram') || [],
    twitter: dashboardData?.accounts?.filter((acc: any) => acc.platform === 'twitter') || []
  };

  const phaseInfo = getPhaseInfo(currentPhase);

  return (
    <div className="space-y-6">
      {/* Phase Progress Header */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">{phaseInfo.title}</h2>
            <p className="text-gray-600">{phaseInfo.description}</p>
          </div>
          <div className={`bg-gradient-to-r ${phaseInfo.color} text-white px-4 py-2 rounded-lg font-medium`}>
            Phase {currentPhase}/3
          </div>
        </div>

        {/* Phase Progress Bar */}
        <div className="mb-4">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>Progress</span>
            <span>{phaseInfo.goal}</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div 
              className={`bg-gradient-to-r ${phaseInfo.color} h-3 rounded-full transition-all duration-500`}
              style={{ width: `${Math.min((currentPhase / 3) * 100, 100)}%` }}
            ></div>
          </div>
        </div>

        {/* Platform Status Indicators */}
        <div className="flex space-x-4">
          <div className={`flex items-center space-x-2 px-3 py-2 rounded-lg ${
            currentPhase >= 1 ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'
          }`}>
            <div className={`w-3 h-3 rounded-full ${currentPhase >= 1 ? 'bg-green-500' : 'bg-gray-400'}`}></div>
            <span className="text-sm font-medium">TikTok</span>
          </div>
          <div className={`flex items-center space-x-2 px-3 py-2 rounded-lg ${
            currentPhase >= 2 ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'
          }`}>
            <div className={`w-3 h-3 rounded-full ${currentPhase >= 2 ? 'bg-green-500' : 'bg-gray-400'}`}></div>
            <span className="text-sm font-medium">Instagram</span>
          </div>
          <div className={`flex items-center space-x-2 px-3 py-2 rounded-lg ${
            currentPhase >= 3 ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'
          }`}>
            <div className={`w-3 h-3 rounded-full ${currentPhase >= 3 ? 'bg-green-500' : 'bg-gray-400'}`}></div>
            <span className="text-sm font-medium">Twitter</span>
          </div>
        </div>
      </div>

      {/* TikTok Section - Always Available */}
      <TikTokSection
        accounts={platformData.tiktok}
        onAddAccount={() => setShowTikTokLogin(true)}
        onRefreshData={onRefreshData}
      />

      {/* Instagram Section - Phase 2+ */}
      <InstagramSection
        accounts={platformData.instagram}
        onAddAccount={() => setShowInstagramLogin(true)}
        onRefreshData={onRefreshData}
        isEnabled={currentPhase >= 2}
      />

      {/* Twitter Section - Phase 3+ */}
      <TwitterSection
        accounts={platformData.twitter}
        onAddAccount={() => setShowTwitterLogin(true)}
        onRefreshData={onRefreshData}
        isEnabled={currentPhase >= 3}
      />

      {/* Modals */}
      {showTikTokLogin && (
        <EnhancedTikTokLogin
          onSuccess={(accountData) => {
            console.log('✅ TikTok account connected:', accountData);
            setShowTikTokLogin(false);
            onRefreshData();
          }}
          onCancel={() => setShowTikTokLogin(false)}
        />
      )}

      {showInstagramLogin && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-lg font-semibold mb-4">Instagram Login</h3>
            <p className="text-gray-600 mb-4">Instagram integration coming soon! Focus on TikTok growth first.</p>
            <button
              onClick={() => setShowInstagramLogin(false)}
              className="w-full bg-purple-600 text-white py-2 rounded-lg hover:bg-purple-700 transition-colors"
            >
              Got It
            </button>
          </div>
        </div>
      )}

      {showTwitterLogin && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-lg font-semibold mb-4">Twitter Login</h3>
            <p className="text-gray-600 mb-4">Twitter integration coming soon! Build your TikTok and Instagram presence first.</p>
            <button
              onClick={() => setShowTwitterLogin(false)}
              className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Got It
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
