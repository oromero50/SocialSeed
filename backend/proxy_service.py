"""
SocialSeed v2.0 - Proxy Service
Proxy rotation and management for scaling operations
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random
import aiohttp
import json
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class ProxyService:
    """Proxy service for managing proxy rotation and health"""
    
    def __init__(self):
        self.proxies = []
        self.current_proxy_index = 0
        self.proxy_health = {}
        self.rotation_enabled = False
        self.proxy_provider = None
        self.is_initialized = False
        
        # Configuration
        self.max_proxies = 50
        self.health_check_interval = 300  # 5 minutes
        self.proxy_timeout = 30  # 30 seconds
        self.max_failures = 3
        
    async def initialize(self):
        """Initialize proxy service"""
        logger.info("Initializing Proxy Service...")
        
        # Check if proxies are enabled
        if not self._get_env_var("USE_PROXIES", "false").lower() == "true":
            logger.info("Proxy service disabled - running without proxies")
            self.is_initialized = True
            return
        
        # Setup proxy provider
        await self._setup_proxy_provider()
        
        # Load initial proxies
        await self._load_proxies()
        
        # Start health monitoring
        asyncio.create_task(self._monitor_proxy_health())
        
        self.is_initialized = True
        logger.info(f"✅ Proxy Service initialized with {len(self.proxies)} proxies")
    
    async def _setup_proxy_provider(self):
        """Setup proxy provider based on configuration"""
        provider_name = self._get_env_var("PROXY_PROVIDER", "iproyal")
        
        if provider_name == "iproyal":
            self.proxy_provider = IPRoyalProvider()
        elif provider_name == "smartproxy":
            self.proxy_provider = SmartProxyProvider()
        elif provider_name == "brightdata":
            self.proxy_provider = BrightDataProvider()
        else:
            logger.warning(f"Unknown proxy provider: {provider_name}, using IPRoyal")
            self.proxy_provider = IPRoyalProvider()
        
        await self.proxy_provider.initialize()
    
    async def _load_proxies(self):
        """Load proxies from provider"""
        try:
            proxy_list = await self.proxy_provider.get_proxy_list()
            
            for proxy_data in proxy_list:
                proxy = Proxy(
                    host=proxy_data['host'],
                    port=proxy_data['port'],
                    username=proxy_data.get('username'),
                    password=proxy_data.get('password'),
                    country=proxy_data.get('country', 'unknown'),
                    provider=proxy_data.get('provider', 'unknown')
                )
                
                self.proxies.append(proxy)
                self.proxy_health[proxy.id] = {
                    'failures': 0,
                    'last_success': None,
                    'last_failure': None,
                    'response_time': None
                }
            
            logger.info(f"Loaded {len(self.proxies)} proxies")
            
        except Exception as e:
            logger.error(f"Failed to load proxies: {e}")
            # Continue without proxies
            self.proxies = []
    
    async def get_proxy(self, platform: str = None, country: str = None) -> Optional[Proxy]:
        """Get a healthy proxy for use"""
        if not self.proxies:
            return None
        
        # Filter healthy proxies
        healthy_proxies = [
            proxy for proxy in self.proxies
            if self._is_proxy_healthy(proxy.id)
        ]
        
        if not healthy_proxies:
            logger.warning("No healthy proxies available")
            return None
        
        # Filter by country if specified
        if country:
            country_proxies = [p for p in healthy_proxies if p.country.lower() == country.lower()]
            if country_proxies:
                healthy_proxies = country_proxies
        
        # Select proxy using round-robin with health weighting
        selected_proxy = self._select_proxy(healthy_proxies)
        
        if selected_proxy:
            logger.debug(f"Selected proxy {selected_proxy.id} for {platform}")
        
        return selected_proxy
    
    def _is_proxy_healthy(self, proxy_id: str) -> bool:
        """Check if proxy is healthy"""
        if proxy_id not in self.proxy_health:
            return False
        
        health = self.proxy_health[proxy_id]
        
        # Check failure count
        if health['failures'] >= self.max_failures:
            return False
        
        # Check if proxy has been used recently
        if health['last_success']:
            time_since_success = (datetime.utcnow() - health['last_success']).total_seconds()
            if time_since_success < 60:  # 1 minute cooldown
                return False
        
        return True
    
    def _select_proxy(self, healthy_proxies: List[Proxy]) -> Optional[Proxy]:
        """Select proxy using weighted round-robin"""
        if not healthy_proxies:
            return None
        
        # Weight proxies by health score
        weighted_proxies = []
        for proxy in healthy_proxies:
            health = self.proxy_health.get(proxy.id, {})
            
            # Calculate health score
            health_score = 1.0
            if health.get('failures', 0) > 0:
                health_score -= (health['failures'] * 0.2)
            
            if health.get('response_time'):
                # Prefer faster proxies
                if health['response_time'] < 1.0:
                    health_score += 0.2
                elif health['response_time'] > 5.0:
                    health_score -= 0.3
            
            health_score = max(0.1, health_score)  # Minimum score
            
            weighted_proxies.append((proxy, health_score))
        
        # Sort by health score (descending)
        weighted_proxies.sort(key=lambda x: x[1], reverse=True)
        
        # Select from top 3 proxies randomly
        top_proxies = weighted_proxies[:3]
        selected = random.choice(top_proxies)[0]
        
        return selected
    
    async def mark_proxy_success(self, proxy_id: str, response_time: float = None):
        """Mark proxy as successful"""
        if proxy_id in self.proxy_health:
            self.proxy_health[proxy_id]['failures'] = 0
            self.proxy_health[proxy_id]['last_success'] = datetime.utcnow()
            if response_time:
                self.proxy_health[proxy_id]['response_time'] = response_time
    
    async def mark_proxy_failure(self, proxy_id: str, error: str = None):
        """Mark proxy as failed"""
        if proxy_id in self.proxy_health:
            self.proxy_health[proxy_id]['failures'] += 1
            self.proxy_health[proxy_id]['last_failure'] = datetime.utcnow()
            
            logger.warning(f"Proxy {proxy_id} failed: {error}")
            
            # Remove proxy if too many failures
            if self.proxy_health[proxy_id]['failures'] >= self.max_failures:
                logger.error(f"Removing proxy {proxy_id} due to repeated failures")
                await self._remove_proxy(proxy_id)
    
    async def _remove_proxy(self, proxy_id: str):
        """Remove a failed proxy"""
        # Remove from health tracking
        if proxy_id in self.proxy_health:
            del self.proxy_health[proxy_id]
        
        # Remove from proxy list
        self.proxies = [p for p in self.proxies if p.id != proxy_id]
        
        # Try to add new proxy if we're running low
        if len(self.proxies) < self.max_proxies // 2:
            await self._add_new_proxies()
    
    async def _add_new_proxies(self):
        """Add new proxies to replace failed ones"""
        try:
            new_proxies = await self.proxy_provider.get_proxy_list(count=5)
            
            for proxy_data in new_proxies:
                proxy = Proxy(
                    host=proxy_data['host'],
                    port=proxy_data['port'],
                    username=proxy_data.get('username'),
                    password=proxy_data.get('password'),
                    country=proxy_data.get('country', 'unknown'),
                    provider=proxy_data.get('provider', 'unknown')
                )
                
                self.proxies.append(proxy)
                self.proxy_health[proxy.id] = {
                    'failures': 0,
                    'last_success': None,
                    'last_failure': None,
                    'response_time': None
                }
            
            logger.info(f"Added {len(new_proxies)} new proxies")
            
        except Exception as e:
            logger.error(f"Failed to add new proxies: {e}")
    
    async def _monitor_proxy_health(self):
        """Monitor proxy health in background"""
        while self.is_initialized:
            try:
                await self._check_all_proxies()
                await asyncio.sleep(self.health_check_interval)
            except Exception as e:
                logger.error(f"Proxy health monitoring error: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying
    
    async def _check_all_proxies(self):
        """Check health of all proxies"""
        logger.debug("Running proxy health check...")
        
        for proxy in self.proxies[:]:  # Copy list to avoid modification during iteration
            try:
                start_time = datetime.utcnow()
                
                # Test proxy with simple HTTP request
                success = await self._test_proxy(proxy)
                
                if success:
                    response_time = (datetime.utcnow() - start_time).total_seconds()
                    await self.mark_proxy_success(proxy.id, response_time)
                else:
                    await self.mark_proxy_failure(proxy.id, "Health check failed")
                
            except Exception as e:
                await self.mark_proxy_failure(proxy.id, str(e))
    
    async def _test_proxy(self, proxy: 'Proxy') -> bool:
        """Test proxy connectivity"""
        try:
            proxy_url = proxy.get_proxy_url()
            
            timeout = aiohttp.ClientTimeout(total=self.proxy_timeout)
            connector = aiohttp.ProxyConnector.from_url(proxy_url)
            
            async with aiohttp.ClientSession(
                connector=connector,
                timeout=timeout
            ) as session:
                async with session.get('http://httpbin.org/ip') as response:
                    if response.status == 200:
                        return True
                    return False
                    
        except Exception as e:
            logger.debug(f"Proxy test failed for {proxy.id}: {e}")
            return False
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get proxy service status"""
        healthy_count = sum(1 for proxy_id in self.proxy_health if self._is_proxy_healthy(proxy_id))
        total_count = len(self.proxies)
        
        return {
            'status': 'active' if self.is_initialized else 'inactive',
            'total_proxies': total_count,
            'healthy_proxies': healthy_count,
            'rotation_enabled': self.rotation_enabled,
            'provider': self.proxy_provider.__class__.__name__ if self.proxy_provider else None,
            'last_updated': datetime.utcnow().isoformat()
        }
    
    def _get_env_var(self, key: str, default: str = None) -> str:
        """Get environment variable"""
        import os
        return os.getenv(key, default)

