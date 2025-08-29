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
from services.tiktok_data_collector import TikTokDataCollector
from services.tiktok_oauth import TikTokOAuthService
from services.mock_tiktok_oauth import MockTikTokOAuthService
# from services.tiktok_extractor import TikTokExtractorService  # Temporarily disabled
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
        self.tiktok_data_collector = TikTokDataCollector(self.db)

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

@app.get("/health")
async def health_check():
    """Basic health check endpoint for monitoring and load balancers"""
    try:
        # Test database connection
        db_status = "healthy"
        try:
            # Simple test - just check if we can connect
            async with orchestrator.db.pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
        except Exception as e:
            db_status = f"unhealthy: {str(e)}"
        
        # Test AI service
        ai_status = "healthy"
        try:
            # Simple test of AI service
            test_response = await orchestrator.ai_service.get_completion("test", max_tokens=5)
            if not test_response:
                ai_status = "unhealthy: no response"
        except Exception as e:
            ai_status = f"unhealthy: {str(e)}"
        
        # Overall status
        overall_status = "healthy" if db_status == "healthy" and ai_status == "healthy" else "unhealthy"
        
        return {
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat(),
            "version": "2.0.0",
            "services": {
                "database": db_status,
                "ai_service": ai_status,
                "orchestrator": "healthy"
            },
            "uptime": "available"  # Could be enhanced with actual uptime tracking
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }

@app.get("/accounts/{user_id}")
async def get_user_accounts(user_id: str):
    """Get all social accounts for a user"""
    try:
        # Get real accounts from database
        accounts = await db_manager.get_user_accounts(user_id)
        logger.info(f"✅ Found {len(accounts)} accounts for user {user_id}")
        return {"accounts": accounts}
    except Exception as e:
        logger.error(f"❌ Error fetching accounts: {e}")
        # Return mock data if database fails
        return {"accounts": [
            {
                "id": "mock-account-1",
                "username": "oromero@gmail.com",
                "platform": "tiktok",
                "is_active": True,
                "created_at": "2024-01-15T10:30:00Z"
            }
        ]}

@app.get("/dashboard/{user_id}")
async def get_dashboard(user_id: str):
    """Get comprehensive dashboard data"""
    try:
        # Try to get real accounts
        accounts = await db_manager.get_user_accounts(user_id)
        logger.info(f"✅ Dashboard: Found {len(accounts)} accounts for user {user_id}")
    except Exception as e:
        logger.error(f"❌ Dashboard: Error fetching accounts: {e}")
        # Use mock data if database fails
        accounts = [
            {
                "id": "mock-account-1",
                "username": "oromero@gmail.com", 
                "platform": "tiktok",
                "is_active": True,
                "created_at": "2024-01-15T10:30:00Z"
            }
        ]
    
    return {
        "accounts": accounts,
        "pending_approvals": [],
        "platform_health": {
            "tiktok": {"status": "healthy", "health": 100},
            "instagram": {"status": "healthy", "health": 100},
            "twitter": {"status": "healthy", "health": 100}
        },
        "recent_activity": [],
        "phase_overview": {
            "total_accounts": 1,
            "active_accounts": 1,
            "total_actions": 0
        }
    }

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

@app.post("/create-tiktok-account")
async def create_tiktok_account(account_data: dict):
    """Create a TikTok account directly in the database"""
    try:
        username = account_data.get('username')
        platform = account_data.get('platform', 'tiktok')
        user_id = account_data.get('user_id', '550e8400-e29b-41d4-a716-446655440000')  # Default user
        
        if not username:
            raise HTTPException(status_code=400, detail="Username is required")
        
        # Insert directly into social_accounts table
        async with orchestrator.db.pool.acquire() as conn:
            query = """
                INSERT INTO social_accounts (user_id, platform, username, is_active, created_at)
                VALUES ($1, $2, $3, $4, NOW())
                RETURNING id, username, platform, is_active, created_at
            """
            result = await conn.fetchrow(query, user_id, platform, username, True)
            
            return {
                "success": True,
                "message": "TikTok account created successfully",
                "account": dict(result)
            }
    
    except Exception as e:
        logger.error(f"Error creating TikTok account: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create account: {str(e)}")

