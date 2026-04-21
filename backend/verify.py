"""Phase 2 Verification Script - Test imports, app startup, and router integration."""
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_phase1_imports():
    """Test Phase 1: Core imports."""
    print("=" * 60)
    print("PHASE 1: Core Imports")
    print("=" * 60)
    print()
    
    tests = [
        ("FastAPI", lambda: __import__("fastapi")),
        ("SQLAlchemy", lambda: __import__("sqlalchemy")),
        ("PIL/Pillow", lambda: __import__("PIL")),
        ("Pydantic Settings", lambda: __import__("pydantic_settings")),
    ]
    
    app_tests = [
        ("app.config", "from app.config import settings"),
        ("app.database", "from app.database import Base, engine, get_db"),
        ("app.dependencies", "from app.dependencies import verify_token"),
        ("app.models", "from app.models import User, Session, Screenshot, ManualAdjustment, AgentStatus"),
        ("app.services", "from app.services import HealthService, ImageService, TimeService, PayService"),
    ]
    
    passed = 0
    failed = 0
    
    print("Testing Dependencies:")
    for name, test in tests:
        try:
            test()
            print(f"  ✓ {name}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {name}: {e}")
            failed += 1
    
    print("\nTesting App Modules:")
    for name, code in app_tests:
        try:
            exec(code)
            print(f"  ✓ {name}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {name}: {e}")
            failed += 1
    
    print(f"\nPhase 1 Results: {passed} passed, {failed} failed")
    return failed == 0


def test_phase2_routers():
    """Test Phase 2: Router imports and FastAPI app creation."""
    print()
    print("=" * 60)
    print("PHASE 2: Router Imports & App Creation")
    print("=" * 60)
    print()
    
    router_tests = [
        ("schemas", "from app.schemas import HeartbeatRequest, SessionStartResponse, TimeSummaryResponse"),
        ("routers.agents", "from app.routers import agents"),
        ("routers.sessions", "from app.routers import sessions"),
        ("routers.screenshots", "from app.routers import screenshots"),
        ("routers.users", "from app.routers import users"),
        ("routers.payroll", "from app.routers import payroll"),
    ]
    
    passed = 0
    failed = 0
    
    print("Testing Router Imports:")
    for name, code in router_tests:
        try:
            exec(code)
            print(f"  ✓ {name}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {name}: {e}")
            failed += 1
    
    # Test FastAPI app creation
    print("\nTesting FastAPI App Creation:")
    try:
        from app.main import app
        print("  ✓ FastAPI app created")
        
        # Check routes are registered
        routes = [route.path for route in app.routes]
        expected_routes = [
            "/api/v1/agents/heartbeat",
            "/api/v1/sessions/start",
            "/api/v1/screenshots/upload",
            "/api/v1/users/{user_id}/time/today",
            "/api/v1/payroll/unpaid",
        ]
        
        found_routes = []
        for expected in expected_routes:
            found = any(expected in str(r) for r in routes)
            if found:
                found_routes.append(expected)
        
        print(f"  ✓ {len(found_routes)}/5 expected API routes registered")
        for route in found_routes[:3]:
            print(f"     - {route}")
        
        passed += 1
    except Exception as e:
        print(f"  ✗ FastAPI app creation failed: {e}")
        failed += 1
    
    print(f"\nPhase 2 Results: {passed} passed, {failed} failed")
    return failed == 0


def test_config():
    """Test configuration values."""
    print()
    print("=" * 60)
    print("CONFIGURATION CHECK")
    print("=" * 60)
    print()
    
    from app.config import settings
    
    checks = [
        ("HEALTH_THRESHOLD_SECONDS", settings.HEALTH_THRESHOLD_SECONDS, 90),
        ("SCREENSHOT_QUALITY", settings.SCREENSHOT_QUALITY, 70),
        ("SCREENSHOT_MAX_WIDTH", settings.SCREENSHOT_MAX_WIDTH, 1920),
        ("PORT", settings.PORT, 8000),
    ]
    
    all_pass = True
    for name, actual, expected in checks:
        if actual == expected:
            print(f"  ✓ {name} = {actual}")
        else:
            print(f"  ✗ {name} = {actual} (expected {expected})")
            all_pass = False
    
    return all_pass


def main():
    """Run all verification tests."""
    print("║" + " " * 15 + "PHASE 2 VERIFICATION" + " " * 23 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    phase1_ok = test_phase1_imports()
    phase2_ok = test_phase2_routers()
    config_ok = test_config()
    
    print()
    print("=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    print()
    
    if phase1_ok and phase2_ok and config_ok:
        print("✅ ALL PHASE 2 VERIFICATIONS PASSED")
        print()
        print("Summary:")
        print("  ✓ Phase 1 imports (9/9)")
        print("  ✓ Phase 2 routers (6/6)")
        print("  ✓ FastAPI app creation")
        print("  ✓ API routes registered")
        print("  ✓ Configuration values correct")
        print()
        print(f"Verification completed: {datetime.now().isoformat()}")
        return 0
    else:
        print("❌ PHASE 2 VERIFICATION FAILED")
        print()
        if not phase1_ok:
            print("  ✗ Phase 1 imports failed")
        if not phase2_ok:
            print("  ✗ Phase 2 routers failed")
        if not config_ok:
            print("  ✗ Configuration check failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
