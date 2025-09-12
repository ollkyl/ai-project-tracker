import httpx
import os
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


async def register_user(name: str, email: str, telegram_id: int):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.post(
            f"{BASE_URL}/users", json={"name": name, "email": email, "telegram_id": telegram_id}
        )
        resp.raise_for_status()
        return resp.json()


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
