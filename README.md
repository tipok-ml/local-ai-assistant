# -AI----Telegram--
Локальный AI-стек на базе Ollama + Open WebUI + Telegram-бот для приватного доступа к LLM.
# tipok-ml — локальный AI-ассистент с веб-интерфейсом и Telegram-ботом

Полностью приватный стек для запуска языковых моделей на собственном железе (NVIDIA RTX 3060 Ti). Включает:

- **Ollama** — сервер для LLM (поддержка GPU)
- **Open WebUI** — веб-интерфейс как у ChatGPT
- **Telegram-бот** — доступ к нейросети с телефона
- **Веб-поиск** через DuckDuckGo (внешний API)

## 🚀 Возможности
- Работа с моделями 7B–14B (Q4_K_M)
- Полная приватность – все данные на вашем ПК
- Офлайн-доступ (после загрузки моделей)
- Гибкая настройка (смена моделей, параметров генерации)

## 🛠️ Технологии
- Ubuntu 24.04 / Kali Linux
- Docker (Open WebUI)
- Python (FastAPI, telegram-bot)
- Nvidia CUDA / GPU

## 📦 Установка (кратко)
1. Установите Ollama: `curl -fsSL https://ollama.com/install.sh | sh`
2. Скачайте модель: `ollama pull qwen3.5:9b-q4_K_M`
3. Запустите контейнер Open WebUI: `docker run -d -p 8080:8080 -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:main`
4. Настройте Telegram-бота (см. `telegram_bot.py`)

## 📁 Структура репозитория
- `telegram_bot.py` – бот для Telegram
- `search_api.py` – сервер для веб-поиска
- `Modelfile` – пример для импорта GGUF-модели
- `docker-compose.yml` (опционально)

## 🔧 Настройка
Подробные инструкции – в Wiki (или отдельном файле). Кратко:
- Для доступа к Ollama из контейнера используйте `http://host.docker.internal:11434`
- Для веб-поиска запустите `python search_api.py` и укажите в Open WebUI внешний API.

## 📜 Лицензия
MIT

## 🙏 Благодарности
- Ollama, Open WebUI, сообщество Hugging Face.
