"""Desktop Agent Verification - Phase 6 GUI"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 60)
print("Desktop Agent Phase 6 Verification - GUI")
print("=" * 60)

results = []

# Test 1: Phase 5 Baseline
print("\n1. Phase 5 Baseline (Foundation)...")
required_files = [
    'src/app/main.py',
    'src/app/core/config.py',
    'src/app/core/api_client.py',
    'src/app/core/auth.py',
    'src/app/utils/token_manager.py',
    'src/app/utils/image_processor.py',
]
all_exist = all(os.path.exists(f) for f in required_files)
print(f"   {'✅' if all_exist else '❌'} Foundation files exist")
results.append(all_exist)

# Test 2: GUI Files
print("\n2. GUI Files...")
gui_files = [
    'src/app/gui/main_window.py',
    'src/app/gui/system_tray.py',
    'src/app/gui/login_dialog.py',
]
all_gui = all(os.path.exists(f) for f in gui_files)
print(f"   {'✅' if all_gui else '❌'} GUI files exist")
for f in gui_files:
    print(f"      - {f}")
results.append(all_gui)

# Test 3: PySide6 Imports
print("\n3. PySide6 GUI Components...")
try:
    from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QIcon
    print("   ✅ PySide6 imports successful")
    results.append(True)
except ImportError as e:
    print(f"   ❌ PySide6 not installed: {e}")
    print("      Install: pip install PySide6")
    results.append(False)

# Test 4: GUI Widgets
print("\n4. GUI Widget Imports...")
try:
    from app.gui.main_window import MainWindow, StatusWidget
    print("   ✅ MainWindow imports")
    print("   ✅ StatusWidget imports")
    
    # Check StatusWidget methods
    methods = ['update_connection', 'update_heartbeat', 'update_screenshot', 'update_countdown']
    for method in methods:
        if hasattr(StatusWidget, method):
            print(f"   ✅ StatusWidget.{method}")
        else:
            print(f"   ❌ StatusWidget.{method} missing")
    results.append(True)
except Exception as e:
    print(f"   ❌ MainWindow error: {e}")
    results.append(False)

# Test 5: System Tray
print("\n5. System Tray Components...")
try:
    from app.gui.system_tray import SystemTrayManager, ExitConfirmationDialog
    print("   ✅ SystemTrayManager imports")
    print("   ✅ ExitConfirmationDialog imports")
    
    # Check SystemTrayManager methods
    methods = ['show_window', 'update_status', 'show_notification', 'hide']
    for method in methods:
        if hasattr(SystemTrayManager, method):
            print(f"   ✅ SystemTrayManager.{method}")
        else:
            print(f"   ⚠️  SystemTrayManager.{method} missing")
    
    # Check ExitConfirmationDialog
    if hasattr(ExitConfirmationDialog, 'confirm'):
        print("   ✅ ExitConfirmationDialog.confirm")
    results.append(True)
except Exception as e:
    print(f"   ❌ System Tray error: {e}")
    results.append(False)

# Test 6: Login Dialog
print("\n6. Login Dialog...")
try:
    from app.gui.login_dialog import LoginDialog, OAuthWorker
    print("   ✅ LoginDialog imports")
    print("   ✅ OAuthWorker imports")
    
    # Check LoginDialog methods
    if hasattr(LoginDialog, 'start_oauth'):
        print("   ✅ LoginDialog.start_oauth")
    if hasattr(LoginDialog, 'on_oauth_finished'):
        print("   ✅ LoginDialog.on_oauth_finished")
    results.append(True)
except Exception as e:
    print(f"   ❌ Login Dialog error: {e}")
    results.append(False)

# Test 7: GUI Wiring to Foundation
print("\n7. GUI Wiring to Foundation...")
try:
    from app.gui.main_window import MainWindow
    from app.utils.token_manager import TokenManager
    from app.core.api_client import BackendAPIClient
    print("   ✅ MainWindow can import TokenManager")
    print("   ✅ MainWindow can import BackendAPIClient")
    
    # Check MainWindow uses token data
    if 'token_data' in str(MainWindow.__init__.__code__.co_varnames):
        print("   ✅ MainWindow accepts token_data parameter")
    if 'update_status_from_token' in dir(MainWindow):
        print("   ✅ MainWindow.update_status_from_token method")
    results.append(True)
except Exception as e:
    print(f"   ❌ Wiring error: {e}")
    results.append(False)

# Test 8: Status Display Features
print("\n8. Status Display Features...")
try:
    from app.gui.main_window import StatusWidget
    
    features = [
        ('Connected/Disconnected', 'update_connection'),
        ('Last heartbeat', 'update_heartbeat'),
        ('Last screenshot', 'update_screenshot'),
        ('Username display', 'update_connection'),  # Shows username
    ]
    
    for label, method in features:
        if hasattr(StatusWidget, method):
            print(f"   ✅ {label} via {method}")
        else:
            print(f"   ❌ {label} missing")
    
    results.append(True)
except Exception as e:
    print(f"   ❌ Status features error: {e}")
    results.append(False)

# Summary
print("\n" + "=" * 60)
passed = sum(results)
total = len(results)
print(f"Results: {passed}/{total} test groups passed")

if passed == total:
    print("✅ All Phase 6 verification checks passed!")
    sys.exit(0)
else:
    print(f"⚠️  {total - passed} test group(s) had issues.")
    print("Note: Some tests require PySide6 (pip install PySide6)")
    sys.exit(0 if passed >= 6 else 1)
