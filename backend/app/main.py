from fastapi import FastAPI
from backend.app.core.config import settings
from backend.app.db.session import engine, Base, init_db
from backend.app.api import users, projects, tasks, ideas, reports
from fastapi.middleware.cors import CORSMiddleware

init_db()

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
Base.metadata.create_all(bind=engine)
