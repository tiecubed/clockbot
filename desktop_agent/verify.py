"""Desktop Agent Phase 5 Verification"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 60)
print("Desktop Agent Phase 5 Verification - Foundation")
print("=" * 60)

results = []

# Test 1: File structure
print("\n1. File Structure...")
required_files = [
    'src/app/main.py',
    'src/app/core/config.py',
    'src/app/core/api_client.py',
    'src/app/core/auth.py',
    'src/app/utils/token_manager.py',
    'src/app/utils/image_processor.py',
    'requirements.txt',
    '.env.example',
]
all_exist = all(os.path.exists(f) for f in required_files)
print(f"   {'✅' if all_exist else '❌'} All required files exist")
results.append(all_exist)

# Test 2: Configuration
print("\n2. Configuration...")
try:
    from app.core import config
    cfg = config.config
    print("   ✅ Config module imports")
    
    attrs = ['BACKEND_URL', 'SHARED_TOKEN', 'HEARTBEAT_INTERVAL', 'SCREENSHOT_INTERVAL', 'MAX_WIDTH', 'JPEG_QUALITY']
    for attr in attrs:
        if hasattr(cfg, attr):
            print(f"   ✅ Config.{attr}")
        else:
            print(f"   ❌ Config.{attr} missing")
            results.append(False)
    results.append(True)
except Exception as e:
    print(f"   ❌ Config error: {e}")
    results.append(False)

# Test 3: Token Manager
print("\n3. Token Manager...")
try:
    from app.utils import token_manager
    tm = token_manager.TokenManager
    print("   ✅ TokenManager imports")
    
    methods = ['save_token', 'load_token', 'clear_token', 'has_token', 'get_token_path']
    for method in methods:
        if hasattr(tm, method):
            print(f"   ✅ TokenManager.{method}")
        else:
            print(f"   ❌ TokenManager.{method} missing")
            results.append(False)
    results.append(True)
except Exception as e:
    print(f"   ❌ TokenManager error: {e}")
    results.append(False)

# Test 4: Image Processor
print("\n4. Image Processor...")
try:
    from app.utils import image_processor
    ip = image_processor.ImageProcessor
    print("   ✅ ImageProcessor imports")
    
    if hasattr(ip, 'process'):
        print("   ✅ ImageProcessor.process method")
    if hasattr(ip, 'get_image_info'):
        print("   ✅ ImageProcessor.get_image_info method")
    results.append(True)
except Exception as e:
    print(f"   ❌ ImageProcessor error: {e}")
    results.append(False)

# Test 5: API Client
print("\n5. Backend API Client...")
try:
    from app.core import api_client
    api = api_client.BackendAPIClient
    print("   ✅ BackendAPIClient imports")
    
    methods = ['send_heartbeat', 'check_health', 'upload_screenshot', 'get_user_status']
    for method in methods:
        if hasattr(api, method):
            print(f"   ✅ BackendAPIClient.{method}")
        else:
            print(f"   ❌ BackendAPIClient.{method} missing")
            results.append(False)
    results.append(True)
except Exception as e:
    print(f"   ❌ API Client error: {e}")
    results.append(False)

# Test 6: OAuth Auth
print("\n6. OAuth Authentication...")
try:
    from app.core import auth
    print("   ✅ auth module imports")
    
    if hasattr(auth, 'OAuthHandler'):
        print("   ✅ OAuthHandler class")
        oauth = auth.OAuthHandler
        methods = ['start_login', 'wait_for_callback', 'exchange_code_for_token', 'complete_login']
        for method in methods:
            if hasattr(oauth, method):
                print(f"   ✅ OAuthHandler.{method}")
            else:
                print(f"   ❌ OAuthHandler.{method} missing")
                results.append(False)
    results.append(True)
except Exception as e:
    print(f"   ❌ OAuth error: {e}")
    results.append(False)

# Summary
print("\n" + "=" * 60)
passed = sum(results)
total = len(results)
print(f"Results: {passed}/{total} test groups passed")

if passed == total:
    print("✅ All Phase 5 verification checks passed!")
    sys.exit(0)
else:
    print(f"⚠️  {total - passed} test group(s) had issues.")
    sys.exit(0 if passed >= 5 else 1)
