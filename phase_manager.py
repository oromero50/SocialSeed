"""
SocialSeed v2.0 - Phase Management System
Sophisticated phased approach with traffic light system and human-in-the-loop safety
"""
import asyncio
import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import json
import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class Phase(Enum):
    PHASE_1 = "phase_1"  # Days 1-30: TikTok only, ultra-conservative
    PHASE_2 = "phase_2"  # Days 31-60: TikTok + Instagram, controlled scaling
    PHASE_3 = "phase_3"  # Days 61+: Full maintenance, hybrid approach

class RiskLevel(Enum):
    GREEN = "green"    # Safe to proceed automatically
    YELLOW = "yellow"  # Caution required, human review recommended
    RED = "red"        # High risk, human approval required

class ActionType(Enum):
    FOLLOW = "follow"
    UNFOLLOW = "unfollow"
    LIKE = "like"
    COMMENT = "comment"
    SHARE = "share"
    VIEW = "view"

@dataclass
class AggressionSettings:
    """Aggression settings for different phases"""
    follows_per_hour: int
    likes_per_hour: int
    comments_per_hour: int
    min_delay_seconds: int
    max_delay_seconds: int
    batch_size: int
    platform_weights: Dict[str, float]  # Platform resource allocation

class PhaseConfig:
    """Configuration for each phase"""

    PHASE_1_CONFIG = AggressionSettings(
        follows_per_hour=5,       # Ultra-conservative
        likes_per_hour=10,
        comments_per_hour=0,      # No comments in Phase 1
        min_delay_seconds=120,    # 2-8 minutes between actions
        max_delay_seconds=480,
        batch_size=3,             # Small batches
        platform_weights={"tiktok": 1.0, "instagram": 0.0, "twitter": 0.0}
    )

    PHASE_2_CONFIG = AggressionSettings(
        follows_per_hour=15,      # Controlled scaling
        likes_per_hour=25,
        comments_per_hour=5,      # Limited comments
        min_delay_seconds=60,     # 1-5 minutes
        max_delay_seconds=300,
        batch_size=5,
        platform_weights={"tiktok": 0.6, "instagram": 0.4, "twitter": 0.0}
    )

    PHASE_3_CONFIG = AggressionSettings(
        follows_per_hour=25,      # Full operational capacity
        likes_per_hour=40,
        comments_per_hour=10,
        min_delay_seconds=30,     # 30 seconds - 3 minutes
        max_delay_seconds=180,
        batch_size=8,
        platform_weights={"tiktok": 0.5, "instagram": 0.35, "twitter": 0.15}
    )

@dataclass
class AccountHealth:
    """Account health metrics and status"""
    account_id: str
    platform: str
    followers_count: int
    following_count: int
    posts_count: int
    engagement_rate: float
    follow_ratio: float
    last_action_timestamp: datetime.datetime
    consecutive_errors: int
    risk_score: float
    phase: Phase
    status: str  # active, paused, banned, warning

@dataclass
class RiskAssessment:
    """Risk assessment result from LLM analysis"""
    risk_level: RiskLevel
    confidence: float
    reasoning: str
    recommended_action: str
    requires_human_approval: bool
    flags: List[str]

