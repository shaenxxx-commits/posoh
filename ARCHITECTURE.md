# Архитектура Sub-0

## Железо
- Android: тонкий клиент. Только Telegram app.
- Ubuntu (nova): сервер. Весь мозг, все файлы.

## Хранение (3 слоя)
| Файл | Назначение | Режим |
|------|-----------|-------|
| `stream.md` | Сырой поток. Все входящие. | Append-only |
| `buffer.md` | Структурированные факты. | Append-only |
| `meta.md` | Мозг. Паттерны, инсайты, профиль. | Перезаписываемый |
| `media/` | Фото. Папки `YYYY-MM-DD/`. | Только запись |

Формат `buffer.md`: `[YYYY-MM-DD HH:MM] [CATEGORY] [FACT]`

## Скрипты
- `bot.py` — Telegram-бот. Принимает входящее, пишет в `stream.md`.
- `reflex.py` — дневной cron. Читает `stream.md` → обновляет `buffer.md` и `meta.md`.

## Цикл агента
1. **INGEST** — бот получает данные → `stream.md`
2. **REFLECT** — cron анализирует → `buffer.md` + `meta.md`
3. **ACT** — критический флаг в `meta.md` → push в Telegram

## Стек
- python-telegram-bot
- APScheduler (cron)
- OpenRouter API (или локальная модель через Ollama)
- plain markdown, без БД

## Локальная структура (nova)
