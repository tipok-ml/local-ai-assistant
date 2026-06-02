# local-ai-assistant
Локальный AI-стек на базе Ollama + Open WebUI + Telegram-бот для приватного доступа к LLM.

# 🤖 Локальный AI-ассистент с веб-интерфейсом и Telegram-ботом

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)

Полностью приватный стек для запуска языковых моделей (LLM) на собственном железе.  
Включает **Ollama**, **Open WebUI** (аналог ChatGPT) и **Telegram-бота** для доступа с мобильных устройств.  
Веб-поиск через DuckDuckGo (внешний API).

🚀 **Особенности**
- Работа с моделями 7B–14B (например, `qwen3.5:9b-q4_K_M` или `llama3.1:8b`)
- Полная приватность – все данные остаются на вашем ПК
- Офлайн‑доступ после загрузки моделей
- Высокая скорость генерации (60+ токенов/с на RTX 3060 Ti)
- Веб-интерфейс с историей чатов и поддержкой документов
- Telegram-бот с сохранением контекста диалога
- Встроенный веб-поиск (DuckDuckGo) для актуальной информации

## 📋 Предварительные требования

- **Операционная система**: Ubuntu 24.04 / Kali Linux (или любой дистрибутив с поддержкой NVIDIA)
- **Видеокарта**: NVIDIA с 8+ ГБ VRAM (рекомендуется RTX 3060 Ti или лучше)
- **Драйверы NVIDIA**: версия 550+ (для CUDA 12)
- **Docker и Docker Compose** (для Open WebUI)
- **Python 3.13+** (для бота и поискового API)

## 🛠️ Установка

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/tipok-ml/-AI----Telegram--
cd -AI----Telegram--
```

### 2. Установите Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Чтобы Ollama слушал на всех интерфейсах (для доступа из Docker), добавьте в systemd:
```bash
sudo mkdir -p /etc/systemd/system/ollama.service.d
sudo tee /etc/systemd/system/ollama.service.d/override.conf > /dev/null <<EOF
[Service]
Environment="OLLAMA_HOST=0.0.0.0"
EOF
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

### 3. Загрузите модель
```bash
ollama pull qwen3.5:9b-q4_K_M    # или другую модель, например llama3.1:8b
```
Проверьте, что модель видна:
```bash
ollama list
```

### 4. Установите Python-зависимости
Рекомендуется создать виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Запустите Open WebUI (веб-интерфейс)
Используйте `docker-compose.yml`:
```bash
docker-compose up -d
```
После запуска откройте браузер по адресу `http://localhost:8080` и зарегистрируйтесь.  
В настройках (Admin Panel → Settings → Connections) укажите `Ollama Base URL = http://host.docker.internal:11434` (или `http://localhost:11434`).

### 6. Запустите сервер веб-поиска
В отдельном терминале (активируйте виртуальное окружение):
```bash
python search_api.py
```
Сервер запустится на порту 8000.  
В Open WebUI включите веб-поиск (Admin Panel → Settings → Web Search) и выберите `external`.  
Укажите URL: `http://localhost:8000/search` и API Key: `your_secret_token_here` (измените в коде `search_api.py`).

### 7. Запустите Telegram-бота
Установите переменную окружения с токеном вашего бота (получите у @BotFather):
```bash
export TELEGRAM_TOKEN="ваш_токен"
```
Затем запустите:
```bash
python telegram_bot.py
```
Бот поддерживает историю диалогов (память на сессию).

## 🧠 Использование

- **Веб-интерфейс**: http://localhost:8080 – полноценный чат с выбором модели, загрузкой файлов, веб-поиском.
- **Telegram-бот**: общайтесь с нейросетью с телефона или другого устройства. Бот отвечает в реальном времени и помнит контекст в рамках текущей сессии.

## 🔧 Настройка и кастомизация

- **Смена модели**: в файлах `telegram_bot.py` и `search_api.py` измените значение `MODEL_NAME`.
- **Секретные ключи**: не публикуйте реальные токены. Используйте переменные окружения или храните ключи в отдельном неверсионируемом файле.
- **Параметры генерации**: в `telegram_bot.py` можно изменить `temperature`, `num_predict` и другие опции.

## 📊 Производительность (на RTX 3060 Ti 8GB)

| Модель                     | Скорость (токен/с) | VRAM  |
|----------------------------|--------------------|-------|
| qwen3.5:9b-q4_K_M          | ~60                | ~6.6ГБ|
| llama3.1:8b (Q4_K_M)       | ~55                | ~4.9ГБ|
| deepseek-r1:14b (Q4_K_M)   | ~15-20 (CPU+GPU)   | ~9ГБ  |

Модель полностью помещается в VRAM (кроме 14B), процессор практически не загружается.  
Веб-поиск добавляет небольшую нагрузку на CPU.

## 🛡️ Безопасность и приватность

- Все данные (логи, диалоги) остаются на вашем компьютере.
- Нет отправки телеметрии в облака.
- Вы можете работать с чувствительными логами, эксплойтами и уязвимостями без риска утечки.
- Подробнее в [WHY_LOCAL_AI.md](./WHY_LOCAL_AI.md).

## 🤝 Как внести вклад

Приветствуются pull requests и создание issues.  
Если вы нашли ошибку или хотите улучшить документацию – пишите!

## 📄 Лицензия

Проект распространяется под лицензией MIT – см. файл [LICENSE](./LICENSE).

## 🙏 Благодарности

- [Ollama](https://ollama.com/) – бэкенд для запуска моделей
- [Open WebUI](https://github.com/open-webui/open-webui) – веб-интерфейс
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) – библиотека для Telegram
- [DuckDuckGo Search](https://duckduckgo.com/) – источник для веб-поиска

## 📬 Контакты

Автор: [tipok-ml](https://github.com/tipok-ml)  
По вопросам и предложениям – создавайте issue в этом репозитории.


⭐ Если проект оказался полезным, поставьте звезду на GitHub!
