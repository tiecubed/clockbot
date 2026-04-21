# Discord Time Tracker - Development Roadmap

**Project:** Virtual Assistant Time Tracking System  
**Repository:** https://github.com/tiecubed/clockbot  
**Status:** Phase 3 Complete ✅

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

### Files
```
backend/
├── requirements.txt
├── verify.py
├── test_api.py
├── .env.example
└── app/
    ├── config.py
    ├── database.py
    ├── dependencies.py
    ├── main.py
    ├── models/
    └── services/
```

### Verification
```bash
cd backend && python verify.py
```

**Results:**
```
Testing Dependencies: ✅ (FastAPI, SQLAlchemy, PIL/Pillow, Pydantic Settings)
Testing App Modules: ✅ 9/9 passed
Config Values: HEALTH_THRESHOLD_SECONDS=90, SCREENSHOT_QUALITY=70
```

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
| GET | `/api/v1/screenshots/session/{id}` | Get session screenshots |
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
```
Testing Router Imports: ✅ 6/6 passed
FastAPI App Creation: ✅ App created, 5/5 routes registered
API Smoke Test: ✅ 3/3 passed
  - GET /health
  - GET /api/v1/agents/{id}/health (returns threshold=90s, healthy=False)
  - GET /api/v1/sessions/active/{id} (returns 404)
```

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
- [x] verify.py import tests

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

### Commands Implemented

**User Commands:**
- `!clock in` - Start session (requires healthy agent)
- `!clock out` - End session
- `!clock pay` - Show unpaid time & earnings
- `!clock help` - Command help

**Admin Commands:**
- `!clock hourlyrate @user 15` - Set hourly rate
- `!clock addtime 30 @user` - Add minutes
- `!clock removetime 30 @user` - Remove minutes
- `!clock day @user` - Today's summary
- `!clock week @user` - Last 7 days summary
- `!clock who` - Currently clocked in users
- `!clock status @user` - User status
- `!clock clear` - Mark all as paid

### Verification
```bash
cd discord_bot && pip install -r requirements.txt
cd discord_bot/src && python verify.py
```

**Results:**
```
✅ main.py imports
✅ bot.config.config
✅ bot.core.api_client.BackendAPIClient
✅ bot.core.checks.ClockChecks
✅ bot.commands.router.ClockCommandRouter
✅ bot.commands.user.UserCommandHandler
✅ bot.commands.admin.AdminCommandHandler
✅ bot.services.formatter.EmbedFormatter
Results: 8/8 passed
```

### Architecture Highlights
1. **Unified Command System**: Single `!clock` command registered, routes via ClockCommandRouter
2. **Health Validation**: `!clock in` validates agent health (90s rule) before session start
3. **Permission Decorators**: Role/channel checks via @ClockChecks decorators
4. **Async API Client**: httpx-based backend communication
5. **Rich Embeds**: Formatted Discord embeds for pay summaries, time reports, help

---

## Phase 4: (NOT STARTED)

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
SHARED_TOKEN=your_secret_token
API_BASE_URL=http://localhost:8000
CLOCK_ROLE_ID=1324268726819754055
ADMIN_ROLE_ID=1298219350817505354
INOUT_CHANNEL_ID=1495997857180684410
```

---

## Running the Project

### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your tokens
cd app && uvicorn main:app --reload --port 8000
```

### Discord Bot
```bash
cd discord_bot
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your tokens
cd src && python main.py
```

---

## Git Commit History

| Commit | Phase | Description |
|--------|-------|-------------|
| a66061c | Phase 3 | Discord bot with unified router, API client, permissions |
| 28de2b4 | Phase 2 | API verification scripts, README docs |
| e1c4848 | Phase 2 | FastAPI routers, schemas, endpoints |
| 9b0370a | Phase 1 | Verification script, README, .env.example |
| 0274548 | Phase 1 | Database schema, health service, image service |
