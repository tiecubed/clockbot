# Discord Time Tracker - Development Roadmap

**Project:** Virtual Assistant Time Tracking System  
**Repository:** https://github.com/tiecubed/clockbot  
**Status:** Phase 5 Complete ✅

---

## Project Overview

Three-component system for tracking virtual assistant work time:
1. **Backend** (FastAPI + SQLite) - REST API, database, business logic
2. **Discord Bot** (discord.py) - User interface via !clock commands
3. **Desktop Agent** (PySide6 + PyInstaller) - Windows portable EXE for screenshots

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
- [x] FastAPI application structure with lifespan events
- [x] Health service (90-second heartbeat threshold)
- [x] Image service (JPG compression, quality 70, max 1920px)
- [x] Time service (session calculations)
- [x] Pay service (payroll logic)
- [x] Configuration (pydantic-settings)
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
- [x] Pydantic schemas for all endpoints
- [x] Agents router (heartbeat, health check)
- [x] Sessions router (clock in/out)
- [x] Screenshots router (upload)
- [x] Users router (time/pay queries)
- [x] Payroll router (payroll management)

### API Endpoints (16 total)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/agents/heartbeat` | Agent heartbeat (30s) |
| GET | `/api/v1/agents/{id}/health` | Check health (90s threshold) |
| POST | `/api/v1/sessions/start` | Clock in (validates agent health) |
| POST | `/api/v1/sessions/{id}/end` | Clock out |
| GET | `/api/v1/sessions/active/{id}` | Get active session |
| POST | `/api/v1/screenshots/upload` | Upload screenshot |
| GET | `/api/v1/users/{id}/time/today` | Today's hours |
| GET | `/api/v1/users/{id}/time/week` | Last 7 days hours |
| GET | `/api/v1/users/{id}/pay/unpaid` | Unpaid summary |
| POST | `/api/v1/payroll/clear` | Mark all as paid |

### Verification
```bash
cd backend && python verify.py && python test_api.py
```

**Results:**
- ✅ Router Imports: 6/6 passed
- ✅ FastAPI App: 5/5 routes registered
- ✅ API Smoke Test: 3/3 passed

---

## Phase 3: Discord Bot Architecture ✅ COMPLETE

### Deliverables
- [x] discord_bot folder structure with src/ layout
- [x] Bot main entry point with unified !clock command
- [x] Unified command router/parser
- [x] Backend API client (httpx-based)
- [x] Permission checks (role/channel validators)
- [x] Discord embed formatter service
- [x] .env.example configuration template

### Verification
```bash
cd discord_bot && pip install -r requirements.txt && python verify.py
```

**Results:** 6/11 test groups passed (5 require discord.py installed)
- ✅ File structure complete (8/8 files)
- ✅ Config loading
- ✅ API Client (13 methods, Bearer auth)

---

## Phase 4: Discord Bot Command Behavior ✅ COMPLETE

### Deliverables
- [x] All user commands (!clock in, out, pay, help)
- [x] All admin commands (hourlyrate, addtime, removetime, day, week, who, status, clear)
- [x] Agent health validation before clock in (90s rule)
- [x] Role/channel/admin checks enforced
- [x] Embed formatter used for responses

### Command Implementation
| Command | Role Check | Channel Check | API Integration | Embeds |
|---------|------------|---------------|-------------------|--------|
| !clock in | ✅ clock_role | ✅ inout_channel | ✅ start_session | ✅ |
| !clock out | - | ✅ inout_channel | ✅ end_session | ✅ |
| !clock pay | - | - | ✅ get_pay_summary | ✅ |
| !clock help | - | - | - | ✅ |
| !clock hourlyrate | ✅ admin | - | ✅ set_hourly_rate | ✅ |
| !clock addtime | ✅ admin | - | ✅ add_manual_time | ✅ |
| !clock removetime | ✅ admin | - | ✅ add_manual_time | ✅ |
| !clock day | ✅ admin | - | ✅ get_today_time | ✅ |
| !clock week | ✅ admin | - | ✅ get_week_time | ✅ |
| !clock who | ✅ admin | - | ✅ get_active_users | ✅ |
| !clock status | ✅ admin | - | ✅ get_user_status | ✅ |
| !clock clear | ✅ admin | - | ✅ clear_payroll | ✅ |

### Verification
```bash
cd discord_bot && pip install -r requirements.txt && python verify.py
```

**Results:** 8/8 test groups passed (with discord.py installed)
- ✅ Permission Checks, Command Router, User/Admin Handlers, Formatter

---

## Phase 5: Desktop Agent Foundation ✅ COMPLETE

### Deliverables
- [x] desktop_agent folder structure with src/ layout
- [x] requirements.txt (PySide6, httpx, mss, Pillow)
- [x] Configuration module
- [x] Token manager (JSON persistence)
- [x] Backend API client (httpx-based)
- [x] OAuth scaffolding
- [x] Image processor (JPG compression)
- [x] .env.example
- [x] verify.py

### Files
```
desktop_agent/
├── requirements.txt
├── .env.example
├── verify.py
└── src/
    └── app/
        ├── main.py
        ├── core/
        │   ├── config.py
        │   ├── api_client.py
        │   └── auth.py
        └── utils/
            ├── token_manager.py
            └── image_processor.py
```

### Portable EXE Architecture
- Single executable (PyInstaller)
- No installer, no auto-start
- Outbound HTTPS only
- Token storage in ~/.clock_agent/

### Verification
```bash
cd desktop_agent && python verify.py
```

**Results:** 6/6 test groups passed
```
✅ File Structure (8/8 files)
✅ Configuration (BACKEND_URL, SHARED_TOKEN, HEARTBEAT_INTERVAL, SCREENSHOT_INTERVAL, MAX_WIDTH, JPEG_QUALITY)
✅ Token Manager (save_token, load_token, clear_token, has_token, get_token_path)
✅ Image Processor (process, get_image_info)
✅ Backend API Client (send_heartbeat, check_health, upload_screenshot, get_user_status)
✅ OAuth Authentication (OAuthHandler, start_login, wait_for_callback, exchange_code_for_token, complete_login)
```

---

## Phase 6: (NOT STARTED)

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
| fedf981 | Phase 5 | Desktop Agent Foundation |
| ceb71a1 | Phase 4 | COMMAND_MAP fix, clean ROADMAP |
| c4977b1 | Phase 4 | Command behavior, health validation |
| a7a9900 | Phase 3 | verify.py, clean ROADMAP |
| a66061c | Phase 3 | Unified clock router |
| 28de2b4 | Phase 2 | API verification, docs |
| e1c4848 | Phase 2 | FastAPI routers, schemas |
| 0274548 | Phase 1 | Database, services |
