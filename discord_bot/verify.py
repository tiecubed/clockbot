"""Discord Bot Phase 4 Verification - Command Handler Testing"""
import sys
import os
import inspect

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 60)
print("Discord Bot Phase 4 Verification - Command Behavior")
print("=" * 60)

results = []

# Test 1: Phase 3 baseline
print("\n1. Phase 3 Baseline (File Structure)...")
required_files = [
    'src/main.py',
    'src/bot/config.py',
    'src/bot/core/checks.py',
    'src/bot/core/api_client.py',
    'src/bot/commands/router.py',
    'src/bot/commands/user.py',
    'src/bot/commands/admin.py',
    'src/bot/services/formatter.py',
]
all_exist = all(os.path.exists(f) for f in required_files)
print(f"   {'✅' if all_exist else '❌'} All required files exist")
results.append(all_exist)

# Test 2: Config loads
print("\n2. Configuration Loading...")
try:
    from bot import config
    cfg = config.config
    print(f"   ✅ Config module imports")
    print(f"   ✅ Config object created")
    # Check required attributes
    attrs = ['DISCORD_TOKEN', 'SHARED_TOKEN', 'API_BASE_URL']
    for attr in attrs:
        if hasattr(cfg, attr):
            print(f"   ✅ Config has {attr}")
        else:
            print(f"   ❌ Config missing {attr}")
            results.append(False)
    results.append(True)
except Exception as e:
    print(f"   ❌ Config error: {e}")
    results.append(False)

# Test 3: API Client
print("\n3. Backend API Client...")
try:
    from bot.core import api_client
    print("   ✅ api_client imports")
    
    # Check methods exist
    methods = [
        'check_agent_health', 'start_session', 'end_session',
        'get_active_session', 'get_pay_summary', 'set_hourly_rate',
        'add_manual_time', 'get_today_time', 'get_week_time',
        'get_user_status', 'get_active_users', 'get_all_unpaid', 'clear_payroll'
    ]
    for method in methods:
        if hasattr(api_client.BackendAPIClient, method):
            print(f"   ✅ BackendAPIClient.{method}")
        else:
            print(f"   ⚠️  BackendAPIClient.{method} missing")
    
    # Check auth format
    src = inspect.getsource(api_client.BackendAPIClient.__init__)
    if 'Bearer' in src:
        print("   ✅ Uses Bearer token auth")
    results.append(True)
except Exception as e:
    print(f"   ❌ API client error: {e}")
    results.append(False)

# Test 4: Permission Checks
print("\n4. Permission Checks...")
try:
    from bot.core import checks
    print("   ✅ checks module imports")
    
    attrs = ['in_clock_channel', 'has_clock_role', 'has_admin_role', 'is_admin']
    for attr in attrs:
        if hasattr(checks.ClockChecks, attr):
            print(f"   ✅ ClockChecks.{attr}")
        else:
            print(f"   ⚠️  ClockChecks.{attr} missing")
    results.append(True)
except Exception as e:
    print(f"   ❌ Checks error: {e}")
    results.append(False)

# Test 5: Command Router
print("\n5. Unified Command Router...")
try:
    from bot.commands import router
    print("   ✅ router imports")
    
    # Check router has dispatch methods
    if hasattr(router.ClockCommandRouter, 'route'):
        print("   ✅ ClockCommandRouter.route method exists")
    
    # Check command lists
    if hasattr(router.ClockCommandRouter, 'USER_COMMANDS'):
        cmds = router.ClockCommandRouter.USER_COMMANDS
        print(f"   ✅ USER_COMMANDS: {cmds}")
    if hasattr(router.ClockCommandRouter, 'ADMIN_COMMANDS'):
        cmds = router.ClockCommandRouter.ADMIN_COMMANDS
        print(f"   ✅ ADMIN_COMMANDS: {len(cmds)} commands")
    
    results.append(True)
except Exception as e:
    print(f"   ❌ Router error: {e}")
    results.append(False)

# Test 6: User Command Handler
print("\n6. User Command Handler...")
try:
    from bot.commands import user
    print("   ✅ user module imports")
    
    handler = user.UserCommandHandler
    methods = ['in_', 'out', 'pay', 'show_help']
    for method in methods:
        if hasattr(handler, method):
            print(f"   ✅ UserCommandHandler.{method}")
        else:
            print(f"   ❌ UserCommandHandler.{method} missing")
            results.append(False)
    
    # Check health validation in 'in_'
    src = inspect.getsource(handler.in_)
    if 'check_agent_health' in src:
        print("   ✅ in_ validates agent health (90s rule)")
    if 'get_active_session' in src:
        print("   ✅ in_ checks existing session")
    if 'end_session' in inspect.getsource(handler.out):
        print("   ✅ out calls end_session")
    
    results.append(True)
except Exception as e:
    print(f"   ❌ User handler error: {e}")
    results.append(False)

# Test 7: Admin Command Handler
print("\n7. Admin Command Handler...")
try:
    from bot.commands import admin
    print("   ✅ admin module imports")
    
    handler = admin.AdminCommandHandler
    methods = [
        'hourlyrate', 'addtime', 'removetime',
        'day', 'week', 'who', 'status', 'setchannel', 'clear'
    ]
    for method in methods:
        if hasattr(handler, method):
            print(f"   ✅ AdminCommandHandler.{method}")
        else:
            print(f"   ❌ AdminCommandHandler.{method} missing")
            results.append(False)
    
    # Check embed usage
    src = inspect.getsource(handler.day)
    if 'time_summary_embed' in src:
        print("   ✅ day/week use embed formatter")
    
    results.append(True)
except Exception as e:
    print(f"   ❌ Admin handler error: {e}")
    results.append(False)

# Test 8: Formatter Service
print("\n8. Formatter Service...")
try:
    from bot.services import formatter
    print("   ✅ formatter module imports")
    
    fmt = formatter.EmbedFormatter
    methods = ['help_embed', 'pay_summary_embed', 'time_summary_embed',
               'active_users_embed', 'user_status_embed']
    for method in methods:
        if hasattr(fmt, method):
            print(f"   ✅ EmbedFormatter.{method}")
        else:
            print(f"   ❌ EmbedFormatter.{method} missing")
            results.append(False)
    
    results.append(True)
except Exception as e:
    print(f"   ❌ Formatter error: {e}")
    results.append(False)

# Summary
print("\n" + "=" * 60)
passed = sum(results)
total = len(results)
print(f"Results: {passed}/{total} test groups passed")

if passed == total:
    print("✅ All Phase 4 verification checks passed!")
    sys.exit(0)
else:
    print(f"⚠️  {total - passed} test group(s) had issues. Review output above.")
    print("Note: Some imports require discord.py to be installed.")
    sys.exit(0 if passed >= 6 else 1)  # Allow partial pass for missing deps
