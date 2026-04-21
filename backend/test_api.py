"""API Smoke Test - Test actual endpoints with HTTP requests."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.database import init_db

# Initialize database before running tests
print("Initializing database...")
init_db()
print("Database initialized.\n")

client = TestClient(app)


def test_health_endpoint():
    """Test GET /health"""
    print("Testing GET /health...")
    response = client.get("/health")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data["status"] == "healthy", f"Expected status=healthy, got {data['status']}"
    print(f"  ✓ Status: {data['status']}")
    return True


def test_agents_health_endpoint():
    """Test GET /api/v1/agents/{user_id}/health"""
    print("\nTesting GET /api/v1/agents/{user_id}/health...")
    
    # Test with token header
    headers = {"token": settings.SHARED_TOKEN}
    response = client.get("/api/v1/agents/test_user/health", headers=headers)
    
    # Should return 200 even if user doesn't exist (not healthy, but request succeeds)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    data = response.json()
    assert "user_id" in data, "Response missing user_id"
    assert "healthy" in data, "Response missing healthy"
    assert "threshold_seconds" in data, "Response missing threshold_seconds"
    print(f"  ✓ User ID: {data['user_id']}")
    print(f"  ✓ Healthy: {data['healthy']}")
    print(f"  ✓ Threshold: {data['threshold_seconds']}s")
    return True


def test_sessions_active_endpoint():
    """Test GET /api/v1/sessions/active/{user_id}"""
    print("\nTesting GET /api/v1/sessions/active/{user_id}...")
    
    headers = {"token": settings.SHARED_TOKEN}
    response = client.get("/api/v1/sessions/active/test_user", headers=headers)
    
    # Should return 404 if no active session (expected behavior)
    if response.status_code == 404:
        data = response.json()
        print(f"  ✓ Status: 404 (No active session - expected)")
        print(f"  ✓ Detail: {data.get('detail', 'No detail')}")
        return True
    elif response.status_code == 200:
        data = response.json()
        print(f"  ✓ Session found: {data.get('id')}")
        return True
    else:
        raise AssertionError(f"Unexpected status code: {response.status_code}")


def main():
    """Run all smoke tests."""
    print("=" * 60)
    print("API SMOKE TEST")
    print("=" * 60)
    print()
    
    tests = [
        ("Health Endpoint", test_health_endpoint),
        ("Agents Health", test_agents_health_endpoint),
        ("Sessions Active", test_sessions_active_endpoint),
    ]
    
    passed = 0
    failed = 0
    
    for name, test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  ✗ {name} failed: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("\n✅ API Smoke Test PASSED")
        return 0
    else:
        print("\n❌ API Smoke Test FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
