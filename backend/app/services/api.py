import httpx
import os

API_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


async def register_user(name, email, telegram_id):
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{API_URL}/users/", json={"name": name, "email": email, "telegram_id": telegram_id}
        )
        return r.json()


async def create_idea(user_id, text):
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{API_URL}/projects/", json={"user_id": user_id, "title": text})
        return r.json()


async def get_projects(user_id):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{API_URL}/projects/{user_id}")
        return r.json()


async def update_task(task_id, status):
    async with httpx.AsyncClient() as client:
        r = await client.put(f"{API_URL}/tasks/{task_id}", json={"status": status})
        return r.status_code == 200


async def get_report(user_id):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{API_URL}/report/{user_id}")
        return r.json()
