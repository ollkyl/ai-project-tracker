# AI Project Tracker

MVP-продукт для трекинга AI-проектов: Telegram-бот, веб-панель администратора и интеграция с AI [(Google Gemini)](https://aistudio.google.com/apikey).

## Структура проекта

```
ai-project-tracker/
├── backend/      # FastAPI backend
├── bot/          # Telegram-бот (aiogram)
├── web/          # Веб-панель (Next.js/React)
```

## Настройка окружения

(`backend/.env`)(`bot/.env`)
```
DATABASE_URL=postgresql+psycopg://postgres:1234@db:5432/trackerdb
TELEGRAM_BOT_TOKEN=ВАШ_ТОКЕН_БОТА
GEMINI_API_KEY=ВАШ_КЛЮЧ_GEMINI_API
GEMINI_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent
LOG_LEVEL=INFO
BACKEND_URL=http://127.0.0.1:8000
BACKEND_URL_FOR_BOT=http://backend:8000

```



### Web (`web/my-admin-panel/.env.local`)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Запуск с Docker Compose

```
docker-compose up --build
```

После запуска:
- Frontend: http://localhost:3000/


Возможности:
- CRUD пользователей, проектов и задач
- Отметка выполнения задач
- AI-Review проектов

## Telegram-бот

- `/start` — регистрация (имя + email)
- `/idea [идея]` — создать проект (roadmap от AI)
- `/projects` — список проектов
- `/update [проект] [задача]` — обновить статус задачи
- `/report [проект]` — отчёт (AI-анализ)
- `/help` — инструкция

## Планировщик задач

- Каждый день в 09:00:
```
scheduler.add_job(send_status_updates, trigger="cron", hour=9, minute=0, args=[bot])
```
- Для теста каждые 10 минут:
```
scheduler.add_job(send_status_updates, trigger="interval", minutes=10, args=[bot])
```




<img width="222" height="275" alt="image" src="https://github.com/user-attachments/assets/87bc6807-f30e-40fe-b3cd-62dc3cce4110" />
<img width="222" height="312" alt="image" src="https://github.com/user-attachments/assets/c55da80d-1db3-4ce8-b412-8db7c06f5e11" />
<img width="217" height="303" alt="image" src="https://github.com/user-attachments/assets/4ccf9929-1107-47dd-8a44-c18ef0a8a07b" />
<img width="629" height="281" alt="image" src="https://github.com/user-attachments/assets/bdc9f510-471f-4c01-9528-7fb385b8fac0" />
<img width="629" height="281" alt="image" src="https://github.com/user-attachments/assets/d6172190-71b3-4def-8352-d6fb89520393" />
<img width="625" height="280" alt="image" src="https://github.com/user-attachments/assets/f9c14f2a-1384-4806-8903-23cbb4fce122" />

