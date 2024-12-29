import requests
import logging

# Настройка логирования
logging.basicConfig(filename='test_service.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

recommendations_url = "http://127.0.0.1:8000"
events_store_url = "http://127.0.0.1:8020"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def fetch_recommendations(user_id):
    params = {"user_id": user_id, 'k': 10}
    
    # Запрос оффлайн рекомендаций
    try:
        resp_offline = requests.post(recommendations_url + "/recommendations_offline", headers=headers, params=params)
        resp_offline.raise_for_status()
        recs_offline = resp_offline.json()["recs"]
        logging.info(f'Fetched offline recommendations for user {user_id}.')
    except requests.exceptions.RequestException as e:
        logging.error(f'Error fetching offline recommendations for user {user_id}: {e}')
        recs_offline = []

    # Запрос онлайн рекомендаций
    try:
        resp_online = requests.post(recommendations_url + "/recommendations_online", headers=headers, params=params)
        resp_online.raise_for_status()
        recs_online = resp_online.json()["recs"]
        logging.info(f'Fetched online recommendations for user {user_id}.')
    except requests.exceptions.RequestException as e:
        logging.error(f'Error fetching online recommendations for user {user_id}: {e}')
        recs_online = []

    # Запрос смешанных рекомендаций
    try:
        resp_blended = requests.post(recommendations_url + "/recommendations", headers=headers, params=params)
        resp_blended.raise_for_status()
        recs_blended = resp_blended.json()["recs"]
        logging.info(f'Fetched blended recommendations for user {user_id}.')
    except requests.exceptions.RequestException as e:
        logging.error(f'Error fetching blended recommendations for user {user_id}: {e}')
        recs_blended = []

    return recs_offline, recs_online, recs_blended

# Сценарии тестирования
test_users = {
    "user_no_recommendations": 1131,  # Пользователь без персональных рекомендаций
    "user_no_online_history": 1132,   # Пользователь с персональными рекомендациями, но без онлайн-истории
    "user_with_online_history": 1133   # Пользователь с персональными рекомендациями и онлайн-историей
}


user_id = 1133
event_item_ids = [589498, 590262, 590303, 99262, 590262, 590303, 99262]

# Отправка событий в хранилище признаков
for event_item_id in event_item_ids:
    try:
        resp = requests.post(events_store_url + "/put", 
                             headers=headers, 
                             params={"user_id": user_id, "track_id": event_item_id})
        # Проверка на HTTP ошибки
        resp.raise_for_status()  
        logging.info(f'Successfully logged event {event_item_id} for user {user_id}.')
    except requests.exceptions.RequestException as e:
        logging.error(f'Error logging event {event_item_id} for user {user_id}: {e}')

user_id = test_users["user_no_recommendations"]
logging.info(f'Testing for user_no_recommendations, user_id: {user_id}')
recs_offline, recs_online, recs_blended = fetch_recommendations(user_id)
print(f"user_no_recommendations - Offline Recommendations: {recs_offline}")

user_id = test_users["user_no_online_history"]
logging.info(f'Testing for user_no_online_history, user_id: {user_id}')
recs_offline, recs_online, recs_blended = fetch_recommendations(user_id)
print(f"user_no_online_history - Online Recommendations: {recs_blended}")

user_id = test_users["user_with_online_history"]
logging.info(f'Testing for user_with_online_history, user_id: {user_id}')
recs_offline, recs_online, recs_blended = fetch_recommendations(user_id)
print(f"user_with_online_history - Blended Recommendations: {recs_blended}")