import httpx
import os
from dotenv import load_dotenv
import logging

load_dotenv()
BASE_URL = os.getenv("BACKEND_URL_FOR_BOT")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def register_user(name: str, email: str, telegram_id: int):
    logger.info(
        f"Attempting to register user: name={name}, email={email}, telegram_id={telegram_id}"
    )
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            resp = await client.post(
                f"{BASE_URL}/users", json={"name": name, "email": email, "telegram_id": telegram_id}
            )
            resp.raise_for_status()
            logger.info(f"User registered successfully: {resp.json()}")
            return resp.json()
        except httpx.HTTPStatusError as e:
            logger.error(
                f"HTTP error during registration: {e.response.status_code} - {e.response.text}"
            )
            raise
        except Exception as e:
            logger.error(f"Unexpected error during registration: {str(e)}")
            raise


async def get_projects(user_id: int):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(f"{BASE_URL}/projects", params={"user_id": user_id})
        resp.raise_for_status()
        return resp.json()


async def create_idea(user_id: int, text: str):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.post(f"{BASE_URL}/ideas", params={"user_id": user_id, "text": text})
        resp.raise_for_status()
        return resp.json()


async def update_task(task_id: int, status: str, progress: int = 0):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.patch(
            f"{BASE_URL}/tasks/{task_id}", json={"status": status, "progress": progress}
        )
        resp.raise_for_status()
        return resp.json()


async def get_report(user_id: int):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(f"{BASE_URL}/report", params={"user_id": user_id})
        resp.raise_for_status()
        return resp.json()


async def get_task(task_id: int):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(f"{BASE_URL}/tasks/{task_id}")
        resp.raise_for_status()
        return resp.json()


async def get_all_users():
    logger.info("Fetching all users")
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            resp = await client.get(f"{BASE_URL}/users")
            resp.raise_for_status()
            logger.info("Users fetched successfully")
            return resp.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching users: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching users: {str(e)}")
            raise


async def get_general_advice(user_id: int):
    logger.info(f"Fetching general advice for user_id={user_id}")
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            resp = await client.get(f"{BASE_URL}/scheduler_advice", params={"user_id": user_id})
            resp.raise_for_status()
            logger.info("General advice fetched successfully")
            return resp.json()
        except httpx.HTTPStatusError as e:
            logger.error(
                f"HTTP error fetching general advice: {e.response.status_code} - {e.response.text}"
            )
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching general advice: {str(e)}")
            raise
