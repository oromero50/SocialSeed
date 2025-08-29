'use client';

import React, { useState } from 'react';

export default function Settings() {
  const [settings, setSettings] = useState({
    notifications: {
      email: true,
      push: false,
      analytics: true
    },
    automation: {
      autoFollow: false,
      autoLike: true,
      autoComment: false,
      maxActionsPerDay: 100
    },
    safety: {
      conservativeMode: true,
      enableBreaks: true,
      randomizeTimings: true
    },
    preferences: {
      theme: 'light',
      timezone: 'UTC',
      language: 'en'
    }
  });

  const handleSave = () => {
    // Save settings to backend
    console.log('Saving settings:', settings);
    alert('Settings saved successfully!');
  };

  const resetToDefaults = () => {
    if (confirm('Are you sure you want to reset all settings to defaults?')) {
      setSettings({
        notifications: {
          email: true,
          push: false,
          analytics: true
        },
        automation: {
          autoFollow: false,
          autoLike: true,
          autoComment: false,
          maxActionsPerDay: 100
        },
        safety: {
          conservativeMode: true,
          enableBreaks: true,
          randomizeTimings: true
        },
        preferences: {
          theme: 'light',
          timezone: 'UTC',
          language: 'en'
        }
      });
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Settings</h2>
        <p className="text-gray-600">Configure your SocialSeed preferences and automation settings</p>
      </div>

      {/* Notifications */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Notifications</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <label className="text-sm font-medium text-gray-700">Email Notifications</label>
              <p className="text-sm text-gray-500">Receive important updates via email</p>
            </div>
            <input
              type="checkbox"
              checked={settings.notifications.email}
              onChange={(e) => setSettings(prev => ({
                ...prev,
                notifications: { ...prev.notifications, email: e.target.checked }
              }))}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
          </div>
          
          <div className="flex items-center justify-between">
            <div>
              <label className="text-sm font-medium text-gray-700">Push Notifications</label>
              <p className="text-sm text-gray-500">Get real-time alerts in your browser</p>
            </div>
            <input
              type="checkbox"
              checked={settings.notifications.push}
              onChange={(e) => setSettings(prev => ({
                ...prev,
                notifications: { ...prev.notifications, push: e.target.checked }
              }))}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
          </div>

          <div className="flex items-center justify-between">
            <div>
              <label className="text-sm font-medium text-gray-700">Analytics Reports</label>
              <p className="text-sm text-gray-500">Weekly analytics summaries</p>
            </div>
            <input
              type="checkbox"
              checked={settings.notifications.analytics}
              onChange={(e) => setSettings(prev => ({
                ...prev,
                notifications: { ...prev.notifications, analytics: e.target.checked }
              }))}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
          </div>
        </div>
      </div>

      {/* Automation */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Automation Settings</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <label className="text-sm font-medium text-gray-700">Auto Follow</label>
              <p className="text-sm text-gray-500">Automatically follow relevant accounts</p>
            </div>
            <input
              type="checkbox"
              checked={settings.automation.autoFollow}
              onChange={(e) => setSettings(prev => ({
                ...prev,
                automation: { ...prev.automation, autoFollow: e.target.checked }
              }))}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
          </div>

          <div className="flex items-center justify-between">
            <div>
              <label className="text-sm font-medium text-gray-700">Auto Like</label>
              <p className="text-sm text-gray-500">Automatically like relevant content</p>
            </div>
            <input
              type="checkbox"
              checked={settings.automation.autoLike}
              onChange={(e) => setSettings(prev => ({
                ...prev,
                automation: { ...prev.automation, autoLike: e.target.checked }
              }))}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
          </div>

          <div className="flex items-center justify-between">
            <div>
              <label className="text-sm font-medium text-gray-700">Auto Comment</label>
              <p className="text-sm text-gray-500">Automatically comment on relevant posts</p>
            </div>
            <input
              type="checkbox"
              checked={settings.automation.autoComment}
              onChange={(e) => setSettings(prev => ({
                ...prev,
                automation: { ...prev.automation, autoComment: e.target.checked }
              }))}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Max Actions Per Day: {settings.automation.maxActionsPerDay}
            </label>
            <input
              type="range"
              min="10"
              max="500"
              value={settings.automation.maxActionsPerDay}
              onChange={(e) => setSettings(prev => ({
                ...prev,
                automation: { ...prev.automation, maxActionsPerDay: parseInt(e.target.value) }
              }))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>Conservative (10)</span>
              <span>Aggressive (500)</span>
            </div>
          </div>
        </div>
      </div>

      {/* Safety */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Safety & Security</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <label className="text-sm font-medium text-gray-700">Conservative Mode</label>
              <p className="text-sm text-gray-500">Use extra safety measures to avoid detection</p>
            </div>
            <input
              type="checkbox"
              checked={settings.safety.conservativeMode}
              onChange={(e) => setSettings(prev => ({
                ...prev,
                safety: { ...prev.safety, conservativeMode: e.target.checked }
              }))}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
          </div>

          <div className="flex items-center justify-between">
            <div>
              <label className="text-sm font-medium text-gray-700">Enable Breaks</label>
              <p className="text-sm text-gray-500">Take random breaks between actions</p>
            </div>
            <input
              type="checkbox"
              checked={settings.safety.enableBreaks}
              onChange={(e) => setSettings(prev => ({
                ...prev,
                safety: { ...prev.safety, enableBreaks: e.target.checked }
              }))}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
          </div>

          <div className="flex items-center justify-between">
            <div>
              <label className="text-sm font-medium text-gray-700">Randomize Timings</label>
              <p className="text-sm text-gray-500">Add random delays to mimic human behavior</p>
            </div>
            <input
              type="checkbox"
              checked={settings.safety.randomizeTimings}
              onChange={(e) => setSettings(prev => ({
                ...prev,
                safety: { ...prev.safety, randomizeTimings: e.target.checked }
              }))}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
          </div>
        </div>
      </div>

      {/* Preferences */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Preferences</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Theme</label>
            <select
              value={settings.preferences.theme}
              onChange={(e) => setSettings(prev => ({
                ...prev,
                preferences: { ...prev.preferences, theme: e.target.value }
              }))}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="light">Light</option>
              <option value="dark">Dark</option>
              <option value="auto">Auto</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Timezone</label>
            <select
              value={settings.preferences.timezone}
              onChange={(e) => setSettings(prev => ({
                ...prev,
                preferences: { ...prev.preferences, timezone: e.target.value }
              }))}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="UTC">UTC</option>
              <option value="America/New_York">Eastern Time</option>
              <option value="America/Los_Angeles">Pacific Time</option>
              <option value="Europe/London">London</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Language</label>
            <select
              value={settings.preferences.language}
              onChange={(e) => setSettings(prev => ({
                ...prev,
                preferences: { ...prev.preferences, language: e.target.value }
              }))}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="en">English</option>
              <option value="es">Español</option>
              <option value="fr">Français</option>
              <option value="de">Deutsch</option>
            </select>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex justify-between">
        <button
          onClick={resetToDefaults}
          className="bg-gray-300 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-400 transition-colors"
        >
          Reset to Defaults
        </button>
        <button
          onClick={handleSave}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          Save Settings
        </button>
      </div>
    </div>
  );
}
