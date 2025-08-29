"""
SocialSeed v2.0 - Database Manager
PostgreSQL database management with async operations and connection pooling
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import asyncpg
from pydantic import BaseModel
import json

logger = logging.getLogger(__name__)

class DatabaseManager:
    """PostgreSQL database manager with async operations"""
    
    def __init__(self):
        self.pool = None
        self.connection_string = None
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize database connection pool"""
        logger.info("Initializing Database Manager...")
        
        # Get database URL from environment
        self.connection_string = self._get_env_var("DATABASE_URL")
        if not self.connection_string:
            raise ValueError("DATABASE_URL environment variable not set")
        
        try:
            # Create connection pool
            self.pool = await asyncpg.create_pool(
                self.connection_string,
                min_size=5,
                max_size=20,
                command_timeout=60
            )
            
            # Test connection
            async with self.pool.acquire() as conn:
                await conn.execute("SELECT 1")
            
            self.is_initialized = True
            logger.info("✅ Database connection pool initialized successfully")
            
            # Initialize database schema
            await self._initialize_schema()
            
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
            raise
    
    async def _initialize_schema(self):
        """Initialize database schema if it doesn't exist"""
        try:
            schema_file = "schema.sql"
            with open(schema_file, 'r') as f:
                schema_sql = f.read()
            
            async with self.pool.acquire() as conn:
                await conn.execute(schema_sql)
            
            logger.info("✅ Database schema initialized")
        except FileNotFoundError:
            logger.warning("Schema file not found, skipping schema initialization")
        except Exception as e:
            logger.error(f"Schema initialization failed: {e}")
    
    async def close(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed")
    
    # Account Management
    async def create_account(self, account_data: Dict[str, Any]) -> str:
        """Create a new social media account"""
        async with self.pool.acquire() as conn:
            query = """
                INSERT INTO social_accounts (
                    username, platform, email, password_hash, 
                    api_key, api_secret, status, created_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                RETURNING id
            """
            
            account_id = await conn.fetchval(
                query,
                account_data['username'],
                account_data['platform'],
                account_data.get('email'),
                account_data.get('password_hash'),
                account_data.get('api_key'),
                account_data.get('api_secret'),
                'active',
                datetime.utcnow()
            )
            
            logger.info(f"Created account {account_data['username']} with ID {account_id}")
            return str(account_id)
    
    async def get_account(self, account_id: str) -> Optional[Dict[str, Any]]:
        """Get account by ID"""
        async with self.pool.acquire() as conn:
            query = "SELECT * FROM social_accounts WHERE id = $1"
            row = await conn.fetchrow(query, account_id)
            
            if row:
                return dict(row)
            return None
    
    async def update_account_status(self, account_id: str, status: str, reason: str = None):
        """Update account status"""
        async with self.pool.acquire() as conn:
            query = """
                UPDATE social_accounts 
                SET status = $2, updated_at = $3, status_reason = $4
                WHERE id = $1
            """
            await conn.execute(query, account_id, status, datetime.utcnow(), reason)
            logger.info(f"Updated account {account_id} status to {status}")
    
    # Phase Management
    async def create_phase_record(self, account_id: str, phase: str, start_date: datetime) -> str:
        """Create a new phase record for an account"""
        async with self.pool.acquire() as conn:
            query = """
                INSERT INTO account_phases (
                    account_id, phase, start_date, status, created_at
                ) VALUES ($1, $2, $3, $4, $5)
                RETURNING id
            """
            
            phase_id = await conn.fetchval(
                query,
                account_id,
                phase,
                start_date,
                'active',
                datetime.utcnow()
            )
            
            return str(phase_id)
    
    async def get_current_phase(self, account_id: str) -> Optional[Dict[str, Any]]:
        """Get current phase for an account"""
        async with self.pool.acquire() as conn:
            query = """
                SELECT * FROM account_phases 
                WHERE account_id = $1 AND status = 'active'
                ORDER BY start_date DESC
                LIMIT 1
            """
            row = await conn.fetchrow(query, account_id)
            
            if row:
                return dict(row)
            return None
    
    async def update_phase_status(self, phase_id: str, status: str, end_date: datetime = None):
        """Update phase status"""
        async with self.pool.acquire() as conn:
            if end_date:
                query = """
                    UPDATE account_phases 
                    SET status = $2, end_date = $3, updated_at = $4
                    WHERE id = $1
                """
                await conn.execute(query, phase_id, status, end_date, datetime.utcnow())
            else:
                query = """
                    UPDATE account_phases 
                    SET status = $2, updated_at = $3
                    WHERE id = $1
                """
                await conn.execute(query, phase_id, status, datetime.utcnow())
    
    # Action Management
    async def log_action(self, action_data: Dict[str, Any]) -> str:
        """Log a social media action"""
        async with self.pool.acquire() as conn:
            query = """
                INSERT INTO actions (
                    account_id, platform, action_type, target_account,
                    status, risk_score, authenticity_score, metadata,
                    created_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                RETURNING id
            """
            
            action_id = await conn.fetchval(
                query,
                action_data['account_id'],
                action_data['platform'],
                action_data['action_type'],
                action_data.get('target_account'),
                action_data.get('status', 'pending'),
                action_data.get('risk_score', 0.0),
                action_data.get('authenticity_score', 0.0),
                json.dumps(action_data.get('metadata', {})),
                datetime.utcnow()
            )
            
            return str(action_id)
    
    async def get_pending_actions(self, account_id: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get pending actions for approval"""
        async with self.pool.acquire() as conn:
            if account_id:
                query = """
                    SELECT * FROM actions 
                    WHERE status = 'pending' AND account_id = $1
                    ORDER BY created_at ASC
                    LIMIT $2
                """
                rows = await conn.fetch(query, account_id, limit)
            else:
                query = """
                    SELECT * FROM actions 
                    WHERE status = 'pending'
                    ORDER BY created_at ASC
                    LIMIT $1
                """
                rows = await conn.fetch(query, limit)
            
            return [dict(row) for row in rows]
    
    async def update_action_status(self, action_id: str, status: str, approval_data: Dict[str, Any] = None):
        """Update action status and approval information"""
        async with self.pool.acquire() as conn:
            if approval_data:
                query = """
                    UPDATE actions 
                    SET status = $2, approved_by = $3, approved_at = $4,
                        approval_reason = $5, updated_at = $6
                    WHERE id = $1
                """
                await conn.execute(
                    query,
                    action_id,
                    status,
                    approval_data.get('approved_by'),
                    datetime.utcnow(),
                    approval_data.get('reason'),
                    datetime.utcnow()
                )
            else:
                query = """
                    UPDATE actions 
                    SET status = $2, updated_at = $3
                    WHERE id = $1
                """
                await conn.execute(query, action_id, status, datetime.utcnow())
    
    # Health Monitoring
    async def log_health_metric(self, health_data: Dict[str, Any]):
        """Log platform health metrics"""
        async with self.pool.acquire() as conn:
            query = """
                INSERT INTO health_metrics (
                    platform, metric_type, value, status, details, created_at
                ) VALUES ($1, $2, $3, $4, $5, $6)
            """
            
            await conn.execute(
                query,
                health_data['platform'],
                health_data['metric_type'],
                health_data['value'],
                health_data.get('status', 'normal'),
                json.dumps(health_data.get('details', {})),
                datetime.utcnow()
            )
    
    async def get_platform_health(self, platform: str, hours: int = 24) -> Dict[str, Any]:
        """Get platform health metrics for the last N hours"""
        async with self.pool.acquire() as conn:
            query = """
                SELECT 
                    metric_type,
                    AVG(value) as avg_value,
                    COUNT(*) as metric_count,
                    MAX(created_at) as last_updated
                FROM health_metrics 
                WHERE platform = $1 AND created_at >= $2
                GROUP BY metric_type
            """
            
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            rows = await conn.fetch(query, platform, cutoff_time)
            
            metrics = {}
            for row in rows:
                metrics[row['metric_type']] = {
                    'average': float(row['avg_value']),
                    'count': row['metric_count'],
                    'last_updated': row['last_updated']
                }
            
            return metrics
    
    # Analytics and Reporting
    async def get_account_analytics(self, account_id: str, days: int = 30) -> Dict[str, Any]:
        """Get account analytics for the last N days"""
        async with self.pool.acquire() as conn:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Action counts by type
            action_query = """
                SELECT 
                    action_type,
                    status,
                    COUNT(*) as count
                FROM actions 
                WHERE account_id = $1 AND created_at >= $2
                GROUP BY action_type, status
            """
            action_rows = await conn.fetch(action_query, account_id, cutoff_date)
            
            # Risk score trends
            risk_query = """
                SELECT 
                    DATE(created_at) as date,
                    AVG(risk_score) as avg_risk,
                    COUNT(*) as action_count
                FROM actions 
                WHERE account_id = $1 AND created_at >= $2
                GROUP BY DATE(created_at)
                ORDER BY date
            """
            risk_rows = await conn.fetch(risk_query, account_id, cutoff_date)
            
            # Authenticity trends
            auth_query = """
                SELECT 
                    DATE(created_at) as date,
                    AVG(authenticity_score) as avg_authenticity
                FROM actions 
                WHERE account_id = $1 AND created_at >= $2
                GROUP BY DATE(created_at)
                ORDER BY date
            """
            auth_rows = await conn.fetch(auth_query, account_id, cutoff_date)
            
            return {
                'actions': {f"{row['action_type']}_{row['status']}": row['count'] for row in action_rows},
                'risk_trends': [dict(row) for row in risk_rows],
                'authenticity_trends': [dict(row) for row in auth_rows],
                'period_days': days
            }
    
    async def get_system_overview(self) -> Dict[str, Any]:
        """Get system overview statistics"""
        async with self.pool.acquire() as conn:
            # Total accounts by platform
            accounts_query = """
                SELECT platform, status, COUNT(*) as count
                FROM social_accounts 
                GROUP BY platform, status
            """
            account_rows = await conn.fetch(accounts_query)
            
            # Total actions by status
            actions_query = """
                SELECT status, COUNT(*) as count
                FROM actions 
                WHERE created_at >= $1
                GROUP BY status
            """
            action_rows = await conn.fetch(actions_query, datetime.utcnow() - timedelta(days=7))
            
            # Phase distribution
            phases_query = """
                SELECT phase, COUNT(*) as count
                FROM account_phases 
                WHERE status = 'active'
                GROUP BY phase
            """
            phase_rows = await conn.fetch(phases_query)
            
            return {
                'accounts': {f"{row['platform']}_{row['status']}": row['count'] for row in account_rows},
                'actions_7d': {row['status']: row['count'] for row in action_rows},
                'phases': {row['phase']: row['count'] for row in phase_rows}
            }
    
    async def get_all_pending_approvals(self) -> List[Dict[str, Any]]:
        """Get all pending approval requests across all accounts."""
        try:
            async with self.pool.acquire() as conn:
                query = """
                    SELECT 
                        a.id,
                        a.account_id,
                        a.action_type,
                        a.platform,
                        a.target_account as target_data,
                        a.created_at,
                        a.status,
                        acc.username as account_username
                    FROM actions a
                    JOIN social_accounts acc ON a.account_id = acc.id
                    WHERE a.status = 'pending'
                    ORDER BY a.created_at DESC
                """
                rows = await conn.fetch(query)
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error fetching pending approvals: {e}")
            return []
    
    async def get_user_accounts(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all accounts for a specific user"""
        try:
            async with self.pool.acquire() as conn:
                query = """
                    SELECT 
                        id,
                        user_id,
                        platform,
                        username,
                        is_active,
                        created_at,
                        updated_at
                    FROM social_accounts 
                    WHERE user_id = $1
                    ORDER BY created_at DESC
                """
                rows = await conn.fetch(query, user_id)
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error fetching user accounts: {e}")
            return []
    
    async def get_account_with_metrics(self, account_id: str) -> Optional[Dict[str, Any]]:
        """Get account with calculated metrics"""
        try:
            async with self.pool.acquire() as conn:
                # Get basic account data from social_accounts table
                query = """
                    SELECT 
                        sa.*,
                        COALESCE(sa.followers_count, 0) as followers_count,
                        COALESCE(sa.following_count, 0) as following_count,
                        COALESCE(sa.posts_count, 0) as posts_count,
                        COALESCE(sa.engagement_rate, 0.0) as engagement_rate,
                        COALESCE(sa.risk_score, 0.0) as risk_score,
                        COALESCE(sa.consecutive_errors, 0) as consecutive_errors
                    FROM social_accounts sa 
                    WHERE sa.id = $1
                """
                row = await conn.fetchrow(query, account_id)
                
                if row:
                    account_data = dict(row)
                    
                    # Add calculated health score based on available metrics
                    health_score = 100.0
                    if account_data.get('consecutive_errors', 0) > 0:
                        health_score -= min(50, account_data['consecutive_errors'] * 10)
                    if account_data.get('risk_score', 0) > 0.5:
                        health_score -= (account_data['risk_score'] * 30)
                    
                    account_data['health_score'] = max(0, health_score)
                    return account_data
                
                return None
        except Exception as e:
            logger.error(f"Error fetching account with metrics: {e}")
            return None
    
    # Utility Methods
    async def execute_query(self, query: str, *args) -> Any:
        """Execute a custom query"""
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)
    
    async def fetch_query(self, query: str, *args) -> List[Dict[str, Any]]:
        """Fetch results from a custom query"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *args)
            return [dict(row) for row in rows]
    
    def _get_env_var(self, key: str) -> Optional[str]:
        """Get environment variable"""
        import os
        return os.getenv(key)
    
    async def __aenter__(self):
        """Async context manager entry"""
        if not self.is_initialized:
            await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()

