"""
SocialSeed v2.0 - Advanced Behavioral Mimicking System
Sophisticated human-like behavior patterns with randomization and safety
"""
import asyncio
import random
import datetime
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging
import math

logger = logging.getLogger(__name__)

class ActionResult(Enum):
    SUCCESS = "success"
    RATE_LIMITED = "rate_limited"
    BLOCKED = "blocked"
    ERROR = "error"
    REQUIRES_APPROVAL = "requires_approval"

@dataclass
class BehaviorPattern:
    """Human behavior pattern configuration"""
    active_hours: Tuple[int, int]  # (start_hour, end_hour) in 24h format
    peak_activity_hours: List[Tuple[int, int]]  # Multiple peak periods
    break_intervals: List[Tuple[int, int]]  # (min_break, max_break) in minutes
    action_bursts: Tuple[int, int]  # (min_actions, max_actions) per burst
    burst_delay: Tuple[int, int]  # (min_delay, max_delay) between bursts in seconds
    daily_variance: float  # 0.0-1.0, how much daily patterns vary
    weekly_patterns: Dict[str, float]  # Day-of-week activity multipliers

class HumanBehaviorSimulator:
    """Sophisticated human behavior simulation system"""

    def __init__(self):
        # Default human behavior patterns
        self.default_patterns = {
            "conservative": BehaviorPattern(
                active_hours=(8, 22),  # 8 AM - 10 PM
                peak_activity_hours=[(12, 14), (19, 21)],  # Lunch and evening
                break_intervals=[(30, 120), (60, 240)],  # 30min-2hr, 1hr-4hr breaks
                action_bursts=(1, 3),  # Very small bursts
                burst_delay=(120, 600),  # 2-10 minute delays
                daily_variance=0.3,
                weekly_patterns={
                    "monday": 0.8, "tuesday": 1.0, "wednesday": 1.0,
                    "thursday": 0.9, "friday": 0.7, "saturday": 0.4, "sunday": 0.3
                }
            ),
            "moderate": BehaviorPattern(
                active_hours=(7, 23),  # 7 AM - 11 PM
                peak_activity_hours=[(9, 11), (14, 16), (20, 22)],
                break_intervals=[(15, 90), (45, 180)],
                action_bursts=(2, 6),
                burst_delay=(60, 300),  # 1-5 minute delays
                daily_variance=0.4,
                weekly_patterns={
                    "monday": 0.9, "tuesday": 1.0, "wednesday": 1.1,
                    "thursday": 1.0, "friday": 0.8, "saturday": 0.6, "sunday": 0.4
                }
            ),
            "aggressive": BehaviorPattern(
                active_hours=(6, 24),  # 6 AM - Midnight
                peak_activity_hours=[(8, 10), (12, 14), (16, 18), (20, 23)],
                break_intervals=[(10, 60), (30, 120)],
                action_bursts=(3, 10),
                burst_delay=(30, 180),  # 30sec-3min delays
                daily_variance=0.5,
                weekly_patterns={
                    "monday": 1.0, "tuesday": 1.1, "wednesday": 1.2,
                    "thursday": 1.1, "friday": 1.0, "saturday": 0.8, "sunday": 0.6
                }
            )
        }

        self.current_session_data = {}  # Track current session state

    def calculate_optimal_delay(
        self, 
        account_id: str, 
        action_type: str, 
        phase: str,
        last_action_time: Optional[datetime.datetime] = None
    ) -> Tuple[int, str]:
        """Calculate human-like delay before next action"""

        pattern_name = self._get_pattern_for_phase(phase)
        pattern = self.default_patterns[pattern_name]

        now = datetime.datetime.now()
        current_hour = now.hour
        current_day = now.strftime('%A').lower()

        # Base delay from pattern
        min_delay, max_delay = pattern.burst_delay
        base_delay = random.randint(min_delay, max_delay)

        # Apply time-of-day modifiers
        if self._is_peak_hours(current_hour, pattern):
            delay_modifier = random.uniform(0.7, 1.0)  # Shorter delays during peak
        elif self._is_active_hours(current_hour, pattern):
            delay_modifier = random.uniform(0.9, 1.3)  # Normal delays
        else:
            delay_modifier = random.uniform(2.0, 5.0)  # Much longer delays outside active hours

        # Apply day-of-week modifier
        day_modifier = pattern.weekly_patterns.get(current_day, 1.0)

        # Apply daily variance (some days are just different)
        variance = random.uniform(1 - pattern.daily_variance, 1 + pattern.daily_variance)

        # Calculate final delay
        final_delay = int(base_delay * delay_modifier * day_modifier * variance)

        # Add burst logic - if we're in a burst, shorter delays
        if self._is_in_action_burst(account_id):
            final_delay = int(final_delay * random.uniform(0.3, 0.7))

        # Ensure minimum realistic delay
        final_delay = max(final_delay, 15)  # Minimum 15 seconds

        reasoning = f"Phase: {phase}, Pattern: {pattern_name}, Hour: {current_hour}, Day: {current_day}, Modifier: {delay_modifier:.2f}"

        return final_delay, reasoning

    def should_take_break(self, account_id: str, actions_in_session: int) -> Tuple[bool, int]:
        """Determine if account should take a human-like break"""

        # Get session data
        session = self.current_session_data.get(account_id, {
            'session_start': datetime.datetime.now(),
            'total_actions': 0,
            'last_break': datetime.datetime.now(),
            'consecutive_actions': 0
        })

        # Time since last break
        time_since_break = (datetime.datetime.now() - session['last_break']).total_seconds() / 60

        # Natural break triggers
        break_triggers = [
            (session['consecutive_actions'] > 20, "Too many consecutive actions"),
            (time_since_break > 90, "Long session without break"),
            (random.random() < 0.05, "Random natural break"),  # 5% chance of random break
            (actions_in_session > 0 and actions_in_session % 15 == 0, "Periodic break pattern")
        ]

        for should_break, reason in break_triggers:
            if should_break:
                break_duration = self._calculate_break_duration(reason, session)
                return True, break_duration

        return False, 0

    def simulate_human_typing_delay(self, text_length: int) -> float:
        """Simulate human typing speed for comments/messages"""

        # Average human typing: 40 WPM = ~200 characters per minute
        base_typing_time = (text_length / 200) * 60  # Base time in seconds

        # Add human variance (people don't type at constant speed)
        variance = random.uniform(0.7, 1.5)  # 70%-150% of average speed

        # Add thinking pauses (longer for longer text)
        thinking_time = random.uniform(2, min(10, text_length / 10))

        return base_typing_time * variance + thinking_time

    def _get_pattern_for_phase(self, phase: str) -> str:
        """Get behavior pattern name for current phase"""
        phase_patterns = {
            "phase_1": "conservative",
            "phase_2": "moderate", 
            "phase_3": "aggressive"
        }
        return phase_patterns.get(phase, "conservative")

    def _is_peak_hours(self, hour: int, pattern: BehaviorPattern) -> bool:
        """Check if current hour is in peak activity period"""
        for start, end in pattern.peak_activity_hours:
            if start <= hour <= end:
                return True
        return False

    def _is_active_hours(self, hour: int, pattern: BehaviorPattern) -> bool:
        """Check if current hour is in active period"""
        start, end = pattern.active_hours
        return start <= hour <= end

    def _is_in_action_burst(self, account_id: str) -> bool:
        """Check if account is currently in an action burst"""
        session = self.current_session_data.get(account_id, {})
        last_action = session.get('last_action_time')

        if not last_action:
            return False

        # If last action was within 2 minutes, consider it part of burst
        return (datetime.datetime.now() - last_action).total_seconds() < 120

    def _calculate_break_duration(self, reason: str, session_data: Dict) -> int:
        """Calculate appropriate break duration based on reason"""

        break_durations = {
            "Too many consecutive actions": (10, 30),  # 10-30 minutes
            "Long session without break": (5, 15),     # 5-15 minutes
            "Random natural break": (2, 8),           # 2-8 minutes
            "Periodic break pattern": (3, 12)         # 3-12 minutes
        }

        min_break, max_break = break_durations.get(reason, (5, 15))
        return random.randint(min_break, max_break) * 60  # Convert to seconds

