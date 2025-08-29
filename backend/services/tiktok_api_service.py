"""
TikTok API Service using TikTokApi library
More reliable and faster than browser automation
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from TikTokApi import TikTokApi

logger = logging.getLogger(__name__)

class TikTokApiService:
    """Enhanced TikTok service using TikTokApi library with ms_token"""
    
    def __init__(self):
        self.api = None
        self.sessions_created = False
        
    async def create_session(self, ms_token: str) -> bool:
        """Create TikTok API session with ms_token"""
        try:
            self.api = TikTokApi()
            await self.api.create_sessions(
                ms_tokens=[ms_token], 
                num_sessions=1, 
                sleep_after=3
            )
            self.sessions_created = True
            logger.info("✅ TikTok API session created successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to create TikTok API session: {e}")
            return False
    
    async def verify_token(self, ms_token: str) -> Dict[str, Any]:
        """Verify ms_token by creating a session and testing basic functionality"""
        try:
            success = await self.create_session(ms_token)
            if not success:
                return {"valid": False, "error": "Failed to create session"}
                
            # Test with a basic API call
            user = self.api.user(username="tiktok")  # Official TikTok account
            user_data = await user.info()
            
            if user_data:
                return {
                    "valid": True, 
                    "message": "Token verified successfully",
                    "test_data": {
                        "username": user_data.get("username", "unknown"),
                        "follower_count": user_data.get("follower_count", 0)
                    }
                }
            else:
                return {"valid": False, "error": "Token verification failed"}
                
        except Exception as e:
            logger.error(f"❌ Token verification failed: {e}")
            return {"valid": False, "error": str(e)}
    
    async def get_user_info(self, username: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive user information"""
        if not self.sessions_created:
            logger.error("❌ No active TikTok session")
            return None
            
        try:
            user = self.api.user(username=username)
            user_data = await user.info()
            
            if user_data:
                return {
                    "username": user_data.get("username"),
                    "display_name": user_data.get("display_name"),
                    "follower_count": user_data.get("follower_count", 0),
                    "following_count": user_data.get("following_count", 0),
                    "likes_count": user_data.get("likes_count", 0),
                    "video_count": user_data.get("video_count", 0),
                    "verified": user_data.get("verified", False),
                    "bio": user_data.get("bio", ""),
                    "profile_image": user_data.get("profile_image_url", ""),
                }
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Failed to get user info for {username}: {e}")
            return None
    
    async def get_followers(self, username: str, count: int = 100) -> List[Dict[str, Any]]:
        """Get user followers"""
        if not self.sessions_created:
            logger.error("❌ No active TikTok session")
            return []
            
        try:
            user = self.api.user(username=username)
            followers = []
            
            async for follower in user.followers(count=count):
                followers.append({
                    "username": follower.username,
                    "display_name": getattr(follower, 'display_name', ''),
                    "follower_count": getattr(follower, 'follower_count', 0),
                    "verified": getattr(follower, 'verified', False)
                })
                
            logger.info(f"✅ Retrieved {len(followers)} followers for {username}")
            return followers
            
        except Exception as e:
            logger.error(f"❌ Failed to get followers for {username}: {e}")
            return []
    
    async def get_following(self, username: str, count: int = 100) -> List[Dict[str, Any]]:
        """Get users that the account is following"""
        if not self.sessions_created:
            logger.error("❌ No active TikTok session")
            return []
            
        try:
            user = self.api.user(username=username)
            following = []
            
            async for followed_user in user.following(count=count):
                following.append({
                    "username": followed_user.username,
                    "display_name": getattr(followed_user, 'display_name', ''),
                    "follower_count": getattr(followed_user, 'follower_count', 0),
                    "verified": getattr(followed_user, 'verified', False)
                })
                
            logger.info(f"✅ Retrieved {len(following)} following for {username}")
            return following
            
        except Exception as e:
            logger.error(f"❌ Failed to get following for {username}: {e}")
            return []
    
    async def analyze_account(self, username: str, ms_token: str) -> Dict[str, Any]:
        """Complete account analysis with followers, following, and growth metrics"""
        try:
            # Create session if needed
            if not self.sessions_created:
                success = await self.create_session(ms_token)
                if not success:
                    return {"error": "Failed to create TikTok session"}
            
            # Get user info
            user_info = await self.get_user_info(username)
            if not user_info:
                return {"error": f"Could not find user: {username}"}
            
            # Get followers and following (limited for performance)
            followers = await self.get_followers(username, count=50)
            following = await self.get_following(username, count=50)
            
            # Calculate engagement metrics
            analysis = {
                "user_info": user_info,
                "stats": {
                    "followers": len(followers),
                    "following": len(following),
                    "total_followers": user_info.get("follower_count", 0),
                    "total_following": user_info.get("following_count", 0),
                    "engagement_ratio": round(user_info.get("likes_count", 0) / max(user_info.get("video_count", 1), 1), 2),
                    "follower_following_ratio": round(user_info.get("follower_count", 0) / max(user_info.get("following_count", 1), 1), 2)
                },
                "recent_followers": followers[:10],
                "recent_following": following[:10],
                "recommendations": self._generate_recommendations(user_info, followers, following)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Failed to analyze account {username}: {e}")
            return {"error": str(e)}
    
    def _generate_recommendations(self, user_info: Dict, followers: List, following: List) -> List[str]:
        """Generate growth recommendations based on account analysis"""
        recommendations = []
        
        follower_count = user_info.get("follower_count", 0)
        following_count = user_info.get("following_count", 0)
        
        if following_count > follower_count * 2:
            recommendations.append("Consider unfollowing inactive accounts to improve your ratio")
        
        if follower_count < 1000:
            recommendations.append("Focus on creating engaging content to reach 1K followers")
        
        if len(followers) < 10:
            recommendations.append("Engage more with your community to attract new followers")
        
        verified_following = sum(1 for user in following if user.get("verified", False))
        if verified_following < 5:
            recommendations.append("Follow more verified accounts in your niche")
        
        if not recommendations:
            recommendations.append("Great account growth! Keep up the consistent content creation")
        
        return recommendations
    
    async def close(self):
        """Close the TikTok API session"""
        if self.api:
            try:
                await self.api.close()
                logger.info("✅ TikTok API session closed")
            except Exception as e:
                logger.error(f"❌ Error closing TikTok session: {e}")


# Global service instance
tiktok_api_service = TikTokApiService()
