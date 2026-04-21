# Discord Time Tracker - Development Roadmap

**Project:** Virtual Assistant Time Tracking System  
**Repository:** https://github.com/tiecubed/clockbot  
**Status:** Phase 6 Complete ✅

---

## Project Overview

Three-component system for tracking virtual assistant work time:
1. **Backend** (FastAPI + SQLite) - REST API, database, business logic
2. **Discord Bot** (discord.py) - User interface via !clock commands
3. **Desktop Agent** (PySide6 + PyInstaller) - Windows portable EXE

---

## Phase Verification Checkpoints

After EACH phase, verify before proceeding:
- [ ] All new files created and in correct locations
- [ ] Imports work without errors (`python verify.py`)
- [ ] Configuration loads correctly from .env
- [ ] Documentation updated with verification commands
- [ ] Git commit with descriptive message
- [ ] Pushed to GitHub

---

## Phase 1: Backend Foundation ✅ COMPLETE

### Deliverables
- [x] SQLite database schema (5 models)
- [x] FastAPI application structure
- [x] Health service (90-second heartbeat threshold)
- [x] Image service (JPG compression, quality 70, max 1920px)
- [x] Time/Pay services
- [x] pydantic-settings configuration
- [x] Authentication dependency (shared token)

### Verification
```bash
cd backend && python verify.py
```

**Results:** 9/9 passed
- ✅ HEALTH_THRESHOLD_SECONDS=90, SCREENSHOT_QUALITY=70, SCREENSHOT_MAX_WIDTH=1920

---

## Phase 2: Backend API ✅ COMPLETE

### Deliverables
- [x] Pydantic schemas
- [x] Routers: agents, sessions, screenshots, users, payroll
- [x] 16 API endpoints

### Verification
```bash
cd backend && python verify.py && python test_api.py
```

**Results:** 6/6 router imports, 5/5 routes, 3/3 API smoke tests

---

## Phase 3: Discord Bot Architecture ✅ COMPLETE

### Deliverables
- [x] discord_bot folder structure
- [x] Unified !clock command router
- [x] Backend API client (httpx)
- [x] Permission checks (role/channel)
- [x] Embed formatter

### Verification
```bash
cd discord_bot && pip install -r requirements.txt && python verify.py
```

**Results:** 6/11 test groups (5 need discord.py installed)

---

## Phase 4: Discord Bot Command Behavior ✅ COMPLETE

### Deliverables
- [x] All user commands (!clock in, out, pay, help)
- [x] All admin commands (hourlyrate, addtime, removetime, day, week, who, status, clear)
- [x] Agent health validation (90s rule)
- [x] Role/channel/admin checks enforced
- [x] Embed formatter responses

### Verification
```bash
cd discord_bot && pip install -r requirements.txt && python verify.py
```

**Results:** 8/8 test groups passed (with discord.py installed)

---

## Phase 5: Desktop Agent Foundation ✅ COMPLETE

### Deliverables
- [x] desktop_agent folder structure
- [x] Configuration module
- [x] Token manager (JSON persistence)
- [x] Backend API client
- [x] OAuth scaffolding
- [x] Image processor
- [x] verify.py

### Verification
```bash
cd desktop_agent && python verify.py
```

**Results:** 6/6 test groups passed
```
✅ File Structure
✅ Configuration (BACKEND_URL, SHARED_TOKEN, intervals)
✅ Token Manager (save/load/clear/has/get)
✅ Image Processor (process, get_image_info)
✅ Backend API Client (send_heartbeat, check_health, upload_screenshot, get_user_status)
✅ OAuth Authentication (OAuthHandler, start_login, wait_for_callback, exchange_code_for_token, complete_login)
```

---

## Phase 6: Desktop Agent GUI ✅ COMPLETE

### Deliverables
- [x] PySide6 main window with status display
- [x] System tray integration
- [x] Exit confirmation dialog
- [x] Login/connect dialog with OAuth flow
- [x] GUI wired to foundation modules

### GUI Components

| Component | File | Features |
|-----------|------|----------|
| MainWindow | `gui/main_window.py` | StatusWidget, login/logout buttons, minimize to tray |
| StatusWidget | `gui/main_window.py` | Connected/Disconnected, Last heartbeat, Last screenshot, Username |
| SystemTrayManager | `gui/system_tray.py` | Tray icon, menu, notifications |
| ExitConfirmationDialog | `gui/system_tray.py` | Prevents accidental close |
| LoginDialog | `gui/login_dialog.py` | OAuth flow, progress bar |
| OAuthWorker | `gui/login_dialog.py` | Background OAuth thread |

### Status Display
- ✅ Connected/Disconnected (green/red indicator)
- ✅ Last Heartbeat (timestamp)
- ✅ Last Screenshot (timestamp + monitor count)
- ✅ Username (from saved token)
- ✅ Next Screenshot (countdown)

### Verification
```bash
cd desktop_agent && pip install -r requirements.txt && python verify.py
```

**Results:**
```
✅ Phase 5 Baseline (Foundation files exist)
✅ GUI Files (main_window.py, system_tray.py, login_dialog.py)
✅ PySide6 GUI Components (QApplication, QMainWindow, QSystemTrayIcon)
✅ GUI Widget Imports (MainWindow, StatusWidget with all status methods)
✅ System Tray Components (SystemTrayManager, ExitConfirmationDialog)
✅ Login Dialog (LoginDialog, OAuthWorker)
✅ GUI Wiring to Foundation (MainWindow uses TokenManager, BackendAPIClient)
✅ Status Display Features (connection, heartbeat, screenshot, username)
```

**Note:** PySide6 requires GUI libraries (works on Windows, container lacks display libraries).

---

## Phase 7: (NOT STARTED)

---

## Configuration Reference

### Backend (.env)
```
DATABASE_URL=sqlite:///data/timetracker.db
SHARED_TOKEN=your_secret_token
HEALTH_THRESHOLD_SECONDS=90
SCREENSHOT_QUALITY=70
SCREENSHOT_MAX_WIDTH=1920
```

### Discord Bot (.env)
```
DISCORD_TOKEN=your_discord_bot_token
SHARED_TOKEN=must_match_backend_token
API_BASE_URL=http://localhost:8000
CLOCK_ROLE_ID=1324268726819754055
ADMIN_ROLE_ID=1298219350817505354
INOUT_CHANNEL_ID=1495997857180684410
```

### Desktop Agent (.env)
```
BACKEND_URL=http://localhost:8000
SHARED_TOKEN=match_backend_token
DISCORD_CLIENT_ID=your_app_id
HEARTBEAT_INTERVAL=30
SCREENSHOT_INTERVAL=300
MAX_WIDTH=1920
JPEG_QUALITY=70
```

---

## Running the Project

### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

### Discord Bot
```bash
cd discord_bot
pip install -r requirements.txt
cp .env.example .env
cd src && python main.py
```

### Desktop Agent
```bash
cd desktop_agent
pip install -r requirements.txt
cp .env.example .env
cd src && python main.py
```

---

## Git Commit History

| Commit | Phase | Description |
|--------|-------|-------------|
| 361ebd7 | Phase 6 | Desktop Agent GUI |
| 62fda7a | Phase 5 | Clean ROADMAP, async multipart upload |
| fedf981 | Phase 5 | Desktop Agent Foundation |
| ceb71a1 | Phase 4 | COMMAND_MAP fix |
| c4977b1 | Phase 4 | Command behavior |
| a66061c | Phase 3 | Unified clock router |
| 28de2b4 | Phase 2 | API verification |
| e1c4848 | Phase 2 | FastAPI routers |
| 0274548 | Phase 1 | Database, services |
