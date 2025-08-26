"""
SocialSeed v2.0 - Account Authenticity Analyzer
Advanced LLM-powered system to identify genuine vs bot accounts
"""
import asyncio
import datetime
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class AuthenticityScore(Enum):
    GENUINE = "genuine"           # 0.8-1.0: Clearly authentic human account
    LIKELY_GENUINE = "likely_genuine"  # 0.6-0.8: Probably human with some concerns
    SUSPICIOUS = "suspicious"     # 0.3-0.6: Unclear, proceed with caution
    LIKELY_BOT = "likely_bot"    # 0.1-0.3: Probably automated account
    DEFINITE_BOT = "definite_bot" # 0.0-0.1: Clear bot patterns

@dataclass
class ProfileAnalysis:
    """Profile analysis result"""
    username: str
    platform: str
    authenticity_score: float  # 0.0-1.0
    authenticity_level: AuthenticityScore
    confidence: float
    reasoning: str
    red_flags: List[str]
    green_flags: List[str]
    recommendation: str

class AccountAuthenticityAnalyzer:
    """Advanced account authenticity analyzer using LLM and pattern analysis"""

    def __init__(self, ai_service):
        self.ai_service = ai_service

        # Bot pattern indicators
        self.bot_patterns = {
            "username_patterns": [
                r"^[a-z]+\d{4,8}$",  # letters followed by numbers
                r"^user\d+$",         # user123
                r"^\w+_\d+$",        # name_123
                r"^[a-z]{8,12}\d{2,4}$"  # random letters + numbers
            ],
            "bio_bot_indicators": [
                "dm for promo", "follow for follow", "f4f", "l4l",
                "click link", "free followers", "bot", "automation",
                "crypto", "investment opportunity", "make money fast"
            ],
            "suspicious_metrics": {
                "high_following_low_followers": 10.0,  # Following:Followers ratio
                "zero_posts_high_followers": True,
                "perfect_engagement": 0.95,  # Suspiciously high engagement
                "zero_engagement": 0.001     # Suspiciously low engagement
            }
        }

    async def analyze_profile(self, profile_data: Dict) -> ProfileAnalysis:
        """Comprehensive profile authenticity analysis"""

        # Extract profile components
        username = profile_data.get('username', '')
        bio = profile_data.get('bio', '')
        followers = profile_data.get('followers_count', 0)
        following = profile_data.get('following_count', 0)
        posts = profile_data.get('posts_count', 0)
        engagement_rate = profile_data.get('engagement_rate', 0.0)
        profile_pic = profile_data.get('has_profile_picture', False)
        verified = profile_data.get('verified', False)
        creation_date = profile_data.get('created_at')
        platform = profile_data.get('platform', 'unknown')

        # Run pattern-based analysis
        pattern_score, pattern_flags = self._analyze_patterns(
            username, bio, followers, following, posts, 
            engagement_rate, profile_pic, verified, creation_date
        )

        # Run LLM-based analysis
        llm_analysis = await self._llm_authenticity_analysis(profile_data)

        # Combine scores (70% LLM, 30% patterns for better accuracy)
        combined_score = (llm_analysis['score'] * 0.7) + (pattern_score * 0.3)

        # Determine authenticity level
        authenticity_level = self._score_to_level(combined_score)

        # Combine flags and recommendations
        all_flags = pattern_flags + llm_analysis.get('red_flags', [])
        green_flags = llm_analysis.get('green_flags', [])

        return ProfileAnalysis(
            username=username,
            platform=platform,
            authenticity_score=combined_score,
            authenticity_level=authenticity_level,
            confidence=llm_analysis.get('confidence', 0.8),
            reasoning=llm_analysis.get('reasoning', ''),
            red_flags=list(set(all_flags)),  # Remove duplicates
            green_flags=green_flags,
            recommendation=self._get_recommendation(authenticity_level, combined_score)
        )

    def _analyze_patterns(
        self, username: str, bio: str, followers: int, following: int,
        posts: int, engagement_rate: float, has_pic: bool, verified: bool,
        created_date: Optional[datetime.datetime]
    ) -> Tuple[float, List[str]]:
        """Pattern-based bot detection analysis"""

        score = 1.0  # Start with maximum authenticity
        flags = []

        # Username analysis
        username_score = self._analyze_username_patterns(username)
        if username_score < 0.5:
            score -= 0.2
            flags.append(f"Suspicious username pattern: {username}")

        # Bio analysis
        bio_lower = bio.lower()
        bot_bio_count = sum(1 for indicator in self.bot_patterns["bio_bot_indicators"] 
                           if indicator in bio_lower)
        if bot_bio_count > 0:
            score -= min(0.3, bot_bio_count * 0.1)
            flags.append(f"Bot-like bio content ({bot_bio_count} indicators)")

        # Follower ratio analysis
        if followers > 0:
            follow_ratio = following / followers
            if follow_ratio > self.bot_patterns["suspicious_metrics"]["high_following_low_followers"]:
                score -= 0.3
                flags.append(f"Suspicious follow ratio: {follow_ratio:.1f}")

        # Posts vs followers analysis
        if followers > 1000 and posts == 0:
            score -= 0.4
            flags.append("High followers but zero posts")

        # Engagement analysis
        if engagement_rate > self.bot_patterns["suspicious_metrics"]["perfect_engagement"]:
            score -= 0.2
            flags.append(f"Suspiciously high engagement: {engagement_rate:.2%}")
        elif engagement_rate < self.bot_patterns["suspicious_metrics"]["zero_engagement"] and followers > 100:
            score -= 0.3
            flags.append(f"Suspiciously low engagement: {engagement_rate:.2%}")

        # Profile picture analysis
        if not has_pic:
            score -= 0.1
            flags.append("No profile picture")

        # Account age analysis (if available)
        if created_date:
            account_age_days = (datetime.datetime.now() - created_date).days
            if account_age_days < 7:  # Very new account
                score -= 0.2
                flags.append(f"Very new account ({account_age_days} days)")

        return max(0.0, score), flags

    def _analyze_username_patterns(self, username: str) -> float:
        """Analyze username for bot-like patterns"""
        username_lower = username.lower()

        for pattern in self.bot_patterns["username_patterns"]:
            if re.match(pattern, username_lower):
                return 0.3  # Low authenticity for matching bot patterns

        # Additional checks
        if len(username) > 15:  # Very long usernames
            return 0.6
        if username.count('_') > 2:  # Multiple underscores
            return 0.5
        if len(re.findall(r'\d', username)) > len(username) * 0.5:  # More than 50% numbers
            return 0.4

        return 1.0  # Looks authentic

    async def _llm_authenticity_analysis(self, profile_data: Dict) -> Dict:
        """LLM-powered authenticity analysis"""

        analysis_prompt = f"""
        Analyze this social media profile for authenticity (human vs bot/fake account):

        Profile Data:
        - Username: {profile_data.get('username', '')}
        - Bio: {profile_data.get('bio', '')}
        - Followers: {profile_data.get('followers_count', 0)}
        - Following: {profile_data.get('following_count', 0)}
        - Posts: {profile_data.get('posts_count', 0)}
        - Engagement Rate: {profile_data.get('engagement_rate', 0):.3f}
        - Has Profile Picture: {profile_data.get('has_profile_picture', False)}
        - Verified: {profile_data.get('verified', False)}
        - Platform: {profile_data.get('platform', 'unknown')}
        - Recent Post Titles: {profile_data.get('recent_posts', [])}

        Consider these authenticity indicators:

        HUMAN INDICATORS:
        - Natural, conversational bio
        - Balanced follower/following ratio
        - Consistent posting history
        - Realistic engagement rates
        - Personal photos/content
        - Genuine interactions
        - Varied content types

        BOT INDICATORS:
        - Generic/promotional bio
        - Extreme follower ratios
        - No posts but high followers
        - Perfect/zero engagement
        - Stock photos
        - Repetitive content
        - Automated responses
        - Suspicious creation patterns

        Respond with JSON:
        {{
            "score": 0.85,
            "confidence": 0.9,
            "reasoning": "Detailed analysis of why this appears genuine/fake",
            "red_flags": ["flag1", "flag2"],
            "green_flags": ["positive1", "positive2"],
            "primary_concern": "Main issue if any"
        }}

        Score: 0.0-0.2 = Definite Bot, 0.2-0.4 = Likely Bot, 0.4-0.6 = Suspicious, 0.6-0.8 = Likely Human, 0.8-1.0 = Genuine Human
        """

        try:
            response = await self.ai_service.analyze_text(analysis_prompt)
            return response
        except Exception as e:
            logger.error(f"LLM authenticity analysis failed: {e}")
            # Fallback to pattern-only analysis
            return {
                "score": 0.5,
                "confidence": 0.5,
                "reasoning": "LLM analysis failed, using pattern analysis only",
                "red_flags": ["LLM analysis unavailable"],
                "green_flags": []
            }

    def _score_to_level(self, score: float) -> AuthenticityScore:
        """Convert numerical score to authenticity level"""
        if score >= 0.8:
            return AuthenticityScore.GENUINE
        elif score >= 0.6:
            return AuthenticityScore.LIKELY_GENUINE
        elif score >= 0.4:
            return AuthenticityScore.SUSPICIOUS
        elif score >= 0.2:
            return AuthenticityScore.LIKELY_BOT
        else:
            return AuthenticityScore.DEFINITE_BOT

    def _get_recommendation(self, level: AuthenticityScore, score: float) -> str:
        """Get interaction recommendation based on authenticity"""
        recommendations = {
            AuthenticityScore.GENUINE: "Safe to interact - genuine human account",
            AuthenticityScore.LIKELY_GENUINE: "Proceed with normal interaction",
            AuthenticityScore.SUSPICIOUS: "Use caution - limited interaction recommended", 
            AuthenticityScore.LIKELY_BOT: "Avoid interaction - high bot probability",
            AuthenticityScore.DEFINITE_BOT: "Do not interact - definite bot account"
        }
        return recommendations.get(level, "Review manually")

    async def batch_analyze_profiles(self, profiles: List[Dict]) -> List[ProfileAnalysis]:
        """Analyze multiple profiles in batch"""
        tasks = []
        for profile in profiles:
            task = self.analyze_profile(profile)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions and return successful analyses
        valid_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Profile analysis failed for profile {i}: {result}")
            else:
                valid_results.append(result)

        return valid_results

    async def should_interact_with_account(self, profile_data: Dict, phase: str) -> Tuple[bool, str]:
        """Determine if account is safe to interact with based on current phase"""

        analysis = await self.analyze_profile(profile_data)

        # Phase-specific interaction thresholds
        phase_thresholds = {
            "phase_1": 0.7,  # Ultra-conservative - only interact with very likely humans
            "phase_2": 0.5,  # Moderate - interact with likely humans
            "phase_3": 0.3   # Operational - interact unless definitely bot
        }

        threshold = phase_thresholds.get(phase, 0.5)
        should_interact = analysis.authenticity_score >= threshold

        reason = f"Authenticity score {analysis.authenticity_score:.2f} {'≥' if should_interact else '<'} threshold {threshold} for {phase}"

        return should_interact, reason