class Proxy:
    """Proxy representation"""
    
    def __init__(self, host: str, port: int, username: str = None, password: str = None, 
                 country: str = "unknown", provider: str = "unknown"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.country = country
        self.provider = provider
        self.id = f"{provider}_{host}_{port}"
    
    def get_proxy_url(self) -> str:
        """Get proxy URL for HTTP client"""
        if self.username and self.password:
            return f"http://{self.username}:{self.password}@{self.host}:{self.port}"
        else:
            return f"http://{self.host}:{self.port}"
    
    def __str__(self):
        return f"Proxy({self.host}:{self.port}, {self.country})"

class IPRoyalProvider:
    """IPRoyal proxy provider"""
    
    def __init__(self):
        self.username = None
        self.password = None
        self.api_url = "https://panel.iproyal.com/api"
    
    async def initialize(self):
        """Initialize IPRoyal provider"""
        import os
        self.username = os.getenv("IPROYAL_USERNAME")
        self.password = os.getenv("IPROYAL_PASSWORD")
        
        if not self.username or not self.password:
            raise ValueError("IPRoyal credentials not configured")
    
    async def get_proxy_list(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get proxy list from IPRoyal"""
        # Mock implementation - in real usage, this would call IPRoyal API
        proxies = []
        
        for i in range(count):
            proxies.append({
                'host': f'proxy-{i}.iproyal.com',
                'port': random.randint(8000, 9000),
                'username': self.username,
                'password': self.password,
                'country': random.choice(['US', 'UK', 'CA', 'DE', 'FR']),
                'provider': 'iproyal'
            })
        
        return proxies

class SmartProxyProvider:
    """SmartProxy provider"""
    
    def __init__(self):
        self.api_key = None
    
    async def initialize(self):
        """Initialize SmartProxy provider"""
        import os
        self.api_key = os.getenv("SMARTPROXY_API_KEY")
        
        if not self.api_key:
            raise ValueError("SmartProxy API key not configured")
    
    async def get_proxy_list(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get proxy list from SmartProxy"""
        # Mock implementation
        proxies = []
        
        for i in range(count):
            proxies.append({
                'host': f'proxy-{i}.smartproxy.com',
                'port': random.randint(7000, 8000),
                'username': f'user-{i}',
                'password': f'pass-{i}',
                'country': random.choice(['US', 'UK', 'CA', 'DE', 'FR']),
                'provider': 'smartproxy'
            })
        
        return proxies

class BrightDataProvider:
    """Bright Data provider"""
    
    def __init__(self):
        self.username = None
        self.password = None
    
    async def initialize(self):
        """Initialize Bright Data provider"""
        import os
        self.username = os.getenv("BRIGHTDATA_USERNAME")
        self.password = os.getenv("BRIGHTDATA_PASSWORD")
        
        if not self.username or not self.password:
            raise ValueError("Bright Data credentials not configured")
    
    async def get_proxy_list(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get proxy list from Bright Data"""
        # Mock implementation
        proxies = []
        
        for i in range(count):
            proxies.append({
                'host': f'proxy-{i}.brightdata.com',
                'port': random.randint(6000, 7000),
                'username': self.username,
                'password': self.password,
                'country': random.choice(['US', 'UK', 'CA', 'DE', 'FR']),
                'provider': 'brightdata'
            })
        
        return proxies

