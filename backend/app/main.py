from fastapi import FastAPI
from app.core.config import settings
from app.db.session import engine, Base
from app.api import users, projects, tasks, ideas, reports
from fastapi.middleware.cors import CORSMiddleware

# This file has been updated. The database initialization logic has been
# removed from here and moved to a separate script to be executed by Docker Compose.
# This avoids a race condition and ensures the database tables exist before the
# application starts.

app = FastAPI(title="AI Project Tracker")

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(ideas.router, prefix="/ideas", tags=["Ideas"])
app.include_router(reports.router, prefix="/report", tags=["Reports"])


@app.get("/")
def root():
    return {"message": "AI Project Tracker backend is running!"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
