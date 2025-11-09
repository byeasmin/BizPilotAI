# tests/test_transactions.py
import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from app.main import app
from app.create_db import create_db_and_tables
from app.seed_demo import seed
from app.database import engine
from sqlmodel import Session, select
from app.models.user import User
from app.models.transaction import Transaction

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    """Setup test database with demo data"""
    create_db_and_tables()
    seed()
    yield
    # Cleanup could be added here for non-SQLite databases

@pytest.fixture(scope="module")
def auth_headers():
    """Get authentication headers for demo user"""
    response = client.post(
        "/auth/login",
        json={
            "email": "demo@example.com",
            "password": "password"
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

class TestTransactions:
    def test_login_success(self, auth_headers):
        """Test successful login"""
        assert "Bearer " in auth_headers["Authorization"]

    def test_get_transactions(self, auth_headers):
        """Test retrieving transactions list"""
        response = client.get("/transactions", headers=auth_headers)
        transactions = response.json()
        
        assert response.status_code == 200
        assert isinstance(transactions, list)
        if len(transactions) > 0:
            assert "id" in transactions[0]
            assert "amount" in transactions[0]
            assert "description" in transactions[0]
            assert "date" in transactions[0]

    def test_create_transaction(self, auth_headers):
        """Test creating a new transaction"""
        new_transaction = {
            "amount": 100.50,
            "description": "Test Transaction",
            "date": datetime.now().isoformat(),
            "category": "INCOME"
        }
        
        response = client.post(
            "/transactions", 
            headers=auth_headers,
            json=new_transaction
        )
        
        assert response.status_code == 200
        created_transaction = response.json()
        assert created_transaction["amount"] == new_transaction["amount"]
        assert created_transaction["description"] == new_transaction["description"]

    def test_get_transaction_by_id(self, auth_headers):
        """Test retrieving a specific transaction"""
        # First create a transaction
        new_transaction = {
            "amount": 75.25,
            "description": "Test Get By ID",
            "date": datetime.now().isoformat(),
            "category": "EXPENSE"
        }
        
        create_response = client.post(
            "/transactions", 
            headers=auth_headers,
            json=new_transaction
        )
        
        transaction_id = create_response.json()["id"]
        
        # Then retrieve it
        response = client.get(f"/transactions/{transaction_id}", headers=auth_headers)
        assert response.status_code == 200
        transaction = response.json()
        assert transaction["id"] == transaction_id

    def test_unauthorized_access(self):
        """Test accessing transactions without authentication"""
        response = client.get("/transactions")
        assert response.status_code == 401

    @pytest.mark.parametrize("invalid_data", [
        {"amount": "invalid", "description": "Test", "date": "2023-01-01"},
        {"amount": 100},  # Missing required fields
        {"amount": -1000000, "description": "Test", "date": "2023-01-01"},  # Invalid amount
    ])
    def test_invalid_transaction_creation(self, auth_headers, invalid_data):
        """Test creating transactions with invalid data"""
        response = client.post(
            "/transactions",
            headers=auth_headers,
            json=invalid_data
        )
        assert response.status_code in [400, 422]
