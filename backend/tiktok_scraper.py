"""
SocialSeed v2.0 - TikTok Web Scraping Implementation
Direct TikTok automation without developer credentials
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random
import time
import os

from playwright.async_api import async_playwright, Page, Browser
from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__name__)

class TikTokScraper:
    """TikTok web scraping service - no developer credentials needed"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.is_logged_in = False
        self.login_retries = 0
        self.max_retries = 3
        
        # Scraping configuration
        self.delays = {
            'page_load': (2, 5),      # Random delay after page loads
            'click_action': (1, 3),    # Random delay between clicks
            'typing': (0.1, 0.3),      # Random delay between keystrokes
            'scroll': (1, 2),          # Random delay for scrolling
        }
        
        # Rate limiting for safety
        self.rate_limits = {
            'follows_per_hour': 50,    # Conservative for scraping
            'likes_per_hour': 200,
            'comments_per_hour': 20,
        }
        
        self.session_actions = {
            'follows': 0,
            'likes': 0,
            'comments': 0,
            'last_reset': datetime.utcnow()
        }
    
    async def initialize(self, headless: bool = True):
        """Initialize browser and setup"""
        try:
            playwright = await async_playwright().start()
            
            # Launch browser with realistic settings
            self.browser = await playwright.chromium.launch(
                headless=headless,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-extensions',
                    '--disable-plugins',
                    '--disable-images',  # Faster loading
                    '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
                ]
            )
            
            # Create page with realistic settings
            self.page = await self.browser.new_page()
            
            # Set realistic headers
            await self.page.set_extra_http_headers({
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            })
            
            # Set viewport
            await self.page.set_viewport_size({"width": 1366, "height": 768})
            
            logger.info("✅ TikTok scraper initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize TikTok scraper: {e}")
            return False
    
    async def login(self, username: str, password: str) -> bool:
        """Login to TikTok using web scraping"""
        try:
            if not self.page:
                raise Exception("Browser not initialized")
            
            logger.info(f"🔑 Attempting TikTok login for: {username}")
            
            # Navigate to TikTok login page
            await self.page.goto('https://www.tiktok.com/login', wait_until='networkidle')
            await self._random_delay('page_load')
            
            # Check if already logged in
            if await self._is_logged_in():
                logger.info("✅ Already logged in to TikTok")
                self.is_logged_in = True
                return True
            
            # Click on "Use phone / email / username" option
            try:
                await self.page.click('[data-e2e="login-form-switch-login-method"]', timeout=5000)
                await self._random_delay('click_action')
            except:
                logger.info("Login method switcher not found, continuing...")
            
            # Fill username/email
            username_selector = 'input[name="username"]'
            await self.page.wait_for_selector(username_selector, timeout=10000)
            await self.page.fill(username_selector, username)
            await self._random_delay('typing')
            
            # Fill password
            password_selector = 'input[type="password"]'
            await self.page.fill(password_selector, password)
            await self._random_delay('typing')
            
            # Click login button
            login_button = 'button[data-e2e="login-button"]'
            await self.page.click(login_button)
            
            # Wait for login to complete
            await asyncio.sleep(5)
            
            # Check if login was successful
            if await self._is_logged_in():
                logger.info("✅ TikTok login successful")
                self.is_logged_in = True
                return True
            else:
                # Check for captcha or 2FA
                if await self._handle_login_challenges():
                    self.is_logged_in = True
                    return True
                else:
                    logger.error("❌ TikTok login failed")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ TikTok login error: {e}")
            self.login_retries += 1
            
            if self.login_retries < self.max_retries:
                logger.info(f"🔄 Retrying login... ({self.login_retries}/{self.max_retries})")
                await asyncio.sleep(10)
                return await self.login(username, password)
            
            return False
    
    async def follow_user(self, target_username: str) -> Dict[str, Any]:
        """Follow a user on TikTok"""
        try:
            if not self.is_logged_in:
                raise Exception("Not logged in to TikTok")
            
            # Check rate limits
            if not self._check_rate_limit('follows'):
                return {
                    'success': False,
                    'error': 'Rate limit exceeded for follows',
                    'retry_after': 3600
                }
            
            logger.info(f"👤 Following TikTok user: @{target_username}")
            
            # Navigate to user profile
            profile_url = f"https://www.tiktok.com/@{target_username}"
            await self.page.goto(profile_url, wait_until='networkidle')
            await self._random_delay('page_load')
            
            # Check if user exists
            if await self._is_user_not_found():
                return {
                    'success': False,
                    'error': f'User @{target_username} not found'
                }
            
            # Check if already following
            if await self._is_already_following():
                return {
                    'success': True,
                    'message': f'Already following @{target_username}',
                    'action': 'already_following'
                }
            
            # Find and click follow button
            follow_selectors = [
                '[data-e2e="follow-button"]',
                'button:has-text("Follow")',
                'button[aria-label*="Follow"]'
            ]
            
            follow_clicked = False
            for selector in follow_selectors:
                try:
                    await self.page.click(selector, timeout=3000)
                    follow_clicked = True
                    break
                except:
                    continue
            
            if not follow_clicked:
                return {
                    'success': False,
                    'error': 'Follow button not found'
                }
            
            await self._random_delay('click_action')
            
            # Verify follow action
            await asyncio.sleep(2)
            if await self._is_already_following():
                self.session_actions['follows'] += 1
                return {
                    'success': True,
                    'action_id': f"follow_{int(time.time())}",
                    'timestamp': datetime.utcnow().isoformat(),
                    'target': target_username
                }
            else:
                return {
                    'success': False,
                    'error': 'Follow action may have failed'
                }
                
        except Exception as e:
            logger.error(f"❌ Follow action failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def like_video(self, video_url: str) -> Dict[str, Any]:
        """Like a TikTok video"""
        try:
            if not self.is_logged_in:
                raise Exception("Not logged in to TikTok")
            
            # Check rate limits
            if not self._check_rate_limit('likes'):
                return {
                    'success': False,
                    'error': 'Rate limit exceeded for likes',
                    'retry_after': 3600
                }
            
            logger.info(f"❤️ Liking TikTok video: {video_url}")
            
            # Navigate to video
            await self.page.goto(video_url, wait_until='networkidle')
            await self._random_delay('page_load')
            
            # Find like button
            like_selectors = [
                '[data-e2e="like-button"]',
                'button[aria-label*="like"]',
                '.like-button'
            ]
            
            like_clicked = False
            for selector in like_selectors:
                try:
                    await self.page.click(selector, timeout=3000)
                    like_clicked = True
                    break
                except:
                    continue
            
            if like_clicked:
                self.session_actions['likes'] += 1
                await self._random_delay('click_action')
                return {
                    'success': True,
                    'action_id': f"like_{int(time.time())}",
                    'timestamp': datetime.utcnow().isoformat(),
                    'video_url': video_url
                }
            else:
                return {
                    'success': False,
                    'error': 'Like button not found'
                }
                
        except Exception as e:
            logger.error(f"❌ Like action failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def get_user_info(self, username: str) -> Dict[str, Any]:
        """Get user information from profile"""
        try:
            profile_url = f"https://www.tiktok.com/@{username}"
            await self.page.goto(profile_url, wait_until='networkidle')
            await self._random_delay('page_load')
            
            # Extract user information
            user_info = {
                'username': username,
                'followers': await self._extract_follower_count(),
                'following': await self._extract_following_count(),
                'likes': await self._extract_likes_count(),
                'videos': await self._extract_video_count(),
                'bio': await self._extract_bio(),
                'verified': await self._is_verified(),
                'profile_pic_url': await self._extract_profile_pic()
            }
            
            return {
                'success': True,
                'data': user_info
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get user info: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def search_users(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search for users on TikTok"""
        try:
            search_url = f"https://www.tiktok.com/search/user?q={query}"
            await self.page.goto(search_url, wait_until='networkidle')
            await self._random_delay('page_load')
            
            # Scroll to load more results
            for _ in range(3):
                await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await self._random_delay('scroll')
            
            # Extract user results
            users = []
            user_containers = await self.page.query_selector_all('[data-e2e="search-user-item"]')
            
            for container in user_containers[:limit]:
                try:
                    username = await container.get_attribute('href')
                    if username:
                        username = username.split('/@')[-1]
                        user_info = await self.get_user_info(username)
                        if user_info['success']:
                            users.append(user_info['data'])
                except:
                    continue
            
            return users
            
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return []
    
    # Helper methods
    async def _random_delay(self, action_type: str):
        """Add random human-like delays"""
        min_delay, max_delay = self.delays.get(action_type, (1, 2))
        delay = random.uniform(min_delay, max_delay)
        await asyncio.sleep(delay)
    
    async def _is_logged_in(self) -> bool:
        """Check if currently logged in"""
        try:
            # Look for profile/logout indicators
            selectors = [
                '[data-e2e="nav-profile"]',
                '[data-e2e="top-bar-profile"]',
                'a[href*="/profile"]'
            ]
            
            for selector in selectors:
                element = await self.page.query_selector(selector)
                if element:
                    return True
            return False
        except:
            return False
    
    async def _handle_login_challenges(self) -> bool:
        """Handle captcha, 2FA, etc."""
        try:
            # Check for captcha
            captcha_selectors = [
                '[data-e2e="captcha"]',
                '.captcha',
                'iframe[src*="captcha"]'
            ]
            
            for selector in captcha_selectors:
                if await self.page.query_selector(selector):
                    logger.warning("⚠️ Captcha detected - manual intervention needed")
                    # Wait for manual captcha solving
                    await asyncio.sleep(30)
                    return await self._is_logged_in()
            
            # Check for 2FA
            if await self.page.query_selector('input[placeholder*="code"]'):
                logger.warning("⚠️ 2FA detected - manual intervention needed")
                await asyncio.sleep(30)
                return await self._is_logged_in()
            
            return False
            
        except:
            return False
    
    def _check_rate_limit(self, action_type: str) -> bool:
        """Check if action is within rate limits"""
        now = datetime.utcnow()
        
        # Reset counters if hour has passed
        if now - self.session_actions['last_reset'] > timedelta(hours=1):
            for key in self.session_actions:
                if key != 'last_reset':
                    self.session_actions[key] = 0
            self.session_actions['last_reset'] = now
        
        # Check specific action limit
        current_count = self.session_actions.get(action_type, 0)
        limit = self.rate_limits.get(f'{action_type}_per_hour', 100)
        
        return current_count < limit
    
    async def _is_already_following(self) -> bool:
        """Check if already following the user"""
        try:
            following_selectors = [
                'button:has-text("Following")',
                '[data-e2e="unfollow-button"]',
                'button[aria-label*="Unfollow"]'
            ]
            
            for selector in following_selectors:
                element = await self.page.query_selector(selector)
                if element:
                    return True
            return False
        except:
            return False
    
    async def _is_user_not_found(self) -> bool:
        """Check if user profile doesn't exist"""
        try:
            not_found_selectors = [
                ':has-text("User not found")',
                ':has-text("This account doesn\'t exist")',
                '[data-e2e="user-not-found"]'
            ]
            
            for selector in not_found_selectors:
                element = await self.page.query_selector(selector)
                if element:
                    return True
            return False
        except:
            return False
    
    async def _extract_follower_count(self) -> int:
        """Extract follower count from profile"""
        try:
            selectors = [
                '[data-e2e="followers-count"]',
                '.number[title*="Followers"]'
            ]
            
            for selector in selectors:
                element = await self.page.query_selector(selector)
                if element:
                    text = await element.text_content()
                    return self._parse_count(text)
            return 0
        except:
            return 0
    
    def _parse_count(self, text: str) -> int:
        """Parse count strings like '1.2M', '500K', etc."""
        try:
            if not text:
                return 0
            
            text = text.strip().upper()
            multipliers = {'K': 1000, 'M': 1000000, 'B': 1000000000}
            
            for suffix, multiplier in multipliers.items():
                if suffix in text:
                    number = float(text.replace(suffix, ''))
                    return int(number * multiplier)
            
            return int(float(text))
        except:
            return 0
    
    async def close(self):
        """Clean up browser resources"""
        try:
            if self.page:
                await self.page.close()
            if self.browser:
                await self.browser.close()
            logger.info("🔄 TikTok scraper closed")
        except Exception as e:
            logger.error(f"Error closing scraper: {e}")

# Integration with existing TikTok service
class TikTokWebService:
    """TikTok service using web scraping instead of API"""
    
    def __init__(self):
        self.scraper = TikTokScraper()
        self.initialized = False
    
    async def initialize(self, username: str, password: str):
        """Initialize and login"""
        try:
            await self.scraper.initialize(headless=True)
            success = await self.scraper.login(username, password)
            self.initialized = success
            return success
        except Exception as e:
            logger.error(f"Failed to initialize TikTok web service: {e}")
            return False
    
    async def follow_user(self, target_username: str) -> Dict[str, Any]:
        """Follow user via web scraping"""
        if not self.initialized:
            return {'success': False, 'error': 'Service not initialized'}
        
        return await self.scraper.follow_user(target_username)
    
    async def get_user_info(self, username: str) -> Dict[str, Any]:
        """Get user information"""
        if not self.initialized:
            return {'success': False, 'error': 'Service not initialized'}
        
        return await self.scraper.get_user_info(username)
    
    async def search_users(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search for users"""
        if not self.initialized:
            return []
        
        return await self.scraper.search_users(query, limit)
    
    async def close(self):
        """Clean up"""
        await self.scraper.close()
        self.initialized = False