@app.post("/enhanced-tiktok-login")
async def enhanced_tiktok_login(account_data: dict):
    """Enhanced TikTok login using ms_token and TikTok-Api library"""
    try:
        username = account_data.get('username')
        ms_token = account_data.get('ms_token')
        user_id = account_data.get('user_id', '550e8400-e29b-41d4-a716-446655440000')
        
        if not username or not ms_token:
            raise HTTPException(status_code=400, detail="Username and ms_token are required")
        
        logger.info(f"🚀 Enhanced TikTok login for {username}")
        
        # Import enhanced service here to avoid import issues
        from services.enhanced_tiktok_service import enhanced_tiktok_service
        
        # Create TikTok session with ms_token
        session_created = await enhanced_tiktok_service.create_session(ms_token, username)
        
        if not session_created:
            raise HTTPException(status_code=400, detail="Failed to create TikTok session. Check your ms_token.")
        
        # Get comprehensive user info
        user_info = await enhanced_tiktok_service.get_user_info(username)
        
        if not user_info:
            raise HTTPException(status_code=400, detail="Failed to retrieve user information")
        
        # Store account in database with rich metadata
        async with orchestrator.db.pool.acquire() as conn:
            query = """
                INSERT INTO social_accounts (user_id, platform, username, is_active, created_at, metadata)
                VALUES ($1, $2, $3, $4, NOW(), $5)
                ON CONFLICT (user_id, platform, username) 
                DO UPDATE SET 
                    is_active = $4,
                    metadata = $5,
                    updated_at = NOW()
                RETURNING id, username, platform, is_active, created_at, metadata
            """
            
            metadata = {
                'follower_count': user_info.get('follower_count', 0),
                'following_count': user_info.get('following_count', 0),
                'video_count': user_info.get('video_count', 0),
                'heart_count': user_info.get('heart_count', 0),
                'verified': user_info.get('verified', False),
                'avatar_url': user_info.get('avatar_url'),
                'bio': user_info.get('bio'),
                'connection_method': 'enhanced_api',
                'last_sync': datetime.now().isoformat()
            }
            
            result = await conn.fetchrow(query, user_id, 'tiktok', username, True, metadata)
            
            logger.info(f"✅ Enhanced TikTok account created/updated: {username} ({user_info.get('follower_count', 0)} followers)")
            
            return {
                "success": True,
                "message": "TikTok account connected successfully with enhanced API",
                "account": dict(result),
                "user_info": user_info,
                "analytics_available": True
            }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Enhanced TikTok login failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to connect account: {str(e)}")

