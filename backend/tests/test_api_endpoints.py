"""
SocialSeed v2.0 - API Endpoint Testing
Comprehensive testing for all API endpoints
"""
import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient


class TestHealthEndpoints:
    """Test health and monitoring endpoints."""
    
    def test_health_check(self, test_client: TestClient):
        """Test basic health check endpoint."""
        response = test_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "services" in data
    
    def test_platform_health(self, test_client: TestClient):
        """Test platform health monitoring."""
        response = test_client.get("/platform-health")
        assert response.status_code == 200
        data = response.json()
        assert "database" in data
        assert "ai_service" in data
        assert "platform_services" in data


class TestAccountManagement:
    """Test account management endpoints."""
    
    @pytest.mark.asyncio
    async def test_get_accounts_empty(self, async_client: AsyncClient):
        """Test getting accounts when none exist."""
        response = await async_client.get("/accounts")
        assert response.status_code == 200
        assert response.json() == []
    
    @pytest.mark.asyncio
    async def test_create_account(self, async_client: AsyncClient, mock_account_data):
        """Test creating a new social media account."""
        response = await async_client.post("/accounts", json=mock_account_data)
        assert response.status_code == 201
        data = response.json()
        assert data["platform"] == mock_account_data["platform"]
        assert data["username"] == mock_account_data["username"]
        assert "id" in data
    
    @pytest.mark.asyncio
    async def test_get_account_by_id(self, async_client: AsyncClient, mock_account_data):
        """Test retrieving specific account by ID."""
        # First create account
        create_response = await async_client.post("/accounts", json=mock_account_data)
        account_id = create_response.json()["id"]
        
        # Then retrieve it
        response = await async_client.get(f"/accounts/{account_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == account_id
        assert data["platform"] == mock_account_data["platform"]


class TestApprovalWorkflow:
    """Test human approval workflow endpoints."""
    
    @pytest.mark.asyncio
    async def test_get_pending_approvals_empty(self, async_client: AsyncClient):
        """Test getting pending approvals when none exist."""
        response = await async_client.get("/approvals/pending")
        assert response.status_code == 200
        assert response.json() == []
    
    @pytest.mark.asyncio
    async def test_approve_action(self, async_client: AsyncClient):
        """Test approving a pending action."""
        # This would require setting up a pending action first
        # For now, test the endpoint structure
        response = await async_client.post("/approvals/mock-id/approve")
        # Expect 404 for non-existent approval
        assert response.status_code in [404, 422]


class TestActionExecution:
    """Test action execution endpoints."""
    
    @pytest.mark.asyncio
    async def test_execute_action_validation(self, async_client: AsyncClient):
        """Test action execution with invalid data."""
        invalid_action = {"invalid": "data"}
        response = await async_client.post("/actions/execute", json=invalid_action)
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.asyncio
    async def test_get_action_history_empty(self, async_client: AsyncClient):
        """Test getting action history when none exist."""
        response = await async_client.get("/actions/history")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestAnalytics:
    """Test analytics and reporting endpoints."""
    
    @pytest.mark.asyncio
    async def test_get_growth_analytics_no_account(self, async_client: AsyncClient):
        """Test growth analytics for non-existent account."""
        response = await async_client.get("/analytics/growth/fake-id")
        assert response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_get_performance_analytics(self, async_client: AsyncClient):
        """Test performance analytics endpoint."""
        response = await async_client.get("/analytics/performance")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