class PhaseManager:
    """Manages phased deployment and progression"""

    def __init__(self, database, ai_service):
        self.db = database
        self.ai_service = ai_service
        self.current_configs = {}

    async def initialize_account_phase(self, account_id: str) -> Phase:
        """Initialize account in Phase 1"""
        account_data = await self.db.get_account(account_id)
        created_date = account_data.get('created_at')

        if not created_date:
            # New account starts in Phase 1
            await self.db.update_account_phase(account_id, Phase.PHASE_1.value)
            return Phase.PHASE_1

        days_active = (datetime.datetime.now() - created_date).days

        if days_active < 30:
            phase = Phase.PHASE_1
        elif days_active < 60:
            phase = Phase.PHASE_2
        else:
            phase = Phase.PHASE_3

        await self.db.update_account_phase(account_id, phase.value)
        return phase

    async def get_current_phase(self, account_id: str) -> Phase:
        """Get current phase for account"""
        account_data = await self.db.get_account(account_id)
        phase_str = account_data.get('current_phase', 'phase_1')
        return Phase(phase_str)

    async def should_progress_phase(self, account_id: str) -> Tuple[bool, Phase]:
        """Check if account should progress to next phase"""
        current_phase = await self.get_current_phase(account_id)
        account_data = await self.db.get_account(account_id)

        created_date = account_data.get('created_at')
        if not created_date:
            return False, current_phase

        days_active = (datetime.datetime.now() - created_date).days
        health = await self.get_account_health(account_id)

        # Phase progression logic
        if current_phase == Phase.PHASE_1 and days_active >= 30:
            # Check if ready for Phase 2
            if (health.risk_score < 0.3 and 
                health.consecutive_errors < 3 and
                health.engagement_rate > 0.01):
                return True, Phase.PHASE_2

        elif current_phase == Phase.PHASE_2 and days_active >= 60:
            # Check if ready for Phase 3
            if (health.risk_score < 0.4 and 
                health.consecutive_errors < 5 and
                health.engagement_rate > 0.02):
                return True, Phase.PHASE_3

        return False, current_phase

    async def progress_account_phase(self, account_id: str) -> bool:
        """Progress account to next phase if eligible"""
        should_progress, next_phase = await self.should_progress_phase(account_id)

        if should_progress:
            await self.db.update_account_phase(account_id, next_phase.value)
            logger.info(f"Account {account_id} progressed to {next_phase.value}")

            # Log phase progression
            await self.db.log_phase_progression(
                account_id=account_id,
                from_phase=await self.get_current_phase(account_id),
                to_phase=next_phase,
                timestamp=datetime.datetime.now(),
                reason="Automatic progression based on health metrics"
            )
            return True

        return False

    def get_aggression_settings(self, phase: Phase) -> AggressionSettings:
        """Get aggression settings for current phase"""
        config_map = {
            Phase.PHASE_1: PhaseConfig.PHASE_1_CONFIG,
            Phase.PHASE_2: PhaseConfig.PHASE_2_CONFIG,
            Phase.PHASE_3: PhaseConfig.PHASE_3_CONFIG
        }
        return config_map[phase]

    async def get_account_health(self, account_id: str) -> AccountHealth:
        """Get comprehensive account health assessment"""
        account_data = await self.db.get_account_with_metrics(account_id)
        phase = await self.get_current_phase(account_id)

        # Calculate health metrics
        followers = account_data.get('followers_count', 0)
        following = account_data.get('following_count', 0)
        posts = account_data.get('posts_count', 0)

        follow_ratio = following / max(followers, 1)
        engagement_rate = account_data.get('engagement_rate', 0.0)

        # Calculate risk score based on multiple factors
        risk_score = await self._calculate_risk_score(account_data)

        return AccountHealth(
            account_id=account_id,
            platform=account_data.get('platform'),
            followers_count=followers,
            following_count=following,
            posts_count=posts,
            engagement_rate=engagement_rate,
            follow_ratio=follow_ratio,
            last_action_timestamp=account_data.get('last_action_at'),
            consecutive_errors=account_data.get('consecutive_errors', 0),
            risk_score=risk_score,
            phase=phase,
            status=account_data.get('status', 'active')
        )

    async def _calculate_risk_score(self, account_data: Dict) -> float:
        """Calculate comprehensive risk score (0.0 = low risk, 1.0 = high risk)"""
        risk_factors = []

        # Follow ratio risk (high following vs followers)
        followers = account_data.get('followers_count', 0)
        following = account_data.get('following_count', 0)
        follow_ratio = following / max(followers, 1)

        if follow_ratio > 5:
            risk_factors.append(0.4)  # High risk
        elif follow_ratio > 2:
            risk_factors.append(0.2)  # Medium risk
        else:
            risk_factors.append(0.0)  # Low risk

        # Engagement rate risk (low engagement suggests bot activity)
        engagement_rate = account_data.get('engagement_rate', 0.0)
        if engagement_rate < 0.01:
            risk_factors.append(0.3)
        elif engagement_rate < 0.02:
            risk_factors.append(0.1)
        else:
            risk_factors.append(0.0)

        # Error rate risk
        consecutive_errors = account_data.get('consecutive_errors', 0)
        if consecutive_errors > 5:
            risk_factors.append(0.3)
        elif consecutive_errors > 2:
            risk_factors.append(0.1)
        else:
            risk_factors.append(0.0)

        # Action frequency risk
        last_action = account_data.get('last_action_at')
        if last_action:
            hours_since_action = (datetime.datetime.now() - last_action).total_seconds() / 3600
            if hours_since_action < 0.5:  # Less than 30 minutes
                risk_factors.append(0.2)
            else:
                risk_factors.append(0.0)

        return min(sum(risk_factors), 1.0)

