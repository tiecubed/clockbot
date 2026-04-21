# Discord Time Tracker - Development Roadmap

**Project:** Virtual Assistant Time Tracking System  
**Status:** Phase 2 Complete

---

## Phase Verification Checkpoints

After EACH phase, verify before proceeding:
- [ ] All new files created and in correct locations
- [ ] Imports work without errors
- [ ] Integration with previous phases works
- [ ] Documentation updated
- [ ] Git commit with descriptive message

---

## Phase 1: Backend Foundation ✅ COMPLETE

### Deliverables
- [x] SQLite database schema (5 models)
- [x] FastAPI application structure
- [x] Health service (90-second heartbeat threshold)
- [x] Image service (JPG compression, quality 70, max 1920px)
- [x] Time service (session calculations)
- [x] Pay service (payroll logic)
- [x] Configuration (pydantic-settings)
- [x] Authentication dependency (shared token)

### Verification Results
```
Testing Dependencies:
  ✓ FastAPI, SQLAlchemy, PIL/Pillow, Pydantic Settings
Testing App Modules:
  ✓ app.config, app.database, app.dependencies, app.models, app.services
Results: 9 passed, 0 failed

Config Values:
  ✓ HEALTH_THRESHOLD_SECONDS = 90
  ✓ SCREENSHOT_QUALITY = 70
  ✓ SCREENSHOT_MAX_WIDTH = 1920

Verification: cd backend && python verify.py
```

### Verification Results

**Phase 1 Import Test:**
```
Testing Dependencies:
  ✓ FastAPI, SQLAlchemy, PIL/Pillow, Pydantic Settings
Testing App Modules:
  ✓ app.config, app.database, app.dependencies, app.models, app.services
Results: 9 passed, 0 failed

Config Values:
  ✓ HEALTH_THRESHOLD_SECONDS = 90
  ✓ SCREENSHOT_QUALITY = 70
  ✓ SCREENSHOT_MAX_WIDTH = 1920

Command: cd backend && python verify.py
```

**Phase 2 Router & API Test:**
```
Testing Router Imports:
  ✓ schemas, routers.agents, routers.sessions
  ✓ routers.screenshots, routers.users, routers.payroll
Results: 6 passed, 0 failed

FastAPI App Creation:
  ✓ App created successfully
  ✓ 5/5 expected API routes registered

API Smoke Test:
  ✓ GET /health - returns healthy
  ✓ GET /api/v1/agents/{id}/health - returns threshold=90s, healthy=False
  ✓ GET /api/v1/sessions/active/{id} - returns 404 (no session)
Results: 3 passed, 0 failed

Command: cd backend && python test_api.py
```

### Phase 2 Complete ✅
## Phase 2: Backend API ✅ COMPLETE

### Deliverables
- [x] **Routers/Endpoints:**
  - `POST /api/v1/agents/heartbeat` - Agent heartbeat
  - `GET /api/v1/agents/{user_id}/health` - Check health (90s rule)
  - `POST /api/v1/sessions/start` - Clock in (checks health)
  - `POST /api/v1/sessions/{id}/end` - Clock out
  - `GET /api/v1/sessions/active/{user_id}` - Get active session
  - `POST /api/v1/screenshots/upload` - Upload screenshots
  - `GET /api/v1/screenshots/session/{id}` - Get screenshots
  - `GET /api/v1/users/{id}/time/today` - Today's hours
  - `GET /api/v1/users/{id}/time/week` - Last 7 days hours
  - `GET /api/v1/users/{id}/pay/unpaid` - Unpaid summary
  - `GET /api/v1/users/{id}/status` - Clock status
  - `POST /api/v1/users/{id}/hourlyrate` - Set rate
  - `GET /api/v1/payroll/unpaid` - All unpaid
  - `POST /api/v1/payroll/clear` - Mark as paid
  - `GET /api/v1/payroll/active` - Active users
  - `POST /api/v1/payroll/adjustments` - Add manual time
- [x] Pydantic schemas (schemas.py)
- [x] Routers integrated in main.py

### Files Created
```
backend/app/
├── schemas.py              # Request/response models
└── routers/
    ├── agents.py           # Heartbeat, health check
    ├── sessions.py           # Clock in/out
    ├── screenshots.py        # Upload screenshots
    ├── users.py              # Time queries, hourly rate
    └── payroll.py            # Payroll, adjustments
```

### API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/agents/heartbeat | Agent heartbeat (30s) |
| GET | /api/v1/agents/{id}/health | Check health (90s rule) |
| POST | /api/v1/sessions/start | Clock in |
| POST | /api/v1/sessions/{id}/end | Clock out |
| POST | /api/v1/screenshots/upload | Upload screenshot |
| GET | /api/v1/users/{id}/time/today | Today's time |
| GET | /api/v1/users/{id}/time/week | Week's time |
| GET | /api/v1/users/{id}/pay/unpaid | Unpaid summary |
| POST | /api/v1/users/{id}/hourlyrate | Set hourly rate |
| GET | /api/v1/payroll/unpaid | All unpaid |
| POST | /api/v1/payroll/clear | Mark paid |
| GET | /api/v1/payroll/active | Clocked in users |

---

## Phase 3: Discord Bot Architecture ⏳ PENDING

### Deliverables
- [ ] Bot main entry point
- [ ] Unified command router (`!clock` dispatcher)
- [ ] Permission decorators (role/channel checks)
- [ ] API client wrapper for backend communication
- [ ] Event handlers (on_ready, on_error)

---

## Phase 4: Discord Bot Commands ⏳ PENDING

### User Commands
- [ ] `!clock in` - Start session
- [ ] `!clock out` - End session
- [ ] `!clock pay` - Show unpaid
- [ ] `!clock help` - Help

### Admin Commands
- [ ] `!clock hourlyrate @user 15`
- [ ] `!clock addtime 30 @user`
- [ ] `!clock removetime 30 @user`
- [ ] `!clock day @user`
- [ ] `!clock week @user`
- [ ] `!clock who`
- [ ] `!clock status @user`
- [ ] `!clock setchannel inout #channel`
- [ ] `!clock pay`
- [ ] `!clock clear`

---

## Phase 5: Desktop Agent - Foundation ⏳ PENDING
- [ ] Project structure, requirements
- [ ] Config module, token manager
- [ ] API client

---

## Phase 6: Desktop Agent - GUI ⏳ PENDING
- [ ] PySide6 main window
- [ ] System tray integration
- [ ] Exit confirmation dialog
- [ ] Status display

---

## Phase 7: Desktop Agent - Core Services ⏳ PENDING
- [ ] OAuth callback server
- [ ] Heartbeat service (30s)
- [ ] Screenshot service (5min)

---

## Phase 8: Integration Testing ⏳ PENDING
- [ ] End-to-end flow testing
- [ ] Error scenario testing

---

## Phase 9: Build & Deployment ⏳ PENDING
- [ ] PyInstaller EXE build
- [ ] Docker Compose

---

## Phase 10: Polish & Security ⏳ PENDING
- [ ] Logging, error handling
- [ ] Documentation

---

## Configuration

```bash
# Backend
SHARED_TOKEN=secure_token
DATABASE_URL=sqlite:///./data/timetracker.db
HEALTH_THRESHOLD_SECONDS=90
SCREENSHOT_QUALITY=70
SCREENSHOT_MAX_WIDTH=1920
```

## Quick Start

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

API runs at http://localhost:8000