class TargetingSystem:
    """Advanced targeting system using authenticity analysis"""

    def __init__(self, authenticity_analyzer, ai_service):
        self.authenticity_analyzer = authenticity_analyzer
        self.ai_service = ai_service

    async def find_authentic_targets(
        self, 
        search_terms: List[str], 
        platform: str, 
        phase: str,
        max_results: int = 100
    ) -> List[Dict]:
        """Find authentic accounts matching search criteria"""

        # This would integrate with platform APIs to search for accounts
        # For now, showing the structure
        raw_profiles = []  # Would be populated by platform search

        # Analyze all found profiles for authenticity
        analyses = await self.authenticity_analyzer.batch_analyze_profiles(raw_profiles)

        # Filter based on phase requirements
        phase_thresholds = {
            "phase_1": AuthenticityScore.LIKELY_GENUINE,
            "phase_2": AuthenticityScore.SUSPICIOUS, 
            "phase_3": AuthenticityScore.LIKELY_BOT
        }

        min_level = phase_thresholds.get(phase, AuthenticityScore.SUSPICIOUS)

        authentic_targets = []
        for analysis in analyses:
            if self._level_meets_threshold(analysis.authenticity_level, min_level):
                profile_data = next(p for p in raw_profiles if p['username'] == analysis.username)
                profile_data['authenticity_analysis'] = analysis
                authentic_targets.append(profile_data)

        return authentic_targets[:max_results]

    def _level_meets_threshold(self, level: AuthenticityScore, threshold: AuthenticityScore) -> bool:
        """Check if authenticity level meets minimum threshold"""
        level_values = {
            AuthenticityScore.DEFINITE_BOT: 0,
            AuthenticityScore.LIKELY_BOT: 1,
            AuthenticityScore.SUSPICIOUS: 2,
            AuthenticityScore.LIKELY_GENUINE: 3,
            AuthenticityScore.GENUINE: 4
        }

        return level_values[level] >= level_values[threshold]
