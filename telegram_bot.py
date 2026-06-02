import asyncio
import aiohttp
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters

# ========== НАСТРОЙКИ ==========
# Токен бота (получите у @BotFather) – лучше через переменную окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "ВАШ_ТОКЕН_СЮДА")
# Адрес Ollama (локальный)
OLLAMA_URL = "http://localhost:11434/api/chat"
# Название модели (укажите ту, которую вы используете, например llama3.1:8b или qwen3.5:9b-q4_K_M)
MODEL_NAME = "qwen3.5:9b-q4_K_M"   # или "llama3.1:8b"
# Сколько последних сообщений хранить на пользователя (макс 10)
MAX_HISTORY_LEN = 10
# ================================

# Хранилище истории диалогов (в оперативной памяти, при перезапуске бота теряется)
history = {}

async def ollama_request(chat_id: int, user_message: str) -> str:
    """Отправляет запрос к Ollama, учитывая историю диалога."""
    chat_history = history.get(chat_id, [])
    # Берём последние MAX_HISTORY_LEN*2 сообщений (пользователь + ассистент)
    messages = chat_history[-(MAX_HISTORY_LEN*2):]
    messages.append({"role": "user", "content": user_message})

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
        "options": {
            "num_predict": 2048,
            "temperature": 0.7,
            "top_p": 0.9
        }
    }

    timeout = aiohttp.ClientTimeout(total=120)

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(OLLAMA_URL, json=payload) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    bot_reply = data.get('message', {}).get('content', 'Извините, я не могу ответить.')
                    # Сохраняем в историю
                    history.setdefault(chat_id, []).append({"role": "user", "content": user_message})
                    history.setdefault(chat_id, []).append({"role": "assistant", "content": bot_reply})
                    # Обрезаем историю, если она слишком длинная
                    if len(history[chat_id]) > MAX_HISTORY_LEN * 2 + 4:
                        history[chat_id] = history[chat_id][-(MAX_HISTORY_LEN * 2):]
                    return bot_reply
                else:
                    error_text = await resp.text()
                    return f"Ошибка API Ollama: {resp.status}\n{error_text[:300]}"
    except asyncio.TimeoutError:
        return "❌ Таймаут: модель слишком долго думает. Попробуйте упростить вопрос."
    except aiohttp.ClientError as e:
        return f"❌ Ошибка сети: {e}"
    except Exception as e:
        return f"❌ Неизвестная ошибка: {e}"

async def handle_message(update: Update, context):
    """Обработчик текстовых сообщений."""
    user_message = update.message.text
    chat_id = update.effective_chat.id
    await update.message.reply_chat_action(action="typing")
    bot_reply = await ollama_request(chat_id, user_message)
    await update.message.reply_text(bot_reply)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Бот запущен. Жду сообщений...")
    app.run_polling()

if __name__ == '__main__':
    main()
