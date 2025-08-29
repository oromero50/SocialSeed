"""
Enhanced TikTok Service using TikTok-Api Library
Provides fast, reliable access to TikTok data using ms_token
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from TikTokApi import TikTokApi
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class EnhancedTikTokService:
    def __init__(self):
        self.api: Optional[TikTokApi] = None
        self.active_sessions = {}
        
    async def create_session(self, ms_token: str, username: str) -> bool:
        """
        Create a TikTok session using ms_token
        
        Args:
            ms_token: The ms_token extracted from browser
            username: TikTok username for this session
            
        Returns:
            bool: True if session created successfully
        """
        try:
            logger.info(f"🔄 Creating TikTok session for user: {username}")
            
            # Initialize TikTok API
            api = TikTokApi()
            
            # Create session with ms_token
            await api.create_sessions(
                ms_tokens=[ms_token],
                num_sessions=1,
                sleep_after=3
            )
            
            # Test the session by getting user info
            user = api.user(username=username)
            user_data = await user.info()
            
            # Store active session
            self.active_sessions[username] = {
                'api': api,
                'ms_token': ms_token,
                'created_at': datetime.now(),
                'user_data': user_data,
                'username': username
            }
            
            logger.info(f"✅ TikTok session created successfully for {username}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create TikTok session for {username}: {e}")
            return False
    
    async def get_user_info(self, username: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive user information"""
        try:
            if username not in self.active_sessions:
                logger.error(f"❌ No active session for {username}")
                return None
                
            session = self.active_sessions[username]
            api = session['api']
            
            user = api.user(username=username)
            user_data = await user.info()
            
            # Extract key metrics
            info = {
                'username': user_data.username,
                'display_name': user_data.display_name,
                'follower_count': user_data.follower_count,
                'following_count': user_data.following_count,
                'heart_count': user_data.heart_count,
                'video_count': user_data.video_count,
                'bio': user_data.bio,
                'verified': user_data.verified,
                'avatar_url': user_data.avatar_url,
                'last_updated': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Retrieved user info for {username}: {info['follower_count']} followers")
            return info
            
        except Exception as e:
            logger.error(f"❌ Failed to get user info for {username}: {e}")
            return None
    
    async def get_followers(self, username: str, count: int = 100) -> List[Dict[str, Any]]:
        """Get user's followers"""
        try:
            if username not in self.active_sessions:
                logger.error(f"❌ No active session for {username}")
                return []
                
            session = self.active_sessions[username]
            api = session['api']
            
            user = api.user(username=username)
            followers = []
            
            async for follower in user.followers(count=count):
                followers.append({
                    'username': follower.username,
                    'display_name': follower.display_name,
                    'follower_count': follower.follower_count,
                    'following_count': follower.following_count,
                    'verified': follower.verified,
                    'avatar_url': follower.avatar_url
                })
                
            logger.info(f"✅ Retrieved {len(followers)} followers for {username}")
            return followers
            
        except Exception as e:
            logger.error(f"❌ Failed to get followers for {username}: {e}")
            return []
    
    async def get_following(self, username: str, count: int = 100) -> List[Dict[str, Any]]:
        """Get users that this account is following"""
        try:
            if username not in self.active_sessions:
                logger.error(f"❌ No active session for {username}")
                return []
                
            session = self.active_sessions[username]
            api = session['api']
            
            user = api.user(username=username)
            following = []
            
            async for followed_user in user.following(count=count):
                following.append({
                    'username': followed_user.username,
                    'display_name': followed_user.display_name,
                    'follower_count': followed_user.follower_count,
                    'following_count': followed_user.following_count,
                    'verified': followed_user.verified,
                    'avatar_url': followed_user.avatar_url
                })
                
            logger.info(f"✅ Retrieved {len(following)} following for {username}")
            return following
            
        except Exception as e:
            logger.error(f"❌ Failed to get following for {username}: {e}")
            return []
    
    async def get_growth_analytics(self, username: str) -> Dict[str, Any]:
        """Get growth analytics and insights"""
        try:
            user_info = await self.get_user_info(username)
            if not user_info:
                return {}
            
            # Calculate engagement rate (simplified)
            followers = user_info['follower_count']
            hearts = user_info['heart_count']
            videos = user_info['video_count']
            
            avg_hearts_per_video = hearts / videos if videos > 0 else 0
            engagement_rate = (avg_hearts_per_video / followers * 100) if followers > 0 else 0
            
            analytics = {
                'follower_count': followers,
                'following_count': user_info['following_count'],
                'video_count': videos,
                'total_hearts': hearts,
                'avg_hearts_per_video': round(avg_hearts_per_video, 2),
                'engagement_rate': round(engagement_rate, 2),
                'follower_following_ratio': round(followers / user_info['following_count'], 2) if user_info['following_count'] > 0 else 0,
                'growth_potential': self._calculate_growth_potential(user_info),
                'last_analyzed': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Generated analytics for {username}: {engagement_rate:.2f}% engagement")
            return analytics
            
        except Exception as e:
            logger.error(f"❌ Failed to get analytics for {username}: {e}")
            return {}
    
    def _calculate_growth_potential(self, user_info: Dict[str, Any]) -> str:
        """Calculate growth potential based on metrics"""
        followers = user_info['follower_count']
        following = user_info['following_count']
        videos = user_info['video_count']
        
        if followers < 1000:
            return "High" if videos > 10 else "Medium"
        elif followers < 10000:
            return "Medium" if following / followers < 2 else "Low"
        else:
            return "Low" if following / followers > 0.5 else "Medium"
    
    async def detect_unfollowers(self, username: str) -> Dict[str, Any]:
        """Detect who unfollowed (requires historical data)"""
        # This would need database storage of previous follower lists
        # For now, return current state with placeholder for future implementation
        try:
            current_followers = await self.get_followers(username, count=1000)
            
            return {
                'current_follower_count': len(current_followers),
                'new_followers': [],  # Would compare with previous data
                'lost_followers': [],  # Would compare with previous data
                'net_change': 0,
                'analysis_date': datetime.now().isoformat(),
                'note': 'Historical tracking will be implemented with database storage'
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to detect unfollowers for {username}: {e}")
            return {}
    
    async def close_session(self, username: str) -> bool:
        """Close TikTok session"""
        try:
            if username in self.active_sessions:
                session = self.active_sessions[username]
                if 'api' in session and session['api']:
                    await session['api'].close()
                del self.active_sessions[username]
                logger.info(f"✅ Closed TikTok session for {username}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"❌ Failed to close session for {username}: {e}")
            return False
    
    async def close_all_sessions(self):
        """Close all active sessions"""
        for username in list(self.active_sessions.keys()):
            await self.close_session(username)
        logger.info("✅ All TikTok sessions closed")

# Global service instance
enhanced_tiktok_service = EnhancedTikTokService()
