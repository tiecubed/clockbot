# Discord Time Tracker - Development Roadmap

**Project:** Virtual Assistant Time Tracking System  
**Repository:** https://github.com/tiecubed/clockbot  
**Status:** Phase 4 Complete ✅

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
- [x] SQLite database schema (5 models: User, Session, Screenshot, ManualAdjustment, AgentStatus)
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
- ✅ FastAPI, SQLAlchemy, PIL/Pillow, Pydantic Settings
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
| POST | `/api/v1/screenshots/upload` | Upload screenshot (JPG conversion) |
| GET | `/api/v1/screenshots/session/{id}` | Get screenshots |
| GET | `/api/v1/users/{id}/time/today` | Today's hours |
| GET | `/api/v1/users/{id}/time/week` | Last 7 days hours |
| GET | `/api/v1/users/{id}/pay/unpaid` | Unpaid time & amount |
| GET | `/api/v1/users/{id}/status` | Clock in/out status |
| POST | `/api/v1/users/{id}/hourlyrate` | Set hourly rate |
| GET | `/api/v1/payroll/unpaid` | All unpaid payroll |
| POST | `/api/v1/payroll/clear` | Mark all as paid |
| GET | `/api/v1/payroll/active` | Currently clocked in users |
| POST | `/api/v1/payroll/adjustments` | Add manual time adjustment |

### Verification
```bash
cd backend && python verify.py
cd backend && python test_api.py
```

**Results:**
- ✅ Router Imports: 6/6 passed
- ✅ FastAPI App: 5/5 routes registered
- ✅ API Smoke Test: 3/3 passed (health, agents/health, sessions/active)

---

## Phase 3: Discord Bot Architecture ✅ COMPLETE

### Deliverables
- [x] discord_bot folder structure with src/ layout
- [x] Bot main entry point (main.py) with unified !clock command
- [x] Unified command router/parser (commands/router.py)
- [x] Backend API client (httpx-based async wrapper)
- [x] Permission checks (role/channel validators)
- [x] Discord embed formatter service
- [x] .env.example configuration template

### Files
```
discord_bot/
├── requirements.txt
├── .env.example
├── verify.py
└── src/
    ├── main.py
    └── bot/
        ├── config.py
        ├── core/
        │   ├── api_client.py
        │   └── checks.py
        ├── commands/
        │   ├── router.py
        │   ├── user.py
        │   └── admin.py
        └── services/
            └── formatter.py
```

### Verification
```bash
cd discord_bot && pip install -r requirements.txt
cd discord_bot && python verify.py
```

**Results:** 6/11 test groups passed (5 require discord.py)
- ✅ File structure complete (8/8 files)
- ✅ Config loading (DISCORD_TOKEN, SHARED_TOKEN, API_BASE_URL)
- ✅ API Client (13 methods, Bearer auth)

---

## Phase 4: Discord Bot Command Behavior ✅ COMPLETE

### Deliverables
- [x] All user commands working (!clock in, out, pay, help)
- [x] All admin commands working (!clock hourlyrate, addtime, removetime, day, week, who, status, clear)
- [x] Agent health validation before clock in (90s rule)
- [x] Role/channel/admin checks enforced
- [x] Embed formatter used for responses
- [x] Backend API client integration
- [x] Command handler verification with discord.py installed

### Command Implementation Status

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

### Not Implemented
- !clock setchannel - Placeholder only (not part of Phase 4 scope)

### Verification
```bash
cd discord_bot && pip install -r requirements.txt
cd discord_bot && python verify.py
```

**Results:** 8/8 test groups passed
```
✅ Phase 3 Baseline (File Structure)
✅ Configuration Loading (DISCORD_TOKEN, SHARED_TOKEN, API_BASE_URL)
✅ Backend API Client (13 methods verified, Bearer auth)
✅ Permission Checks (in_clock_channel, has_clock_role, has_admin_role, is_admin)
✅ Unified Command Router (route method, USER_COMMANDS, ADMIN_COMMANDS)
✅ User Command Handler (in_, out, pay, show_help with health validation)
✅ Admin Command Handler (hourlyrate, addtime, removetime, day, week, who, status, clear, setchannel)
✅ Formatter Service (5 embed methods)
```

---

## Phase 5: (NOT STARTED)

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
SCREENSHOT_CHANNEL_ID=1407132078121816156
```

---

## Running the Project

### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env
uvicorn app.main:app --reload --port 8000
```

### Discord Bot
```bash
cd discord_bot
pip install -r requirements.txt
cp .env.example .env
# Edit .env
cd src && python main.py
```

---

## Git Commit History

| Commit | Phase | Description |
|--------|-------|-------------|
| c4977b1 | Phase 4 | Command behavior, health validation, embeds |
| a7a9900 | Phase 3 | Unified router, API client, permissions |
| 28de2b4 | Phase 2 | API verification, docs |
| e1c4848 | Phase 2 | FastAPI routers, schemas |
| 9b0370a | Phase 1 | Verification, README |
| 0274548 | Phase 1 | Database, services |
