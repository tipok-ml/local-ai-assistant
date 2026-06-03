#!/bin/bash
set -e

echo "🚀 Установка локального AI-ассистента..."

# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
sudo apt install -y docker.io
sudo systemctl enable docker --now
sudo usermod -aG docker $USER

# Установка Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Установка Python и зависимостей
sudo apt install -y python3 python3-pip python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Загрузка модели (пример: Qwen3.5 9B)
ollama pull qwen3.5:9b-q4_K_M

# Запуск Open WebUI
docker run -d -p 8080:8080 --network host -v open-webui:/app/backend/data --name open-webui ghcr.io/open-webui/open-webui:main

echo "✅ Установка завершена."
echo "Запустите Telegram-бота: python telegram_bot.py"
echo "Запустите веб-поиск: python search_api.py &"
echo "Откройте Open WebUI: http://localhost:8080"
