"""
SocialSeed v2.0 - Main Application
Sophisticated phased social media orchestration system with enterprise-grade safety
"""
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn

# Import our sophisticated modules
from phase_manager import PhaseManager, TrafficLightSystem, HumanApprovalWorkflow
from authenticity_analyzer import AccountAuthenticityAnalyzer, TargetingSystem
from behavioral_service import HumanBehaviorSimulator, PlatformHealthMonitor, GracefulDegradationHandler
from ai_service import AIServiceProvider
from database import DatabaseManager
from tiktok_service import TikTokService
from instagram_service import InstagramService
from twitter_service import TwitterService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()

class SocialSeedOrchestrator:
    """Main orchestration system for SocialSeed v2.0"""

    def __init__(self):
        # Core services
        self.db = DatabaseManager()
        self.ai_service = AIServiceProvider()

        # Phase and safety systems
        self.phase_manager = PhaseManager(self.db, self.ai_service)
        self.traffic_light = TrafficLightSystem(self.ai_service, self.phase_manager)
        self.approval_workflow = HumanApprovalWorkflow(self.db)

        # Analysis and behavior systems
        self.authenticity_analyzer = AccountAuthenticityAnalyzer(self.ai_service)
        self.targeting_system = TargetingSystem(self.authenticity_analyzer, self.ai_service)
        self.behavior_simulator = HumanBehaviorSimulator()
        self.health_monitor = PlatformHealthMonitor()
        self.degradation_handler = GracefulDegradationHandler()

        # Platform services
        self.platform_services = {
            'tiktok': TikTokService(
                behavior_simulator=self.behavior_simulator,
                health_monitor=self.health_monitor,
                authenticity_analyzer=self.authenticity_analyzer
            ),
            'instagram': InstagramService(
                behavior_simulator=self.behavior_simulator,
                health_monitor=self.health_monitor,
                authenticity_analyzer=self.authenticity_analyzer
            ),
            'twitter': TwitterService(
                behavior_simulator=self.behavior_simulator,
                health_monitor=self.health_monitor,
                authenticity_analyzer=self.authenticity_analyzer
            )
        }

        # Background task queue
        self.task_queue = asyncio.Queue()
        self.running_tasks = {}

    async def initialize(self):
        """Initialize all systems"""
        logger.info("Initializing SocialSeed v2.0...")

        # Initialize database
        await self.db.initialize()

        # Initialize AI service
        await self.ai_service.initialize()

        # Initialize platform services
        for platform, service in self.platform_services.items():
            try:
                await service.initialize()
                logger.info(f"✅ {platform.title()} service initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize {platform}: {e}")

        # Start background task processor
        asyncio.create_task(self._process_background_tasks())

        logger.info("🚀 SocialSeed v2.0 fully initialized")

    async def execute_action(
        self, 
        account_id: str, 
        action_type: str, 
        target_data: Dict,
        force_execute: bool = False
    ) -> Dict:
        """Execute social media action with full safety pipeline"""

        try:
            # Get account and phase information  
            account = await self.db.get_account(account_id)
            current_phase = await self.phase_manager.get_current_phase(account_id)

            # Step 1: Risk Assessment via Traffic Light System
            risk_assessment = await self.traffic_light.assess_action_risk(
                account_id=account_id,
                action_type=action_type,
                target_data=target_data
            )

            logger.info(f"Risk assessment for {action_type}: {risk_assessment.risk_level.value}")

            # Step 2: Handle based on risk level
            if risk_assessment.requires_human_approval and not force_execute:
                # Request human approval
                approval_id = await self.approval_workflow.request_approval(
                    account_id=account_id,
                    action_type=action_type,
                    risk_assessment=risk_assessment,
                    action_data=target_data
                )

                return {
                    'status': 'approval_required',
                    'approval_id': approval_id,
                    'risk_level': risk_assessment.risk_level.value,
                    'reasoning': risk_assessment.reasoning
                }

            # Step 3: Calculate human-like delay
            delay_seconds, delay_reason = self.behavior_simulator.calculate_optimal_delay(
                account_id=account_id,
                action_type=action_type,
                phase=current_phase.value
            )

            # Step 4: Check if should take break
            session_actions = await self.db.get_session_action_count(account_id)
            should_break, break_duration = self.behavior_simulator.should_take_break(
                account_id, session_actions
            )

            if should_break:
                logger.info(f"Account {account_id} taking {break_duration}s break")
                return {
                    'status': 'break_required',
                    'break_duration': break_duration,
                    'reason': 'Human-like behavior pattern'
                }

            # Step 5: Execute the action
            platform = account['platform']
            platform_service = self.platform_services.get(platform)

            if not platform_service:
              
                raise HTTPException(status_code=400, detail=f"Platform {platform} not supported")

            # Wait for calculated delay
            if delay_seconds > 0:
                await asyncio.sleep(delay_seconds)

            # Execute with platform service
            result = await platform_service.execute_action(
                account_id=account_id,
                action_type=action_type,
                target_data=target_data,
                risk_assessment=risk_assessment
            )

            # Step 6: Log the action and update health
            await self._log_action_result(
                account_id=account_id,
                action_type=action_type,
                target_data=target_data,
                result=result,
                risk_assessment=risk_assessment,
                delay_seconds=delay_seconds,
                delay_reason=delay_reason
            )

            # Step 7: Check for phase progression
            await self.phase_manager.progress_account_phase(account_id)

            return result

        except Exception as e:
            logger.error(f"Action execution failed: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }

    async def get_dashboard_data(self, user_id: str) -> Dict:
        """Get comprehensive dashboard data"""

        # Get user accounts
        accounts = await self.db.get_user_accounts(user_id)

        dashboard_data = {
            'accounts': [],
            'pending_approvals': [],
            'platform_health': {},
            'recent_activity': [],
            'phase_overview': {}
        }

        for account in accounts:
            account_id = account['id']

            # Get account health
            health = await self.phase_manager.get_account_health(account_id)

            # Get recent actions
            recent_actions = await self.db.get_recent_actions(account_id, limit=10)

            dashboard_data['accounts'].append({
                'id': account_id,
                'platform': account['platform'],
                'username': account['username'],
                'phase': health.phase.value,
                'status': health.status,
                'risk_score': health.risk_score,
                'followers': health.followers_count,
                'following': health.following_count,
                'engagement_rate': health.engagement_rate,
                'recent_actions': recent_actions
            })

        # Get pending approvals
        dashboard_data['pending_approvals'] = await self.approval_workflow.get_pending_approvals()

        # Get platform health
        for platform in ['tiktok', 'instagram', 'twitter']:
            platform_health = self.health_monitor.platform_health.get(platform, {})
            dashboard_data['platform_health'][platform] = platform_health

        return dashboard_data

    async def _log_action_result(
        self, 
        account_id: str, 
        action_type: str, 
        target_data: Dict,
        result: Dict,
        risk_assessment,
        delay_seconds: int,
        delay_reason: str
    ):
        """Log action execution results"""

        await self.db.log_action_history({
            'account_id': account_id,
            'action_type': action_type,
            'target_data': target_data,
            'status': result.get('status'),
            'response_code': result.get('response_code'),
            'response_time_ms': result.get('response_time_ms'),
            'error_message': result.get('error'),
            'risk_assessment_id': risk_assessment.id if hasattr(risk_assessment, 'id') else None,
            'delay_before_action': delay_seconds,
            'delay_reasoning': delay_reason,
            'executed_at': datetime.now()
        })

    async def _process_background_tasks(self):
        """Process background tasks continuously"""
        while True:
            try:
                task = await self.task_queue.get()
                await self._execute_background_task(task)
            except Exception as e:
                logger.error(f"Background task failed: {e}")
            await asyncio.sleep(1)

    async def _execute_background_task(self, task: Dict):
        """Execute individual background task"""
        task_type = task.get('type')

        if task_type == 'health_check':
            await self._health_check_task(task)
        elif task_type == 'phase_progression':
            await self._phase_progression_task(task)
        elif task_type == 'cleanup':
            await self._cleanup_task(task)

# Initialize the orchestrator
orchestrator = SocialSeedOrchestrator()

# FastAPI application
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await orchestrator.initialize()
    yield
    # Shutdown
    logger.info("Shutting down SocialSeed v2.0")

app = FastAPI(
    title="SocialSeed v2.0",
    description="Enterprise-grade social media orchestration with phased safety approach",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
@app.get("/")
async def root():
    return {
        "message": "SocialSeed v2.0 - Enterprise Social Media Orchestration",
        "version": "2.0.0",
        "features": [
            "Phased deployment (30/60+ day progression)",
            "TikTok-first platform strategy", 
            "LLM-powered risk assessment",
            "Human-in-the-loop approvals",
            "Advanced behavioral mimicking",
            "Real-time health monitoring",
            "Graceful degradation"
        ]
    }

@app.get("/dashboard/{user_id}")
async def get_dashboard(user_id: str):
    """Get comprehensive dashboard data"""
    return await orchestrator.get_dashboard_data(user_id)

@app.post("/accounts/{account_id}/actions")
async def execute_action(
    account_id: str,
    action_data: Dict,
    background_tasks: BackgroundTasks
):
    """Execute social media action with safety pipeline"""

    result = await orchestrator.execute_action(
        account_id=account_id,
        action_type=action_data['action_type'],
        target_data=action_data['target_data'],
        force_execute=action_data.get('force_execute', False)
    )

    return result

@app.get("/approvals/pending")
async def get_pending_approvals():
    """Get all pending approval requests"""
    return await orchestrator.approval_workflow.get_pending_approvals()

@app.post("/approvals/{approval_id}/approve")
async def approve_action(approval_id: str, approval_data: Dict):
    """Approve pending action"""
    success = await orchestrator.approval_workflow.approve_action(
        approval_id=approval_id,
        approver_id=approval_data['approver_id'],
        notes=approval_data.get('notes', '')
    )

    if not success:
        raise HTTPException(status_code=404, detail="Approval request not found")

    return {"status": "approved"}

@app.post("/approvals/{approval_id}/reject")
async def reject_action(approval_id: str, rejection_data: Dict):
    """Reject pending action"""
    success = await orchestrator.approval_workflow.reject_action(
        approval_id=approval_id,
        approver_id=rejection_data['approver_id'],
        reason=rejection_data['reason']
    )

    if not success:
        raise HTTPException(status_code=404, detail="Approval request not found")

    return {"status": "rejected"}

@app.get("/accounts/{account_id}/health")
async def get_account_health(account_id: str):
    """Get detailed account health assessment"""
    health = await orchestrator.phase_manager.get_account_health(account_id)
    return {
        'account_id': account_id,
        'phase': health.phase.value,
        'status': health.status,
        'risk_score': health.risk_score,
        'followers_count': health.followers_count,
        'following_count': health.following_count,
        'engagement_rate': health.engagement_rate,
        'consecutive_errors': health.consecutive_errors,
        'last_action': health.last_action_timestamp
    }

@app.get("/platform-health")
async def get_platform_health():
    """Get platform health status"""
    return {
        platform: health for platform, health in 
        orchestrator.health_monitor.platform_health.items()
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
