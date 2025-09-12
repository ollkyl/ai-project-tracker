from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True)

    projects = relationship("Project", back_populates="user")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    status = Column(String, default="todo")
    progress = Column(Integer, default=0)
    project_id = Column(Integer, ForeignKey("projects.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.utc))
    updated_at = Column(
        DateTime, default=lambda: datetime.now(pytz.utc), onupdate=lambda: datetime.now(pytz.utc)
    )

    project = relationship("Project", back_populates="tasks")
