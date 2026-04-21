# Discord Time Tracker

Virtual assistant time tracking system with Discord bot, FastAPI backend, and Windows desktop agent.

## Quick Start

### Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your tokens
# SHARED_TOKEN=your_secret_here

# Start server
uvicorn app.main:app --reload --port 8000
```

Backend runs at http://localhost:8000

### Discord Bot

```bash
cd discord_bot

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your tokens:
# DISCORD_TOKEN=your_discord_bot_token
# SHARED_TOKEN=must_match_backend_token
# API_BASE_URL=http://localhost:8000

# Run verification
cd src && python verify.py

# Start bot
python main.py
```

## Project Structure

```
├── backend/          # FastAPI + SQLite (Phases 1-2 ✅)
├── discord_bot/      # discord.py (Phase 3 ✅)
└── desktop_agent/    # PySide6 + PyInstaller (Phase 5+)
```

## Configuration

### Backend (.env)
```
SHARED_TOKEN=your_secret_token_here
DATABASE_URL=sqlite:///data/timetracker.db
HEALTH_THRESHOLD_SECONDS=90
SCREENSHOT_QUALITY=70
SCREENSHOT_MAX_WIDTH=1920
```

### Discord Bot (.env)
```
DISCORD_TOKEN=your_discord_bot_token
SHARED_TOKEN=must_match_backend_token
API_BASE_URL=http://localhost:8000

# Role/Channel IDs (from your Discord server)
CLOCK_ROLE_ID=1324268726819754055
ADMIN_ROLE_ID=1298219350817505354
INOUT_CHANNEL_ID=1495997857180684410
SCREENSHOT_CHANNEL_ID=1407132078121816156
```

## Verification

### Phase 1-2: Backend
```bash
cd backend && python verify.py      # Import tests
cd backend && python test_api.py    # API smoke tests
```

### Phase 3: Discord Bot
```bash
cd discord_bot && pip install -r requirements.txt
cd discord_bot && python verify.py  # Structure and import tests
```

**Expected Phase 3 Results:**
```
✅ requirements.txt exists
✅ .env.example exists
✅ File structure complete (8/8 files)
✅ bot.config imports
✅ bot.core.api_client imports
✅ API client uses Bearer token format
Results: 6/11 passed (5 need discord.py installed)
```

## Documentation

See [ROADMAP.md](ROADMAP.md) for full project plan and phase details.

## Commands

**User Commands:**
- `!clock in` - Start work session (requires healthy desktop agent)
- `!clock out` - End work session
- `!clock pay` - View unpaid time and earnings
- `!clock help` - Show command help

**Admin Commands:**
- `!clock hourlyrate @user 15` - Set hourly rate
- `!clock addtime 30 @user` / `!clock removetime 30 @user` - Adjust time
- `!clock day @user` / `!clock week @user` - View time summaries
- `!clock who` - See currently clocked in users
- `!clock status @user` - Check user status
- `!clock clear` - Mark all as paid

## Development

**Running the full stack locally:**
```bash
# Terminal 1: Backend
cd backend && uvicorn app.main:app --reload --port 8000

# Terminal 2: Discord Bot
cd discord_bot/src && python main.py
```

## License

MIT
