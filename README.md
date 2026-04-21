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

# Start server
uvicorn app.main:app --reload
```

Backend runs at http://localhost:8000

## Project Structure

```
├── backend/          # FastAPI + SQLite
├── discord_bot/      # discord.py (Phase 3+)
└── desktop_agent/    # PySide6 + PyInstaller (Phase 5+)
```

## Configuration

Copy `.env.example` to `.env` and set:
- `SHARED_TOKEN` - Secret token for bot/agent auth
- `DATABASE_URL` - SQLite database path

## Documentation

See [ROADMAP.md](ROADMAP.md) for full project plan.
