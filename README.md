# AI Project Tracker

AI Project Tracker is a comprehensive solution for managing AI projects with a Telegram bot interface, web dashboard, and backend API.

## Project Structure

```
ai-project-tracker/
├── backend/                # FastAPI + SQLAlchemy
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Configuration and logging
│   │   ├── db/             # Database models and session
│   │   ├── services/       # AI integration and business logic
│   │   ├── schemas/        # Pydantic schemas
│   │   └── main.py         # Application entry point
│   ├── alembic/            # Database migrations
│   └── requirements.txt    
│
├── bot/                    # Telegram bot
│   ├── handlers/           # Command handlers (/start, /idea, /projects, /update, /report)
│   ├── services/           # Backend and AI service calls
│   └── bot.py              # Bot startup script
│
├── web/                    # Next.js application
│   ├── app/                # Pages
│   ├── components/         # UI components
│   └── package.json        
│
├── docker-compose.yml      # Orchestration
└── README.md               # This file
```

## Getting Started

1. Clone the repository
2. Install dependencies for each component:
   - Backend: `pip install -r backend/requirements.txt`
   - Web: `cd web && npm install`
3. Configure environment variables
4. Run with Docker: `docker-compose up`

## Components

### Backend (FastAPI + SQLAlchemy)
REST API for managing projects, ideas, and reports.

### Bot (Telegram)
Telegram bot interface for interacting with the system.

### Web (Next.js)
Web dashboard for visualizing project data.

## Deployment

Use the provided `docker-compose.yml` for easy deployment.