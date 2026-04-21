"""Phase 1 Verification Script - Test imports and basic functionality."""
import sys
from datetime import datetime

def test_imports():
    """Test all module imports."""
    print("=" * 50)
    print("PHASE 1 VERIFICATION")
    print("=" * 50)
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
    
    # Test dependencies
    print("Testing Dependencies:")
    for name, test in tests:
        try:
            test()
            print(f"  ✓ {name}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {name}: {e}")
            failed += 1
    
    print()
    
    # Test app modules
    print("Testing App Modules:")
    for name, code in app_tests:
        try:
            exec(code)
            print(f"  ✓ {name}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {name}: {e}")
            failed += 1
    
    print()
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    if failed == 0:
        print("\n✅ Phase 1 Verification PASSED")
        return 0
    else:
        print(f"\n❌ Phase 1 Verification FAILED ({failed} errors)")
        return 1


def test_config():
    """Test configuration values."""
    print("\nTesting Configuration:")
    from app.config import settings
    
    checks = [
        ("HEALTH_THRESHOLD_SECONDS", settings.HEALTH_THRESHOLD_SECONDS, 90),
        ("SCREENSHOT_QUALITY", settings.SCREENSHOT_QUALITY, 70),
        ("SCREENSHOT_MAX_WIDTH", settings.SCREENSHOT_MAX_WIDTH, 1920),
        ("PORT", settings.PORT, 8000),
    ]
    
    for name, actual, expected in checks:
        if actual == expected:
            print(f"  ✓ {name} = {actual}")
        else:
            print(f"  ✗ {name} = {actual} (expected {expected})")
    
    print()


def test_services():
    """Test service instantiation."""
    print("Testing Services (with mock DB):")
    
    # We can't test with real DB here, but we can verify classes exist
    try:
        from app.services import HealthService, ImageService, TimeService, PayService
        from app.database import SessionLocal
        
        print("  ✓ HealthService class available")
        print("  ✓ ImageService class available")
        print("  ✓ TimeService class available")
        print("  ✓ PayService class available")
        print("  ✓ Database SessionLocal available")
    except Exception as e:
        print(f"  ✗ Service import error: {e}")
    
    print()


if __name__ == "__main__":
    exit_code = test_imports()
    test_config()
    test_services()
    
    print(f"\nVerification completed at: {datetime.now().isoformat()}")
    sys.exit(exit_code)