class PlatformHealthMonitor:
    """Real-time platform health monitoring with exponential backoff"""

    def __init__(self):
        self.platform_health = {}
        self.rate_limit_history = {}
        self.error_patterns = {}

    async def monitor_platform_response(
        self, 
        platform: str, 
        response_code: int, 
        response_time: float,
        account_id: str
    ) -> Dict:
        """Monitor platform response for health indicators"""

        now = datetime.datetime.now()

        # Initialize platform tracking
        if platform not in self.platform_health:
            self.platform_health[platform] = {
                'status': 'healthy',
                'last_error': None,
                'consecutive_errors': 0,
                'avg_response_time': response_time,
                'rate_limit_count': 0,
                'last_rate_limit': None
            }

        health = self.platform_health[platform]

        # Update response time average
        health['avg_response_time'] = (health['avg_response_time'] + response_time) / 2

        # Analyze response
        if response_code == 429:  # Rate limited
            health['rate_limit_count'] += 1
            health['last_rate_limit'] = now
            await self._handle_rate_limit(platform, account_id)
            return {'status': 'rate_limited', 'backoff_seconds': self._get_backoff_time(platform)}

        elif 400 <= response_code < 500:  # Client error
            health['consecutive_errors'] += 1
            health['last_error'] = now
            await self._handle_client_error(platform, account_id, response_code)
            return {'status': 'error', 'severity': 'medium'}

        elif response_code >= 500:  # Server error
            health['consecutive_errors'] += 1
            health['last_error'] = now
            await self._handle_server_error(platform, account_id, response_code)
            return {'status': 'error', 'severity': 'high'}

        else:  # Success
            health['consecutive_errors'] = 0
            health['status'] = 'healthy'
            return {'status': 'success'}

    async def _handle_rate_limit(self, platform: str, account_id: str):
        """Handle rate limiting with exponential backoff"""

        # Track rate limit patterns
        if platform not in self.rate_limit_history:
            self.rate_limit_history[platform] = []

        self.rate_limit_history[platform].append(datetime.datetime.now())

        # Keep only last 24 hours of rate limit data
        cutoff = datetime.datetime.now() - datetime.timedelta(hours=24)
        self.rate_limit_history[platform] = [
            ts for ts in self.rate_limit_history[platform] if ts > cutoff
        ]

        logger.warning(f"Rate limited on {platform} for account {account_id}")

    def _get_backoff_time(self, platform: str) -> int:
        """Calculate exponential backoff time for rate limits"""

        rate_limits = self.rate_limit_history.get(platform, [])
        recent_limits = len([
            ts for ts in rate_limits 
            if ts > datetime.datetime.now() - datetime.timedelta(hours=1)
        ])

        # Exponential backoff: 2^recent_limits * base_time
        base_time = 60  # 1 minute base
        backoff_time = min(base_time * (2 ** recent_limits), 3600)  # Max 1 hour

        return backoff_time

    async def _handle_client_error(self, platform: str, account_id: str, error_code: int):
        """Handle client errors (4xx responses)"""

        error_handlers = {
            401: "Authentication failed - check credentials",
            403: "Forbidden - possible account restriction", 
            404: "Resource not found - target may be deleted",
            422: "Invalid request data - check parameters"
        }

        message = error_handlers.get(error_code, f"Client error {error_code}")
        logger.error(f"{platform} client error {error_code} for {account_id}: {message}")

        # If too many consecutive errors, pause account
        health = self.platform_health[platform]
        if health['consecutive_errors'] > 5:
            logger.critical(f"Too many errors on {platform} - pausing operations")

    async def _handle_server_error(self, platform: str, account_id: str, error_code: int):
        """Handle server errors (5xx responses)"""

        logger.error(f"{platform} server error {error_code} for {account_id}")

        # Server errors often resolve themselves, but track patterns
        health = self.platform_health[platform]
        if health['consecutive_errors'] > 3:
            logger.warning(f"{platform} experiencing server issues - reducing activity")

