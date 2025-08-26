"""
SocialSeed v2.0 - Instagram Service
Instagram-specific operations with rate limiting and safety measures
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random
import time
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class InstagramService:
    """Instagram service with safety measures and rate limiting"""
    
    def __init__(self, behavior_simulator, health_monitor, authenticity_analyzer):
        self.behavior_simulator = behavior_simulator
        self.health_monitor = health_monitor
        self.authenticity_analyzer = authenticity_analyzer
        
        # Rate limiting configuration (Instagram limits)
        self.rate_limits = {
            'follows_per_hour': 150,  # Instagram's limit
            'likes_per_hour': 800,
            'comments_per_hour': 80,
            'unfollows_per_hour': 100
        }
        
        # Current usage tracking
        self.usage_tracker = {
            'follows': {'count': 0, 'last_reset': datetime.utcnow()},
            'likes': {'count': 0, 'last_reset': datetime.utcnow()},
            'comments': {'count': 0, 'last_reset': datetime.utcnow()},
            'unfollows': {'count': 0, 'last_reset': datetime.utcnow()}
        }
        
        # Safety settings
        self.safety_thresholds = {
            'min_followers': 200,
            'max_following_ratio': 8.0,
            'min_account_age_days': 45,
            'max_daily_actions': 120
        }
        
        self.is_initialized = False
    
    async def initialize(self):
        """Initialize Instagram service"""
        logger.info("Initializing Instagram Service...")
        
        # Initialize API client (placeholder for actual Instagram API)
        self.api_client = self._create_api_client()
        
        # Reset usage counters
        self._reset_usage_counters()
        
        self.is_initialized = True
        logger.info("✅ Instagram Service initialized")
    
    def _create_api_client(self):
        """Create Instagram API client (placeholder implementation)"""
        return MockInstagramClient()
    
    def _reset_usage_counters(self):
        """Reset usage counters for new hour"""
        now = datetime.utcnow()
        for action_type in self.usage_tracker:
            if (now - self.usage_tracker[action_type]['last_reset']).total_seconds() > 3600:
                self.usage_tracker[action_type]['count'] = 0
                self.usage_tracker[action_type]['last_reset'] = now
    
    async def follow_user(self, target_username: str, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Follow a user on Instagram with safety checks"""
        logger.info(f"Attempting to follow {target_username} on Instagram")
        
        # Check rate limits
        if not self._check_rate_limit('follows'):
            return {
                'success': False,
                'error': 'Rate limit exceeded for follows',
                'retry_after': self._get_retry_delay('follows')
            }
        
        # Analyze target account authenticity
        target_info = await self._get_user_info(target_username)
        if not target_info:
            return {
                'success': False,
                'error': 'Could not retrieve target user information'
            }
        
        authenticity_result = await self.authenticity_analyzer.analyze_authenticity(target_info)
        
        # Safety check
        if not self._passes_safety_check(target_info, authenticity_result):
            return {
                'success': False,
                'error': 'Target account failed safety checks',
                'authenticity_score': authenticity_result.get('authenticity_score', 0.0),
                'risk_factors': authenticity_result.get('risk_factors', [])
            }
        
        # Simulate human behavior
        delay = self.behavior_simulator.get_action_delay('follow', 'instagram')
        await asyncio.sleep(delay)
        
        # Execute follow action
        try:
            result = await self._execute_follow(target_username, account_data)
            
            if result['success']:
                self.usage_tracker['follows']['count'] += 1
                await self._log_action('follow', target_username, result, authenticity_result)
                logger.info(f"Successfully followed {target_username} on Instagram")
            
            return result
            
        except Exception as e:
            logger.error(f"Follow action failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'retry_after': self._get_retry_delay('follows')
            }
    
    async def like_post(self, post_id: str, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Like a post on Instagram"""
        logger.info(f"Attempting to like post {post_id} on Instagram")
        
        if not self._check_rate_limit('likes'):
            return {
                'success': False,
                'error': 'Rate limit exceeded for likes',
                'retry_after': self._get_retry_delay('likes')
            }
        
        delay = self.behavior_simulator.get_action_delay('like', 'instagram')
        await asyncio.sleep(delay)
        
        try:
            result = await self._execute_like(post_id, account_data)
            
            if result['success']:
                self.usage_tracker['likes']['count'] += 1
                await self._log_action('like', post_id, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Like action failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def comment_on_post(self, post_id: str, comment_text: str, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comment on a post on Instagram"""
        logger.info(f"Attempting to comment on post {post_id} on Instagram")
        
        if not self._check_rate_limit('comments'):
            return {
                'success': False,
                'error': 'Rate limit exceeded for comments',
                'retry_after': self._get_retry_delay('comments')
            }
        
        if not self._validate_comment(comment_text):
            return {
                'success': False,
                'error': 'Comment text failed validation'
            }
        
        delay = self.behavior_simulator.get_action_delay('comment', 'instagram')
        await asyncio.sleep(delay)
        
        try:
            result = await self._execute_comment(post_id, comment_text, account_data)
            
            if result['success']:
                self.usage_tracker['comments']['count'] += 1
                await self._log_action('comment', post_id, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Comment action failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def unfollow_user(self, target_username: str, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Unfollow a user on Instagram"""
        logger.info(f"Attempting to unfollow {target_username} on Instagram")
        
        if not self._check_rate_limit('unfollows'):
            return {
                'success': False,
                'error': 'Rate limit exceeded for unfollows',
                'retry_after': self._get_retry_delay('unfollows')
            }
        
        delay = self.behavior_simulator.get_action_delay('unfollow', 'instagram')
        await asyncio.sleep(delay)
        
        try:
            result = await self._execute_unfollow(target_username, account_data)
            
            if result['success']:
                self.usage_tracker['unfollows']['count'] += 1
                await self._log_action('unfollow', target_username, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Unfollow action failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _check_rate_limit(self, action_type: str) -> bool:
        """Check if action is within rate limits"""
        self._reset_usage_counters()
        
        if action_type not in self.usage_tracker:
            return False
        
        current_usage = self.usage_tracker[action_type]['count']
        limit = self.rate_limits.get(f'{action_type}_per_hour', 100)
        
        return current_usage < limit
    
    def _get_retry_delay(self, action_type: str) -> int:
        """Get retry delay for rate-limited actions"""
        base_delay = 90  # 1.5 minutes for Instagram
        jitter = random.uniform(0.8, 1.2)
        return int(base_delay * jitter)
    
    async def _get_user_info(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user information from Instagram"""
        try:
            return {
                'username': username,
                'followers_count': random.randint(200, 15000),
                'following_count': random.randint(100, 2000),
                'posts_count': random.randint(20, 800),
                'bio': f"Mock bio for {username}",
                'account_age_days': random.randint(45, 1200),
                'verified': random.choice([True, False]),
                'is_private': random.choice([True, False])
            }
        except Exception as e:
            logger.error(f"Failed to get user info for {username}: {e}")
            return None
    
    def _passes_safety_check(self, target_info: Dict[str, Any], authenticity_result: Dict[str, Any]) -> bool:
        """Check if target account passes safety requirements"""
        # Check minimum followers
        if target_info.get('followers_count', 0) < self.safety_thresholds['min_followers']:
            return False
        
        # Check following ratio
        followers = target_info.get('followers_count', 1)
        following = target_info.get('following_count', 0)
        if following > 0 and (followers / following) > self.safety_thresholds['max_following_ratio']:
            return False
        
        # Check account age
        if target_info.get('account_age_days', 0) < self.safety_thresholds['min_account_age_days']:
            return False
        
        # Check if account is private
        if target_info.get('is_private', False):
            return False
        
        # Check authenticity score
        authenticity_score = authenticity_result.get('authenticity_score', 0.0)
        if authenticity_score < 0.4:  # Higher threshold for Instagram
            return False
        
        return True
    
    def _validate_comment(self, comment_text: str) -> bool:
        """Validate comment text for safety"""
        if not comment_text or len(comment_text.strip()) < 2:
            return False
        
        if len(comment_text) > 2200:  # Instagram comment limit
            return False
        
        # Check for inappropriate content
        inappropriate_words = ['spam', 'bot', 'automated', 'follow4follow']
        comment_lower = comment_text.lower()
        
        for word in inappropriate_words:
            if word in comment_lower:
                return False
        
        return True
    
    async def _execute_follow(self, username: str, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute follow action using Instagram API"""
        try:
            success_rate = 0.92  # 92% success rate for Instagram
            
            if random.random() < success_rate:
                return {
                    'success': True,
                    'action_id': f"ig_follow_{int(time.time())}",
                    'timestamp': datetime.utcnow().isoformat(),
                    'target': username
                }
            else:
                return {
                    'success': False,
                    'error': 'Follow action failed (simulated)',
                    'retry_after': 600  # 10 minutes
                }
        except Exception as e:
            raise Exception(f"Follow execution failed: {e}")
    
    async def _execute_like(self, post_id: str, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute like action using Instagram API"""
        try:
            success_rate = 0.96  # 96% success rate
            
            if random.random() < success_rate:
                return {
                    'success': True,
                    'action_id': f"ig_like_{int(time.time())}",
                    'timestamp': datetime.utcnow().isoformat(),
                    'post_id': post_id
                }
            else:
                return {
                    'success': False,
                    'error': 'Like action failed (simulated)'
                }
        except Exception as e:
            raise Exception(f"Like execution failed: {e}")
    
    async def _execute_comment(self, post_id: str, comment_text: str, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute comment action using Instagram API"""
        try:
            success_rate = 0.85  # 85% success rate (comments are riskier on Instagram)
            
            if random.random() < success_rate:
                return {
                    'success': True,
                    'action_id': f"ig_comment_{int(time.time())}",
                    'timestamp': datetime.utcnow().isoformat(),
                    'post_id': post_id,
                    'comment': comment_text
                }
            else:
                return {
                    'success': False,
                    'error': 'Comment action failed (simulated)'
                }
        except Exception as e:
            raise Exception(f"Comment execution failed: {e}")
    
    async def _execute_unfollow(self, username: str, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute unfollow action using Instagram API"""
        try:
            success_rate = 0.94  # 94% success rate
            
            if random.random() < success_rate:
                return {
                    'success': True,
                    'action_id': f"ig_unfollow_{int(time.time())}",
                    'timestamp': datetime.utcnow().isoformat(),
                    'target': username
                }
            else:
                return {
                    'success': False,
                    'error': 'Unfollow action failed (simulated)'
                }
        except Exception as e:
            raise Exception(f"Unfollow execution failed: {e}")
    
    async def _log_action(self, action_type: str, target: str, result: Dict[str, Any], authenticity_result: Dict[str, Any] = None):
        """Log action for monitoring and analytics"""
        log_entry = {
            'action_type': action_type,
            'target': target,
            'result': result,
            'authenticity_result': authenticity_result,
            'timestamp': datetime.utcnow().isoformat(),
            'platform': 'instagram'
        }
        
        logger.info(f"Action logged: {log_entry}")
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get current service status and usage"""
        self._reset_usage_counters()
        
        return {
            'status': 'active' if self.is_initialized else 'inactive',
            'rate_limits': self.rate_limits,
            'current_usage': self.usage_tracker,
            'safety_thresholds': self.safety_thresholds,
            'last_updated': datetime.utcnow().isoformat()
        }

class MockInstagramClient:
    """Mock Instagram API client for development/testing"""
    
    def __init__(self):
        self.is_authenticated = False
    
    async def authenticate(self, credentials: Dict[str, Any]) -> bool:
        """Mock authentication"""
        self.is_authenticated = True
        return True
    
    async def get_user_info(self, username: str) -> Dict[str, Any]:
        """Mock user info retrieval"""
        return {
            'username': username,
            'followers_count': 2000,
            'following_count': 800,
            'posts_count': 100,
            'verified': False,
            'is_private': False
        }