class TrafficLightSystem:
    """Advanced traffic light system with LLM-powered risk assessment"""

    def __init__(self, ai_service, phase_manager):
        self.ai_service = ai_service
        self.phase_manager = phase_manager

    async def assess_action_risk(
        self, 
        account_id: str, 
        action_type: ActionType, 
        target_data: Dict,
        context: Dict = None
    ) -> RiskAssessment:
        """Assess risk of performing action using LLM analysis"""

        # Get account health
        health = await self.phase_manager.get_account_health(account_id)
        phase = await self.phase_manager.get_current_phase(account_id)

        # Prepare context for LLM
        assessment_context = {
            "account_health": {
                "followers": health.followers_count,
                "following": health.following_count,
                "follow_ratio": health.follow_ratio,
                "engagement_rate": health.engagement_rate,
                "consecutive_errors": health.consecutive_errors,
                "risk_score": health.risk_score,
                "phase": phase.value
            },
            "action": {
                "type": action_type.value,
                "target_data": target_data
            },
            "context": context or {}
        }

        # Get LLM risk assessment
        risk_prompt = self._build_risk_assessment_prompt(assessment_context)
        llm_response = await self.ai_service.analyze_risk(risk_prompt)

        # Parse LLM response and determine risk level
        risk_level = self._parse_risk_level(llm_response, health, phase)

        return RiskAssessment(
            risk_level=risk_level,
            confidence=llm_response.get('confidence', 0.8),
            reasoning=llm_response.get('reasoning', ''),
            recommended_action=llm_response.get('recommendation', ''),
            requires_human_approval=risk_level in [RiskLevel.YELLOW, RiskLevel.RED],
            flags=llm_response.get('flags', [])
        )

    def _build_risk_assessment_prompt(self, context: Dict) -> str:
        """Build prompt for LLM risk assessment"""
        return f"""
        Analyze the risk of performing this social media automation action:

        Account Status:
        - Followers: {context['account_health']['followers']}
        - Following: {context['account_health']['following']}
        - Follow Ratio: {context['account_health']['follow_ratio']:.2f}
        - Engagement Rate: {context['account_health']['engagement_rate']:.3f}
        - Recent Errors: {context['account_health']['consecutive_errors']}
        - Current Risk Score: {context['account_health']['risk_score']:.2f}
        - Phase: {context['account_health']['phase']}

        Proposed Action:
        - Type: {context['action']['type']}
        - Target: {context['action']['target_data']}

        Consider:
        1. Platform detection patterns
        2. Account health indicators
        3. Timing and frequency
        4. Target account authenticity
        5. Phase-appropriate behavior

        Respond with:
        {{
            "risk_level": "green|yellow|red",
            "confidence": 0.85,
            "reasoning": "Detailed explanation",
            "recommendation": "Specific advice",
            "flags": ["flag1", "flag2"]
        }}
        """

    def _parse_risk_level(self, llm_response: Dict, health: AccountHealth, phase: Phase) -> RiskLevel:
        """Parse LLM response and apply phase-specific risk thresholds"""
        llm_risk = llm_response.get('risk_level', 'yellow').lower()

        # Phase 1: Ultra-conservative - any yellow becomes red
        if phase == Phase.PHASE_1:
            if llm_risk in ['yellow', 'red']:
                return RiskLevel.RED
            return RiskLevel.GREEN

        # Phase 2: Controlled - moderate risk tolerance
        elif phase == Phase.PHASE_2:
            if llm_risk == 'red' or health.risk_score > 0.6:
                return RiskLevel.RED
            elif llm_risk == 'yellow' or health.risk_score > 0.3:
                return RiskLevel.YELLOW
            return RiskLevel.GREEN

        # Phase 3: Operational - higher risk tolerance
        else:
            if llm_risk == 'red' or health.risk_score > 0.8:
                return RiskLevel.RED
            elif llm_risk == 'yellow' or health.risk_score > 0.5:
                return RiskLevel.YELLOW
            return RiskLevel.GREEN