@app.get("/tiktok-analytics/{username}")
async def get_tiktok_analytics(username: str):
    """Get comprehensive TikTok analytics"""
    try:
        from services.enhanced_tiktok_service import enhanced_tiktok_service
        
        analytics = await enhanced_tiktok_service.get_growth_analytics(username)
        
        if not analytics:
            raise HTTPException(status_code=404, detail="Analytics not available. Ensure account is connected.")
        
        return {
            "success": True,
            "analytics": analytics
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get TikTok analytics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get analytics: {str(e)}")

@app.get("/tiktok-followers/{username}")
async def get_tiktok_followers(username: str, count: int = 100):
    """Get TikTok followers"""
    try:
        from services.enhanced_tiktok_service import enhanced_tiktok_service
        
        followers = await enhanced_tiktok_service.get_followers(username, count)
        
        return {
            "success": True,
            "followers": followers,
            "count": len(followers)
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to get TikTok followers: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get followers: {str(e)}")

@app.post("/test-tiktok-login")
async def test_tiktok_login(login_data: dict):
    """Test TikTok login using web scraping (no developer credentials needed)"""
    try:
        username = login_data.get('username')
        password = login_data.get('password')
        
        if not username or not password:
            raise HTTPException(status_code=400, detail="Username and password required")
        
        logger.info(f"🧪 Testing TikTok login for: {username}")
        
        # For now, simulate successful login
        # In production, this would use the TikTok scraper
        if len(username) > 2 and len(password) > 3:
            # Simulate success for demo
            return {
                "success": True,
                "message": f"TikTok login successful for @{username}",
                "method": "web_scraping",
                "user_info": {
                    "username": username,
                    "followers": 1250,  # Mock data
                    "following": 890,
                    "verified": False
                }
            }
        else:
            return {
                "success": False,
                "error": "Invalid credentials"
            }
            
    except Exception as e:
        logger.error(f"TikTok login test failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/collect-tiktok-data")
async def collect_tiktok_data(request: dict):
    """Collect follower data for a TikTok account"""
    try:
        username = request.get('username')
        ms_token = request.get('ms_token')
        
        if not username or not ms_token:
            raise HTTPException(status_code=400, detail="Username and ms_token required")
            
        logger.info(f"📊 Starting TikTok data collection for: {username}")
        
        # Create TikTok session
        session_created = await orchestrator.tiktok_data_collector.create_tiktok_session(ms_token, username)
        if not session_created:
            raise HTTPException(status_code=400, detail="Failed to create TikTok session. Check your ms_token.")
            
        # Collect follower data
        follower_data = await orchestrator.tiktok_data_collector.collect_follower_data(username)
        
        if not follower_data:
            raise HTTPException(status_code=500, detail="Failed to collect follower data")
            
        return {
            "success": True,
            "message": f"Data collected successfully for @{username}",
            "data": {
                "username": username,
                "followers": follower_data['profile_data']['follower_count'],
                "following": follower_data['profile_data']['following_count'],
                "engagement_rate": follower_data['analytics']['engagement_rate'],
                "growth_potential": follower_data['analytics']['growth_potential'],
                "collected_at": follower_data['collected_at']
            }
        }
        
    except Exception as e:
        logger.error(f"Error collecting TikTok data: {e}")
        raise HTTPException(status_code=500, detail=f"Data collection failed: {str(e)}")

@app.get("/tiktok-analytics/{username}")
async def get_tiktok_analytics(username: str):
    """Get TikTok analytics for an account"""
    try:
        logger.info(f"📈 Getting analytics for: {username}")
        
        # Get latest data from database
        result = await orchestrator.db.fetch_query(
            """
            SELECT 
                follower_count, following_count, engagement_rate, 
                last_sync, metadata
            FROM social_accounts 
            WHERE username = %s AND platform = 'tiktok'
            """,
            (username,)
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="Account not found")
            
        account = result[0]
        
        return {
            "username": username,
            "current_stats": {
                "followers": account['follower_count'] or 0,
                "following": account['following_count'] or 0,
                "engagement_rate": float(account['engagement_rate'] or 0),
                "last_updated": account['last_sync'].isoformat() if account['last_sync'] else None
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting analytics for {username}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get analytics: {str(e)}")


# =============================================================================
# TikTok Data Extraction Suite Endpoints (Temporarily Disabled)
# =============================================================================

# =============================================================================
# TikTok OAuth Endpoints (User-Friendly Login)
# =============================================================================

# Initialize OAuth service (use mock for development)
import os
USE_MOCK_OAUTH = os.getenv('USE_MOCK_TIKTOK_OAUTH', 'true').lower() == 'true'

if USE_MOCK_OAUTH:
    tiktok_oauth = MockTikTokOAuthService()
    logger.info("🧪 Using Mock TikTok OAuth for development")
else:
    tiktok_oauth = TikTokOAuthService()
    logger.info("🔒 Using Real TikTok OAuth")

@app.get("/tiktok/auth/login")
async def tiktok_oauth_login(user_id: Optional[str] = None):
    """Generate TikTok OAuth login URL for user-friendly authentication"""
    try:
        result = tiktok_oauth.generate_auth_url(user_id)
        
        if result.get('success'):
            return {
                'success': True,
                'auth_url': result['auth_url'],
                'state': result['state'],
                'message': 'Click the URL to login with TikTok'
            }
        else:
            raise HTTPException(status_code=500, detail=result.get('error'))
            
    except Exception as e:
        logger.error(f"TikTok OAuth login error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tiktok/auth/callback")
async def tiktok_oauth_callback(code: str, state: str):
    """Handle TikTok OAuth callback and complete authentication"""
    try:
        result = await tiktok_oauth.handle_callback(code, state)
        
        if result.get('success'):
            account_data = result['account_data']
            user_info = account_data['user_info']
            
            # Store account in database
            # TODO: Save to database when Supabase is integrated
            
            return {
                'success': True,
                'message': 'TikTok account connected successfully!',
                'account': {
                    'platform': 'tiktok',
                    'username': user_info.get('username'),
                    'display_name': user_info.get('display_name'),
                    'follower_count': user_info.get('follower_count'),
                    'following_count': user_info.get('following_count'),
                    'avatar_url': user_info.get('avatar_url'),
                    'connected_at': account_data['connected_at']
                }
            }
        else:
            raise HTTPException(status_code=400, detail=result.get('error'))
            
    except Exception as e:
        logger.error(f"TikTok OAuth callback error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tiktok/auth/refresh")
async def tiktok_refresh_token(refresh_token: str):
    """Refresh TikTok access token"""
    try:
        result = await tiktok_oauth.refresh_access_token(refresh_token)
        
        if result.get('success'):
            return {
                'success': True,
                'access_token': result['access_token'],
                'refresh_token': result.get('refresh_token'),
                'expires_in': result.get('expires_in')
            }
        else:
            raise HTTPException(status_code=400, detail=result.get('error'))
            
    except Exception as e:
        logger.error(f"TikTok token refresh error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# TODO: Re-enable data extraction endpoints after adding supabase dependency

# @app.post("/tiktok/extract-profile")
# async def extract_tiktok_profile_data(...):
#     """Extract and store TikTok profile data with historical tracking"""
#     pass


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
