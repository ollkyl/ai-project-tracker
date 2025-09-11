from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from backend.app.db import models
from backend.app.db.session import get_db
from backend.app.schemas.user import UserCreate, UserOut
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        logger.info(
            f"Attempting to create user: email={user.email}, telegram_id={user.telegram_id}"
        )
        db_user = db.query(models.User).filter(models.User.email == user.email).first()
        if db_user:
            logger.warning(f"Email already registered: {user.email}")
            raise HTTPException(status_code=400, detail="Email already registered")

        db_user = db.query(models.User).filter(models.User.telegram_id == user.telegram_id).first()
        if db_user:
            logger.warning(f"Telegram ID already registered: {user.telegram_id}")
            raise HTTPException(status_code=400, detail="Telegram ID already registered")

        new_user = models.User(name=user.name, email=user.email, telegram_id=user.telegram_id)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f"User created successfully: {user.email}")
        return new_user
    except IntegrityError as e:
        logger.error(f"Integrity error while creating user: {str(e)}")
        raise HTTPException(
            status_code=400, detail="Database integrity error: email or telegram_id already exists"
        )
    except Exception as e:
        logger.error(f"Unexpected error while creating user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    try:
        users = db.query(models.User).all()
        logger.info("Fetched all users")
        return users
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")
