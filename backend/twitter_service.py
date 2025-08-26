"""
SocialSeed v2.0 - Twitter Service
Twitter-specific operations with rate limiting and safety measures
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random
import time
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class TwitterService:
    """Twitter service with safety measures and rate limiting"""
    
    def __init__(self, behavior_simulator, health_monitor, authenticity_analyzer):
        self.behavior_simulator = behavior_simulator
        self.health_monitor = health_monitor
        self.authenticity_analyzer = authenticity_analyzer
        
        # Rate limiting configuration (Twitter limits)
        self.rate_limits = {
            'follows_per_hour': 400,  # Twitter's premium limit
            'likes_per_hour': 1000,
            'retweets_per_hour': 300,
            'tweets_per_hour': 50
        }
        
        # Current usage tracking
        self.usage_tracker = {
            'follows': {'count': 0, 'last_reset': datetime.utcnow()},
            'likes': {'count': 0, 'last_reset': datetime.utcnow()},
            'retweets': {'count': 0, 'last_reset': datetime.utcnow()},
            'tweets': {'count': 0, 'last_reset': datetime.utcnow()}
        }
        
        # Safety settings
        self.safety_thresholds = {
            'min_followers': 150,
            'max_following_ratio': 12.0,
            'min_account_age_days': 60,
            'max_daily_actions': 200
        }
        
        self.is_initialized = False
    
    async def initialize(self):
        """Initialize Twitter service"""
        logger.info("Initializing Twitter Service...")
        
        # Initialize API client (placeholder for actual Twitter API)
        self.api_client = self._create_api_client()
        
        # Reset usage counters
        self._reset_usage_counters()
        
        self.is_initialized = True
        logger.info("✅ Twitter Service initialized")
    
    def _create_api_client(self):
        """Create Twitter API client (placeholder implementation)"""
        return MockTwitterClient()
    
    def _reset_usage_counters(self):
        """Reset usage counters for new hour"""
        now = datetime.utcnow()
        for action_type in self.usage_tracker:
            if (now - self.usage_tracker[action_type]['last_reset']).total_seconds() > 3600:
                self.usage_tracker[action_type]['count'] = 0
                self.usage_tracker[action_type]['last_reset'] = now
    
    async def follow_user(self, target_username: str, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Follow a user on Twitter with safety checks"""
        logger.info(f"Attempting to follow {target_username} on Twitter")
        
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
        delay = self.behavior_simulator.get_action_delay('follow', 'twitter')
        await asyncio.sleep(delay)
        
        # Execute follow action
        try:
            result = await self._execute_follow(target_username, account_data)
            
            if result['success']:
                self.usage_tracker['follows']['count'] += 1
                await self._log_action('follow', target_username, result, authenticity_result)
                logger.info(f"Successfully followed {target_username} on Twitter")
            
            return result
            
        except Exception as e:
            logger.error(f"Follow action failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'retry_after': self._get_retry_delay('follows')
            }
    
    async def like_tweet(self, tweet_id: str, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Like a tweet on Twitter"""
        logger.info(f"Attempting to like tweet {tweet_id} on Twitter")
        
        if not self._check_rate_limit('likes'):
            return {
                'success': False,
                'error': 'Rate limit exceeded for likes',
                'retry_after': self._get_retry_delay('likes')
            }
        
        delay = self.behavior_simulator.get_action_delay('like', 'twitter')
        await asyncio.sleep(delay)
        
        try:
            result = await self._execute_like(tweet_id, account_data)
            
            if result['success']:
                self.usage_tracker['likes']['count'] += 1
                await self._log_action('like', tweet_id, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Like action failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def retweet(self, tweet_id: str, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Retweet a tweet on Twitter"""
        logger.info(f"Attempting to retweet {tweet_id} on Twitter")
        
        if not self._check_rate_limit('retweets'):
            return {
                'success': False,
                'error': 'Rate limit exceeded for retweets',
                'retry_after': self._get_retry_delay('retweets')
            }
        
        delay = self.behavior_simulator.get_action_delay('retweet', 'twitter')
        await asyncio.sleep(delay)
        
        try:
            result = await self._execute_retweet(tweet_id, account_data)
            
            if result['success']:
                self.usage_tracker['retweets']['count'] += 1
                await self._log_action('retweet', tweet_id, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Retweet action failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def post_tweet(self, tweet_text: str, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Post a tweet on Twitter"""
        logger.info(f"Attempting to post tweet on Twitter")
        
        if not self._check_rate_limit('tweets'):
            return {
                'success': False,
                'error': 'Rate limit exceeded for tweets',
                'retry_after': self._get_retry_delay('tweets')
            }
        
        if not self._validate_tweet(tweet_text):
            return {
                'success': False,
                'error': 'Tweet text failed validation'
            }
        
        delay = self.behavior_simulator.get_action_delay('tweet', 'twitter')
        await asyncio.sleep(delay)
        
        try:
            result = await self._execute_tweet(tweet_text, account_data)
            
            if result['success']:
                self.usage_tracker['tweets']['count'] += 1
                await self._log_action('tweet', result.get('tweet_id', 'unknown'), result)
            
            return result
            
        except Exception as e:
            logger.error(f"Tweet action failed: {e}")
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
        base_delay = 120  # 2 minutes for Twitter
        jitter = random.uniform(0.8, 1.2)
        return int(base_delay * jitter)
    
    async def _get_user_info(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user information from Twitter"""
        try:
            return {
                'username': username,
                'followers_count': random.randint(150, 20000),
                'following_count': random.randint(200, 3000),
                'tweets_count': random.randint(50, 1000),
                'bio': f"Mock bio for {username}",
                'account_age_days': random.randint(60, 1500),
                'verified': random.choice([True, False]),
                'protected': random.choice([True, False])
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
        
        # Check if account is protected
        if target_info.get('protected', False):
            return False
        
        # Check authenticity score
        authenticity_score = authenticity_result.get('authenticity_score', 0.0)
        if authenticity_score < 0.35:  # Medium threshold for Twitter
            return False
        
        return True
    
    def _validate_tweet(self, tweet_text: str) -> bool:
        """Validate tweet text for safety"""
        if not tweet_text or len(tweet_text.strip()) < 2:
            return False
        
        if len(tweet_text) > 280:  # Twitter character limit
            return False
        
        # Check for inappropriate content
        inappropriate_words = ['spam', 'bot', 'automated', 'followback']
        tweet_lower = tweet_text.lower()
        
        for word in inappropriate_words:
            if word in tweet_lower:
                return False
        
        return True
    
    async def _execute_follow(self, username: str, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute follow action using Twitter API"""
        try:
            success_rate = 0.94  # 94% success rate for Twitter
            
            if random.random() < success_rate:
                return {
                    'success': True,
                    'action_id': f"tw_follow_{int(time.time())}",
                    'timestamp': datetime.utcnow().isoformat(),
                    'target': username
                }
            else:
                return {
                    'success': False,
                    'error': 'Follow action failed (simulated)',
                    'retry_after': 900  # 15 minutes
                }
        except Exception as e:
            raise Exception(f"Follow execution failed: {e}")
    
    async def _execute_like(self, tweet_id: str, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute like action using Twitter API"""
        try:
            success_rate = 0.97  # 97% success rate
            
            if random.random() < success_rate:
                return {
                    'success': True,
                    'action_id': f"tw_like_{int(time.time())}",
                    'timestamp': datetime.utcnow().isoformat(),
                    'tweet_id': tweet_id
                }
            else:
                return {
                    'success': False,
                    'error': 'Like action failed (simulated)'
                }
        except Exception as e:
            raise Exception(f"Like execution failed: {e}")
    
    async def _execute_retweet(self, tweet_id: str, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute retweet action using Twitter API"""
        try:
            success_rate = 0.93  # 93% success rate
            
            if random.random() < success_rate:
                return {
                    'success': True,
                    'action_id': f"tw_retweet_{int(time.time())}",
                    'timestamp': datetime.utcnow().isoformat(),
                    'tweet_id': tweet_id
                }
            else:
                return {
                    'success': False,
                    'error': 'Retweet action failed (simulated)'
                }
        except Exception as e:
            raise Exception(f"Retweet execution failed: {e}")
    
    async def _execute_tweet(self, tweet_text: str, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tweet action using Twitter API"""
        try:
            success_rate = 0.88  # 88% success rate (tweets are riskier)
            
            if random.random() < success_rate:
                tweet_id = f"tweet_{int(time.time())}"
                return {
                    'success': True,
                    'action_id': f"tw_tweet_{int(time.time())}",
                    'timestamp': datetime.utcnow().isoformat(),
                    'tweet_id': tweet_id,
                    'tweet_text': tweet_text
                }
            else:
                return {
                    'success': False,
                    'error': 'Tweet action failed (simulated)'
                }
        except Exception as e:
            raise Exception(f"Tweet execution failed: {e}")
    
    async def _log_action(self, action_type: str, target: str, result: Dict[str, Any], authenticity_result: Dict[str, Any] = None):
        """Log action for monitoring and analytics"""
        log_entry = {
            'action_type': action_type,
            'target': target,
            'result': result,
            'authenticity_result': authenticity_result,
            'timestamp': datetime.utcnow().isoformat(),
            'platform': 'twitter'
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

class MockTwitterClient:
    """Mock Twitter API client for development/testing"""
    
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
            'followers_count': 3000,
            'following_count': 1200,
            'tweets_count': 200,
            'verified': False,
            'protected': False
        }

