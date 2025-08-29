#!/usr/bin/env python3
"""
TikTok Data Extraction Service for SocialSeed
Integrated with Supabase for historical metrics storage

Based on the comprehensive TikTok extraction suite with three methods:
- Playwright Browser Automation
- TikTok-Api Library 
- Mobile API Direct

Author: SocialSeed Team
"""

import asyncio
import json
import time
import random
import hashlib
import hmac
import base64
import urllib.parse
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import requests
import logging
from playwright.async_api import async_playwright
from supabase import Client

logger = logging.getLogger(__name__)

class TikTokPlaywrightExtractor:
    """Browser automation extractor with anti-detection"""
    
    def __init__(self, headless: bool = True, proxy: Optional[str] = None):
        self.headless = headless
        self.proxy = proxy
        self.browser = None
        self.context = None
        self.page = None
        self.rate_limiter = {
            'last_request': 0,
            'min_delay': 2.0,
            'max_delay': 5.0
        }

    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        await self.playwright.stop()

    async def setup_browser(self, user_agent: Optional[str] = None):
        """Initialize browser with anti-detection settings"""
        if not user_agent:
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=['--no-sandbox', '--disable-blink-features=AutomationControlled'],
            proxy={"server": self.proxy} if self.proxy else None
        )

        self.context = await self.browser.new_context(
            user_agent=user_agent,
            viewport={'width': 1920, 'height': 1080}
        )

        self.page = await self.context.new_page()
        logger.info("✓ Browser setup completed")

    async def rate_limit(self):
        """Implement rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.rate_limiter['last_request']
        delay = random.uniform(self.rate_limiter['min_delay'], self.rate_limiter['max_delay'])

        if time_since_last < delay:
            await asyncio.sleep(delay - time_since_last)

        self.rate_limiter['last_request'] = time.time()

    async def get_user_profile(self, username: str) -> Dict[str, Any]:
        """Extract complete user profile data"""
        await self.rate_limit()

        try:
            url = f"https://www.tiktok.com/@{username}"
            await self.page.goto(url, wait_until='domcontentloaded', timeout=30000)
            await self.page.wait_for_selector('[data-e2e="user-page"]', timeout=10000)

            profile_data = await self.page.evaluate("""
                () => {
                    function parseCount(text) {
                        if (!text) return 0;
                        text = text.toLowerCase().replace(/[^0-9.kmb]/g, '');
                        const num = parseFloat(text);
                        if (text.includes('k')) return Math.floor(num * 1000);
                        if (text.includes('m')) return Math.floor(num * 1000000);
                        if (text.includes('b')) return Math.floor(num * 1000000000);
                        return Math.floor(num) || 0;
                    }

                    const data = {
                        username: '',
                        display_name: '',
                        follower_count: 0,
                        following_count: 0,
                        like_count: 0,
                        video_count: 0,
                        avatar_url: '',
                        bio: '',
                        is_verified: false,
                        is_private: false
                    };

                    const usernameEl = document.querySelector('[data-e2e="user-subtitle"]');
                    if (usernameEl) data.username = usernameEl.textContent.trim();

                    const nameEl = document.querySelector('[data-e2e="user-title"]');
                    if (nameEl) data.display_name = nameEl.textContent.trim();

                    const followersEl = document.querySelector('[data-e2e="followers-count"]');
                    if (followersEl) data.follower_count = parseCount(followersEl.textContent.trim());

                    const followingEl = document.querySelector('[data-e2e="following-count"]');
                    if (followingEl) data.following_count = parseCount(followingEl.textContent.trim());

                    const likesEl = document.querySelector('[data-e2e="likes-count"]');
                    if (likesEl) data.like_count = parseCount(likesEl.textContent.trim());

                    const avatarEl = document.querySelector('[data-e2e="user-avatar"] img');
                    if (avatarEl) data.avatar_url = avatarEl.src;

                    const bioEl = document.querySelector('[data-e2e="user-bio"]');
                    if (bioEl) data.bio = bioEl.textContent.trim();

                    const verifiedEl = document.querySelector('[data-e2e="user-verified"]');
                    data.is_verified = !!verifiedEl;

                    return data;
                }
            """)

            profile_data['extracted_at'] = datetime.now().isoformat()
            profile_data['source'] = 'playwright'
            
            logger.info(f"✓ Extracted profile data for @{username}")
            return profile_data

        except Exception as e:
            logger.error(f"✗ Error extracting profile for @{username}: {str(e)}")
            return {'error': str(e)}

    async def get_followers_list(self, username: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Extract followers list with pagination"""
        await self.rate_limit()

        try:
            followers_url = f"https://www.tiktok.com/@{username}/followers"
            await self.page.goto(followers_url, wait_until='domcontentloaded', timeout=30000)

            followers = []
            processed_users = set()
            scroll_attempts = 0
            max_scrolls = 50

            while len(followers) < limit and scroll_attempts < max_scrolls:
                await self.rate_limit()

                new_followers = await self.page.evaluate("""
                    () => {
                        const followerElements = document.querySelectorAll(
                            '[data-e2e="user-item"], [data-e2e="followers-item"], .user-item'
                        );

                        return Array.from(followerElements).map(el => {
                            const data = {
                                username: '',
                                display_name: '',
                                avatar_url: '',
                                is_verified: false,
                                user_id: ''
                            };

                            const usernameEl = el.querySelector('[data-e2e="user-username"]');
                            if (usernameEl) data.username = usernameEl.textContent.trim().replace('@', '');

                            const nameEl = el.querySelector('[data-e2e="user-name"]');
                            if (nameEl) data.display_name = nameEl.textContent.trim();

                            const avatarEl = el.querySelector('img[src*="avatar"]');
                            if (avatarEl) data.avatar_url = avatarEl.src;

                            const verifiedEl = el.querySelector('[data-e2e="user-verified"]');
                            data.is_verified = !!verifiedEl;

                            data.user_id = data.username || Math.random().toString(36);

                            return data;
                        }).filter(user => user.username);
                    }
                """)

                for follower in new_followers:
                    if follower['user_id'] not in processed_users and len(followers) < limit:
                        followers.append(follower)
                        processed_users.add(follower['user_id'])

                if len(followers) < limit:
                    await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    await asyncio.sleep(random.uniform(2, 4))

                    if len(new_followers) == 0:
                        scroll_attempts += 1
                    else:
                        scroll_attempts = 0

            timestamp = datetime.now().isoformat()
            for follower in followers:
                follower['extracted_at'] = timestamp

            logger.info(f"✓ Extracted {len(followers)} followers for @{username}")
            return followers

        except Exception as e:
            logger.error(f"✗ Error extracting followers for @{username}: {str(e)}")
            return []

    async def close(self):
        """Clean up browser resources"""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()


