"""
TikTok OAuth Service for SocialSeed
User-friendly login flow without manual token extraction
"""

import os
import secrets
import hashlib
import base64
import urllib.parse
from typing import Dict, Optional, Any
import httpx
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class TikTokOAuthService:
    """TikTok OAuth 2.0 implementation for user-friendly login"""
    
    def __init__(self):
        self.client_id = os.getenv('TIKTOK_CLIENT_ID', 'your_tiktok_client_id')
        self.client_secret = os.getenv('TIKTOK_CLIENT_SECRET', 'your_tiktok_client_secret')
        self.redirect_uri = os.getenv('TIKTOK_REDIRECT_URI', 'http://localhost:3000/tiktok-callback')
        
        # TikTok OAuth endpoints
        self.auth_url = "https://www.tiktok.com/v2/auth/authorize/"
        self.token_url = "https://open.tiktokapis.com/v2/oauth/token/"
        self.user_info_url = "https://open.tiktokapis.com/v2/user/info/"
        
        # Scopes we need
        self.scopes = [
            'user.info.basic',     # Basic user info
            'user.info.profile',   # Profile info including follower count
            'user.info.stats',     # User statistics
        ]
        
        # Store pending auth states
        self.auth_states = {}
    
    def generate_auth_url(self, user_id: str = None) -> Dict[str, str]:
        """Generate OAuth authorization URL for user-friendly login"""
        try:
            # Generate secure state parameter
            state = secrets.token_urlsafe(32)
            
            # Store state for verification
            self.auth_states[state] = {
                'user_id': user_id,
                'created_at': datetime.now(),
                'expires_at': datetime.now() + timedelta(minutes=10)
            }
            
            # Generate code challenge for PKCE (more secure)
            code_verifier = secrets.token_urlsafe(32)
            code_challenge = base64.urlsafe_b64encode(
                hashlib.sha256(code_verifier.encode()).digest()
            ).decode().rstrip('=')
            
            # Store verifier for later use
            self.auth_states[state]['code_verifier'] = code_verifier
            
            # Build authorization URL
            params = {
                'client_key': self.client_id,
                'scope': ','.join(self.scopes),
                'response_type': 'code',
                'redirect_uri': self.redirect_uri,
                'state': state,
                'code_challenge': code_challenge,
                'code_challenge_method': 'S256'
            }
            
            auth_url = f"{self.auth_url}?{urllib.parse.urlencode(params)}"
            
            return {
                'auth_url': auth_url,
                'state': state,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error generating auth URL: {str(e)}")
            return {
                'error': f'Failed to generate authorization URL: {str(e)}',
                'success': False
            }
    
    async def handle_callback(self, code: str, state: str) -> Dict[str, Any]:
        """Handle OAuth callback and exchange code for access token"""
        try:
            # Verify state parameter
            if state not in self.auth_states:
                return {'error': 'Invalid state parameter', 'success': False}
            
            auth_state = self.auth_states[state]
            
            # Check if state has expired
            if datetime.now() > auth_state['expires_at']:
                del self.auth_states[state]
                return {'error': 'Authorization session expired', 'success': False}
            
            # Exchange code for access token
            token_data = await self._exchange_code_for_token(code, auth_state['code_verifier'])
            
            if not token_data.get('success'):
                return token_data
            
            # Get user info with the access token
            user_info = await self._get_user_info(token_data['access_token'])
            
            if not user_info.get('success'):
                return user_info
            
            # Clean up auth state
            del self.auth_states[state]
            
            # Return complete account information
            return {
                'success': True,
                'account_data': {
                    'access_token': token_data['access_token'],
                    'refresh_token': token_data.get('refresh_token'),
                    'expires_in': token_data.get('expires_in'),
                    'token_type': token_data.get('token_type', 'Bearer'),
                    'user_info': user_info['user_data'],
                    'connected_at': datetime.now().isoformat(),
                    'platform': 'tiktok'
                }
            }
            
        except Exception as e:
            logger.error(f"OAuth callback error: {str(e)}")
            return {
                'error': f'Authentication failed: {str(e)}',
                'success': False
            }
    
    async def _exchange_code_for_token(self, code: str, code_verifier: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        try:
            async with httpx.AsyncClient() as client:
                data = {
                    'client_key': self.client_id,
                    'client_secret': self.client_secret,
                    'code': code,
                    'grant_type': 'authorization_code',
                    'redirect_uri': self.redirect_uri,
                    'code_verifier': code_verifier
                }
                
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Cache-Control': 'no-cache'
                }
                
                response = await client.post(
                    self.token_url,
                    data=data,
                    headers=headers,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    token_data = response.json()
                    
                    if 'access_token' in token_data:
                        return {
                            'success': True,
                            'access_token': token_data['access_token'],
                            'refresh_token': token_data.get('refresh_token'),
                            'expires_in': token_data.get('expires_in'),
                            'token_type': token_data.get('token_type', 'Bearer')
                        }
                    else:
                        return {
                            'success': False,
                            'error': f"Token exchange failed: {token_data.get('error_description', 'Unknown error')}"
                        }
                else:
                    return {
                        'success': False,
                        'error': f"Token request failed with status {response.status_code}: {response.text}"
                    }
                    
        except Exception as e:
            logger.error(f"Token exchange error: {str(e)}")
            return {
                'success': False,
                'error': f'Token exchange failed: {str(e)}'
            }
    
    async def _get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get user information using access token"""
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                }
                
                response = await client.post(
                    self.user_info_url,
                    headers=headers,
                    json={'fields': ['open_id', 'union_id', 'avatar_url', 'display_name', 'username', 'follower_count', 'following_count', 'likes_count']},
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    user_data = response.json()
                    
                    if 'data' in user_data and 'user' in user_data['data']:
                        user_info = user_data['data']['user']
                        
                        return {
                            'success': True,
                            'user_data': {
                                'tiktok_user_id': user_info.get('open_id'),
                                'union_id': user_info.get('union_id'),
                                'username': user_info.get('username'),
                                'display_name': user_info.get('display_name'),
                                'avatar_url': user_info.get('avatar_url'),
                                'follower_count': user_info.get('follower_count', 0),
                                'following_count': user_info.get('following_count', 0),
                                'likes_count': user_info.get('likes_count', 0),
                                'is_verified': user_info.get('is_verified', False),
                                'bio': user_info.get('bio_description', '')
                            }
                        }
                    else:
                        return {
                            'success': False,
                            'error': f"Invalid user data response: {user_data}"
                        }
                else:
                    return {
                        'success': False,
                        'error': f"User info request failed with status {response.status_code}: {response.text}"
                    }
                    
        except Exception as e:
            logger.error(f"User info error: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to get user info: {str(e)}'
            }
    
    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh an expired access token"""
        try:
            async with httpx.AsyncClient() as client:
                data = {
                    'client_key': self.client_id,
                    'client_secret': self.client_secret,
                    'grant_type': 'refresh_token',
                    'refresh_token': refresh_token
                }
                
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                
                response = await client.post(
                    self.token_url,
                    data=data,
                    headers=headers,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    token_data = response.json()
                    
                    if 'access_token' in token_data:
                        return {
                            'success': True,
                            'access_token': token_data['access_token'],
                            'refresh_token': token_data.get('refresh_token'),
                            'expires_in': token_data.get('expires_in')
                        }
                    else:
                        return {
                            'success': False,
                            'error': f"Token refresh failed: {token_data.get('error_description', 'Unknown error')}"
                        }
                else:
                    return {
                        'success': False,
                        'error': f"Token refresh failed with status {response.status_code}: {response.text}"
                    }
                    
        except Exception as e:
            logger.error(f"Token refresh error: {str(e)}")
            return {
                'success': False,
                'error': f'Token refresh failed: {str(e)}'
            }
    
    def cleanup_expired_states(self):
        """Clean up expired authorization states"""
        now = datetime.now()
        expired_states = [
            state for state, data in self.auth_states.items()
            if now > data['expires_at']
        ]
        
        for state in expired_states:
            del self.auth_states[state]
        
        logger.info(f"Cleaned up {len(expired_states)} expired auth states")