class HumanApprovalWorkflow:
    """Human-in-the-loop approval system for risky actions"""

    def __init__(self, database):
        self.db = database
        self.pending_approvals = {}

    async def request_approval(
        self, 
        account_id: str, 
        action_type: ActionType, 
        risk_assessment: RiskAssessment,
        action_data: Dict
    ) -> str:
        """Request human approval for risky action"""
        approval_id = f"approval_{account_id}_{int(datetime.datetime.now().timestamp())}"

        approval_request = {
            "approval_id": approval_id,
            "account_id": account_id,
            "action_type": action_type.value,
            "risk_level": risk_assessment.risk_level.value,
            "reasoning": risk_assessment.reasoning,
            "recommendation": risk_assessment.recommended_action,
            "flags": risk_assessment.flags,
            "action_data": action_data,
            "requested_at": datetime.datetime.now(),
            "status": "pending"
        }

        # Store in database
        await self.db.create_approval_request(approval_request)

        # Add to in-memory queue for real-time processing
        self.pending_approvals[approval_id] = approval_request

        logger.info(f"Human approval requested: {approval_id}")
        return approval_id

    async def get_pending_approvals(self, account_id: str = None) -> List[Dict]:
        """Get pending approval requests"""
        if account_id:
            return await self.db.get_pending_approvals_for_account(account_id)
        return await self.db.get_all_pending_approvals()

    async def approve_action(self, approval_id: str, approver_id: str, notes: str = "") -> bool:
        """Approve pending action"""
        approval = await self.db.get_approval_request(approval_id)
        if not approval or approval['status'] != 'pending':
            return False

        await self.db.update_approval_status(
            approval_id, 
            'approved', 
            approver_id, 
            notes
        )

        if approval_id in self.pending_approvals:
            del self.pending_approvals[approval_id]

        logger.info(f"Action approved: {approval_id} by {approver_id}")
        return True

    async def reject_action(self, approval_id: str, approver_id: str, reason: str) -> bool:
        """Reject pending action"""
        approval = await self.db.get_approval_request(approval_id)
        if not approval or approval['status'] != 'pending':
            return False

        await self.db.update_approval_status(
            approval_id, 
            'rejected', 
            approver_id, 
            reason
        )

        if approval_id in self.pending_approvals:
            del self.pending_approvals[approval_id]

        logger.info(f"Action rejected: {approval_id} by {approver_id}")
        return True

    async def is_action_approved(self, approval_id: str) -> Optional[bool]:
        """Check if action has been approved"""
        approval = await self.db.get_approval_request(approval_id)
        if not approval:
            return None

        if approval['status'] == 'approved':
            return True
        elif approval['status'] == 'rejected':
            return False
        else:
            return None  # Still pending
