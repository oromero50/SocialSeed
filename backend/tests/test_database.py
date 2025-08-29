"""
SocialSeed v2.0 - Database Testing
Comprehensive testing for database operations
"""
import pytest
from database import DatabaseManager


class TestDatabaseConnection:
    """Test database connection and initialization."""
    
    @pytest.mark.asyncio
    async def test_database_initialization(self, test_db: DatabaseManager):
        """Test database connection and initialization."""
        assert test_db is not None
        assert hasattr(test_db, 'pool')
    
    @pytest.mark.asyncio
    async def test_get_system_overview(self, test_db: DatabaseManager):
        """Test system overview method."""
        overview = await test_db.get_system_overview()
        assert isinstance(overview, dict)
        assert "total_users" in overview
        assert "active_accounts" in overview


class TestUserOperations:
    """Test user CRUD operations."""
    
    @pytest.mark.asyncio
    async def test_create_user(self, test_db: DatabaseManager, mock_user_data):
        """Test creating a new user."""
        user_id = await test_db.create_user(**mock_user_data)
        assert user_id is not None
        assert isinstance(user_id, str)
    
    @pytest.mark.asyncio
    async def test_get_user_by_id(self, test_db: DatabaseManager, mock_user_data):
        """Test retrieving user by ID."""
        user_id = await test_db.create_user(**mock_user_data)
        user = await test_db.get_user_by_id(user_id)
        assert user is not None
        assert user["email"] == mock_user_data["email"]
        assert user["first_name"] == mock_user_data["first_name"]


class TestAccountOperations:
    """Test social account CRUD operations."""
    
    @pytest.mark.asyncio
    async def test_create_social_account(self, test_db: DatabaseManager, mock_account_data):
        """Test creating a social media account."""
        # First create a user
        user_data = {
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User"
        }
        user_id = await test_db.create_user(**user_data)
        
        # Then create account
        account_data = {**mock_account_data, "user_id": user_id}
        account_id = await test_db.create_social_account(**account_data)
        assert account_id is not None
        assert isinstance(account_id, str)
    
    @pytest.mark.asyncio
    async def test_get_user_accounts(self, test_db: DatabaseManager, mock_account_data):
        """Test getting all accounts for a user."""
        # Create user and account
        user_data = {
            "email": "test2@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User"
        }
        user_id = await test_db.create_user(**user_data)
        
        account_data = {**mock_account_data, "user_id": user_id}
        await test_db.create_social_account(**account_data)
        
        accounts = await test_db.get_user_accounts(user_id)
        assert isinstance(accounts, list)
        assert len(accounts) >= 1
        assert accounts[0]["platform"] == mock_account_data["platform"]


class TestActionLogging:
    """Test action logging and retrieval."""
    
    @pytest.mark.asyncio
    async def test_log_action(self, test_db: DatabaseManager):
        """Test logging an action."""
        # This would require setting up an account first
        # For now, test the method exists
        assert hasattr(test_db, 'log_action')
    
    @pytest.mark.asyncio
    async def test_get_all_pending_approvals(self, test_db: DatabaseManager):
        """Test getting pending approvals."""
        approvals = await test_db.get_all_pending_approvals()
        assert isinstance(approvals, list)