class GracefulDegradationHandler:
    """Handle platform policy changes and API failures gracefully"""

    def __init__(self):
        self.degraded_services = {}
        self.fallback_strategies = {}

    async def handle_api_failure(self, platform: str, service: str, error: Exception) -> Dict:
        """Handle API failures with graceful degradation"""

        failure_type = self._classify_failure(error)

        degradation_strategies = {
            "rate_limit": self._handle_rate_limit_degradation,
            "authentication": self._handle_auth_degradation,
            "api_change": self._handle_api_change_degradation,
            "network": self._handle_network_degradation,
            "unknown": self._handle_unknown_degradation
        }

        handler = degradation_strategies.get(failure_type, self._handle_unknown_degradation)
        return await handler(platform, service, error)

    def _classify_failure(self, error: Exception) -> str:
        """Classify failure type for appropriate handling"""

        error_str = str(error).lower()

        if "rate limit" in error_str or "429" in error_str:
            return "rate_limit"
        elif "unauthorized" in error_str or "401" in error_str:
            return "authentication"
        elif "not found" in error_str or "404" in error_str:
            return "api_change"
        elif "network" in error_str or "timeout" in error_str:
            return "network"
        else:
            return "unknown"

    async def _handle_rate_limit_degradation(self, platform: str, service: str, error: Exception) -> Dict:
        """Handle rate limiting gracefully"""

        return {
            "action": "pause_and_retry",
            "delay_seconds": 900,  # 15 minutes
            "reduce_activity": True,
            "message": f"{platform} {service} rate limited - reducing activity"
        }

    async def _handle_auth_degradation(self, platform: str, service: str, error: Exception) -> Dict:
        """Handle authentication failures"""

        return {
            "action": "pause_service",
            "require_manual_intervention": True,
            "message": f"{platform} {service} authentication failed - manual intervention required"
        }

    async def _handle_api_change_degradation(self, platform: str, service: str, error: Exception) -> Dict:
        """Handle API changes/deprecations"""

        return {
            "action": "disable_service",
            "require_update": True,
            "message": f"{platform} {service} API may have changed - service disabled pending update"
        }

    async def _handle_network_degradation(self, platform: str, service: str, error: Exception) -> Dict:
        """Handle network issues"""

        return {
            "action": "retry_with_backoff",
            "max_retries": 3,
            "backoff_multiplier": 2,
            "message": f"{platform} {service} network issue - retrying with backoff"
        }

    async def _handle_unknown_degradation(self, platform: str, service: str, error: Exception) -> Dict:
        """Handle unknown failures"""

        return {
            "action": "pause_and_alert",
            "delay_seconds": 300,  # 5 minutes
            "require_investigation": True,
            "message": f"{platform} {service} unknown error - investigation required"
        }
