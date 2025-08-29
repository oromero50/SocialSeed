"""
TikTok Data Collector Service
Collects followers, following, engagement data using TikTok-Api library
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
from TikTokApi import TikTokApi
from database import DatabaseManager

logger = logging.getLogger(__name__)

class TikTokDataCollector:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.api_sessions = {}
        
    async def create_tiktok_session(self, ms_token: str, username: str) -> bool:
        """Create TikTok API session with ms_token"""
        try:
            logger.info(f"🔄 Creating TikTok session for {username}")
            
            async with TikTokApi() as api:
                await api.create_sessions(
                    ms_tokens=[ms_token], 
                    num_sessions=1, 
                    sleep_after=3
                )
                
                # Test the session by getting user info
                user = api.user(username=username)
                user_data = await user.info()
                
                if user_data:
                    self.api_sessions[username] = {
                        'api': api,
                        'ms_token': ms_token,
                        'created_at': datetime.now(),
                        'user_data': user_data
                    }
                    logger.info(f"✅ TikTok session created successfully for {username}")
                    return True
                    
        except Exception as e:
            logger.error(f"❌ Failed to create TikTok session for {username}: {e}")
            return False
            
    async def collect_follower_data(self, username: str) -> Dict[str, Any]:
        """Collect comprehensive follower data for a TikTok account"""
        try:
            logger.info(f"📊 Collecting follower data for {username}")
            
            if username not in self.api_sessions:
                logger.error(f"No active session for {username}")
                return {}
                
            api = self.api_sessions[username]['api']
            user = api.user(username=username)
            
            # Get user profile info
            user_info = await user.info()
            
            # Collect followers (limited to avoid rate limits)
            followers = []
            follower_count = 0
            async for follower in user.followers(count=100):
                followers.append({
                    'username': follower.username,
                    'display_name': getattr(follower, 'display_name', ''),
                    'follower_count': getattr(follower, 'followerCount', 0),
                    'following_count': getattr(follower, 'followingCount', 0),
                    'collected_at': datetime.now().isoformat()
                })
                follower_count += 1
                if follower_count >= 100:  # Limit to prevent rate limiting
                    break
                    
            # Collect following
            following = []
            following_count = 0
            async for follow in user.following(count=100):
                following.append({
                    'username': follow.username,
                    'display_name': getattr(follow, 'display_name', ''),
                    'follower_count': getattr(follow, 'followerCount', 0),
                    'collected_at': datetime.now().isoformat()
                })
                following_count += 1
                if following_count >= 100:
                    break
                    
            # Calculate engagement metrics
            total_followers = user_info.get('followerCount', 0)
            total_following = user_info.get('followingCount', 0)
            total_likes = user_info.get('heartCount', 0)
            total_videos = user_info.get('videoCount', 0)
            
            engagement_rate = 0
            if total_videos > 0:
                engagement_rate = (total_likes / total_videos / max(total_followers, 1)) * 100
                
            follower_data = {
                'username': username,
                'profile_data': {
                    'display_name': user_info.get('displayName', ''),
                    'bio': user_info.get('signature', ''),
                    'follower_count': total_followers,
                    'following_count': total_following,
                    'video_count': total_videos,
                    'like_count': total_likes,
                    'verified': user_info.get('verified', False)
                },
                'followers': followers,
                'following': following,
                'analytics': {
                    'engagement_rate': round(engagement_rate, 2),
                    'follower_following_ratio': round(total_followers / max(total_following, 1), 2),
                    'avg_likes_per_video': round(total_likes / max(total_videos, 1), 0),
                    'growth_potential': self._calculate_growth_potential(total_followers, total_following, engagement_rate)
                },
                'collected_at': datetime.now().isoformat()
            }
            
            # Store in database
            await self._store_follower_data(username, follower_data)
            
            logger.info(f"✅ Collected data for {username}: {total_followers} followers, {total_following} following")
            return follower_data
            
        except Exception as e:
            logger.error(f"❌ Error collecting follower data for {username}: {e}")
            return {}
            
    def _calculate_growth_potential(self, followers: int, following: int, engagement_rate: float) -> str:
        """Calculate growth potential based on metrics"""
        ratio = followers / max(following, 1)
        
        if engagement_rate > 5 and ratio > 2:
            return "High"
        elif engagement_rate > 2 and ratio > 1:
            return "Medium"
        else:
            return "Low"
            
    async def _store_follower_data(self, username: str, data: Dict[str, Any]):
        """Store collected data in database"""
        try:
            # Update account with latest metrics
            await self.db_manager.execute_query(
                """
                UPDATE social_accounts 
                SET 
                    follower_count = %s,
                    following_count = %s,
                    engagement_rate = %s,
                    last_sync = %s,
                    metadata = %s
                WHERE username = %s AND platform = 'tiktok'
                """,
                (
                    data['profile_data']['follower_count'],
                    data['profile_data']['following_count'],
                    data['analytics']['engagement_rate'],
                    datetime.now(),
                    json.dumps(data),
                    username
                )
            )
            
            # Store follower snapshot
            await self.db_manager.execute_query(
                """
                INSERT INTO follower_snapshots 
                (account_id, follower_count, following_count, engagement_rate, snapshot_data, created_at)
                SELECT 
                    id, %s, %s, %s, %s, %s
                FROM social_accounts 
                WHERE username = %s AND platform = 'tiktok'
                """,
                (
                    data['profile_data']['follower_count'],
                    data['profile_data']['following_count'],
                    data['analytics']['engagement_rate'],
                    json.dumps(data),
                    datetime.now(),
                    username
                )
            )
            
            logger.info(f"✅ Stored follower data for {username} in database")
            
        except Exception as e:
            logger.error(f"❌ Error storing follower data for {username}: {e}")
            
    async def detect_unfollowers(self, username: str) -> List[Dict[str, Any]]:
        """Detect who unfollowed since last check"""
        try:
            # Get current followers
            current_data = await self.collect_follower_data(username)
            current_followers = {f['username'] for f in current_data.get('followers', [])}
            
            # Get previous followers from database
            result = await self.db_manager.fetch_query(
                """
                SELECT snapshot_data 
                FROM follower_snapshots 
                WHERE account_id = (
                    SELECT id FROM social_accounts 
                    WHERE username = %s AND platform = 'tiktok'
                )
                ORDER BY created_at DESC 
                LIMIT 2
                """,
                (username,)
            )
            
            if len(result) < 2:
                logger.info(f"Not enough historical data for {username} to detect unfollowers")
                return []
                
            previous_data = json.loads(result[1]['snapshot_data'])
            previous_followers = {f['username'] for f in previous_data.get('followers', [])}
            
            # Find unfollowers
            unfollowers = previous_followers - current_followers
            new_followers = current_followers - previous_followers
            
            unfollower_list = []
            for unfollower_username in unfollowers:
                # Find details from previous data
                unfollower_details = next(
                    (f for f in previous_data.get('followers', []) if f['username'] == unfollower_username),
                    {'username': unfollower_username, 'display_name': ''}
                )
                unfollower_list.append({
                    'username': unfollower_username,
                    'display_name': unfollower_details.get('display_name', ''),
                    'unfollowed_at': datetime.now().isoformat(),
                    'type': 'unfollower'
                })
                
            # Store unfollower events
            if unfollower_list:
                await self._store_unfollower_events(username, unfollower_list)
                
            logger.info(f"🔍 Unfollower detection for {username}: {len(unfollower_list)} unfollowers, {len(new_followers)} new followers")
            
            return {
                'unfollowers': unfollower_list,
                'new_followers': len(new_followers),
                'net_change': len(new_followers) - len(unfollower_list)
            }
            
        except Exception as e:
            logger.error(f"❌ Error detecting unfollowers for {username}: {e}")
            return []
            
    async def _store_unfollower_events(self, username: str, unfollowers: List[Dict[str, Any]]):
        """Store unfollower events in database"""
        try:
            for unfollower in unfollowers:
                await self.db_manager.execute_query(
                    """
                    INSERT INTO unfollower_events 
                    (account_id, unfollower_username, unfollower_display_name, detected_at)
                    SELECT 
                        id, %s, %s, %s
                    FROM social_accounts 
                    WHERE username = %s AND platform = 'tiktok'
                    """,
                    (
                        unfollower['username'],
                        unfollower['display_name'],
                        datetime.now(),
                        username
                    )
                )
                
        except Exception as e:
            logger.error(f"❌ Error storing unfollower events: {e}")
            
    async def schedule_data_collection(self, username: str, interval_hours: int = 6):
        """Schedule periodic data collection for an account"""
        logger.info(f"📅 Scheduling data collection for {username} every {interval_hours} hours")
        
        while True:
            try:
                await self.collect_follower_data(username)
                await self.detect_unfollowers(username)
                await asyncio.sleep(interval_hours * 3600)  # Convert hours to seconds
                
            except Exception as e:
                logger.error(f"❌ Error in scheduled collection for {username}: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes before retrying
