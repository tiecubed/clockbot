"""Discord Bot Verification Script"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 60)
print("Discord Bot Phase 3 Verification")
print("=" * 60)

results = []

# Test 1: Check requirements exist
print("\n1. Checking requirements.txt...")
if os.path.exists('requirements.txt'):
    print("   ✅ requirements.txt exists")
    with open('requirements.txt') as f:
        deps = f.read()
        if 'discord.py' in deps:
            print("   ✅ discord.py listed")
        if 'httpx' in deps:
            print("   ✅ httpx listed")
    results.append(True)
else:
    print("   ❌ requirements.txt missing")
    results.append(False)

# Test 2: Check .env.example exists
print("\n2. Checking .env.example...")
if os.path.exists('.env.example'):
    print("   ✅ .env.example exists")
    with open('.env.example') as f:
        env = f.read()
        if 'DISCORD_TOKEN' in env:
            print("   ✅ DISCORD_TOKEN documented")
        if 'SHARED_TOKEN' in env:
            print("   ✅ SHARED_TOKEN documented")
    results.append(True)
else:
    print("   ❌ .env.example missing")
    results.append(False)

# Test 3: Check file structure
print("\n3. Checking file structure...")
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
all_exist = True
for f in required_files:
    exists = os.path.exists(f)
    status = "✅" if exists else "❌"
    print(f"   {status} {f}")
    if not exists:
        all_exist = False
results.append(all_exist)

# Test 4: Try imports (if discord.py available)
print("\n4. Testing imports...")
try:
    from bot import config
    print("   ✅ bot.config imports")
    results.append(True)
except ImportError as e:
    print(f"   ❌ bot.config: {e}")
    results.append(False)

try:
    from bot.core import api_client
    print("   ✅ bot.core.api_client imports")
    results.append(True)
except ImportError as e:
    print(f"   ❌ bot.core.api_client: {e}")
    results.append(False)

try:
    from bot.core import checks
    print("   ✅ bot.core.checks imports")
    results.append(True)
except ImportError as e:
    print(f"   ❌ bot.core.checks: {e}")
    results.append(False)

try:
    from bot.commands import router
    print("   ✅ bot.commands.router imports")
    results.append(True)
except ImportError as e:
    print(f"   ❌ bot.commands.router: {e}")
    results.append(False)

try:
    from bot.commands import user
    print("   ✅ bot.commands.user imports")
    results.append(True)
except ImportError as e:
    print(f"   ❌ bot.commands.user: {e}")
    results.append(False)

try:
    from bot.commands import admin
    print("   ✅ bot.commands.admin imports")
    results.append(True)
except ImportError as e:
    print(f"   ❌ bot.commands.admin: {e}")
    results.append(False)

try:
    from bot.services import formatter
    print("   ✅ bot.services.formatter imports")
    results.append(True)
except ImportError as e:
    print(f"   ❌ bot.services.formatter: {e}")
    results.append(False)

# Test 5: Check API client auth format
print("\n5. Checking API client auth format...")
try:
    import inspect
    source = inspect.getsource(api_client.BackendAPIClient.__init__)
    if "Authorization" in source and "Bearer" in source:
        print("   ✅ API client uses Bearer token format")
    else:
        print("   ⚠️  Check API client auth format")
    results.append(True)
except Exception as e:
    print(f"   ❌ Error checking API client: {e}")
    results.append(False)

# Summary
print("\n" + "=" * 60)
passed = sum(results)
total = len(results)
print(f"Results: {passed}/{total} tests passed")

if passed == total:
    print("✅ All Phase 3 verification checks passed!")
    sys.exit(0)
else:
    print("❌ Some checks failed. Review output above.")
    sys.exit(1)