class TikTokApiExtractor:
    """TikTok-Api library based extractor"""
    
    def __init__(self, ms_token: str = None, proxy: Optional[str] = None):
        self.ms_token = ms_token
        self.proxy = proxy
        self.session = requests.Session()
        self.rate_limiter = {'last_request': 0, 'min_delay': 1.0, 'max_delay': 3.0}

        if proxy:
            self.session.proxies.update({'http': proxy, 'https': proxy})

    def rate_limit(self):
        """Rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.rate_limiter['last_request']
        delay = random.uniform(self.rate_limiter['min_delay'], self.rate_limiter['max_delay'])

        if time_since_last < delay:
            time.sleep(delay - time_since_last)

        self.rate_limiter['last_request'] = time.time()

    def get_user_info(self, username: str) -> Dict[str, Any]:
        """Get user profile information via API"""
        self.rate_limit()

        try:
            url = "https://www.tiktok.com/api/user/detail/"
            params = {'uniqueId': username, 'language': 'en'}

            if self.ms_token:
                params['msToken'] = self.ms_token

            response = self.session.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                if 'userInfo' in data:
                    user_info = data['userInfo']['user']
                    stats = data['userInfo']['stats']

                    return {
                        'user_id': user_info.get('id', ''),
                        'username': user_info.get('uniqueId', ''),
                        'display_name': user_info.get('nickname', ''),
                        'follower_count': stats.get('followerCount', 0),
                        'following_count': stats.get('followingCount', 0),
                        'like_count': stats.get('heartCount', 0),
                        'video_count': stats.get('videoCount', 0),
                        'avatar_url': user_info.get('avatarLarger', ''),
                        'bio': user_info.get('signature', ''),
                        'is_verified': user_info.get('verified', False),
                        'is_private': user_info.get('privateAccount', False),
                        'extracted_at': datetime.now().isoformat(),
                        'source': 'api'
                    }

            return {'error': f'API request failed with status {response.status_code}'}

        except Exception as e:
            logger.error(f"✗ API error: {str(e)}")
            return {'error': str(e)}


class TikTokExtractorService:
    """Main service integrating all extraction methods with Supabase storage"""
    
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        self.playwright_extractor = None
        self.api_extractor = None

    async def extract_and_store_profile(self, user_id: str, username: str, 
                                      method: str = 'api', ms_token: str = None) -> Dict[str, Any]:
        """Extract profile data and store in Supabase with historical tracking"""
        try:
            profile_data = {}

            if method == 'playwright':
                self.playwright_extractor = TikTokPlaywrightExtractor(headless=True)
                async with self.playwright_extractor as browser:
                    await browser.setup_browser()
                    profile_data = await browser.get_user_profile(username)
            
            elif method == 'api':
                self.api_extractor = TikTokApiExtractor(ms_token=ms_token)
                profile_data = self.api_extractor.get_user_info(username)

            if profile_data and 'error' not in profile_data:
                # Store in Supabase user_profile_history table
                result = self.supabase.table('user_profile_history').insert({
                    'user_id': user_id,
                    'platform': 'tiktok',
                    'username': username,
                    'display_name': profile_data.get('display_name'),
                    'follower_count': profile_data.get('follower_count', 0),
                    'following_count': profile_data.get('following_count', 0),
                    'like_count': profile_data.get('like_count', 0),
                    'video_count': profile_data.get('video_count', 0),
                    'avatar_url': profile_data.get('avatar_url'),
                    'bio': profile_data.get('bio'),
                    'is_verified': profile_data.get('is_verified', False),
                    'is_private': profile_data.get('is_private', False),
                    'extraction_method': method
                }).execute()

                # Calculate growth metrics
                await self._calculate_growth_metrics(user_id, username)

                return {
                    'success': True,
                    'data': profile_data,
                    'stored_id': result.data[0]['id'] if result.data else None
                }

            return {'error': profile_data.get('error', 'Failed to extract profile data')}

        except Exception as e:
            logger.error(f"Profile extraction error: {str(e)}")
            return {'error': str(e)}

    async def extract_and_store_followers(self, user_id: str, username: str,
                                        limit: int = 100, method: str = 'playwright') -> Dict[str, Any]:
        """Extract follower list and detect changes"""
        try:
            followers = []

            if method == 'playwright':
                self.playwright_extractor = TikTokPlaywrightExtractor(headless=True)
                async with self.playwright_extractor as browser:
                    await browser.setup_browser()
                    followers = await browser.get_followers_list(username, limit)

            if followers:
                # Get previous follower list for comparison
                previous_followers = self._get_latest_followers(username)
                
                # Detect changes
                changes = self._detect_follower_changes(previous_followers, followers)

                # Store new follower data
                for follower in followers:
                    self.supabase.table('follower_history').insert({
                        'source_user_id': user_id,
                        'source_username': username,
                        'follower_username': follower.get('username'),
                        'follower_user_id': follower.get('user_id'),
                        'follower_display_name': follower.get('display_name'),
                        'follower_avatar_url': follower.get('avatar_url'),
                        'is_verified': follower.get('is_verified', False),
                        'status': 'active'
                    }).execute()

                return {
                    'success': True,
                    'followers_extracted': len(followers),
                    'changes': changes
                }

            return {'error': 'No followers extracted'}

        except Exception as e:
            logger.error(f"Follower extraction error: {str(e)}")
            return {'error': str(e)}

    async def _calculate_growth_metrics(self, user_id: str, username: str):
        """Calculate and store growth analytics"""
        try:
            # Get last 30 days of data
            thirty_days_ago = datetime.now() - timedelta(days=30)
            
            result = self.supabase.table('user_profile_history').select('*').eq(
                'user_id', user_id
            ).eq('username', username).gte(
                'extracted_at', thirty_days_ago.isoformat()
            ).order('extracted_at', desc=False).execute()

            if len(result.data) >= 2:
                first_record = result.data[0]
                last_record = result.data[-1]
                
                followers_start = first_record['follower_count']
                followers_end = last_record['follower_count']
                net_growth = followers_end - followers_start
                
                period_days = (
                    datetime.fromisoformat(last_record['extracted_at']) - 
                    datetime.fromisoformat(first_record['extracted_at'])
                ).days
                
                if period_days > 0:
                    avg_daily_growth = net_growth / period_days
                    growth_rate = (net_growth / followers_start * 100) if followers_start > 0 else 0
                    
                    # Store growth analytics
                    self.supabase.table('growth_analytics').upsert({
                        'user_id': user_id,
                        'username': username,
                        'period_start': first_record['extracted_at'],
                        'period_end': last_record['extracted_at'],
                        'followers_start': followers_start,
                        'followers_end': followers_end,
                        'net_growth': net_growth,
                        'growth_rate': round(growth_rate, 2),
                        'avg_daily_growth': round(avg_daily_growth, 2)
                    }).execute()

        except Exception as e:
            logger.error(f"Growth calculation error: {str(e)}")

    def _get_latest_followers(self, username: str) -> List[str]:
        """Get latest follower list for comparison"""
        try:
            result = self.supabase.table('follower_history').select(
                'follower_username'
            ).eq('source_username', username).order(
                'extracted_at', desc=True
            ).limit(1000).execute()

            return [f['follower_username'] for f in result.data]
        except:
            return []

    def _detect_follower_changes(self, previous: List[str], current: List[Dict]) -> Dict[str, Any]:
        """Detect new and lost followers"""
        current_usernames = [f['username'] for f in current]
        
        new_followers = set(current_usernames) - set(previous)
        lost_followers = set(previous) - set(current_usernames)
        
        return {
            'new_followers': list(new_followers),
            'lost_followers': list(lost_followers),
            'new_count': len(new_followers),
            'lost_count': len(lost_followers),
            'net_change': len(new_followers) - len(lost_followers)
        }

    def get_growth_analytics(self, user_id: str, username: str, days: int = 30) -> Dict[str, Any]:
        """Get growth analytics for dashboard"""
        try:
            start_date = datetime.now() - timedelta(days=days)
            
            result = self.supabase.table('growth_analytics').select('*').eq(
                'user_id', user_id
            ).eq('username', username).gte(
                'period_start', start_date.isoformat()
            ).order('period_end', desc=True).limit(1).execute()

            if result.data:
                return {
                    'success': True,
                    'analytics': result.data[0]
                }

            return {'error': 'No growth data available'}

        except Exception as e:
            return {'error': str(e)}

    def get_historical_chart_data(self, user_id: str, username: str, days: int = 30) -> Dict[str, Any]:
        """Get data for growth charts"""
        try:
            start_date = datetime.now() - timedelta(days=days)
            
            result = self.supabase.table('user_profile_history').select(
                'extracted_at, follower_count, following_count, like_count'
            ).eq('user_id', user_id).eq('username', username).gte(
                'extracted_at', start_date.isoformat()
            ).order('extracted_at', desc=False).execute()

            return {
                'success': True,
                'chart_data': result.data
            }

        except Exception as e:
            return {'error': str(e)}
