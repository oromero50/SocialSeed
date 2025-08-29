"""
Mock TikTok OAuth Service for Development
Use this while waiting for TikTok Developer approval
"""

import secrets
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class MockTikTokOAuthService:
    """Mock TikTok OAuth for development/testing"""
    
    def __init__(self):
        self.mock_users = {
            'demo_user_1': {
                'username': 'demo_creator',
                'display_name': 'Demo Creator',
                'follower_count': 125000,
                'following_count': 850,
                'likes_count': 2500000,
                'avatar_url': 'https://via.placeholder.com/150/ff69b4/ffffff?text=DC',
                'bio': 'Demo TikTok creator for testing',
                'is_verified': True
            },
            'demo_user_2': {
                'username': 'test_influencer',
                'display_name': 'Test Influencer',
                'follower_count': 45000,
                'following_count': 320,
                'likes_count': 890000,
                'avatar_url': 'https://via.placeholder.com/150/9b59b6/ffffff?text=TI',
                'bio': 'Testing social media automation',
                'is_verified': False
            }
        }
        
        self.current_user = 'demo_user_1'  # Default for testing
    
    def generate_auth_url(self, user_id: str = None) -> Dict[str, str]:
        """Generate mock OAuth URL"""
        try:
            state = secrets.token_urlsafe(32)
            
            # Mock authorization URL - in real implementation this goes to TikTok
            mock_auth_url = f"http://localhost:3000/mock-tiktok-auth?state={state}"
            
            return {
                'auth_url': mock_auth_url,
                'state': state,
                'success': True,
                'is_mock': True,
                'message': 'Mock OAuth for development - click to simulate TikTok login'
            }
            
        except Exception as e:
            logger.error(f"Mock auth URL generation error: {str(e)}")
            return {
                'error': f'Failed to generate mock auth URL: {str(e)}',
                'success': False
            }
    
    async def handle_callback(self, code: str, state: str) -> Dict[str, Any]:
        """Handle mock OAuth callback"""
        try:
            # Simulate TikTok OAuth success
            user_data = self.mock_users[self.current_user].copy()
            
            return {
                'success': True,
                'account_data': {
                    'access_token': f"mock_token_{secrets.token_urlsafe(16)}",
                    'refresh_token': f"mock_refresh_{secrets.token_urlsafe(16)}",
                    'expires_in': 86400,  # 24 hours
                    'token_type': 'Bearer',
                    'user_info': {
                        'tiktok_user_id': f"mock_id_{secrets.token_urlsafe(8)}",
                        'union_id': f"union_{secrets.token_urlsafe(8)}",
                        **user_data
                    },
                    'connected_at': datetime.now().isoformat(),
                    'platform': 'tiktok',
                    'is_mock': True
                }
            }
            
        except Exception as e:
            logger.error(f"Mock OAuth callback error: {str(e)}")
            return {
                'error': f'Mock authentication failed: {str(e)}',
                'success': False
            }
    
    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """Mock token refresh"""
        try:
            return {
                'success': True,
                'access_token': f"mock_token_{secrets.token_urlsafe(16)}",
                'refresh_token': f"mock_refresh_{secrets.token_urlsafe(16)}",
                'expires_in': 86400,
                'is_mock': True
            }
            
        except Exception as e:
            logger.error(f"Mock token refresh error: {str(e)}")
            return {
                'success': False,
                'error': f'Mock token refresh failed: {str(e)}'
            }
    
    def switch_mock_user(self, user_key: str):
        """Switch between mock users for testing"""
        if user_key in self.mock_users:
            self.current_user = user_key
            logger.info(f"Switched to mock user: {user_key}")
        else:
            logger.warning(f"Unknown mock user: {user_key}")
    
    def get_available_mock_users(self) -> Dict[str, str]:
        """Get list of available mock users"""
        return {
            key: data['display_name'] 
            for key, data in self.mock_users.items()
        }
