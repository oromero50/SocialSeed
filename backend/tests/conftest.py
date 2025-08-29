"""
SocialSeed v2.0 - Test Configuration and Fixtures
Comprehensive testing setup for backend API and services
"""
import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from fastapi.testclient import TestClient

from main import app, SocialSeedOrchestrator
from database import DatabaseManager
import os

# Test Database Configuration
TEST_DATABASE_URL = "sqlite:///./test_socialseed.db"
os.environ["DATABASE_URL"] = TEST_DATABASE_URL
os.environ["TESTING"] = "true"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def test_db():
    """Create test database and clean up after tests."""
    db = DatabaseManager()
    await db.initialize()
    yield db
    await db.close()

@pytest.fixture
def test_client():
    """Create test client for API testing."""
    return TestClient(app)

@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Create async client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def test_orchestrator(test_db):
    """Create test orchestrator instance."""
    orchestrator = SocialSeedOrchestrator()
    orchestrator.db = test_db
    return orchestrator

@pytest.fixture
def mock_user_data():
    """Mock user data for testing."""
    return {
        "email": "test@socialseed.com",
        "password": "test_password_123",
        "first_name": "Test",
        "last_name": "User"
    }

@pytest.fixture
def mock_account_data():
    """Mock social account data for testing."""
    return {
        "platform": "tiktok",
        "username": "test_tiktok_user",
        "access_token": "mock_access_token_123"
    }

@pytest.fixture
def mock_action_data():
    """Mock action data for testing."""
    return {
        "action_type": "follow",
        "target_account": "target_user_123",
        "target_data": {"followers": 1000, "engagement_rate": 0.05}
    }

