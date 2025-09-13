# AI Project Tracker

MVP-продукт для трекинга AI-проектов: Telegram-бот, веб-панель администратора и интеграция с AI (Google Gemini).

---

## Структура проекта

```
ai-project-tracker/
├── backend/      # FastAPI backend
├── bot/          # Telegram-бот (aiogram)
├── web/          # Веб-панель (Next.js/React)

```

---

## Запуск через Docker 

Настройка
Создайте файл .env в директории /backend и /bot.

Получите токен для Telegram-бота у @BotFather.

Получите ключ для Google Gemini API в Google AI Studio.

Заполните .env следующими переменными:

DATABASE_URL=postgresql+psycopg://postgres:737372@localhost:5432/trackerdb
TELEGRAM_BOT_TOKEN=ВАШ_ТОКЕН_БОТА
GEMINI_API_KEY=ВАШ_КЛЮЧ_GEMINI_API
GEMINI_API_URL=[https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent](https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent)
BACKEND_URL=[http://127.0.0.1:8000](http://127.0.0.1:8000)


---

### 3. `web/my-admin-panel/.env.local`

**Путь:**  
`ai-project-tracker/web/my-admin-panel/.env.local`

**Пример содержимого:**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```


## Основные команды Telegram-бота

- `/start` — регистрация пользователя (имя + email)
- `/idea [ваша идея]` — создать проект
- `/projects` — список идей/проектов пользователя
- `/update [номер проекта] [номер задачи]` — отметить задачу как выполненную
- `/report [номер проекта]` — отчёт по проекту (AI-анализ)
- `/help` — инструкция

---

## Веб-панель

- Таблица пользователей и их проектов
- Возможность отмечать задачи как выполненные
- Кнопка «AI Review» — анализ прогресса проекта через AI

---

## Примечания
- Ежедневный отчет в /bot/handlers/scheduler.py 
scheduler.add_job(send_status_updates, trigger="cron", hour=9, minute=0, args=[bot]) каждый день в 9 утра
Для тестирования каждые 10 минут:
scheduler.add_job(send_status_updates, trigger="interval", minutes=10, args=[bot]) 
- Для работы AI-интеграции нужен валидный ключ Google Gemini API.
- Для работы с БД используется PostgreSQL (настраивается в `.env` и `docker-compose.yml`).


<img width="222" height="275" alt="image" src="https://github.com/user-attachments/assets/a7f09ba4-42eb-4fa5-9adc-fe8196e60044" />
<img width="222" height="312" alt="image" src="https://github.com/user-attachments/assets/a7c85458-a2db-4824-ae45-2e05425b9d50" />
<img width="217" height="303" alt="image" src="https://github.com/user-attachments/assets/ff0eb79a-5ddc-46ac-80e7-2720e61c01a3" />
<img width="629" height="281" alt="image" src="https://github.com/user-attachments/assets/d250ac4f-19e2-44d0-a49f-46816451e023" />
<img width="629" height="281" alt="image" src="https://github.com/user-attachments/assets/be19627f-25f0-4ba1-9bb1-85dd73c8f7c0" />
<img width="625" height="280" alt="image" src="https://github.com/user-attachments/assets/0e2b7757-de89-4373-9c99-633dc50b860d" />
