# Discord Time Tracker - Development Roadmap

**Project:** Virtual Assistant Time Tracking System
**Status:** Phase 1 Complete

## Phase Verification Checkpoints

After EACH phase, verify before proceeding:
- [ ] All new files created and in correct locations
- [ ] Imports work without errors
- [ ] Integration with previous phases works
- [ ] Documentation updated
- [ ] Git commit with descriptive message

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

### Verification Checklist
- [x] All models import correctly
- [x] All services import correctly
- [x] Config values correct (HEALTH_THRESHOLD_SECONDS=90)

### Files Created
```
backend/
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── session.py
│   │   ├── screenshot.py
│   │   ├── manual_adjustment.py
│   │   └── agent_status.py
│   ├── routers/
│   │   └── __init__.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── health_service.py
│   │   ├── image_service.py
│   │   ├── time_service.py
│   │   └── pay_service.py
│   └── utils/
```

## Next Phases

### Phase 2: Backend API
- [ ] FastAPI routers (agents, sessions, screenshots, users, payroll)
- [ ] Pydantic request/response models
- [ ] Error handling middleware

### Phase 3: Discord Bot Architecture
- [ ] Unified command router
- [ ] Permission decorators
- [ ] API client

### Phase 4: Discord Bot Commands
- [ ] User commands (in, out, pay, help)
- [ ] Admin commands

### Phase 5: Desktop Agent Foundation
- [ ] Project structure, config, token manager

### Phase 6: Desktop Agent GUI
- [ ] PySide6 GUI, system tray, status display

### Phase 7: Desktop Agent Core Services
- [ ] OAuth, heartbeat, screenshots

### Phase 8: Integration Testing
- [ ] End-to-end testing

### Phase 9: Build & Deployment
- [ ] PyInstaller EXE, Docker Compose

### Phase 10: Polish & Security
- [ ] Logging, error handling, documentation
