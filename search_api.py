import uvicorn
from fastapi import FastAPI, Header, Body, HTTPException
from pydantic import BaseModel
from duckduckgo_search import DDGS

# --- НАСТРОЙКИ ---
# Замените "your_secret_token_here" на свой секретный ключ (должен совпадать с тем, что укажете в Open WebUI)
EXPECTED_BEARER_TOKEN = "your_secret_token_here"
# -----------------

app = FastAPI()

class SearchRequest(BaseModel):
    query: str
    count: int = 5

class SearchResult(BaseModel):
    link: str
    title: str | None
    snippet: str | None

@app.post("/search")
async def external_search(
    search_request: SearchRequest = Body(...),
    authorization: str | None = Header(None),
):
    # Проверка ключа для безопасности
    expected_auth_header = f"Bearer {EXPECTED_BEARER_TOKEN}"
    if authorization != expected_auth_header:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(keywords=search_request.query, max_results=search_request.count))
            formatted_results = [
                SearchResult(
                    link=r.get('href', ''),
                    title=r.get('title', 'No title'),
                    snippet=r.get('body', 'No snippet')
                ) for r in results
            ]
            return formatted_results
    except Exception as e:
        print(f"Search error: {e}")
        return []   # возвращаем пустой массив при ошибке

if __name__ == "__main__":
    # Хост 0.0.0.0 позволяет принимать запросы из контейнера Docker
    uvicorn.run(app, host="0.0.0.0", port=8000)
