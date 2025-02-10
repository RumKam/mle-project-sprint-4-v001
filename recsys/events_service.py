from fastapi import FastAPI
import requests
import logging

# Настройка логирования
logging.basicConfig(filename='../test_service.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

logger = logging.getLogger("uvicorn.error")

class EventStore:

    def __init__(self, max_events_per_user=10):

        self.events = {}
        self.max_events_per_user = max_events_per_user

    def put(self, user_id, item_id):
        """
        Сохраняет событие
        """

        user_events = self.events.get(user_id, [])
        self.events[user_id] = [item_id] + user_events[: self.max_events_per_user]

    def get(self, user_id, k):
        """
        Возвращает события для пользователя
        """
        user_events = self.events.get(user_id, [])

        # Добавим проверку отсутствия событий
        if user_events == []:
            logging.info("Events not found") 
        else:
            logging.info(f"Number of events for user {user_id}: {len(user_events)}")

        return user_events[:k]

events_store = EventStore()

# создаём приложение FastAPI
app = FastAPI(title="events")

@app.post("/put")
async def put(user_id: int, item_id: int):
    """
    Сохраняет событие для user_id, item_id
    """

    events_store.put(user_id, item_id)

    return {"result": "ok"}

@app.post("/get")
async def get(user_id: int, k: int = 100):
    """
    Возвращает список последних k событий для пользователя user_id
    """

    events = events_store.get(user_id, k)

    return {"events": events}
